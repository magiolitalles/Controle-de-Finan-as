import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import pandas as pd
import openpyxl
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Caminho do arquivo Excel
ARQUIVO_EXCEL = "planilha_financeira.xlsx"

# Estados da conversa
DESCRICAO, VALOR, TIPO, METODO, CATEGORIA = range(5)

# Funções auxiliares
def carregar_configuracoes():
    """Carrega as configurações da planilha"""
    try:
        df_config = pd.read_excel(ARQUIVO_EXCEL, sheet_name='Configurações', header=None)
        
        necessidades = df_config.iloc[1:, 0].dropna().tolist()
        desejos = df_config.iloc[1:, 1].dropna().tolist()
        investimentos = df_config.iloc[1:, 2].dropna().tolist()
        metodos = df_config.iloc[1:, 3].dropna().tolist()
        tipos = df_config.iloc[1:, 4].dropna().tolist()
        
        todas_categorias = necessidades + desejos + investimentos
        
        return {
            'todas_categorias': todas_categorias,
            'metodos': metodos,
            'tipos': tipos
        }
    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")
        return None

def adicionar_lancamento(data, descricao, categoria, tipo, valor, metodo):
    """Adiciona um novo lançamento à planilha"""
    try:
        wb = openpyxl.load_workbook(ARQUIVO_EXCEL)
        ws = wb['Lançamentos']
        
        ultima_linha = ws.max_row + 1
        
        ws[f'A{ultima_linha}'] = data
        ws[f'B{ultima_linha}'] = descricao
        ws[f'C{ultima_linha}'] = categoria
        ws[f'D{ultima_linha}'] = tipo
        ws[f'E{ultima_linha}'] = valor
        ws[f'F{ultima_linha}'] = metodo
        ws[f'G{ultima_linha}'] = 'Realizado'
        
        wb.save(ARQUIVO_EXCEL)
        wb.close()
        
        return True
    except Exception as e:
        print(f"Erro ao adicionar lançamento: {e}")
        return False

def calcular_saldo():
    """Calcula o saldo realizado e a transcorrer"""
    try:
        df = pd.read_excel(ARQUIVO_EXCEL, sheet_name='Lançamentos')
        
        if df.empty:
            return None
        
        hoje = pd.Timestamp(datetime.now().date())
        
        # Calcular o último dia do mês seguinte
        if hoje.month == 12:
            proximo_mes = hoje.replace(year=hoje.year + 1, month=1, day=1)
        else:
            proximo_mes = hoje.replace(month=hoje.month + 1, day=1)
        
        if proximo_mes.month == 12:
            ultimo_dia_mes_seguinte = proximo_mes.replace(year=proximo_mes.year + 1, month=1, day=1) - pd.Timedelta(days=1)
        else:
            ultimo_dia_mes_seguinte = proximo_mes.replace(month=proximo_mes.month + 1, day=1) - pd.Timedelta(days=1)
        
        # Realizados
        df_realizados = df[df['Data'].dt.date <= hoje.date()]
        receitas_realizadas = df_realizados[df_realizados['Tipo'] == 'Receita']['Valor'].sum()
        despesas_realizadas = df_realizados[df_realizados['Tipo'] == 'Despesa']['Valor'].sum()
        saldo_realizado = receitas_realizadas - despesas_realizadas
        
        # A transcorrer
        amanha = hoje + pd.Timedelta(days=1)
        df_transcorrer = df[
            (df['Data'].dt.date >= amanha.date()) & 
            (df['Data'].dt.date <= ultimo_dia_mes_seguinte.date())
        ]
        receitas_transcorrer = df_transcorrer[df_transcorrer['Tipo'] == 'Receita']['Valor'].sum()
        despesas_transcorrer = df_transcorrer[df_transcorrer['Tipo'] == 'Despesa']['Valor'].sum()
        
        return {
            'saldo_realizado': saldo_realizado,
            'receitas_realizadas': receitas_realizadas,
            'despesas_realizadas': despesas_realizadas,
            'receitas_transcorrer': receitas_transcorrer,
            'despesas_transcorrer': despesas_transcorrer
        }
    except Exception as e:
        print(f"Erro ao calcular saldo: {e}")
        return None

# Comandos do bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    mensagem = (
        "🤖 *Bem-vindo ao Bot de Controle Financeiro!*\n\n"
        "Comandos disponíveis:\n"
        "/novo - Adicionar novo lançamento\n"
        "/saldo - Ver saldo e resumo\n"
        "/cancelar - Cancelar operação atual\n"
        "/ajuda - Ver esta mensagem"
    )
    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ajuda"""
    await start(update, context)

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /saldo"""
    resultado = calcular_saldo()
    
    if resultado is None:
        await update.message.reply_text("📭 Nenhum lançamento registrado ainda.")
        return
    
    mensagem = (
        "💰 *Resumo Financeiro*\n\n"
        f"✅ *Saldo Realizado:* R$ {resultado['saldo_realizado']:,.2f}\n"
        f"💚 Receitas realizadas: R$ {resultado['receitas_realizadas']:,.2f}\n"
        f"❤️ Despesas realizadas: R$ {resultado['despesas_realizadas']:,.2f}\n\n"
        f"📅 *A Transcorrer:*\n"
        f"Receitas: R$ {resultado['receitas_transcorrer']:,.2f}\n"
        f"Despesas: R$ {resultado['despesas_transcorrer']:,.2f}"
    )
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def novo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia o processo de adicionar novo lançamento"""
    await update.message.reply_text(
        "📝 Vamos adicionar um novo lançamento!\n\n"
        "Por favor, envie a *descrição* do lançamento:\n"
        "(Ex: Almoço, Compras, Salário, etc.)\n\n"
        "Use /cancelar para cancelar.",
        parse_mode='Markdown'
    )
    return DESCRICAO

async def receber_descricao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe a descrição"""
    context.user_data['descricao'] = update.message.text
    
    await update.message.reply_text(
        f"✅ Descrição: *{update.message.text}*\n\n"
        "💰 Agora, envie o *valor*:\n"
        "(Ex: 50.00 ou 50)",
        parse_mode='Markdown'
    )
    return VALOR

async def receber_valor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe o valor"""
    try:
        valor = float(update.message.text.replace(',', '.'))
        if valor <= 0:
            await update.message.reply_text("⚠️ O valor deve ser maior que zero. Tente novamente:")
            return VALOR
        
        context.user_data['valor'] = valor
        
        config = carregar_configuracoes()
        if config is None:
            await update.message.reply_text("❌ Erro ao carregar configurações.")
            return ConversationHandler.END
        
        # Criar teclado com os tipos
        keyboard = [[tipo] for tipo in config['tipos']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            f"✅ Valor: *R$ {valor:.2f}*\n\n"
            "💵 Selecione o *tipo*:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return TIPO
    except ValueError:
        await update.message.reply_text("⚠️ Valor inválido. Use números (Ex: 50.00). Tente novamente:")
        return VALOR

async def receber_tipo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe o tipo"""
    context.user_data['tipo'] = update.message.text
    
    config = carregar_configuracoes()
    if config is None:
        await update.message.reply_text("❌ Erro ao carregar configurações.")
        return ConversationHandler.END
    
    # Criar teclado com os métodos
    keyboard = [[metodo] for metodo in config['metodos']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        f"✅ Tipo: *{update.message.text}*\n\n"
        "💳 Selecione o *método de pagamento*:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return METODO

async def receber_metodo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe o método"""
    context.user_data['metodo'] = update.message.text
    
    config = carregar_configuracoes()
    if config is None:
        await update.message.reply_text("❌ Erro ao carregar configurações.")
        return ConversationHandler.END
    
    # Criar teclado com as categorias (2 por linha para facilitar)
    categorias = config['todas_categorias']
    keyboard = [categorias[i:i+2] for i in range(0, len(categorias), 2)]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        f"✅ Método: *{update.message.text}*\n\n"
        "🏷️ Selecione a *categoria*:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return CATEGORIA

async def receber_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe a categoria e finaliza o lançamento"""
    context.user_data['categoria'] = update.message.text
    
    # Salvar o lançamento
    data = datetime.now()
    descricao = context.user_data['descricao']
    valor = context.user_data['valor']
    tipo = context.user_data['tipo']
    metodo = context.user_data['metodo']
    categoria = context.user_data['categoria']
    
    if adicionar_lancamento(data, descricao, categoria, tipo, valor, metodo):
        mensagem = (
            "✅ *Lançamento adicionado com sucesso!*\n\n"
            f"📝 Descrição: {descricao}\n"
            f"💰 Valor: R$ {valor:.2f}\n"
            f"💵 Tipo: {tipo}\n"
            f"💳 Método: {metodo}\n"
            f"🏷️ Categoria: {categoria}\n"
            f"📅 Data: {data.strftime('%d/%m/%Y')}"
        )
        await update.message.reply_text(
            mensagem,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "❌ Erro ao adicionar lançamento. Tente novamente.",
            reply_markup=ReplyKeyboardRemove()
        )
    
    # Limpar dados do usuário
    context.user_data.clear()
    
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela a operação atual"""
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Operação cancelada.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    """Função principal"""
    # Carregar token do arquivo .env
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        print("❌ ERRO: Token do Telegram não encontrado!")
        print("Por favor, crie um arquivo .env baseado no .env.example")
        return
    
    # Criar a aplicação
    application = Application.builder().token(TOKEN).build()
    
    # Handler de conversa para adicionar lançamento
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('novo', novo)],
        states={
            DESCRICAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_descricao)],
            VALOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_valor)],
            TIPO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_tipo)],
            METODO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_metodo)],
            CATEGORIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_categoria)],
        },
        fallbacks=[CommandHandler('cancelar', cancelar)]
    )
    
    # Adicionar handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ajuda', ajuda))
    application.add_handler(CommandHandler('saldo', saldo))
    application.add_handler(conv_handler)
    
    # Iniciar o bot
    print("🤖 Bot iniciado! Pressione Ctrl+C para parar.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
