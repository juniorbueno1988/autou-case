# app.py
import os
import io
import csv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PyPDF2 import PdfReader

# ----------------------------
# Configurações de ambiente
# ----------------------------
USE_AI = os.environ.get("USE_AI", "false").lower() in ("1", "true", "yes")
GROQ_KEY = os.environ.get("GROQ_KEY", None)

# Importa IA apenas se ativada e chave definida
try:
    if USE_AI and GROQ_KEY:
        from ai_groq import analisar_com_groq  # módulo de IA
    else:
        USE_AI = False
        if os.environ.get("USE_AI", "false").lower() in ("1", "true", "yes"):
            print("USE_AI ativado, mas chave GROQ_KEY não encontrada.")
except Exception as e:
    print(f"Falha ao importar AI: {e}")
    USE_AI = True

# ----------------------------
# Inicializa API
# ----------------------------
app = FastAPI(title="AutoU API")

# ----------------------------
# Configuração CORS
# ----------------------------
origins = [
    "http://localhost:5173",  # front local
    "https://front-end-ochre-eta.vercel.app/",  # front remoto
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if not USE_AI else ["*"],  # permitir todos se usar AI
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Modelo de entrada
# ----------------------------
class EmailPayload(BaseModel):
    texto: str | None = None
    subject: str | None = None
    body: str | None = None

# ----------------------------
# Função fallback local
# ----------------------------
def analisar_texto_local(texto: str):
    t = texto.lower()

    # improdutivo social
    if any(k in t for k in ["feliz", "obrigado", "parabéns", "bom dia", "boa tarde", "boa noite", "felicit"]):
        return "Improdutivo", "Olá! Agradecemos sua mensagem. Atenciosamente, Equipe."

    # improdutivo promocional
    if any(k in t for k in ["promoção", "oferta", "compre", "desconto"]):
        return "Improdutivo", "Mensagem identificada como promocional. Obrigado pelo contato."

    # produtivo
    if any(k in t for k in ["status", "andamento", "pedido", "protocolo", "preciso", "ajuda", "suporte", "erro", "reclama", "cancelar", "comprovante", "anexo"]):
        if any(k in t for k in ["status", "andamento", "pedido", "protocolo"]):
            resposta = "Olá! Recebemos sua solicitação sobre status. Retornaremos em até 2 dias úteis."
        elif any(k in t for k in ["comprovante", "anexo", ".pdf"]):
            resposta = "Olá! Confirmamos o recebimento do documento e faremos a validação."
        elif "cancelar" in t:
            resposta = "Olá! Recebemos a solicitação de cancelamento. Encaminharemos para análise."
        elif "reclam" in t or "erro" in t:
            resposta = "Olá! Sentimos pelo ocorrido. Encaminhamos a reclamação ao setor responsável."
        else:
            resposta = "Olá! Sua mensagem foi encaminhada para análise. Retornaremos em breve."
        return "Produtivo", resposta

    return "Produtivo", "Olá! Sua mensagem foi recebida e será avaliada pela equipe."

# ----------------------------
# ENDPOINTS
# ----------------------------
@app.post("/classificar")
async def classificar(payload: EmailPayload):
    texto = payload.texto or f"{payload.subject or ''} {payload.body or ''}".strip()
    if not texto:
        raise HTTPException(status_code=400, detail="Envie 'texto' ou 'subject'/'body' no JSON.")

    try:
        if USE_AI:
            categoria, resposta = analisar_com_groq(texto)
        else:
            categoria, resposta = analisar_texto_local(texto)
    except Exception as e:
        print(f"[classificar] Erro AI: {e}")
        categoria, resposta = analisar_texto_local(texto)

    return {
        "categoria": categoria,
        "resposta_sugerida": resposta,
        "usou_ai": USE_AI
    }

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not (file.filename.endswith((".txt", ".pdf", ".csv"))):
        raise HTTPException(status_code=400, detail="Envie apenas .txt, .pdf ou .csv")

    conteudo = ""

    # TXT
    if file.filename.endswith(".txt"):
        conteudo = (await file.read()).decode("utf-8", errors="ignore")

    # PDF
    elif file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        for page in reader.pages:
            conteudo += page.extract_text() or ""

    # CSV
    elif file.filename.endswith(".csv"):
        data = await file.read()
        decoded = data.decode("utf-8", errors="ignore")
        reader = csv.reader(io.StringIO(decoded))
        for row in reader:
            if row and row[0].strip().lower() in ("assunto", "subject"):
                continue
            conteudo += " ".join(row) + "\n"

    if not conteudo.strip():
        raise HTTPException(status_code=400, detail="Arquivo sem conteúdo legível.")

    try:
        if USE_AI:
            categoria, resposta = analisar_com_groq(conteudo)
        else:
            categoria, resposta = analisar_texto_local(conteudo)
    except Exception as e:
        print(f"[upload] Erro AI: {e}")
        categoria, resposta = analisar_texto_local(conteudo)

    return {
        "arquivo": file.filename,
        "categoria": categoria,
        "resposta_sugerida": resposta,
        "usou_ai": USE_AI
    }

@app.get("/")
async def root():
    return {"mensagem": "API funcionando com IA gratuita!", "usou_ai": USE_AI}
