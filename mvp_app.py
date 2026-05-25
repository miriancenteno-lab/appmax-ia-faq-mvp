"""
Appmax IA FAQ — MVP v2
Cores: Appmax brand palette (#9B6AFA Pantone 265C)
Credenciais: via .env (nunca no código)
"""

import streamlit as st
import anthropic
import datetime
import os

# ─── CARREGA .env LOCAL (ignorado no Streamlit Cloud — usa st.secrets) ────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv não instalado no Cloud — OK, usa st.secrets

def get_secret(key: str, default: str = "") -> str:
    """Busca credencial: st.secrets (Cloud) → .env local → default."""
    try:
        return st.secrets[key]
    except Exception:
        return os.environ.get(key, default)

# ─── CONFIG ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Appmax IA FAQ",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── ESTILOS — Appmax Brand Palette ──────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');

  /* Reset fonts */
  html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #F7F3FF !important;
  }

  /* Header da página */
  .appmax-header {
    background: linear-gradient(135deg, #281E49 0%, #553999 100%);
    padding: 16px 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
  }

  /* Bolhas do chat */
  .chat-bubble-user {
    background: #C4A6FD;
    border-radius: 14px 14px 2px 14px;
    padding: 12px 16px;
    margin: 6px 0;
    font-family: 'DM Sans', sans-serif;
    color: #281E49;
    max-width: 80%;
    float: right;
    clear: both;
    font-size: 14px;
  }
  .chat-bubble-ai {
    background: #FFFFFF;
    border-left: 4px solid #9B6AFA;
    border-radius: 2px 14px 14px 14px;
    padding: 12px 16px;
    margin: 6px 0;
    font-family: 'DM Sans', sans-serif;
    color: #281E49;
    max-width: 90%;
    float: left;
    clear: both;
    font-size: 14px;
    box-shadow: 0 2px 8px rgba(40,30,73,0.08);
  }
  .chat-wrapper { overflow: hidden; margin-bottom: 8px; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background-color: #281E49 !important;
  }
  [data-testid="stSidebar"] * {
    color: #E6E0FC !important;
    font-family: 'DM Sans', sans-serif !important;
  }
  [data-testid="stSidebar"] .stMarkdown p {
    color: #C4A6FD !important;
  }

  /* Botões */
  div.stButton > button {
    background: linear-gradient(135deg, #9B6AFA, #7252BF) !important;
    color: #FFFFFF !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    transition: opacity 0.2s !important;
  }
  div.stButton > button:hover {
    opacity: 0.88 !important;
  }

  /* Input de texto */
  .stTextInput input, .stTextArea textarea {
    border: 2px solid #C4A6FD !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    background: #FFFFFF !important;
    color: #281E49 !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #9B6AFA !important;
    box-shadow: 0 0 0 3px rgba(155,106,250,0.18) !important;
  }

  /* Chat input */
  [data-testid="stChatInput"] textarea {
    border: 2px solid #C4A6FD !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    background: #FFFFFF !important;
    color: #281E49 !important;
  }

  /* Mensagem de chat user */
  [data-testid="stChatMessage"] {
    background: transparent !important;
  }

  /* Divider */
  hr { border-color: #553999 !important; opacity: 0.3; }

  /* Links */
  a { color: #9B6AFA !important; }
</style>
""", unsafe_allow_html=True)

# ─── BASE DE CONHECIMENTO ─────────────────────────────────────────────────────
# ATENÇÃO: No MVP, o conteúdo abaixo é PLACEHOLDER ILUSTRATIVO.
# Para produção, substituir pela documentação real das equipes internas da Appmax.

KNOWLEDGE_BASE = {
    "checkout_transparente": {
        "nivel_minimo": 1,
        "categoria": "Checkout",
        "titulo": "Checkout Transparente",
        "conteudo_nivel1": """
## Checkout Transparente

O Checkout Transparente permite ao parceiro realizar cobranças diretamente em seu próprio site, sem redirecionar o cliente para uma página externa.

**O que é:**
Modalidade de pagamento onde o formulário de cobrança fica integrado ao site do parceiro. O cliente não percebe que está usando a infraestrutura da Appmax.

**Meios de pagamento suportados:**
- Cartão de crédito (parcelado ou à vista)
- Cartão de débito
- Pix
- Boleto bancário

**Vantagens para o parceiro:**
- Maior conversão (cliente não sai da loja)
- Controle total da experiência visual
- Sem redirecionamento

**Quando usar:**
Indicado para parceiros com equipe técnica capaz de integrar via API.
        """,
        "conteudo_nivel2": """
## Checkout Transparente — Detalhes Técnicos

[PLACEHOLDER — substituir pela documentação técnica oficial da Appmax]

**Integração:**
A integração é feita via API REST. O parceiro envia os dados do pedido para o endpoint de criação de transação, recebe um token e finaliza o pagamento no frontend.

**Fluxo técnico:**
1. Backend do parceiro chama `POST /v1/transactions` com dados do pedido
2. Appmax retorna `transaction_id` e `payment_token`
3. Frontend usa o SDK JavaScript da Appmax para tokenização segura (PCI)
4. Frontend envia token + dados do cartão para `POST /v1/transactions/{id}/pay`
5. Appmax processa e retorna status: `approved`, `refused`, `pending`

**Parâmetros principais:**
- `amount`: valor em centavos (ex: 10000 = R$ 100,00)
- `installments`: número de parcelas (1 a 12)
- `payment_method`: `credit_card`, `debit_card`, `pix`, `boleto`

**Documentação de Referência:**
https://docs.appmax.com.br/checkout-transparente *(link placeholder — atualizar com URL real)*
        """
    },
    "pix": {
        "nivel_minimo": 1,
        "categoria": "Meios de Pagamento",
        "titulo": "Pix",
        "conteudo_nivel1": """
## Pix

O Pix é um meio de pagamento instantâneo do Banco Central. A Appmax oferece o Pix como opção de pagamento para os parceiros.

**Como funciona:**
O comprador escolhe Pix na hora de pagar. A Appmax gera um QR Code ou código copia-e-cola. O pagamento é confirmado em segundos.

**Características:**
- Pagamento instantâneo
- Disponível 24h/7 dias
- Sem parcelamento (à vista)
- QR Code com validade configurável (padrão: 30 minutos)

**Vantagem:**
Taxa menor que cartão de crédito. Liquidação mais rápida.
        """,
        "conteudo_nivel2": """
## Pix — Detalhes Técnicos

[PLACEHOLDER — substituir pela documentação técnica oficial da Appmax]

**Criação de cobrança Pix:**
```
POST /v1/transactions
{
  "payment_method": "pix",
  "amount": 10000,
  "pix_expiration_seconds": 1800,
  "customer": { "name": "...", "document": "...", "email": "..." }
}
```

**Resposta:**
```json
{
  "transaction_id": "txn_abc123",
  "status": "pending",
  "pix": {
    "qr_code": "data:image/png;base64,...",
    "qr_code_text": "00020126...",
    "expiration_at": "2025-05-01T10:30:00Z"
  }
}
```

**Confirmação:** webhook `transaction.approved`
**Liquidação:** D+1 (próximo dia útil)

**Documentação de Referência:**
https://docs.appmax.com.br/pix *(link placeholder — atualizar com URL real)*
        """
    },
    "antifraude": {
        "nivel_minimo": 1,
        "categoria": "Segurança",
        "titulo": "Antifraude",
        "conteudo_nivel1": """
## Antifraude

O sistema Antifraude da Appmax analisa automaticamente todas as transações de cartão de crédito antes de autorizar o pagamento.

**O que faz:**
Analisa variáveis de cada transação (dispositivo, localização, comportamento do comprador, histórico) e atribui um score de risco.

**Resultados possíveis:**
- **Aprovado:** transação segura
- **Revisão manual:** risco médio, análise manual
- **Recusado:** alto risco, bloqueado

**O parceiro precisa configurar algo?**
Não. O antifraude roda automaticamente em todas as transações de cartão.

**Chargebacks:**
Em caso de fraude aprovada pelo antifraude, existe cobertura conforme contrato.
        """,
        "conteudo_nivel2": """
## Antifraude — Detalhes Técnicos

[PLACEHOLDER — substituir pela documentação técnica oficial da Appmax]

**Score de risco (0 a 1000):**
| Score | Resultado | Ação |
|-------|-----------|------|
| 0 – 399 | Baixo risco | Aprovado automaticamente |
| 400 – 699 | Risco médio | Fila de revisão manual |
| 700 – 1000 | Alto risco | Recusado automaticamente |

**Resposta na API:**
```json
{
  "antifraud": {
    "score": 120,
    "result": "approved",
    "recommendation": "approve"
  }
}
```

**Documentação de Referência:**
https://docs.appmax.com.br/antifraude *(link placeholder — atualizar com URL real)*
        """
    },
}

# ─── USUÁRIOS — carregados do .env / st.secrets ───────────────────────────────
# Formato no .env:
# USER_suporte_at_appmax_com={"nome":"Colaborador Suporte","equipe":"Suporte","nivel":1,"senha":"SUA_SENHA"}
# Ou use USERS_JSON com o dicionário completo serializado em JSON.
#
# Para o MVP de demonstração, se não houver usuários no .env, usa os defaults abaixo.

import json

def load_users() -> dict:
    raw = get_secret("USERS_JSON", "")
    if raw:
        try:
            return json.loads(raw)
        except Exception:
            pass
    # Fallback demo — SÓ PARA MVP/DEMONSTRAÇÃO
    return {
        "suporte@appmax.com":  {"nome": "Colaborador Suporte",  "equipe": "Suporte",     "nivel": 1, "senha": get_secret("DEMO_PASS", "appmax@2025")},
        "tecnico@appmax.com":  {"nome": "Colaborador Técnico",  "equipe": "Integrações", "nivel": 2, "senha": get_secret("DEMO_PASS", "appmax@2025")},
        "gestor@appmax.com":   {"nome": "Gestor",               "equipe": "Produto",     "nivel": 4, "senha": get_secret("DEMO_PASS", "appmax@2025")},
    }

USERS = load_users()

# ─── FUNÇÕES AUXILIARES ───────────────────────────────────────────────────────

def get_knowledge_context(nivel: int) -> str:
    docs = []
    for key, doc in KNOWLEDGE_BASE.items():
        if doc["nivel_minimo"] <= nivel:
            content = doc["conteudo_nivel2"] if nivel >= 2 else doc["conteudo_nivel1"]
            docs.append(f"### {doc['titulo']} (Categoria: {doc['categoria']})\n{content}")
    return "\n\n---\n\n".join(docs)


def build_system_prompt(nivel: int, nome: str, equipe: str) -> str:
    conhecimento = get_knowledge_context(nivel)
    nivel_instrucoes = ""
    if nivel >= 2:
        nivel_instrucoes = "- Ao final de cada resposta inclua uma seção chamada **Documentação de Referência** com o link relevante da documentação oficial do produto ou serviço consultado.\n- Você pode fornecer dados técnicos, tabelas, exemplos de código e parâmetros de API."
    else:
        nivel_instrucoes = "- Forneça apenas explicações conceituais simples. Não inclua dados técnicos, parâmetros de API ou links externos.\n- Seu objetivo é ajudar o colaborador a esclarecer dúvidas para responder parceiros no atendimento."

    return f"""Você é o assistente interno de FAQ da Appmax, empresa processadora de pagamentos online.

Você está respondendo para: {nome} (Equipe: {equipe}, Nível de acesso: {nivel})

REGRAS OBRIGATÓRIAS:
1. Responda APENAS com base nas informações da Base de Conhecimento fornecida abaixo.
2. NÃO busque informações externas, NÃO invente dados, NÃO crie links que não estejam na documentação.
3. Use linguagem clara, objetiva e direta. Sem gírias ou superlativos.
4. Se a dúvida não tiver resposta na Base de Conhecimento, responda EXATAMENTE: "Desculpe, ainda não tenho informações sobre esse produto ou serviço."
5. Todos os usuários são colaboradores da Appmax — seja direto, sem introduções desnecessárias.
{nivel_instrucoes}

BASE DE CONHECIMENTO:
{conhecimento}"""


def ask_claude(pergunta: str, historico: list, nivel: int, nome: str, equipe: str) -> str:
    api_key = get_secret("ANTHROPIC_API_KEY")
    if not api_key:
        return "⚠️ **Chave de API não configurada.** Adicione `ANTHROPIC_API_KEY` no arquivo `.env` (local) ou em `Secrets` no Streamlit Cloud."

    try:
        client = anthropic.Anthropic(api_key=api_key)
        messages = []
        for msg in historico[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": pergunta})

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            system=build_system_prompt(nivel, nome, equipe),
            messages=messages,
        )
        return response.content[0].text
    except Exception as e:
        return f"⚠️ Erro ao conectar com a IA: {str(e)}"


def registrar_sem_resposta(pergunta: str, nome: str, equipe: str):
    """Registra no Google Sheets se configurado."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        creds_raw = get_secret("GOOGLE_CREDENTIALS")
        if not creds_raw:
            return
        creds = Credentials.from_service_account_info(
            json.loads(creds_raw),
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        gc = gspread.authorize(creds)
        sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1LgadVm-akVlONdwrSEuoC7aFN8lOXIqSIYr4yLkvNkM/edit")
        ws = sheet.get_worksheet(0)
        ws.append_row([datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), pergunta, nome, equipe])
    except Exception:
        pass

# ─── ESTADO ───────────────────────────────────────────────────────────────────
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "historico" not in st.session_state:
    st.session_state.historico = []

# ─── TELA DE LOGIN ────────────────────────────────────────────────────────────
if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:48px 0 24px 0;">
          <div style="font-size:48px; font-weight:800; font-family:'DM Sans',sans-serif; color:#281E49; letter-spacing:-1px;">
            <span style="color:#9B6AFA;">APP</span>MAX
          </div>
          <div style="font-size:15px; color:#7252BF; font-family:'DM Sans',sans-serif; margin-top:6px; font-weight:500;">
            IA FAQ — Processos e Serviços
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("##### Entrar na plataforma")
            email = st.text_input("E-mail", placeholder="seu@appmax.com", label_visibility="collapsed")
            senha = st.text_input("Senha", type="password", placeholder="Senha", label_visibility="collapsed")

            if st.button("Entrar →", use_container_width=True):
                if not email.endswith("@appmax.com"):
                    st.error("⛔ Acesso restrito a e-mails @appmax.com.")
                elif email not in USERS:
                    st.error("Usuário não encontrado. Solicite convite ao seu gestor.")
                elif USERS[email]["senha"] != senha:
                    st.error("Senha incorreta.")
                else:
                    st.session_state.autenticado = True
                    st.session_state.usuario = {**USERS[email], "email": email}
                    st.session_state.historico = []
                    st.rerun()

        st.markdown("""
        <div style="text-align:center; margin-top:32px; color:#A8A7BC; font-size:12px; font-family:'DM Sans',sans-serif; line-height:1.8;">
          MVP — Demonstração<br/>
          <strong>suporte@appmax.com</strong> · <strong>tecnico@appmax.com</strong> · <strong>gestor@appmax.com</strong><br/>
          Senha definida em <code>DEMO_PASS</code> no .env
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ─── APP PRINCIPAL ────────────────────────────────────────────────────────────
u = st.session_state.usuario
nivel_labels = {1: "Suporte", 2: "Técnico / Comercial", 3: "Escritor", 4: "Gestor"}

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 8px 0;">
      <div style="font-size:22px; font-weight:800; letter-spacing:-0.5px; color:#C4A6FD; font-family:'DM Sans',sans-serif;">
        <span style="color:#9B6AFA;">APP</span>MAX
      </div>
      <div style="font-size:11px; color:#7252BF; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:16px;">IA FAQ</div>
      <div style="font-size:15px; font-weight:600; color:#E6E0FC;">{u['nome']}</div>
      <div style="font-size:12px; color:#A8A7BC;">{u['email']}</div>
      <div style="font-size:12px; color:#A8A7BC;">Equipe: {u['equipe']}</div>
      <div style="margin-top:10px;">
        <span style="background:#9B6AFA; color:#FFFFFF; font-weight:700; font-size:11px; padding:3px 12px; border-radius:20px;">
          Nível {u['nivel']} — {nivel_labels.get(u['nivel'], '')}
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='font-size:11px; text-transform:uppercase; letter-spacing:1px; color:#7252BF; margin-bottom:6px;'>Base de Conhecimento</div>", unsafe_allow_html=True)
    for key, doc in KNOWLEDGE_BASE.items():
        if doc["nivel_minimo"] <= u["nivel"]:
            st.markdown(f"<div style='font-size:12px; color:#C4A6FD; padding:2px 0;'>• {doc['titulo']}</div>", unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️ Nova conversa", use_container_width=True):
        st.session_state.historico = []
        st.rerun()
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.autenticado = False
        st.session_state.usuario = None
        st.session_state.historico = []
        st.rerun()

# Header
st.markdown(f"""
<div style="background:linear-gradient(135deg,#281E49 0%,#553999 100%);padding:14px 24px;border-radius:12px;margin-bottom:20px;display:flex;align-items:center;gap:12px;">
  <span style="font-size:20px;font-weight:800;color:white;font-family:'DM Sans',sans-serif;">
    <span style="color:#9B6AFA;">APP</span>MAX &nbsp;|&nbsp; IA FAQ
  </span>
  <span style="flex:1;"></span>
  <span style="font-size:12px;color:#C4A6FD;">💬 Tire suas dúvidas sobre produtos e serviços</span>
</div>
""", unsafe_allow_html=True)

# Chat
if not st.session_state.historico:
    st.markdown("""
    <div style="text-align:center;padding:48px;color:#A8A7BC;font-family:'DM Sans',sans-serif;">
      <div style="font-size:40px;margin-bottom:14px;">💬</div>
      <div style="font-size:16px;color:#7252BF;font-weight:600;">Como posso ajudar?</div>
      <div style="font-size:13px;margin-top:8px;">Digite sua dúvida sobre qualquer produto ou serviço da Appmax.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.historico:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["content"])

pergunta = st.chat_input("Digite sua dúvida sobre produtos ou serviços da Appmax...")

if pergunta:
    st.session_state.historico.append({"role": "user", "content": pergunta})
    with st.spinner("Consultando base de conhecimento..."):
        resposta = ask_claude(pergunta, st.session_state.historico[:-1], u["nivel"], u["nome"], u["equipe"])
    if "ainda não tenho informações" in resposta.lower():
        registrar_sem_resposta(pergunta, u["nome"], u["equipe"])
    st.session_state.historico.append({"role": "assistant", "content": resposta})
    st.rerun()
