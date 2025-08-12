import requests
import os
from typing import List, Dict

# Dicionário com explicações educativas dos analitos
ANALITO_EXPLICACOES = {
    "leucocitos": {
        "nome": "Leucócitos (Glóbulos Brancos)",
        "explicacao": "São as células de defesa do seu corpo. Eles combatem infecções e doenças. Valores alterados podem indicar infecções, inflamações ou problemas no sistema imunológico.",
        "valores_altos": "Pode indicar infecção bacteriana, inflamação, estresse físico ou uso de alguns medicamentos.",
        "valores_baixos": "Pode sugerir infecções virais, problemas na medula óssea ou efeito de alguns medicamentos."
    },
    "hemacias": {
        "nome": "Hemácias (Glóbulos Vermelhos)",
        "explicacao": "São responsáveis por transportar oxigênio pelo seu corpo. Alterações podem indicar anemia ou outros problemas sanguíneos.",
        "valores_altos": "Pode indicar desidratação, problemas pulmonares ou cardíacos, ou vida em altitudes elevadas.",
        "valores_baixos": "Pode sugerir anemia, perda de sangue, deficiências nutricionais ou problemas na medula óssea."
    },
    "hemoglobina": {
        "nome": "Hemoglobina",
        "explicacao": "É a proteína que carrega oxigênio no sangue. Valores baixos geralmente indicam anemia.",
        "valores_altos": "Pode indicar desidratação, problemas pulmonares ou vida em grandes altitudes.",
        "valores_baixos": "Geralmente indica anemia, que pode ter várias causas como deficiência de ferro, vitaminas ou doenças crônicas."
    },
    "hematocrito": {
        "nome": "Hematócrito",
        "explicacao": "Mostra a porcentagem do seu sangue que é composta por glóbulos vermelhos. Ajuda a diagnosticar anemia ou excesso de glóbulos vermelhos.",
        "valores_altos": "Pode indicar desidratação ou excesso de glóbulos vermelhos.",
        "valores_baixos": "Geralmente indica anemia ou perda de sangue."
    },
    "plaquetas": {
        "nome": "Plaquetas",
        "explicacao": "São responsáveis pela coagulação do sangue. Elas ajudam a parar sangramentos quando você se machuca.",
        "valores_altos": "Pode aumentar o risco de coágulos sanguíneos. Pode ser causado por inflamações, câncer ou problemas na medula óssea.",
        "valores_baixos": "Pode causar sangramentos excessivos. Pode ser causado por medicamentos, infecções ou problemas na medula óssea."
    },
    "neutrófilos": {
        "nome": "Neutrófilos",
        "explicacao": "São um tipo específico de glóbulo branco que combate principalmente infecções bacterianas.",
        "valores_altos": "Geralmente indica infecção bacteriana, inflamação ou estresse físico.",
        "valores_baixos": "Pode indicar infecções virais, problemas na medula óssea ou efeito de medicamentos."
    },
    "linfócitos": {
        "nome": "Linfócitos",
        "explicacao": "São glóbulos brancos que combatem infecções virais e participam da imunidade do corpo.",
        "valores_altos": "Pode indicar infecções virais, algumas doenças autoimunes ou tipos específicos de câncer no sangue.",
        "valores_baixos": "Pode sugerir problemas no sistema imunológico, estresse ou efeito de alguns medicamentos."
    },
    "eosinófilos": {
        "nome": "Eosinófilos",
        "explicacao": "São glóbulos brancos que combatem parasitas e estão envolvidos em reações alérgicas.",
        "valores_altos": "Pode indicar alergias, asma, infecções parasitárias ou algumas doenças autoimunes.",
        "valores_baixos": "Geralmente não é preocupante, mas pode ocorrer durante infecções graves."
    },
    "basófilos": {
        "nome": "Basófilos",
        "explicacao": "São glóbulos brancos envolvidos em reações alérgicas e inflamatórias.",
        "valores_altos": "Pode indicar alergias graves, algumas doenças do sangue ou inflamações crônicas.",
        "valores_baixos": "Geralmente normal e não preocupante."
    },
    "monócitos": {
        "nome": "Monócitos",
        "explicacao": "São glóbulos brancos que combatem infecções e ajudam a limpar células mortas e detritos.",
        "valores_altos": "Pode indicar infecções crônicas, doenças autoimunes ou alguns tipos de câncer no sangue.",
        "valores_baixos": "Geralmente não é preocupante."
    },
    "vcm": {
        "nome": "VCM (Volume Corpuscular Médio)",
        "explicacao": "Mede o tamanho médio dos seus glóbulos vermelhos. Ajuda a identificar diferentes tipos de anemia.",
        "valores_altos": "Pode indicar deficiência de vitamina B12 ou ácido fólico, problemas no fígado ou uso de álcool.",
        "valores_baixos": "Pode indicar deficiência de ferro ou talassemia."
    },
    "hcm": {
        "nome": "HCM (Hemoglobina Corpuscular Média)",
        "explicacao": "Mede a quantidade média de hemoglobina em cada glóbulo vermelho.",
        "valores_altos": "Pode indicar deficiência de vitamina B12 ou ácido fólico.",
        "valores_baixos": "Pode indicar deficiência de ferro ou talassemia."
    },
    "chcm": {
        "nome": "CHCM (Concentração de Hemoglobina Corpuscular Média)",
        "explicacao": "Mede a concentração de hemoglobina dentro dos glóbulos vermelhos.",
        "valores_altos": "Pode indicar desidratação ou algumas doenças hereditárias do sangue.",
        "valores_baixos": "Pode indicar deficiência de ferro ou talassemia."
    },
    "rdw": {
        "nome": "RDW (Amplitude de Distribuição dos Glóbulos Vermelhos)",
        "explicacao": "Mede a variação no tamanho dos glóbulos vermelhos. Ajuda a identificar diferentes tipos de anemia.",
        "valores_altos": "Pode indicar deficiência de ferro, vitamina B12, ácido fólico ou mistura de diferentes tipos de anemia.",
        "valores_baixos": "Geralmente normal."
    }
}

def get_analito_explanation(analito: str, resultado: str) -> str:
    """Retorna explicação específica para um analito baseado no resultado"""
    analito_lower = analito.lower()
    
    if analito_lower not in ANALITO_EXPLICACOES:
        return f"**{analito}**: Este é um parâmetro importante do seu exame que precisa ser avaliado pelo médico."
    
    info = ANALITO_EXPLICACOES[analito_lower]
    explicacao_base = f"**{info['nome']}**: {info['explicacao']}"
    
    if resultado.lower() == 'alto' and 'valores_altos' in info:
        explicacao_base += f" \n*Seu resultado está alto*: {info['valores_altos']}"
    elif resultado.lower() == 'baixo' and 'valores_baixos' in info:
        explicacao_base += f" \n*Seu resultado está baixo*: {info['valores_baixos']}"
    
    return explicacao_base

def build_briefing(findings: List[Dict], specialties: List[str]) -> str:
    if not findings:
        return "Não foram encontrados achados anormais nos exames."
    
    # Prepara informações detalhadas dos achados
    achados_detalhados = []
    explicacoes_analitos = []
    
    for f in findings:
        achado = f"{f['analito']}: {f['valor']} ({f['resultado']})"
        if f.get('descricao_achado'):
            achado += f" - {f['descricao_achado']}"
        achados_detalhados.append(achado)
        
        # Adiciona explicação do analito
        explicacao = get_analito_explanation(f['analito'], f['resultado'])
        explicacoes_analitos.append(explicacao)
    
    resumo_achados = "; ".join(achados_detalhados)
    especialidades_str = ", ".join(specialties)
    explicacoes_texto = "\n\n".join(explicacoes_analitos)
    
    prompt = f"""Você é um assistente médico especializado em preparar pacientes para consultas.

Resultados dos exames laboratoriais:
{resumo_achados}

Especialidades recomendadas: {especialidades_str}

Explicações dos analitos encontrados:
{explicacoes_texto}

Crie um texto simples e claro para ajudar o paciente a se preparar para a consulta médica. O texto deve:
1. Explicar de forma simples o que os resultados significam
2. Orientar sobre perguntas importantes para fazer ao médico
3. Sugerir informações que o paciente deve levar para a consulta
4. Tranquilizar o paciente de forma apropriada
5. Incorporar as explicações dos analitos de forma educativa

Mantenha um tom acolhedor e informativo, evitando termos muito técnicos."""

    # Tenta usar Google Gemini
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if gemini_api_key:
        try:
            return _call_gemini_api(prompt, gemini_api_key)
        except Exception as e:
            print(f"Erro ao chamar Gemini API: {e}")
    
    # Fallback para Ollama
    try:
        return _call_ollama_api(prompt)
    except Exception as e:
        print(f"Erro ao chamar Ollama API: {e}")
    
    # Fallback final - texto estático com explicações
    return _generate_fallback_briefing_with_explanations(resumo_achados, especialidades_str, explicacoes_analitos)

def _call_gemini_api(prompt: str, api_key: str) -> str:
    """Chama a API do Google Gemini"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    if 'candidates' in data and len(data['candidates']) > 0:
        content = data['candidates'][0]['content']['parts'][0]['text']
        return content.strip()
    else:
        raise ValueError("Resposta inválida da API Gemini")

def _call_ollama_api(prompt: str) -> str:
    """Chama a API do Ollama como fallback"""
    response = requests.post(
        "http://localhost:11434/api/generate", 
        json={
            "model": "phi",
            "prompt": prompt,
            "stream": False
        },
        timeout=30
    )
    response.raise_for_status()
    
    data = response.json()
    if "response" not in data:
        raise ValueError(f"Erro ao gerar resposta: {data}")
    
    return data["response"]

def _generate_fallback_briefing_with_explanations(resumo_achados: str, especialidades_str: str, explicacoes: List[str]) -> str:
    """Gera um briefing básico com explicações quando as APIs não estão disponíveis"""
    explicacoes_formatadas = "\n\n".join([f"📋 {exp}" for exp in explicacoes])
    
    return f"""📋 **Preparação para sua consulta médica**

**Resultados encontrados em seus exames:**
{resumo_achados}

**Especialista(s) recomendado(s):** {especialidades_str}

**📚 Entenda seus exames:**

{explicacoes_formatadas}

**Como se preparar para a consulta:**

1. **Leve seus exames completos** - Traga todos os resultados originais
2. **Liste seus sintomas** - Anote quando começaram e como se manifestam
3. **Histórico médico** - Prepare informações sobre medicamentos atuais e doenças na família
4. **Perguntas importantes:**
   - O que esses resultados significam para minha saúde?
   - Preciso de exames complementares?
   - Há mudanças no estilo de vida que devo fazer?
   - Quando devo retornar para acompanhamento?

**Lembre-se:** Estes resultados precisam ser interpretados por um médico especialista. Não se preocupe antecipadamente - muitas alterações são tratáveis e controláveis.

💡 **Dica:** Anote suas dúvidas antes da consulta para não esquecer de perguntar!"""