from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as BraveService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.microsoft import IEDriverManager
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.opera import OperaDriverManager


class SetupTools:
    def __init__(self) -> None:
        pass

    def install_selenium_tool(self, driver: str) -> webdriver:
        """
        Installs and configures a Selenium WebDriver for a specified web browser.

        Parameters:
        - driver (str): The name of the web browser driver to install.

        Returns:
        - test_driver (webdriver): An instance of the configured Selenium WebDriver.

        Supported Drivers:
        - 'Chrome': Installs the Chrome WebDriver using ChromeDriverManager.
        - 'ChromeService': Installs the Chrome WebDriver as a service using ChromeDriverManager.
        - 'Brave': Installs the Brave browser's WebDriver using ChromeDriverManager with BraveType.
        - 'BraveService': Installs the Brave browser's WebDriver as a service using ChromeDriverManager with BraveType.
        - 'Firefox': Installs the Firefox WebDriver using GeckoDriverManager.
        - 'FirefoxService': Installs the Firefox WebDriver as a service using GeckoDriverManager.
        - 'IE': Installs the Internet Explorer WebDriver using IEDriverManager.
        - 'IEService': Installs the Internet Explorer WebDriver as a service using IEDriverManager.
        - 'Edge': Installs the Microsoft Edge WebDriver using EdgeChromiumDriverManager.
        - 'EdgeService': Installs the Microsoft Edge WebDriver as a service using EdgeChromiumDriverManager.
        - 'Opera': Installs the Opera WebDriver using OperaDriverManager.

        Usage:
        You can use this method to conveniently install and configure WebDriver for different web browsers
        by specifying the 'driver' parameter. The method returns an instance of the configured WebDriver.

        Example:
        setup_tools = SetupTools()
        chrome_driver = setup_tools.install_selenium_tool('Chrome')
        firefox_driver = setup_tools.install_selenium_tool('Firefox')
        """

        test_driver = None

        if driver == 'Chrome':
            test_driver = webdriver.Chrome(ChromeDriverManager().install())
        elif driver == 'ChromeService':
            test_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif driver == 'Brave':
            test_driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
        elif driver == 'BraveService':
            test_driver = webdriver.Chrome(
                service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
            )
        elif driver == 'Firefox':
            test_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        elif driver == 'FirefoxService':
            test_driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        elif driver == 'IE':
            test_driver = webdriver.Ie(IEDriverManager().install())
        elif driver == 'IEService':
            test_driver = webdriver.Ie(service=IEService(IEDriverManager().install()))
        elif driver == 'Edge':
            test_driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        elif driver == 'EdgeService':
            test_driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        elif driver == 'Opera':
            test_driver = webdriver.Opera(executable_path=OperaDriverManager().install())

        return test_driver
