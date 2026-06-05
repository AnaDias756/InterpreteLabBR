from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 🆕 Adicionar
from pydantic import BaseModel, Field
from typing import List, Optional
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
    from .services.rule_engine import apply_rules, get_display_name, comparar_referencias
    from .services.specialty_selector import select_specialties
    from .services.nlg import build_briefing
except ImportError:
    # Fallback para execução direta
    from services.pdf_parser import extract_lab_values
    from services.rule_engine import apply_rules, get_display_name, comparar_referencias
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

class RawLabValue(BaseModel):
    analito: str
    valor: float

class ReferenceComparison(BaseModel):
    analito: str
    valor: float
    classificacao_pns: str
    classificacao_lab: str
    divergente: bool

class InterpretationResponse(BaseModel):
    lab_findings: List[LabFinding]
    recommended_specialties: List[str]
    patient_briefing: str
    lab_values_raw: List[RawLabValue]
    comparacao_referencias: List[ReferenceComparison] = []

class ManualLabValues(BaseModel):
    """Entrada manual de valores de hemograma (sem PDF).

    Todos os analitos são opcionais — a análise é feita apenas com os
    informados. Valores da série branca (leucócitos, neutrófilos, etc.) e
    plaquetas devem ser em valor ABSOLUTO (/μL), conforme a referência da PNS.
    """
    genero: str = Field(..., description="'masculino' ou 'feminino'.")
    idade: int = Field(..., ge=0, le=150, description="Idade do paciente em anos.")
    hemacias: Optional[float] = None
    hemoglobina: Optional[float] = None
    hematocrito: Optional[float] = None
    vcm: Optional[float] = None
    hcm: Optional[float] = None
    chcm: Optional[float] = None
    rdw: Optional[float] = None
    leucocitos: Optional[float] = None
    neutrofilos: Optional[float] = None
    eosinofilos: Optional[float] = None
    basofilos: Optional[float] = None
    linfocitos: Optional[float] = None
    monocitos: Optional[float] = None
    plaquetas: Optional[float] = None

    def to_lab_values(self) -> List[dict]:
        """Converte os campos preenchidos na lista esperada pelo motor de regras."""
        analitos = [
            "hemacias", "hemoglobina", "hematocrito", "vcm", "hcm", "chcm", "rdw",
            "leucocitos", "neutrofilos", "eosinofilos", "basofilos",
            "linfocitos", "monocitos", "plaquetas",
        ]
        return [
            {"analito": nome, "valor": float(getattr(self, nome))}
            for nome in analitos
            if getattr(self, nome) is not None
        ]

# --- Aplicação FastAPI ---
app = FastAPI(
    title="Interpretador de Laudos Laboratoriais",
    description="API para analisar resultados de exames e sugerir especialistas.",
    version="1.0.0"
)

# Evento de startup para verificar dependências
@app.on_event("startup")
async def startup_event():
    """Verificar se todas as dependências estão funcionando na inicialização."""
    logger.info("🚀 Iniciando API do Interpretador de Laudos...")
    
    try:
        # Testar imports críticos
        from services.pdf_parser import extract_lab_values
        from services.rule_engine import apply_rules
        from services.specialty_selector import select_specialties
        from services.nlg import build_briefing
        logger.info("✅ Todos os serviços importados com sucesso")
        
        # Verificar arquivos de dados
        import os
        data_files = ['../data/patterns.csv', '../data/guideline_map.csv']
        for file_path in data_files:
            if os.path.exists(file_path):
                logger.info(f"✅ Arquivo encontrado: {file_path}")
            else:
                logger.warning(f"⚠️ Arquivo não encontrado: {file_path}")
        
        logger.info("🎉 API inicializada com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro durante inicialização: {e}")
        logger.error(f"📍 Traceback: {traceback.format_exc()}")
        # Não falhar a inicialização, apenas logar o erro

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup durante o shutdown."""
    logger.info("🛑 API sendo finalizada...")
    logger.info("👋 Shutdown concluído")

# 🆕 Adicionar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "https://interpretlabbr.netlify.app",  # Netlify production
        "https://interpretador-lab-backend.onrender.com",  # Backend URL
        "*",  # Permitir todas as origens temporariamente para debug
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Endpoint para verificar se a API está funcionando."""
    import os
    import time
    
    try:
        # Verificar se os serviços críticos estão funcionando
        test_import = True
        try:
            # Como os imports já foram feitos no topo, apenas verificar se estão disponíveis
            # Não precisamos reimportar, apenas verificar se as funções existem
            if 'extract_lab_values' in globals() and 'apply_rules' in globals():
                test_import = True
            else:
                test_import = False
        except Exception:
            test_import = False
        
        health_data = {
            "status": "healthy",
            "message": "API esta funcionando corretamente",
            "timestamp": time.time(),
            "version": "1.0.0",
            "system": {
                "python_version": os.environ.get('PYTHON_VERSION', 'unknown'),
                "port": os.environ.get('PORT', 'unknown')
            },
            "services": {
                "imports_working": test_import,
                "pdf_processing": test_import
            }
        }
        
        # Se algum serviço crítico não estiver funcionando, retornar status degraded
        if not test_import:
            health_data["status"] = "degraded"
            health_data["message"] = "Alguns serviços não estão funcionando corretamente"
        
        return health_data
        
    except Exception as e:
        logger.error(f"❌ Erro no health check: {e}")
        return {
            "status": "unhealthy",
            "message": f"Erro no health check: {str(e)}",
            "timestamp": time.time()
        }

@app.get("/debug")
async def debug_info():
    """Endpoint para informações de debug (apenas para desenvolvimento)."""
    import os
    import sys
    
    try:
        debug_data = {
            "python_version": sys.version,
            "working_directory": os.getcwd(),
            "environment_variables": {
                "PYTHON_VERSION": os.environ.get('PYTHON_VERSION'),
                "PORT": os.environ.get('PORT'),
                "PYTHONPATH": os.environ.get('PYTHONPATH')
            },
            "files_exist": {
                "data/patterns.csv": os.path.exists('data/patterns.csv'),
                "data/guideline_map.csv": os.path.exists('data/guideline_map.csv'),
                "backend/services/pdf_parser.py": os.path.exists('backend/services/pdf_parser.py')
            },
            "sys_path": sys.path[:5]  # Primeiros 5 itens do sys.path
        }
        
        return debug_data
        
    except Exception as e:
        return {"error": str(e)}

@app.post("/interpret", response_model=InterpretationResponse)
async def interpret_results(
        file: UploadFile = File(..., description="Arquivo PDF do laudo laboratorial."),
        genero: str = Form(..., description="Gênero do paciente (ex: 'masculino' ou 'feminino')."),
        idade: int = Form(..., description="Idade do paciente em anos.")
):
    """
    Analisa um laudo laboratorial em PDF para interpretar os resultados.
    """
    # Log detalhado dos dados recebidos para debug
    logger.info(f"🔍 Dados recebidos - Arquivo: {file.filename}, Gênero: {genero}, Idade: {idade}")
    
    # Validações de entrada com logging detalhado
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        logger.error(f"❌ Arquivo inválido: {file.filename}")
        raise HTTPException(status_code=422, detail="Formato de arquivo inválido. Por favor, envie um PDF.")
    
    if genero.lower() not in ['masculino', 'feminino']:
        logger.error(f"❌ Gênero inválido: {genero}")
        raise HTTPException(status_code=422, detail="Gênero deve ser 'masculino' ou 'feminino'.")
    
    # Aceitar idade 0 como válida (quando não informada) ou entre 1 e 150
    if idade < 0 or idade > 150:
        logger.error(f"❌ Idade inválida: {idade}")
        raise HTTPException(status_code=422, detail="Idade deve estar entre 0 e 150 anos.")
    
    # Se idade for 0, usar um valor padrão para análise (ex: 30 anos)
    idade_para_analise = idade if idade > 0 else 30
    logger.info(f"📊 Usando idade {idade_para_analise} para análise (original: {idade})")

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
            logger.warning(
                "Nenhum valor laboratorial encontrado. Possíveis causas: PDF corrompido/não suportado, texto ilegível, ou ausência de resultados. Sugestões: reenviar PDF válido, verificar qualidade/legibilidade, garantir texto selecionável."
            )
            raise HTTPException(
                status_code=422,
                detail=(
                    "Nenhum valor laboratorial foi encontrado no PDF.\n\n"
                    "Possíveis causas:\n"
                    "- PDF corrompido ou com formato/layout não suportado;\n"
                    "- Texto do laudo ilegível, muito distorcido ou apenas imagem;\n"
                    "- O arquivo não contém resultados de exames laboratoriais.\n\n"
                    "Como resolver:\n"
                    "- Tente enviar outro PDF ou exportar novamente o laudo em melhor qualidade;\n"
                    "- Verifique se o PDF possui texto selecionável (não apenas imagens);\n"
                    "- Se o problema persistir, verifique se o laudo segue formatos comuns de laboratórios."
                )
            )

        # 2. Aplicar motor de regras
        try:
            analyzed_findings = apply_rules(raw_values, genero=genero, idade=idade_para_analise)
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

        # Preparar lista de valores brutos com nomes amigáveis
        raw_display_values = [
            {"analito": get_display_name(v["analito"]), "valor": v["valor"]}
            for v in raw_values
        ]

        # Comparação entre referência PNS e laboratorial
        comparacao = comparar_referencias(raw_values, genero=genero, idade=idade_para_analise)

        logger.info("✅ Processamento concluído com sucesso")
        return {
            "lab_findings": analyzed_findings,
            "recommended_specialties": specialties,
            "patient_briefing": briefing,
            "lab_values_raw": raw_display_values,
            "comparacao_referencias": comparacao
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

@app.post("/interpret-manual", response_model=InterpretationResponse)
async def interpret_manual(dados: ManualLabValues):
    """
    Analisa valores de hemograma informados manualmente (sem PDF).

    Útil para quem não possui o laudo em PDF suportado, melhorando o acesso.
    Reaproveita o mesmo motor de regras, seleção de especialidades e briefing.
    """
    logger.info(f"📝 Entrada manual - Gênero: {dados.genero}, Idade: {dados.idade}")

    # Validações de entrada
    if dados.genero.lower() not in ['masculino', 'feminino']:
        raise HTTPException(status_code=422, detail="Gênero deve ser 'masculino' ou 'feminino'.")

    if dados.idade < 0 or dados.idade > 150:
        raise HTTPException(status_code=422, detail="Idade deve estar entre 0 e 150 anos.")

    raw_values = dados.to_lab_values()
    if not raw_values:
        raise HTTPException(
            status_code=422,
            detail="Informe ao menos um valor de exame para análise."
        )

    # Se idade for 0, usar valor padrão para análise (consistente com /interpret)
    idade_para_analise = dados.idade if dados.idade > 0 else 30
    logger.info(f"📊 Analisando {len(raw_values)} valor(es) informado(s) manualmente")

    try:
        # 1. Aplicar motor de regras
        analyzed_findings = apply_rules(raw_values, genero=dados.genero, idade=idade_para_analise)
        logger.info(f"⚙️ Regras aplicadas: {len(analyzed_findings)} achados")

        # 2. Selecionar especialidades
        specialties = select_specialties(analyzed_findings)
        logger.info(f"👨‍⚕️ Especialidades selecionadas: {len(specialties)}")

        # 3. Construir o briefing
        try:
            briefing = build_briefing(analyzed_findings, specialties)
        except Exception as e:
            logger.error(f"❌ Erro na geração do briefing: {e}")
            briefing = "Briefing temporariamente indisponível. Os resultados dos exames estão disponíveis acima."

        # Lista de valores informados com nomes amigáveis
        raw_display_values = [
            {"analito": get_display_name(v["analito"]), "valor": v["valor"]}
            for v in raw_values
        ]

        # Comparação entre referência PNS e laboratorial
        comparacao = comparar_referencias(raw_values, genero=dados.genero, idade=idade_para_analise)

        logger.info("✅ Análise manual concluída com sucesso")
        return {
            "lab_findings": analyzed_findings,
            "recommended_specialties": specialties,
            "patient_briefing": briefing,
            "lab_values_raw": raw_display_values,
            "comparacao_referencias": comparacao
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro inesperado na análise manual: {e}")
        logger.error(f"📍 Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno do servidor. Tente novamente."
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