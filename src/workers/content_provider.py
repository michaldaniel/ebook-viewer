#!/usr/bin/env python3

import hashlib
import zipfile
import os
import shutil
from workers.xml2obj import *
import urllib

class ContentProvider:  # Manages book files and provides metadata
    def __init__(self, window):

        self.__window = window
        # Checks if cache folder exists
        self.__cache_path = self.__window.config_provider.config["Application"]["cacheDir"]
        if not os.path.exists(self.__cache_path):
            os.mkdir(self.__cache_path)  # If not create it
        self.__ready = False
        self.current_chapter = 0

    def prepare_book(self, file_path):
        """
        Loads book meta data and chapters
        :param file_path:
        :return True when book loaded successfully, False when loading failed:
        """

        # Clears any old files from the cache
        if os.path.exists(self.__cache_path):
            shutil.rmtree(self.__cache_path)

        # Extracts new book
        try:
            zipfile.ZipFile(file_path).extractall(path=self.__cache_path)
        except:
            # Is not zip file
            self.ready = False
            return False

        # Sets permissions
        os.system("chmod 700 " + self.__cache_path)

        # Finds opf file
        if os.path.exists(self.__cache_path+"META-INF/container.xml"):

            # Gets metadata
            metadata = self.__get_metadata

            # Calculates MD5 of book (for use in bookmarks)
            md5 = self.__calculate_book_md5(file_path)

            # Sets metadata
            self.book_name = str(bytes.decode(str(metadata.metadata.dc_title).encode("utf-8")))
            self.book_author = str(bytes.decode(str(metadata.metadata.dc_creator).encode("utf-8")))
            self.book_md5 = md5.hexdigest()

            # Adds book to config (for use in bookmarks)
            if self.book_md5 not in self.__window.config_provider.config:
                self.__window.config_provider.add_book_to_config(self.book_md5)

            # Get oebps
            self.__oebps  = self.__get_oebps

            # Loads titles and file paths
            self.__load_titles_and_files()

            # Validates files
            self.__validate_files(metadata)

            # End of preparations
            self.__ready = True
            return True
        else:  # Else returns False to indicate errors
            self.__ready = False
            return False

    @property
    def __get_opf_file_path(self):
        """
        Finds and returns OPF file path
        :return OPF file path:
        """
        container_data = xml2obj(open(self.__cache_path+"META-INF/container.xml", "r"))
        return container_data.rootfiles.rootfile.full_path

    @property
    def __get_metadata(self):
        """
        Creates and returns metadata object
        :return metadata object:
        """

        # Gets OPF file path
        opf_file_path = self.__get_opf_file_path
        # Loads OPF file and parse it
        return xml2obj(open(self.__cache_path+opf_file_path, "r"))

    def __calculate_book_md5(self, file_path):
        """
        Calculates and returns unique MD5 hash based on book content to be used in config
        :param file_path:
        :return MD5 hash of book content:
        """
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                piece = f.read(28*md5.block_size)
                if not piece:
                    break
                md5.update(piece)
        f.close()
        return md5

    @property
    def __get_oebps(self):
        """
        Finds and returns oebps
        :return oebps:
        """
        return os.path.split(self.__get_opf_file_path)[0]

    @property
    def __get_ncx_file_path(self):
        """
        Finds and returns NCX file path
        :return NCX file path:
        """

        # Gets metadata object
        metadata = self.__get_metadata
        # Finds NCX file
        for x in metadata.manifest.item:
            if x.media_type == "application/x-dtbncx+xml":
                return self.__cache_path + "/" + self.__get_oebps + "/" + x.href

    def __load_titles_and_files(self):
        """
        Loads titles and chapter file paths
        """
        ncx_file_path = self.__get_ncx_file_path
        self.__titles = []
        self.__files = []
        if os.access(ncx_file_path, os.R_OK):  # Checks if NCX is accessible
            # Parse NCX file
            pat=re.compile('-(.*)-')
            for line in open(ncx_file_path):
                line = line.strip()
                if "<text>" in line:
                    out = line.replace("<text>", "")
                    out = out.replace("</text>", "")
                    out = out.replace("<content", "")
                    self.__titles.append(out)
                if "<content" in line:
                    out = line.replace("<content src=\"", "")
                    out = out.replace("\"", "")
                    out = out.replace("/>", "")
                    self.__files.append(out)
            while not len(self.__titles) == len(self.__files):
                self.__titles.remove(self.__titles[0])

    def __validate_files(self, metadata):
        """
        Validates files and reloads them if necessary
        :param metadata:
        """
        if not os.path.exists(self.__cache_path + "/" + self.__oebps + "/" + self.__files[0]):
            # Reloads files
            self.__files = []
            for x in metadata.manifest.item:
                if x.media_type == "application/xhtml+xml":
                    self.__files.append(x.href)
            self.__titles = []
            i = 1
            while not len(self.__titles) == len(self.__files):
                self.__titles.append("Chapter "+str(i))
                i += 1

    def get_chapter_file(self, number):
        """
        Returns a chapter file to feed into viewer
        :param number:
        :return chapter file:
        """
        return self.__cache_path + "/" + self.__oebps + "/" + self.__files[number]

    @property
    def chapter_count(self):
        """
        Returns number of chapters
        :return chapter number:
        """
        return len(self.__files) - 1

    @property
    def status(self):
        """
        Returns boolean status of book loading
        :return book status:
        """
        return self.__ready

    def set_data_from_uri(self, uri):
        print(uri)
        for i in range(0, self.chapter_count):

            if urllib.parse.unquote((os.path.split(uri)[-1]).split("#")[0]) == os.path.split(self.__files[i])[-1]:
                self.current_chapter = i
