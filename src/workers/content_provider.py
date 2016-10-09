#!/usr/bin/env python3

import hashlib
import zipfile
import os
import shutil
from workers.xml2obj import *
import urllib
import functools

class ContentProvider:  # Manages book files and provides metadata
    def __init__(self, window):

        self.__window = window
        # Checks if cache folder exists
        self.__cache_path = self.__window.config_provider.config["Application"]["cacheDir"]
        if not os.path.exists(self.__cache_path):
            os.mkdir(self.__cache_path)  # If not create it
        self.__ready = False
        self.current_chapter = 0
        self.titles = []

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
            raw_athor = str(bytes.decode(str(metadata.metadata.dc_creator).encode("utf-8")))
            processed_author = ""
            first = True
            while "data:" in raw_athor:
                if not first:
                    processed_author += ", "
                first = False
                processed_author += self.find_between(raw_athor, "data:'", "'")
                raw_athor = raw_athor[raw_athor.index("data:") + len("data:"):]
            if processed_author == "":
                self.book_author = str(bytes.decode(str(metadata.metadata.dc_creator).encode("utf-8")))
            else:
                self.book_author = processed_author
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
                return self.__cache_path + self.__get_oebps + "/" + x.href

    def __load_titles_and_files(self):
        """
        Loads titles and chapter file paths
        """
        ncx_file_path = self.__get_ncx_file_path
        metadata = self.__get_metadata
        __files = []
        self.chapter_links = []
        chapter_order = []
        for x in metadata.manifest.item:
            if x.media_type == "application/xhtml+xml":
                __files.append(x.href)

        self.titles = []
        if os.access(ncx_file_path, os.R_OK):  # Checks if NCX is accessible
            # Parse NCX file
            pat=re.compile('-(.*)-')
            for line in open(ncx_file_path):
                line = line.strip()
                # Find text elements witch chapter titles
                if "<text>" in line:
                    out = self.find_between(line,'<text>','</text>')
                    self.titles.append(out)
                # Find content elements witch chapter links
                if "<content" in line:
                    out = self.find_between(line, '<content src="', '"')
                    self.chapter_links.append(out.split("#")[0])
                # Find ordering elements of chapters
                if "playOrder=" in line:
                    out = self.find_between(line,'playOrder="','"')
                    chapter_order.append(int(out))
            chapter_order = functools.reduce(lambda l, x: l.append(x) or l if x not in l else l, chapter_order, [])
            self.chapter_links = functools.reduce(lambda l, x: l.append(x) or l if x not in l else l, self.chapter_links, [])

            # Remove unlinked chapter names
            while not len(self.titles) <= len(self.chapter_links):
                self.titles.remove(self.titles[0])

            # Append unstated chapter names
            #base_chapter_name = "Chapter "
            #if len(self.titles) > 0:
            #    base_chapter_name = "Unnamed chapter  "
            #i = 1
            #while not len(self.titles) >= len(self.chapter_links):
            #    self.titles.append(base_chapter_name + str(i))
            #    i += 1


            # Sort chapter links according to order
            if len(self.chapter_links) == len(chapter_order):
                sorted_chapters = list(chapter_order)
                sorted_chapters, self.chapter_links = (list(t) for t in zip(*sorted(zip(sorted_chapters, self.chapter_links))))

            # Sort chapter names according to order
            if len(chapter_order) == len(self.titles):
                sorted_chapters = list(chapter_order)
                sorted_chapters, self.titles = (list(t) for t in zip(*sorted(zip(sorted_chapters, self.titles))))

            for i in range(len(self.titles)):
                self.titles[i] = [self.titles[i], self.chapter_links[i]]


            # If not all all files are chaptered append them
            #chater_number = 1;
            if len(__files) > len(self.chapter_links):
                for i in range(len(__files)):
                    if __files[i] not in self.chapter_links:
                        self.chapter_links.insert(i, __files[i])
                        #self.titles.insert(i, "Unnamed chapter" + " (" + str(chater_number) + ")")
                        #chater_number += 1;

            # Print some debug
            print("Files: " + str(__files))
            print("Chapters: " + str(self.chapter_links))
            print("Names: " + str(self.titles))
            print("Chapter count: " + str(self.chapter_count))

    def __validate_files(self, metadata):
        """
        Validates files and reloads them if necessary
        :param metadata:
        """
        if not os.path.exists(self.__cache_path + self.__oebps + "/" + self.chapter_links[0]):
            # Reloads files
            self.chapter_links = []
            for x in metadata.manifest.item:
                if x.media_type == "application/xhtml+xml":
                    self.chapter_links.append(x.href)
            self.titles = []
            i = 1
            while not len(self.titles) == len(self.chapter_links):
                self.titles.append("Chapter " + str(i))
                i += 1

    def get_chapter_file(self, number):
        """
        Returns a chapter file to feed into viewer
        :param number:
        :return chapter file:
        """
        return self.__cache_path + self.__oebps + "/" + self.chapter_links[number].split("#")[0]

    @property
    def chapter_count(self):
        """
        Returns number of chapters
        :return chapter number:
        """
        return len(self.chapter_links) - 1

    @property
    def status(self):
        """
        Returns boolean status of book loading
        :return book status:
        """
        return self.__ready

    def set_data_from_uri(self, uri):
        for i in range(0, self.chapter_count+1):
            if urllib.parse.unquote((os.path.split(uri)[-1]).split("#")[0]) == os.path.split(self.chapter_links[i])[-1]:
                self.current_chapter = i
                self.__window.header_bar_component.set_current_chapter(i+1)
                self.__window.chapters_list_component.set_current_chapter(i+1)
                break

    def find_between(self, s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""
