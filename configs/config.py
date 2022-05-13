import os
import ast
from configparser import ConfigParser


class ConfigBase:
    def __init__(self):
        self.config = ConfigParser()
        property_name = "config.properties"
        path = (os.path.dirname(os.path.abspath(__file__)))
        self.property_file_path = os.path.join((path + "/"), property_name)
        self.config.read(self.property_file_path)

    def get(self, section, key):
        """
        Function to get the values from the config file
        :param section: section of the key value pair
        :param key: key  to get the desired value
        :return: value of the given key and section
        """
        try:
            return ast.literal_eval(dict(self.config.items(section))[key])
        except FileNotFoundError as error:
            raise error

