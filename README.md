
# AutoU - Classificador de Emails

## Descrição do Projeto

O **AutoU** é uma aplicação web desenvolvida para automatizar a leitura e classificação de emails em **Produtivo** ou **Improdutivo**, sugerindo respostas automáticas de acordo com o teor da mensagem.  

O objetivo é liberar a equipe do atendimento manual, permitindo que o sistema faça a triagem e gere respostas automáticas para emails de forma rápida e eficiente.

---

## Funcionalidades

- Inserção de texto manual ou upload de arquivos de email (.txt, .pdf, .csv)
- Classificação automática do email:
  - **Produtivo:** emails que requerem ação ou resposta (ex.: solicitações, dúvidas técnicas)
  - **Improdutivo:** emails que não necessitam ação imediata (ex.: felicitações, agradecimentos)
- Sugestão de respostas automáticas baseadas na classificação
- Backend em **FastAPI** com integração de NLP/IA (opcional)
- Frontend simples e responsivo em **HTML/CSS/JS**
- Deploy pronto para nuvem (Render para backend, Vercel para frontend)

---

## Tecnologias Utilizadas

- **Backend:** Python, FastAPI, PyPDF2, pydantic
- **Frontend:** HTML5, CSS3, JavaScript
- **Hospedagem:** Render (API) e Vercel (Frontend)
- **Processamento de Linguagem Natural:** fallback local em Python, integração opcional com AI/GROQ

---

## Estrutura do Projeto

```
/autoU-case
│
├─ app.py             # Backend FastAPI
├─ index.html         # Interface web
├─ requirements.txt   # Dependências Python
└─ README.md          # Este arquivo
```

---

## Instalação Local

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/autoU-case.git
cd autoU-case
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a API:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

5. Abra o `index.html` no navegador ou use um servidor local para testes (ex.: Live Server no VSCode)

---

## Uso da Aplicação

1. **Inserir texto do email** no campo disponível **ou** enviar um arquivo (.txt, .pdf, .csv)
2. Clicar em **Classificar Email**
3. O resultado será exibido:
   - **Categoria:** Produtivo ou Improdutivo
   - **Resposta sugerida:** texto automático baseado na classificação
4. Para limpar os campos, clique em **Limpar**

---

## Deploy Online

- **Frontend:** [https://front-end-ochre-eta.vercel.app](https://vercel.com/juniorbueno1988s-projects/autou-case)
- **Backend:** [https://autou-case-backend-8ata.onrender.com](https://autou-case-backend-8ata.onrender.com)

> A aplicação online permite testar a classificação de emails diretamente no navegador, sem necessidade de instalação local.

---

## Demonstração

1. Inserção de texto:

![Exemplo de texto](docs/demo-text.png)

2. Upload de arquivo:

![Exemplo de upload](docs/demo-upload.png)

---

## Observações Técnicas

- O backend utiliza **CORS configurado** para permitir requisições do frontend.
- A classificação local é baseada em palavras-chave; integração com IA é opcional se a variável `USE_AI` estiver configurada.
- Suporta arquivos `.txt`, `.pdf` e `.csv` para envio de emails.

---

## Contato / Autor

- Desenvolvido por **Júnior Bueno**
- GitHub: [https://github.com/juniorbueno1988](https://github.com/juniorbueno1988)
- LinkedIn: [https://www.linkedin.com/in/junior-bueno/](https://www.linkedin.com/in/junior-bueno/)

---

## Licença

Projeto open-source, livre para uso e estudo.

