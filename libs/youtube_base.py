__author__ = "Sasi Kumar"

import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from libs.selenium_base import SeleniumBase
from configs.config import ConfigBase


class YoutubeBase:
    def __init__(self, incognito, headless):
        self.config = ConfigBase()
        self.base_url = self.config.get("urls", "base_url")
        self.google_url = self.config.get("urls", "google_login")
        self.channel_name = self.config.get("channels", "channel_name")
        self.sel = SeleniumBase()
        options = self.sel.get_web_driver_options()
        if headless:
            self.sel.set_automation_as_head_less(options)
        if incognito:
            self.sel.set_browser_as_incognito(options)
        self.sel.set_ignore_certificate_error(options)
        self.sel.set_disable_notication_and_sandbox(options)
        self.driver = self.sel.driver

    def locators(self):
        """
        Function to load locators used in youtube base class
        :return: None
        """
        self.live_chat_frame = "chatframe"
        self.email_field = [By.XPATH, "//input[@type='email']"]
        self.next_btn = [By.XPATH, "//span[contains(text(), 'Next')]"]
        self.password_field = [By.XPATH, "//input[@type='password']"]
        self.search_box = [By.XPATH, "//input[@id='search']"]
        self.search_button = [By.XPATH, "//button[@id='search-icon-legacy']"]
        self.live_now = [By.XPATH, "//a[contains(text(), '{0}')]/../../../../../..//"
                                   "span[contains(text(), 'LIVE')]".format(self.channel_name)]
        self.youtube_like_button = [By.XPATH, "(//div[@id='top-level-buttons-computed']//button[@id='button'])[1]"]
        self.chat_input_field = [By.XPATH, "//div[@id='input']"]

    def go_to_youtube(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.refresh()
        time.sleep(10)

    def search_for_channel(self, text):
        """
        Function to search for a channel using channel name
        :param text: Channel name as a string
        :return: None
        """
        search_field = self.driver.find_element(self.search_box[0], self.search_box[1])
        search_field.click()
        search_field.send_keys(text)
        time.sleep(2)
        self.driver.find_element(self.search_button[0], self.search_button[1]).click()
        time.sleep(10)

    def login_workaround_for_google(self, email, password):
        """
        Function to login to youtube or else you can use direct youtube login
        :param email: Google email ID
        :param password: Google email password
        :return: None
        """
        self.driver.delete_all_cookies()
        self.driver.get(self.google_url)
        time.sleep(5)
        self.driver.find_element(self.email_field[0], self.email_field[1]).send_keys(email)
        self.driver.find_element(self.next_btn[0], self.next_btn[1]).click()
        time.sleep(5)
        self.driver.find_element(self.password_field[0], self.password_field[1]).send_keys(password)
        self.driver.find_element(self.next_btn[0], self.next_btn[1]).click()
        time.sleep(8)
        session = self.driver.session_id
        print("Successfully logged in...") if session else Exception("Unable to login")

    def like_given_video_url(self, url):
        """
        Function to like the youtube video. Use only after login!!
        :param url: Youtube video url
        :return: None
        """
        self.driver.get(url)
        time.sleep(3)
        self.driver.find_element(self.youtube_like_button[0], self.youtube_like_button[1]).click()

    def get_live_video_if_streamed(self):
        """
        Function to get the live video url
        :return: live video url as string if live else empty string
        """
        live_now_element = self.driver.find_element(self.live_now[0], self.live_now[1])
        if live_now_element:
            live_now_element.click()
            current_url = self.driver.current_url
            return current_url
        return ""

    def switch_to_live_chat_frame(self, frame):
        self.driver.switch_to.frame(frame)

    def input_text_on_the_live_chat(self, text):
        """
        Function to post messages on the live chat
        :param text: text to be commented on the live chat
        :return: None
        """
        live_chat_input_field = self.driver.find_element(self.chat_input_field[0], self.chat_input_field[1])
        live_chat_input_field.send_keys(text)
        live_chat_input_field.send_keys(Keys.ENTER)

