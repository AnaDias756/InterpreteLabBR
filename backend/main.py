from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 🆕 Adicionar
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

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

# 🆕 Adicionar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Endpoint para verificar se a API está funcionando."""
    return {"status": "healthy", "message": "API está funcionando corretamente"}

@app.post("/interpret", response_model=InterpretationResponse)
async def interpret_results(
        file: UploadFile = File(..., description="Arquivo PDF do laudo laboratorial."),
        genero: str = Form(..., description="Gênero do paciente (ex: 'masculino' ou 'feminino')."),
        idade: int = Form(..., description="Idade do paciente em anos.")
):
    """
    Analisa um laudo laboratorial em PDF para interpretar os resultados.
    """
    # Validações de entrada
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Formato de arquivo inválido. Por favor, envie um PDF.")
    
    if genero.lower() not in ['masculino', 'feminino']:
        raise HTTPException(status_code=400, detail="Gênero deve ser 'masculino' ou 'feminino'.")
    
    if idade < 0 or idade > 150:
        raise HTTPException(status_code=400, detail="Idade deve estar entre 0 e 150 anos.")

    try:
        pdf_content = await file.read()
        
        if len(pdf_content) == 0:
            raise HTTPException(status_code=400, detail="Arquivo PDF está vazio.")

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
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno do servidor: {str(e)}"
        )