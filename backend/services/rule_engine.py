import pandas as pd
from typing import List, Dict

# O DataFrame com as regras é carregado eficientemente uma única vez.
try:
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    guideline_path = os.path.join(project_root, "data", "guideline_map.csv")
    df_regras = pd.read_csv(guideline_path)
except FileNotFoundError:
    print("AVISO: Arquivo de regras 'guideline_map.csv' não encontrado.")
    df_regras = pd.DataFrame()


def normalize_analito_name(analito_name: str) -> str:
    """
    Normaliza nomes de analitos para correspondência com guideline_map.csv
    """
    analito_lower = analito_name.lower()
    
    # Mapeamento de nomes alternativos para nomes padrão
    mapping = {
        'plaquetas_alt': 'plaquetas',
        'plaquetas_alt2': 'plaquetas',
        'plaquetas_ponto': 'plaquetas',
        'plaquetas_ponto_alt': 'plaquetas',
        'plaquetas_formato_exato': 'plaquetas',
        'hemacias_alt': 'hemacias',
        'leucocitos_novo': 'leucocitos',
        'neutrofilos_novo': 'neutrofilos',
        'eosinofilos_novo': 'eosinofilos',
        'basofilos_novo': 'basofilos',
        'linfocitos_novo': 'linfocitos',
        'monocitos_novo': 'monocitos',
        'neutrofilos_hemograma': 'neutrofilos',
        'eosinofilos_hemograma': 'eosinofilos',
        'basofilos_hemograma': 'basofilos',
        'linfocitos_hemograma': 'linfocitos',
        'monocitos_hemograma': 'monocitos',
        'leucocitos_hemograma': 'leucocitos'
    }
    
    return mapping.get(analito_lower, analito_lower)

def apply_rules(lab_values: List[Dict], genero: str, idade: int) -> List[Dict]:
    """
    O coração do sistema. Compara os valores do exame com as diretrizes
    e retorna uma lista de achados anormais já enriquecidos.
    """
    if df_regras.empty:
        return []

    resultados_analisados = []
    sexo_map = {'masculino': 'M', 'feminino': 'F'}
    sexo_paciente = sexo_map.get(genero.lower(), 'Todos')

    for valor_exame in lab_values:
        analito_id = valor_exame["analito"]
        valor_paciente = valor_exame["valor"]
        
        # Normalizar nome do analito para correspondência
        analito_normalizado = normalize_analito_name(analito_id)

        # 1. Filtra as regras para o analito, idade e sexo corretos (comparação case-insensitive)
        regras_aplicaveis = df_regras[
            (df_regras['analito_id'].str.lower() == analito_normalizado.lower()) &
            (df_regras['idade_min'] <= idade) &
            (df_regras['idade_max'] >= idade) &
            (df_regras['sexo'].isin([sexo_paciente, 'Todos']))
            ]

        if regras_aplicaveis.empty:
            continue

        regra = regras_aplicaveis.sort_values(by='sexo', ascending=False).iloc[0]

        # 2. Aplica a regra de forma segura
        resultado_final = "normal"
        if valor_paciente < regra['limite_inferior']:
            resultado_final = "baixo"
        elif valor_paciente > regra['limite_superior']:
            resultado_final = "alto"

        # 3. Adiciona à lista de achados apenas se for anormal
        if resultado_final != "normal":
            resultados_analisados.append({
                "analito": analito_id,
                "valor": valor_paciente,
                "resultado": resultado_final,
                "severidade": 1,  # Valor fixo simplificado
                "especialidade": regra['especialidade'],
                "descricao_achado": f"{analito_id} {resultado_final}",  # Descrição simples
                "diretriz": "Valores de Referência Laboratoriais"
            })

    return resultados_analisados