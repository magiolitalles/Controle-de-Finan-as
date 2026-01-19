"""
Script para visualizar os logs dos serviços em tempo real
"""
import sys
import time
from pathlib import Path
import os

def tail_file(file_path, lines=20):
    """Lê as últimas N linhas de um arquivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Ler todas as linhas e pegar as últimas N
            all_lines = f.readlines()
            return all_lines[-lines:]
    except:
        return []

def watch_logs():
    """Monitora os logs em tempo real"""
    
    base_dir = Path(__file__).parent
    streamlit_log = base_dir / "streamlit.log"
    bot_log = base_dir / "bot_telegram.log"
    
    # Verificar se os serviços estão rodando
    streamlit_pid = base_dir / ".streamlit.pid"
    bot_pid = base_dir / ".bot.pid"
    
    if not streamlit_pid.exists() and not bot_pid.exists():
        print("⚠️  Nenhum serviço em execução.")
        print("Use 'python start.py' para iniciar os serviços.")
        return
    
    print("📋 Monitorando logs dos serviços...")
    print("Pressione Ctrl+C para sair\n")
    print("="*80)
    
    # Posições atuais dos arquivos
    streamlit_pos = 0
    bot_pos = 0
    
    try:
        while True:
            # Ler logs do Streamlit
            if streamlit_log.exists():
                with open(streamlit_log, 'r', encoding='utf-8', errors='ignore') as f:
                    f.seek(streamlit_pos)
                    new_lines = f.readlines()
                    streamlit_pos = f.tell()
                    
                    for line in new_lines:
                        print(f"[STREAMLIT] {line.rstrip()}")
            
            # Ler logs do Bot
            if bot_log.exists():
                with open(bot_log, 'r', encoding='utf-8', errors='ignore') as f:
                    f.seek(bot_pos)
                    new_lines = f.readlines()
                    bot_pos = f.tell()
                    
                    for line in new_lines:
                        print(f"[BOT] {line.rstrip()}")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n✨ Monitoramento de logs encerrado.")
        print("\n💡 Os serviços continuam rodando em background.")
        print("   Use 'python stop.py' para parar os serviços.")

if __name__ == '__main__':
    watch_logs()
