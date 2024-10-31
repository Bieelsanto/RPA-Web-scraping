import os
import time
from dotenv import load_dotenv

# Executa uma função contabilizando o tempo de sua execução, e por fim inserindo esta execução no log
def execute_step(func: callable, desc: str):

    # Obtém o tempo atual
    startTime = time.time()

    # Inicializa a flag de erro
    erro = False

    # Inicializa flag de status
    status = "SUCESSO"

    # Tenta executar a função
    try:

        # Executa a função
        func()

    # Se falhar a execução, adiciona "ERRO" na descrição da etapa e determina que houve erro por meio da flag de erro
    except Exception as e:

        # Adiciona "ERRO" na descrição e o log no final
        desc = (f'{desc}: {str(e)}')[:1000]

        # Altera a flag de erro para True
        erro = True

        # Altera a flag de status para Erro
        status = "ERRO"

    # Imprime estas informações para depuração e por fim, insere no log.
    finally:
        
        # Obtém o tempo atual
        endTime = time.time()

        # Obtém a diferença de tempo entre o momento inicial e final da execução do fluxo
        differenceTime = endTime - startTime

        # Obtém a quantidade de horas da execução
        hours = int(differenceTime // 3600)

        # Obtém a quantidade de minutos da execução
        munites = int((differenceTime % 3600) // 60)

        # Obtém a quantidade de segundos da execução
        seconds = int(differenceTime % 60)

        # Imprime o tempo da execução para depuração
        print (f"{status} ({hours:02d}:{munites:02d}:{seconds:02d}) - {desc}")

        # Substitui aspas simples por aspas duplas para não confundir o banco
        desc = desc.replace("'", '"')

        # Se a flag de erro estiver ativa, pare a execução imediatamente
        if erro:

            # Para a execução
            raise Exception("Execução interrompida")
    
    return

def loadEnv(path: str) -> None:
    # Carrega as informações do arquivo .env do banco de dados
    if os.path.exists(path):
        load_dotenv(path)
    else:
        raise FileNotFoundError(f'O arquivo .env não foi encontrado em {path}')
    
    return

def download_wait(directory: str, timeout: int):
    """
    Espera o download terminar com tempo limite

    Args
    ----
    directory : str
        O caminho da pasta de download
    timeout : int
        Tempo limite

    """
    seconds = 0
    directory = directory.replace('"', "")
    previous_dir_len: int = len(os.listdir(directory))
    while seconds < timeout:
        time.sleep(1)
        current_dir_len: int = len(os.listdir(directory))
        if previous_dir_len != current_dir_len:
            return

        seconds += 1
    raise Exception(f"O download estourou o tempo limite de {timeout} segundos.")