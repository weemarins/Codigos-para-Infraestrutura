import os
import time
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Caminhos de monitoramento e origem
pasta_monitorada = r'C:\exemplo\exemplo'  # Pasta de rede a ser monitorada
pasta_origem = r'C:\exemplo\exemplo'      # Pasta onde procurar pastas com o mesmo nome

# Função para verificar se há espaço suficiente no disco de destino
def espaco_suficiente(necessario, destino):
    total, usado, livre = shutil.disk_usage(destino)
    return livre > necessario

# Função para copiar o conteúdo de uma pasta para outra, incluindo subpastas e arquivos
def copiar_conteudo(origem, destino):
    try:
        total_size = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(origem) for file in files)
        
        # Verifica se há espaço suficiente no destino
        if not espaco_suficiente(total_size, destino):
            logging.error(f'Espaço insuficiente para copiar o conteúdo de {origem} para {destino}.')
            return

        for root, dirs, files in os.walk(origem):
            # Calcula o caminho relativo da origem para manter a estrutura de pastas
            caminho_relativo = os.path.relpath(root, origem)
            destino_completo = os.path.join(destino, caminho_relativo)

            # Cria subpastas no destino, se necessário
            if not os.path.exists(destino_completo):
                os.makedirs(destino_completo)

            # Copia todos os arquivos
            for file in files:
                origem_arquivo = os.path.join(root, file)
                destino_arquivo = os.path.join(destino_completo, file)
                shutil.copy2(origem_arquivo, destino_arquivo)  # Copia o arquivo preservando metadados

        logging.info(f'Todo o conteúdo da pasta {origem} foi copiado para {destino}.')

    except Exception as e:
        logging.error(f'Erro ao copiar conteúdo: {e}')

# Handler que irá lidar com novos eventos
class MonitoramentoHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Quando uma nova pasta for criada
        if event.is_directory:
            nova_pasta = os.path.basename(event.src_path)
            logging.info(f'Nova pasta detectada: {nova_pasta}')

            # Verifica se existe uma pasta com o mesmo nome na pasta de origem
            origem_completa = os.path.join(pasta_origem, nova_pasta)
            destino_completo = event.src_path
            
            if os.path.exists(origem_completa):
                # Se a pasta existir na origem, copia o conteúdo para a nova pasta criada
                copiar_conteudo(origem_completa, destino_completo)
            else:
                logging.info(f'A pasta {nova_pasta} não foi encontrada na origem. Continuando a verificação.')

# Função principal para iniciar o monitoramento
def iniciar_monitoramento():
    event_handler = MonitoramentoHandler()
    observer = Observer()
    observer.schedule(event_handler, pasta_monitorada, recursive=False)
    
    logging.info(f'Iniciando monitoramento da pasta: {pasta_monitorada}')
    observer.start()

    try:
        while True:
            time.sleep(5)  # Intervalo entre verificações
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    iniciar_monitoramento()
