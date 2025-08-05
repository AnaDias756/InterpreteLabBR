import requests
import os
from typing import List, Dict

def build_briefing(findings: List[Dict], specialties: List[str]) -> str:
    if not findings:
        return "Não foram encontrados achados anormais nos exames."
    
    # Prepara informações detalhadas dos achados
    achados_detalhados = []
    for f in findings:
        achado = f"{f['analito']}: {f['valor']} ({f['resultado']})"
        if f.get('descricao_achado'):
            achado += f" - {f['descricao_achado']}"
        achados_detalhados.append(achado)
    
    resumo_achados = "; ".join(achados_detalhados)
    especialidades_str = ", ".join(specialties)
    
    prompt = f"""Você é um assistente médico especializado em preparar pacientes para consultas.

Resultados dos exames laboratoriais:
{resumo_achados}

Especialidades recomendadas: {especialidades_str}

Crie um texto simples e claro para ajudar o paciente a se preparar para a consulta médica. O texto deve:
1. Explicar de forma simples o que os resultados significam
2. Orientar sobre perguntas importantes para fazer ao médico
3. Sugerir informações que o paciente deve levar para a consulta
4. Tranquilizar o paciente de forma apropriada

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
    
    # Fallback final - texto estático
    return _generate_fallback_briefing(resumo_achados, especialidades_str)

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

def _generate_fallback_briefing(resumo_achados: str, especialidades_str: str) -> str:
    """Gera um briefing básico quando as APIs não estão disponíveis"""
    return f"""📋 **Preparação para sua consulta médica**

**Resultados encontrados em seus exames:**
{resumo_achados}

**Especialista(s) recomendado(s):** {especialidades_str}

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