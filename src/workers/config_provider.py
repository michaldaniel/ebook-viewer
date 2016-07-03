#!/usr/bin/env python3

import os
import configparser
import getpass


class ConfigProvider:  # Manages book files and provides metadata
        def __init__(self):
            self.config = configparser.ConfigParser()
            # Loads configuration from ~/.ebook-viewer.conf
            self.__config_path = os.path.expanduser(os.path.join("~",".ebook-viewer.conf"))
            if os.access(self.__config_path, os.W_OK):  # Checks if a config file exists
                # Config file exists, loads it.
                self.config.read(self.__config_path)
            else:
                # Config file doesn't exist, creates new
                self.__create_new_configuration()

            #Validates configuration
            self.__validate_configuration()

        def __create_new_configuration(self):
            """
            Creates new Main configuration and saves it to file
            """
            self.config["Application"] = {"cacheDir": "/tmp/ebook-viewer-cache-"+getpass.getuser()+"/",
                                   "javascript": "False",
                                   "caret": "False",
                                   "stylesheet": "Day"}
            self.save_configuration()

        def __validate_configuration(self):
            """
            Validates that all essential keys are present in configuration, if not creates them with default values
            """
            was_valid = True  # If any value is not present indicates need to save configuration to file
            if "Application" not in self.config:
                self.config["Application"]={}
                was_valid = False
            if "cacheDir" not in self.config['Application']:
                self.config["Application"]["cacheDir"] = "/tmp/ebook-viewer-cache-" + getpass.getuser() + "/"
                was_valid = False
            if "javascript" not in self.config['Application']:
                self.config["Application"]["javascript"] = "False"
                was_valid = False
            if "caret" not in self.config['Application']:
                self.config["Application"]["caret"] = "False"
                was_valid = False
            if "stylesheet" not in self.config['Application']:
                self.config["Application"]["stylesheet"] = "Day"
                was_valid = False
            if not was_valid:  # Something changed?
                self.save_configuration()

        def save_configuration(self):
            """
            Saves configuration to file ~/.ebook-viewer.conf
            """
            with open(self.__config_path, "w") as configfile:
                    self.config.write(configfile)

        def add_book_to_config(self, book_md5):
            """
            Helper method to easily create default book configuration
            :param book_md5:
            """
            self.config[book_md5] = {}
            self.config[book_md5]["bookmarks"] = "0"
            self.config[book_md5]["chapter"] = "0"
            self.config[book_md5]["position"] = "0.0"
            self.save_configuration()

        def save_chapter_position(self, book_md5, chapter, pos):
            """
            Helper method to easily save book chapter position and scroll offset
            :param book_md5:
            :param chapter:
            :param pos:
            """
            self.config[book_md5]["chapter"] = str(chapter)
            self.config[book_md5]["position"] = str(pos)
            self.save_configuration()
