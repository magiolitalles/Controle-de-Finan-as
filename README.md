# 💰 Sistema de Controle Financeiro

Sistema completo de controle financeiro com interface web (Streamlit) e bot do Telegram para registro de lançamentos.

## 🚀 Início Rápido

### Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o token do Telegram:
   - Copie `.env.example` para `.env`
   - Adicione seu token do BotFather no arquivo `.env`

### Executando o Sistema

**Iniciar todos os serviços:**
```bash
python start.py
```

Isso iniciará:
- 🌐 Aplicativo Streamlit em http://localhost:8501
- 🤖 Bot do Telegram em background

**Ver logs em tempo real:**
```bash
python logs.py
```
Pressione `Ctrl+C` para sair (os serviços continuam rodando)

**Parar todos os serviços:**
```bash
python stop.py
```

## 📋 Funcionalidades

### Aplicativo Web (Streamlit)
- ✅ Registro de lançamentos financeiros
- 📊 Visualização de histórico com filtros
- 📈 Gráficos e resumos financeiros
- 💰 Acompanhamento de saldo realizado vs a transcorrer

### Bot do Telegram
- 💬 Adicionar lançamentos via chat
- 📊 Consultar saldo e resumo
- 🔔 Interface interativa com teclados personalizados

## 🛠️ Tecnologias

- Python 3.11+
- Streamlit
- python-telegram-bot
- pandas
- openpyxl

## 📝 Estrutura de Arquivos

```
├── app_lancamentos.py.py   # Aplicativo Streamlit
├── bot_telegram.py          # Bot do Telegram
├── start.py                 # Script para iniciar serviços
├── stop.py                  # Script para parar serviços
├── logs.py                  # Script para ver logs
├── requirements.txt         # Dependências
├── .env                     # Configurações (não versionado)
└── planilha_financeira.xlsx # Dados (não versionado)
```

## 🔐 Segurança

- O token do Telegram é armazenado em `.env` (não versionado)
- A planilha com dados financeiros não é enviada ao Git
- Logs são mantidos localmente

## 📄 Licença

Desenvolvido com Python e Streamlit
