import os
import sys
import json

# Adiciona o diretório RPA ao diretório de execução
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from lib.browser import Browser
from lib.database import Database
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
            execute_step(self, self.step_0, "Etapa 0 - Conectar com o banco e configurar BOT")

            execute_step(self, self.step_1, "Etapa 1 - Abrir e carregar o SIGOF")

            execute_step(self, self.step_2, "Etapa 2 - Realizar login")

            execute_step(self, self.step_3, "Etapa 3 - Abre todas as telas")

            execute_step(self, self.step_4, "Etapa 4 - Teste")

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

                # Não faça nada
                None

            # Caso haja uma exceção, não faça nada
            except:

                # Não faça nada
                None

            # Avisa que a execução chegou ao fim
            print("Execução terminada")

    def step_0(self) -> None:

        # Determina o diretório principal do bot
        self.execution_dir:str = os.path.dirname(os.path.abspath(__file__))

        # Carrega as informações do arquivo .env do banco de dados
        loadEnv(f'{self.execution_dir}\params\database.env')

        # Obtém um objeto da classe que gerencia a conexão com o banco de dados
        self.conn: Database = Database()

        # Carrega as informações do arquivo .env das configurações
        loadEnv(f'{self.execution_dir}\params\config.env')
        
        # Determina o ID do BOT
        self.bot_id: str = os.getenv('BOT_ID')
        
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

        # Inicializa variável de parâmetros global (para as etapas conseguirem se comunicar caso precisem)
        self.params: json = {}

    def step_1(self) -> None:

        # Abre o site de transparência
        self.webdriver.get('https://techpulseglobal.com.br/SIGOF_HOM/open.do?sys=SFH')

        # Atribui valor à variável xpath para diminuir tamanho da linha do código
        xpath: str = '//iframe'

        # Coloca o webdriver no contexto do iframe do formulário quando estiver carregado
        self.wait.until(EC.frame_to_be_available_and_switch_to_it([By.XPATH, xpath]))

        # Atribui valor à variável xpath para diminuir tamanho da linha do código
        xpath: str = '//input[contains(@class, "form-control")]'

        # Espera o iframe carregar os elementos internos para dar prosseguimento
        self.wait.until(EC.presence_of_all_elements_located([By.XPATH, xpath]))

    def step_2(self) -> None:

        # Atribui valor à variável xpath para diminuir tamanho da linha do código
        xpath: str = '//input[contains(@class, "form-control")]'
        
        # Obtém o campo de login
        login: WebElement = self.webdriver.find_elements(By.XPATH, xpath)[0]

        # Aguarda o login ser clicável
        self.wait.until(EC.element_to_be_clickable(login))

        # Coloca o login
        login.send_keys("123")

        # Obtém o campo de senha
        password: WebElement = self.webdriver.find_elements(By.XPATH, xpath)[1]

        # Aguarda a senha ser clicável
        self.wait.until(EC.element_to_be_clickable(password))

        # Coloca o senha
        password.send_keys("softwell")

        # Atribui valor à variável xpath para diminuir tamanho da linha do código
        xpath: str = '//div[@id="loginbutton"]//button'

        # Obtém o botão de entrar
        enter: WebElement = self.wait.until(EC.presence_of_element_located([By.XPATH, xpath]))

        # Aguarda o botão de entrar ser clicável
        self.wait.until(EC.element_to_be_clickable(enter))

        # Clica no botão
        enter.click()

        # Aguarda o botão não ser mais clicável para saber se o login concluiu
        self.wait.until_not(EC.element_to_be_clickable(enter))

    def step_3(self) -> None:
        # Carrega o iframe principal
        switch_to_main_iframe(self)

        # Atribui valor à variável xpath para diminuir tamanho da linha do código
        xpath: str = '//div[@id="MenuPrincipal"]/*'

        # Obtém o menu principal do sistema
        menu: list[WebElement] = self.wait.until(EC.presence_of_all_elements_located([By.XPATH, xpath]))

        # Determina uma lista negra de opções que devem ser ignoradas do menu
        menu_black_list: list[str] = ["Executar Script SQL", "Grupos de Usuários", "Modo Gerente", "Modo Projeto", "Recarregar Sistema", "LOG", "Sair"]

        # Visita todo o menu de maneira recursiva
        def visit_all_menu(menu: list[WebElement]) -> None:

            # Faz um loop em cada item do menu
            for i in range(0, len(menu), 1):

                # Obtém a opção atual do menu
                option: WebElement = menu[i]

                # Se a opção estiver na lista negra ou for uma div, ignore
                if (option.find_element(By.TAG_NAME, 'span').text in menu_black_list) or (option.tag_name == "div"):
                    continue

                # Clica na opção
                self.wait.until(EC.element_to_be_clickable(option))
                self.wait.until(EC.visibility_of(option))
                option.click()

                # A opção é um submenu?
                if option.get_attribute("data-bs-toggle") == "collapse":

                    # Faz a chamada da função novamente
                    visit_all_menu(menu[i+1].find_elements(By.XPATH, './*'))

                    # Depois de executar toda a função acima, fecha submenu
                    option.click()

                    # Aguarda a animação do menu recolher
                    sleep(0.2)

                # Se não é um submenu, é uma tela
                else:

                    # Espera o iframe de conteúdo carregar
                    switch_to_main_iframe(self)

                    # Aguarda um tempo após o carregamento para dar tempo de popular erros
                    sleep(1)

                    # Atribui valor à variável xpath para diminuir tamanho da linha do código
                    xpath: str = '//button[contains(@title, "Fechar")]'

                    # Obtém botão de fechar a tela
                    close_button: WebElement = self.wait.until(EC.presence_of_element_located([By.XPATH, xpath]))

                    # Aguarda botão ser clicável
                    self.wait.until(EC.element_to_be_clickable)

                    # Clica no botão
                    close_button.click()

        # Visita todo o menu principal de maneira recursiva
        visit_all_menu(menu)

    def step_4(self) -> None:

        open_form(self, "Cadastro de Previsões de Despesas")
        switch_to_form_iframe(self)
        execute_maker_function(self, "entrarNoModoInserir")
        sleep(0.5)
        # Atribui valor à variável xpath para diminuir tamanho da linha do código
        for x in range (0, 50, 1):
            xpath: str = '//div[@id="tab0"]//input'
            campos: list[WebElement] = self.wait.until(EC.presence_of_all_elements_located([By.XPATH, xpath]))
            for i in range(0, len(campos)-1, 1):
                campos[i].send_keys("11/11/2025")
            execute_maker_function(self, 'navSalvarMais')
            click_popup_button(self, 'ok')
        execute_maker_function(self, 'navCancelar')
        for x in range (0, 50, 1):
            execute_maker_function(self, 'navRegistroUltimo')
            execute_maker_function(self, 'navRegistroDeletar')
            click_popup_button(self, 'ok')

# Se tiver sido executado diretamente, crie uma instância da classe
if __name__ == '__main__':
    Core()