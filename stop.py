"""
Script para parar o aplicativo Streamlit e o Bot Telegram
"""
import os
import sys
from pathlib import Path
import signal

def stop_services():
    """Para os serviços em execução"""
    
    # Diretório atual
    base_dir = Path(__file__).parent
    
    # Arquivos de PID
    streamlit_pid_file = base_dir / ".streamlit.pid"
    bot_pid_file = base_dir / ".bot.pid"
    
    stopped = False
    
    # Parar Streamlit
    if streamlit_pid_file.exists():
        try:
            with open(streamlit_pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Tentar parar o processo
            if sys.platform == 'win32':
                os.system(f'taskkill /PID {pid} /F >nul 2>&1')
            else:
                os.kill(pid, signal.SIGTERM)
            
            streamlit_pid_file.unlink()
            print(f"✅ Streamlit parado (PID: {pid})")
            stopped = True
        except Exception as e:
            print(f"⚠️  Erro ao parar Streamlit: {e}")
            # Remover arquivo PID mesmo com erro
            if streamlit_pid_file.exists():
                streamlit_pid_file.unlink()
    
    # Parar Bot Telegram
    if bot_pid_file.exists():
        try:
            with open(bot_pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Tentar parar o processo
            if sys.platform == 'win32':
                os.system(f'taskkill /PID {pid} /F >nul 2>&1')
            else:
                os.kill(pid, signal.SIGTERM)
            
            bot_pid_file.unlink()
            print(f"✅ Bot Telegram parado (PID: {pid})")
            stopped = True
        except Exception as e:
            print(f"⚠️  Erro ao parar Bot Telegram: {e}")
            # Remover arquivo PID mesmo com erro
            if bot_pid_file.exists():
                bot_pid_file.unlink()
    
    if not stopped:
        print("ℹ️  Nenhum serviço em execução.")
    else:
        print("\n✨ Todos os serviços foram parados com sucesso!")

if __name__ == '__main__':
    stop_services()
