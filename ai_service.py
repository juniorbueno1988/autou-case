# ai_service.py
import os
from groq import Groq
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Pega a chave da API do ambiente
GROQ_KEY = os.getenv("GROQ_KEY") or os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise ValueError("Chave GROQ_KEY ou GROQ_API_KEY não encontrada nas variáveis de ambiente.")

# Inicializa cliente Groq
client = Groq(api_key=GROQ_KEY)

def gerar_resposta_ia(prompt: str, max_tokens: int = 300) -> str:
    """
    Gera uma resposta usando a IA Groq (modelo LLaMA3).
    
    Args:
        prompt (str): Texto de entrada.
        max_tokens (int): Número máximo de tokens na resposta.
    
    Returns:
        str: Resposta gerada pela IA.
    """
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.get("content", "").strip()
    except Exception as e:
        print(f"[gerar_resposta_ia] Erro ao gerar resposta: {e}")
        return "Erro ao gerar resposta IA. Por favor, tente novamente mais tarde."
