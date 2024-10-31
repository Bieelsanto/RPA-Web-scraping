import os
import sys

# Adiciona o diretório RPA ao diretório de execução
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from lib.browser import Browser
from repository import *

from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# Classe principal
class Core():

    # Sequência de comandos do RPA
    def __init__(self) -> None:

        # Tenta executar a sequência de comandos do RPA
        try:
            execute_step(self.step_0, "Etapa 0 - Conectar com o banco e configurar BOT")

            execute_step(self.step_1, "Etapa 1 - Abrir e carregar o Relatório de Pagamento")

            execute_step(self.step_2, "Etapa 2 - Preenche campos necessários")

            execute_step(self.step_3, "Etapa 3 - Realiza download")

        # Se houver alguma exceção na sequência de comandos, pare imediatamente
        except Exception as e:

            # Retorna o erro que houve durante a sequência
            raise Exception(e)

        # Independente se houver erro de execução, tenta finalizar o webdriver
        finally:

            # Tenta finalizar o webdriver
            try:

                # Finaliza o webdriver
                self.webdriver.quit()
                None

            # Caso haja uma exceção, não faça nada
            except:

                # Não faça nada
                None

            # Avisa que a execução chegou ao fim
            print("Execução finalizada")

    def step_0(self) -> None:

        # Determina o diretório principal do bot
        self.execution_dir:str = os.path.dirname(os.path.abspath(__file__))

        # Carrega as informações do arquivo .env das configurações
        loadEnv(f'{self.execution_dir}\params\config.env')
        
        # Obtém um objeto da classe que gerencia o browser
        self.browser: Browser = Browser('chrome')

        # Obtém uma referência do webdriver para gerenciar o Firefox
        self.webdriver: WebDriver = self.browser.webdriver

        # Maximiza a tela
        self.webdriver.maximize_window()

        # Obtém um objeto da classe que simula ações de um usuário no browser
        self.actions = ActionChains(self.webdriver)

        # Coloca o tempo de espera para 20 segundos de tolerância em métodos que dependem da API do DOM
        self.wait = WebDriverWait(self.webdriver, 20)

    def step_1(self) -> None:

        # Abre o site de transparência
        self.webdriver.get('https://relatorioaps.saude.gov.br/gerenciaaps/pagamento')

        # Atribui valor à variável css_selector para diminuir tamanho da linha do código
        css_selector: str = 'div#pn_id_3'

        # Coloca o webdriver no contexto do iframe do formulário quando estiver carregado
        self.wait.until(EC.presence_of_element_located([By.CSS_SELECTOR, css_selector]))
        sleep(1)

    def step_2(self) -> None:

        def choose_option(id_campo: str, option: int):

            # Atribui valor à variável css_selector para diminuir tamanho da linha do código
            css_selector: str = f'div#{id_campo}'
            
            # Obtém o campo
            campo: WebElement = self.wait.until(EC.presence_of_element_located([By.CSS_SELECTOR, css_selector]))

            # Aguarda o campo ser clicável
            self.wait.until(EC.element_to_be_clickable(campo))

            # Clica no campo
            sleep(0.5)
            campo.click()
            sleep(0.5)

            # Atribui valor à variável css_selector para diminuir tamanho da linha do código
            css_selector: str = 'ul[role="listbox"] li'
            
            # Obtém a opção
            campo: WebElement = self.wait.until(EC.presence_of_all_elements_located([By.CSS_SELECTOR, css_selector]))[option-1]

            # Aguarda a opção ser clicável
            self.wait.until(EC.element_to_be_clickable(campo))

            # Clica na opção
            campo.click()

        choose_option('pn_id_3', 2)
        choose_option('pn_id_5', 6)
        choose_option('pn_id_7', 1)
        choose_option('pn_id_15', 335)
        choose_option('pn_id_9', 5)
        choose_option('pn_id_11', 1)

    def step_3(self) -> None:
        
        # Atribui valor à variável css_selector para diminuir tamanho da linha do código
        css_selector: str = f'button'
        
        # Obtém o botão de download
        download_button: WebElement = self.webdriver.find_elements(By.CSS_SELECTOR, css_selector)[1]

        # Aguarda o botão de download ser clicável
        self.wait.until(EC.element_to_be_clickable(download_button))

        # Clica no botão
        download_button.click()
        
        # Espera um novo arquivo aparecer no diretório de downloads
        download_wait(self.browser.download_dir, 60)

# Se tiver sido executado diretamente, crie uma instância da classe
if __name__ == '__main__':
    Core()