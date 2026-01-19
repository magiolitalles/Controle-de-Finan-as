"""
Script para iniciar o aplicativo Streamlit e o Bot Telegram em background
"""
import subprocess
import sys
import os
from pathlib import Path

def start_services():
    """Inicia os serviços em background"""
    
    # Diretório atual
    base_dir = Path(__file__).parent
    
    # Arquivos de PID e logs
    streamlit_pid_file = base_dir / ".streamlit.pid"
    bot_pid_file = base_dir / ".bot.pid"
    streamlit_log_file = base_dir / "streamlit.log"
    bot_log_file = base_dir / "bot_telegram.log"
    
    # Verificar se já estão rodando
    if streamlit_pid_file.exists() or bot_pid_file.exists():
        print("⚠️  Serviços já estão em execução!")
        print("Use 'python stop.py' para parar os serviços antes de iniciá-los novamente.")
        return
    
    print("🚀 Iniciando serviços...")
    
    # Iniciar Streamlit
    try:
        with open(streamlit_log_file, 'w', encoding='utf-8') as log:
            streamlit_process = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", "app_lancamentos.py.py", "--server.headless", "true"],
                stdout=log,
                stderr=log,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
        
        # Salvar PID do Streamlit
        with open(streamlit_pid_file, 'w') as f:
            f.write(str(streamlit_process.pid))
        
        print(f"✅ Streamlit iniciado (PID: {streamlit_process.pid})")
        print(f"   Acesse: http://localhost:8501")
    except Exception as e:
        print(f"❌ Erro ao iniciar Streamlit: {e}")
        return
    
    # Iniciar Bot Telegram
    try:
        with open(bot_log_file, 'w', encoding='utf-8') as log:
            bot_process = subprocess.Popen(
                [sys.executable, "bot_telegram.py"],
                stdout=log,
                stderr=log,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
        
        # Salvar PID do Bot
        with open(bot_pid_file, 'w') as f:
            f.write(str(bot_process.pid))
        
        print(f"✅ Bot Telegram iniciado (PID: {bot_process.pid})")
    except Exception as e:
        print(f"❌ Erro ao iniciar Bot Telegram: {e}")
        # Parar Streamlit se o bot falhar
        streamlit_process.terminate()
        streamlit_pid_file.unlink()
        return
    
    print("\n" + "="*50)
    print("✨ Todos os serviços foram iniciados com sucesso!")
    print("="*50)
    print("\n📋 Comandos disponíveis:")
    print("  • python logs.py      - Ver logs em tempo real")
    print("  • python stop.py      - Parar todos os serviços")
    print("\n💡 Os serviços estão rodando em background.")

if __name__ == '__main__':
    start_services()
