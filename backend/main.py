from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel, Field
from typing import List

from backend.services.pdf_parser import extract_lab_values
from backend.services.rule_engine import apply_rules
from backend.services.specialty_selector import select_specialties
from backend.services.nlg import build_briefing

# --- Modelos de Resposta Pydantic ---
class LabFinding(BaseModel):
    analito: str
    valor: float
    resultado: str
    severidade: int
    especialidade: str
    descricao_achado: str
    diretriz: str

class InterpretationResponse(BaseModel):
    lab_findings: List[LabFinding]
    recommended_specialties: List[str]
    patient_briefing: str

# --- Aplicação FastAPI ---
app = FastAPI(
    title="Interpretador de Laudos Laboratoriais",
    description="API para analisar resultados de exames e sugerir especialistas.",
    version="1.0.0"
)

@app.post("/interpret", response_model=InterpretationResponse)
async def interpret_results(
        file: UploadFile = File(..., description="Arquivo PDF do laudo laboratorial."),
        genero: str = Form(..., description="Gênero do paciente (ex: 'masculino' ou 'feminino')."),
        idade: int = Form(..., description="Idade do paciente em anos.")
):
    """
    Analisa um laudo laboratorial em PDF para interpretar os resultados.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Formato de arquivo inválido. Por favor, envie um PDF.")

    pdf_content = await file.read()

    # 1. Extrair valores brutos
    raw_values = extract_lab_values(pdf_content)
    if not raw_values:
        raise HTTPException(
            status_code=422,
            detail="Não foi possível extrair valores do PDF. Verifique se o arquivo é um laudo legível."
        )

    # 2. Aplicar motor de regras
    analyzed_findings = apply_rules(raw_values, genero=genero, idade=idade)

    # 3. Selecionar especialidades
    specialties = select_specialties(analyzed_findings)

    # 4. Construir o briefing
    briefing = build_briefing(analyzed_findings, specialties)

    return {
        "lab_findings": analyzed_findings,
        "recommended_specialties": specialties,
        "patient_briefing": briefing
    }