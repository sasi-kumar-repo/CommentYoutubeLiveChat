import undetected_chromedriver.v2 as uc
from selenium.webdriver.support.wait import WebDriverWait


class SeleniumBase:
    def __init__(self):
        self.driver = uc.Chrome()
        self.wait = WebDriverWait(self.driver, 30)

    def get_web_driver_options(self):
        return uc.ChromeOptions()

    def set_ignore_certificate_error(self, options):
        options.add_argument('--ignore-certificate-errors')

    def set_disable_notication_and_sandbox(self, options):
        options.add_argument('--disable-notification')
        options.add_argument('--no-sandbox')

    def set_browser_as_incognito(self, options):
        options.add_argument('--incognito')

    def set_automation_as_head_less(self, options):
        options.add_argument('--headless')
