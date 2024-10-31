import os
import logging
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class Browser:
    def __init__(self, browser: str) -> None:

        if browser == 'firefox':
            self.loadFirefox()
        else:
            self.loadChrome()

    def loadChrome(self) -> None:

    # Tenta iniciar o webdriver
        try:
            # Caminho para o GeckoDriver
            webdriver_path: str = chromedriver_autoinstaller.install(cwd=False, path=os.getenv('BROWSER_CHROME_WEBDRIVER_PATH', ''))

            # Caminho do diretório de downloads
            download_dir = os.getenv("BROWSER_DOWNLOAD_DIR", "").replace("\\\\", "\\")

            # Inicializa o serviço do GeckoDriver
            chrome_service = ChromeService(webdriver_path)

            # Inicializa as opções do WebDriver
            chrome_options = ChromeOptions()
            chrome_prefs = {
                "download.prompt_for_download": False,
                "safebrowsing.disable_download_protection": True,
                "download.default_directory" : f"{download_dir}"
            }

            chrome_options.add_experimental_option("prefs", chrome_prefs)
            chrome_options.add_experimental_option("detach", True)
            logging.getLogger("selenium").setLevel(logging.FATAL)

            # Pega as opções colocadas no .env
            options_str = os.getenv('BROWSER_OPTIONS', '')
            if options_str:
                options = options_str.split(',')
                for option in options:
                    chrome_options.add_argument(option)

            # Inicializa o WebDriver
            self.webdriver: WebDriver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            self.download_dir = os.getenv('BROWSER_DOWNLOAD_DIR', '')

        # Se houver uma falha na tentativa de abrir o webdriver, retornar o erro           
        except Exception as e:
            raise Exception(f"Erro ao tentar abrir o navegador: {e}")
        
    def loadFirefox(self) -> None:

        # Tenta iniciar o webdriver
        try:

            # Inicializa o serviço do GeckoDriver
            firefox_service = FirefoxService(os.getenv('BROWSER_FIREFOX_WEBDRIVER_PATH', ''))

            # Inicializa as opções do WebDriver
            firefox_options = FirefoxOptions()

            firefox_options.set_preference("browser.download.folderList", 2)
            firefox_options.set_preference("browser.download.dir", os.getenv('BROWSER_DOWNLOAD_DIR', ''))
            firefox_options.set_preference("browser.download.manager.showWhenStarting", False)

            # Pega as opções colocadas no .env
            options_str = os.getenv('BROWSER_OPTIONS', '')
            if options_str:
                options = options_str.split(',')
                for option in options:
                    firefox_options.add_argument(option)

            # Inicializa o WebDriver
            self.webdriver: WebDriver = webdriver.Firefox(service=firefox_service, options=firefox_options)
            self.download_dir = os.getenv('BROWSER_DOWNLOAD_DIR', '')

        # Se houver uma falha na tentativa de abrir o webdriver, retornar o erro           
        except Exception as e:
            raise(f"Erro ao tentar abrir o navegador: {e}")