import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.nlg import build_briefing

def test_build_briefing_response():
    findings = [{"analito": "Hemoglobina", "sev": "baixo"}]
    specialties = ["hematologia"]
    response = build_briefing(findings, specialties)
    assert isinstance(response, str)
    assert len(response.strip()) > 0
