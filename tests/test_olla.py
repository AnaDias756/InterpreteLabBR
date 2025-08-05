import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.nlg import build_briefing

def test_build_briefing_response():
    findings = [{
        "analito": "hemoglobina", 
        "valor": 10.5,
        "resultado": "baixo",
        "severidade": 2,
        "especialidade": "Hematologia",
        "descricao_achado": "Anemia",
        "diretriz": "SBHH"
    }]
    specialties = ["Hematologia"]
    response = build_briefing(findings, specialties)
    assert isinstance(response, str)
    assert len(response.strip()) > 0
    print("✅ Teste de briefing executado com sucesso! Resposta:", response[:100] + "...")
