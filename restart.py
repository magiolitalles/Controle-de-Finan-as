"""
Script para reiniciar o aplicativo Streamlit e o Bot Telegram
"""
import subprocess
import sys
import os
import time
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
    
    print("🛑 Parando serviços...")
    
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
            print(f"  ✅ Streamlit parado (PID: {pid})")
            stopped = True
        except Exception as e:
            print(f"  ⚠️  Erro ao parar Streamlit: {e}")
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
            print(f"  ✅ Bot Telegram parado (PID: {pid})")
            stopped = True
        except Exception as e:
            print(f"  ⚠️  Erro ao parar Bot Telegram: {e}")
            # Remover arquivo PID mesmo com erro
            if bot_pid_file.exists():
                bot_pid_file.unlink()
    
    if not stopped:
        print("  ℹ️  Nenhum serviço estava em execução.")
    
    # Aguardar um momento para garantir que os processos foram encerrados
    time.sleep(2)
    
    return stopped

def start_services():
    """Inicia os serviços em background"""
    
    # Diretório atual
    base_dir = Path(__file__).parent
    
    # Arquivos de PID e logs
    streamlit_pid_file = base_dir / ".streamlit.pid"
    bot_pid_file = base_dir / ".bot.pid"
    streamlit_log_file = base_dir / "streamlit.log"
    bot_log_file = base_dir / "bot_telegram.log"
    
    print("\n🚀 Iniciando serviços...")
    
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
        
        print(f"  ✅ Streamlit iniciado (PID: {streamlit_process.pid})")
        print(f"     Acesse: http://localhost:8501")
    except Exception as e:
        print(f"  ❌ Erro ao iniciar Streamlit: {e}")
        return False
    
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
        
        print(f"  ✅ Bot Telegram iniciado (PID: {bot_process.pid})")
    except Exception as e:
        print(f"  ❌ Erro ao iniciar Bot Telegram: {e}")
        # Parar Streamlit se o bot falhar
        streamlit_process.terminate()
        streamlit_pid_file.unlink()
        return False
    
    return True

def restart_services():
    """Reinicia todos os serviços"""
    print("🔄 REINICIANDO SERVIÇOS")
    print("="*50)
    
    # Parar serviços
    stop_services()
    
    # Iniciar serviços
    if start_services():
        print("\n" + "="*50)
        print("✨ Serviços reiniciados com sucesso!")
        print("="*50)
        print("\n📋 Comandos disponíveis:")
        print("  • python logs.py      - Ver logs em tempo real")
        print("  • python stop.py      - Parar todos os serviços")
        print("  • python restart.py   - Reiniciar todos os serviços")
        print("\n💡 Os serviços estão rodando em background.")
    else:
        print("\n❌ Erro ao reiniciar os serviços.")

if __name__ == '__main__':
    restart_services()
