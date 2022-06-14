__author__ = "Sasi Kumar"

import re
import time
import pytchat
from random import randint
from libs.youtube_base import YoutubeBase


class YoutubeAPI(YoutubeBase):
    def __init__(self, incognito=False, headless=False):
        super().__init__(incognito=incognito, headless=headless)
        self.user = self.config.get("login", "username")
        self.author = self.config.get("author", "name")
        self.passcode = self.config.get("login", "password")
        self.word_list = self.config.get("wordlist", "comments")
        self.locators()

    def comment_on_a_live_chat(self):
        """
        Flow Function to comment on a live chat
        :return: None
        """
        self.login_workaround_for_google(self.user, self.passcode)
        self.go_to_youtube(self.base_url)
        self.search_for_channel(self.channel_name)
        live_video_url = self.get_live_video_if_streamed()
        self.like_given_video_url(live_video_url) if live_video_url else Exception("There is no Live stream currently.."
                                                                                   ". Please try again later")
        self.switch_to_live_chat_frame(self.live_chat_frame)
        self.make_random_chats(infinite=True)
        # Comment the above line to run the below line
        # self.comment_after_someone_reply(live_video_url)

    def make_random_chats(self, infinite=False):
        """
        Function to make infinite loop call to insert messages to the live chat after specific interval
        :return: None
        """
        print("Commenting on Live Chat.....")
        if infinite:
            while True:
                number = randint(0, len(self.word_list) - 1)
                self.input_text_on_the_live_chat(self.word_list[number])
                time.sleep(100)
        else:
            number = randint(0, len(self.word_list) - 1)
            self.input_text_on_the_live_chat(self.word_list[number])
            print("Successfully sent message to a live chat")

    def comment_after_someone_reply(self, url):
        """
        Function to sent continuous reply after someone's comment. Sometimes this looks like spam
        :param url: Youtube live video url
        :return: None
        """
        video_id = (re.split(r'=', url))[1]
        if len(video_id) == 11:
            chat = pytchat.create(video_id=video_id)
            while chat.is_alive():
                for c in chat.get().sync_items():
                    if c.author.name != self.author:
                        number = randint(0, len(self.word_list) - 1)
                        self.input_text_on_the_live_chat(self.word_list[number])
        else:
            raise Exception("Error in getting Video ID from the given url")


if __name__ == "__main__":
    youtube_app = YoutubeAPI()
    youtube_app.comment_on_a_live_chat()
