# 🤖 Bot Telegram - Controle Financeiro

Bot do Telegram integrado com a planilha financeira para registrar lançamentos de forma rápida e prática.

## 📋 Pré-requisitos

1. Python 3.8 ou superior instalado
2. Conta no Telegram
3. Planilha financeira (planilha_financeira.xlsx) na mesma pasta

## 🚀 Como Configurar

### 1. Criar o Bot no Telegram

1. Abra o Telegram e procure por `@BotFather`
2. Envie o comando `/newbot`
3. Escolha um nome para o bot (Ex: Meu Controle Financeiro)
4. Escolha um username único (Ex: meu_financeiro_bot)
5. **Copie o TOKEN** que o BotFather vai fornecer (algo como: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Instalar Dependências

Abra o terminal na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

### 3. Configurar o Token

Abra o arquivo `bot_telegram.py` e localize a linha:

```python
TOKEN = "SEU_TOKEN_AQUI"
```

Substitua `SEU_TOKEN_AQUI` pelo token que você recebeu do BotFather.

### 4. Executar o Bot

No terminal, execute:

```bash
python bot_telegram.py
```

Você verá a mensagem: `🤖 Bot iniciado! Pressione Ctrl+C para parar.`

## 📱 Como Usar

### Comandos Disponíveis

- `/start` - Iniciar o bot e ver os comandos disponíveis
- `/novo` - Adicionar um novo lançamento financeiro
- `/saldo` - Ver saldo realizado e a transcorrer
- `/ajuda` - Ver lista de comandos
- `/cancelar` - Cancelar a operação atual

### Fluxo de Adicionar Lançamento

Ao digitar `/novo`, o bot vai perguntar em sequência:

1. **Descrição**: Digite a descrição do lançamento (Ex: Almoço, Compras)
2. **Valor**: Digite o valor (Ex: 50.00 ou 50)
3. **Tipo**: Selecione usando o teclado (Receita ou Despesa)
4. **Método**: Selecione o método de pagamento usando o teclado
5. **Categoria**: Selecione a categoria usando o teclado

Após preencher todos os campos, o lançamento será salvo automaticamente na planilha Excel!

## 🔒 Segurança

- **Mantenha seu TOKEN em segredo!** Nunca compartilhe ou publique em repositórios públicos
- O bot acessa apenas o arquivo Excel local
- Não há envio de dados para servidores externos (além do Telegram)

## 🛠️ Solução de Problemas

### Bot não responde
- Verifique se o bot está rodando no terminal
- Confirme se o TOKEN está correto
- Verifique sua conexão com a internet

### Erro ao salvar lançamento
- Certifique-se de que o arquivo `planilha_financeira.xlsx` está na mesma pasta
- Verifique se o arquivo não está aberto no Excel
- Confirme que a planilha tem as abas "Lançamentos" e "Configurações"

### Erro de dependências
Execute novamente:
```bash
pip install --upgrade -r requirements.txt
```

## 💡 Dicas

- O bot usa teclados personalizados para facilitar a seleção de opções
- Você pode usar `/cancelar` a qualquer momento para cancelar uma operação
- O saldo é calculado automaticamente considerando a data atual
- Múltiplos usuários podem usar o bot simultaneamente

## 🌐 Hospedagem (Opcional)

Para manter o bot rodando 24/7, você pode hospedá-lo em:

### Opções Gratuitas:
- **Railway** (railway.app)
- **Render** (render.com) - 500h/mês grátis
- **PythonAnywhere** (pythonanywhere.com)

### Opções Pagas (~R$ 20-50/mês):
- DigitalOcean
- AWS EC2
- Google Cloud
- Azure

## 📞 Suporte

Se encontrar problemas, verifique:
1. Logs no terminal onde o bot está rodando
2. Se o arquivo Excel está correto
3. Se todas as dependências foram instaladas

---

💰 Bot desenvolvido para integração com o sistema de Controle Financeiro
