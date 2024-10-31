import os
import time
from time import sleep
from typing import Literal
from dotenv import load_dotenv
from datetime import datetime
from start import Core
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Executa uma função contabilizando o tempo de sua execução, e por fim inserindo esta execução no log
def execute_step(core: Core, func: callable, desc: str):

    # Obtém o tempo atual
    startTime = time.time()

    # Obtém a data atual
    startDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

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
        horas = int(differenceTime // 3600)

        # Obtém a quantidade de minutos da execução
        minutos = int((differenceTime % 3600) // 60)

        # Obtém a quantidade de segundos da execução
        segundos = int(differenceTime % 60)

        # Imprime o tempo da execução para depuração
        print (f"{status} ({horas:02d}:{minutos:02d}:{segundos:02d}) - {desc}")

        # Substitui aspas simples por aspas duplas para não confundir o banco
        desc = desc.replace("'", '"')

        # Insere na tabela de LOG a execução da etapa e o tempo que ela levou para ser concluída
        if (hasattr(core, 'conn')):
            insert_log(core, [f"'{desc}'", f"'{horas:02d}:{minutos:02d}:{segundos:02d}'", f"'{status}'", f"'{core.bot_id}'", f"'{startDate}'"])

        # Se a flag de erro estiver ativa, pare a execução imediatamente
        if erro:

            # Para a execução
            raise Exception("Execução interrompida")
    
    return

# Faz a execução parar enquanto existirem spinners na tela. Continua se o tempo estourar
def wait_spinners(webdriver: WebDriver, spinner_xpath: str, initial_sleep: float, tolerance_time: int):

    # Espera os spinners desaparecerem com tempo de tolerância
    try:

        # Espera 3 segundos para garantir que os spinners surjam
        sleep(initial_sleep)

        # Obtém os spinners na tela
        spinners: list[WebElement] = webdriver.find_elements(By.XPATH, spinner_xpath)

        # Se houver algum spinner, aguarda todos desaparecerem
        for spinner in spinners: WebDriverWait(webdriver, tolerance_time).until(EC.staleness_of(spinner))

    # Independente do erro, não para o código e informa que um spinner quebrou o tempo limite
    except:

        # Informa que um spinner não sumiu no tempo limite e que a execução continuará
        print("Um spinner na tela estourou o tempo máximo. A execução continuará.")
    
    return

def loadEnv(path: str) -> None:
    # Carrega as informações do arquivo .env do banco de dados
    if os.path.exists(path):
        load_dotenv(path)
    else:
        raise FileNotFoundError(f'O arquivo .env não foi encontrado em {path}')
    
    return

def insert_log(core: Core, values: list):
    # Insere na tabela de LOG
    core.conn.insert_on_Table("SGA_LOG_BOT", ["LGB_ETAPA", "LGB_DURACAO", "LGB_STATUS", "LGB_BOT", "LGB_DATA_EXECUCAO"], values)

    return

def switch_to_main_iframe(core: Core) -> None:

    # Retorna ao contexto raiz do HTML e carrega o iframe principal
    core.webdriver.switch_to.default_content()

    # Atribui valor à variável xpath para diminuir tamanho da linha do código
    xpath: str = '//iframe'

    # Carrega primeiro iframe
    core.wait.until(EC.frame_to_be_available_and_switch_to_it([By.XPATH, xpath]))

    # Carrega iframe principal
    core.wait.until(EC.frame_to_be_available_and_switch_to_it([By.XPATH, xpath]))

    return

def switch_to_form_iframe(core: Core) -> None:

    # Atribui valor à variável xpath para diminuir tamanho da linha do código
    xpath: str = '//div[@id="Aba"]//iframe'

    # Carrega iframe de conteúdo
    core.wait.until(EC.frame_to_be_available_and_switch_to_it([By.XPATH, xpath]))

    # Atribui valor à variável xpath para diminuir tamanho da linha do código
    xpath: str = '//iframe'

    # Carrega iframe de conteúdo
    core.wait.until(EC.frame_to_be_available_and_switch_to_it([By.XPATH, xpath]))

    return

def click_popup_button(core: Core, button: Literal["ok", "nao", "cancelar"]) -> None:

    match button:
        case "ok":
            button = "swal2-confirm swal2-styled"
        case "nao":
            button = "swal2-deny swal2-styled"
        case "cancelar":
            button = "swal2-cancel swal2-styled)"
        case _:
            raise Exception(f'Opção de botão "{button}" inválida.')
        
    # Atribui valor à variável xpath para diminuir tamanho da linha do código
    xpath: str = f'//button[@class="{button}"]'
    try:
        # Obtém o botão
        button: WebElement = core.wait.until(EC.presence_of_element_located([By.XPATH, xpath]))
        core.wait.until(EC.element_to_be_clickable(button))

        # Clica no botão
        sleep(0.05)
        button.click()
    except:
        raise Exception("Houve um erro ao tentar clicar no botão de navegação do formulário")

    return

def open_form(core: Core, name: str) -> None:
    """
    Abre o formulário com base no nome que ele possui no menu. \n
    Essa função utiliza a caixa de pesquisa do menu do maker para buscar a tela
    """

    # Atribui valor à variável xpath para diminuir tamanho da linha do código
    switch_to_main_iframe(core)

    # Atribui valor à variável xpath para diminuir tamanho da linha do código
    xpath: str = '//div[@id="Menu"]//input'

    # Obtém o campo de pesquisa do menu do sistema
    search: WebElement = core.wait.until(EC.presence_of_element_located([By.XPATH, xpath]))

    # Envia o nome da tela para o campo de pesquisa
    search.send_keys(name)

    # Espera um segundo para pesquisar
    sleep(1)

    # Atribui valor à variável xpath para diminuir tamanho da linha do código
    xpath: str = '//ul[contains(@class, "resultSearchLis")]//a'

    # Obtém a opção retornada da pesquisa
    option: WebElement = core.wait.until(EC.element_to_be_clickable([By.XPATH, xpath]))

    # Clica no elemento
    option.click()

    # Atribui valor à variável xpath para diminuir tamanho da linha do código
    xpath: str = '//div[@id = "Menu"]//button'

    # Obtém o botão de fechar pesquisa
    option: WebElement = core.wait.until(EC.element_to_be_clickable([By.XPATH, xpath]))

    # Clica no botão
    option.click()

    return

def execute_maker_function(core: Core, function: str) -> any:
    """
    Executa uma função cliente do maker e obtém o seu retorno (se houver)\n
    Opções:\n
    [-] "estaNoModoInserir" - Retorna 'True' se o formulário está no modo insercao\n
    [-] "entrarNoModoInserir" - Entra no modo inserir\n
    [-] "estaNoModoEdicao" - Retorna 'True' se o formulário está no modo edicao\n
    [-] "entrarNoModoEdicao" - Entra no modo edicao\n
    [-] "estaNoModoNavegacao" - Retorna 'True' se o formulário está no modo navegacao\n
    [-] "navCancelar" - Cancela edição ou inserção\n
    [-] "navRegistroPrimeiro" - Navega ao primeiro registro\n
    [-] "navRegistroAnterior" - Navega ao registro anterior\n
    [-] "navRegistroProximo" - Navega ao próximo registro\n
    [-] "navRegistroUltimo" - Navega ao último registro\n
    [-] "navRegistroDeletar" - Deleta registro atual\n
    [-] "navSalvarMais" - Salva e continua inserindo\n
    [-] "navSalvar" - Salva registro atual\n
    [-] "navRegistroDeletar" - Salva registro atual\n
    """

    match function:
        case "estaNoModoInserir":
            function = "ebfFormIsInInsertMode()"
        case "entrarNoModoInserir":
            function = "ebfFormInsertMode()"
        case "estaNoModoEdicao":
            function = "ebfFormIsInEditMode()"
        case "entrarNoModoEdicao":
            function = "ebfFormEditMode()"
        case "estaNoModoNavegacao":
            function = "ebfFormIsInBrowserMode()"
        case "navCancelar":
            function = "ebfNavEditCancel()"
        case "navRegistroPrimeiro":
            function = "ebfNavFirstRecord()"
        case "navRegistroAnterior":
            function = "ebfNavPreviousRecord()"
        case "navRegistroProximo":
            function = "ebfNavNextRecord()"
        case "navRegistroUltimo":
            function = "ebfNavLastRecord()"
        case "navRegistroDeletar":
            function = "ebfNavDeleteCurrentRecord()"
        case "navSalvarMais":
            function = "ebfNavIncludeMoreSaveRecord()"
        case "navSalvar":
            function = "ebfNavIncludeSaveRecord()"
        case _:
            raise Exception("A função executada não existe")
        
    return core.webdriver.execute_script(f"return {function};")