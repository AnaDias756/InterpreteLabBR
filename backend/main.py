from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 🆕 Adicionar
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import logging
import traceback

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Imports relativos para execução como módulo ou absolutos para execução direta
try:
    from .services.pdf_parser import extract_lab_values
    from .services.rule_engine import apply_rules
    from .services.specialty_selector import select_specialties
    from .services.nlg import build_briefing
except ImportError:
    # Fallback para execução direta
    from services.pdf_parser import extract_lab_values
    from services.rule_engine import apply_rules
    from services.specialty_selector import select_specialties
    from services.nlg import build_briefing

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
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "https://interpretlabbr.netlify.app",  # Netlify production
        "https://*.netlify.app",  # Netlify preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Endpoint para verificar se a API está funcionando."""
    return {"status": "healthy", "message": "API esta funcionando corretamente"}

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
        logger.info(f"📋 Processando arquivo: {file.filename} (tamanho: {file.size} bytes)")
        
        # Verificar tamanho do arquivo
        if file.size and file.size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=413, 
                detail="Arquivo muito grande. O tamanho máximo permitido é 10MB."
            )
        
        pdf_content = await file.read()
        
        if len(pdf_content) == 0:
            raise HTTPException(status_code=400, detail="Arquivo PDF está vazio.")
        
        logger.info(f"📄 Arquivo lido: {len(pdf_content)} bytes")

        # 1. Extrair valores brutos
        try:
            raw_values = extract_lab_values(pdf_content)
            logger.info(f"🔍 Valores extraídos: {len(raw_values)} analitos")
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Erro na extração: {error_msg}")
            
            # Mensagens específicas baseadas no tipo de erro
            if "PDF protegido por senha" in error_msg:
                raise HTTPException(
                    status_code=422,
                    detail="PDF protegido por senha. Remova a proteção antes de enviar."
                )
            elif "assinatura PDF válida" in error_msg:
                raise HTTPException(
                    status_code=422,
                    detail="Arquivo não é um PDF válido. Verifique o formato do arquivo."
                )
            elif "muito pequeno" in error_msg:
                raise HTTPException(
                    status_code=422,
                    detail="Arquivo muito pequeno ou corrompido. Envie um PDF válido."
                )
            elif "corrompido" in error_msg:
                raise HTTPException(
                    status_code=422,
                    detail="PDF corrompido ou danificado. Tente gerar o PDF novamente."
                )
            elif "OCR não disponível" in error_msg:
                raise HTTPException(
                    status_code=422,
                    detail="PDF baseado em imagens detectado, mas OCR não está disponível. Envie um PDF com texto selecionável."
                )
            elif "configuração não encontrado" in error_msg:
                logger.error("❌ Erro de configuração do sistema")
                raise HTTPException(
                    status_code=500,
                    detail="Erro de configuração do sistema. Tente novamente em alguns minutos."
                )
            else:
                raise HTTPException(
                    status_code=422,
                    detail=f"Não foi possível extrair texto do PDF: {error_msg}"
                )
        
        if not raw_values:
            raise HTTPException(
                status_code=422,
                detail="Nenhum valor laboratorial encontrado no PDF. Verifique se o arquivo contém resultados de exames laboratoriais."
            )

        # 2. Aplicar motor de regras
        try:
            analyzed_findings = apply_rules(raw_values, genero=genero, idade=idade)
            logger.info(f"⚙️ Regras aplicadas: {len(analyzed_findings)} achados")
        except Exception as e:
            logger.error(f"❌ Erro no motor de regras: {e}")
            raise HTTPException(
                status_code=500,
                detail="Erro ao processar regras de análise. Tente novamente."
            )

        # 3. Selecionar especialidades
        try:
            specialties = select_specialties(analyzed_findings)
            logger.info(f"👨‍⚕️ Especialidades selecionadas: {len(specialties)}")
        except Exception as e:
            logger.error(f"❌ Erro na seleção de especialidades: {e}")
            raise HTTPException(
                status_code=500,
                detail="Erro ao selecionar especialidades. Tente novamente."
            )

        # 4. Construir o briefing
        try:
            briefing = build_briefing(analyzed_findings, specialties)
            logger.info("📝 Briefing gerado com sucesso")
        except Exception as e:
            logger.error(f"❌ Erro na geração do briefing: {e}")
            # Briefing é opcional, não deve falhar a requisição
            briefing = "Briefing temporariamente indisponível. Os resultados dos exames estão disponíveis acima."

        logger.info("✅ Processamento concluído com sucesso")
        return {
            "lab_findings": analyzed_findings,
            "recommended_specialties": specialties,
            "patient_briefing": briefing
        }
    
    except HTTPException:
        raise
    except Exception as e:
        # Log completo do erro para debug
        logger.error(f"❌ Erro inesperado: {e}")
        logger.error(f"📍 Traceback: {traceback.format_exc()}")
        
        raise HTTPException(
            status_code=500, 
            detail="Erro interno do servidor. Nossa equipe foi notificada e está trabalhando na correção."
        )

# Executar servidor quando chamado diretamente
if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Iniciando servidor de desenvolvimento...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )