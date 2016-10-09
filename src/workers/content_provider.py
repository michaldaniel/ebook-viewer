#!/usr/bin/env python3

# Easy eBook Viewer by Michal Daniel

# Easy eBook Viewer is free software; you can redistribute it and/or modify it under the terms
# of the GNU General Public Licence as published by the Free Software Foundation.

# Easy eBook Viewer is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public Licence for more details.

# You should have received a copy of the GNU General Public Licence along with
# Easy eBook Viewer; if not, write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA.


import functools
import hashlib
import os
import shutil
import urllib
import zipfile

from workers.xml2obj import *

# What happens here is:
# 1. Read META-INF/container.xml that every ePub should have
# 2. From META-INF/container.xml get path to OPF file
# 3. From OPF file read every application/xhtml+xml file path and save them temporarily in self.chapter_links
# 4. From OPF file read book metadata
# 5. From OPF file read NCX file location
# 6. From NCX file read chapter list and chapter ordering
# 7. Save chapter list in self.titles with titles and path to files
# 8. Sort chapter titles and chapter links according to read ordering
# 9. Compare list from NCX with OPF list and append not chaptered files
# Every file path is created like this: path to tmp folder + path to OPF file location + path to file read from OPF/NCX
# Bonus: do bunch of other stuff like setting data based on uri, telling when book loaded etc.


class ContentProvider:
    def __init__(self, window):

        """
        Manages book files and provides metadata
        :param window: Main application window reference, serves as communication hub
        """
        self.__window = window
        # Checks if cache folder exists
        self.__cache_path = self.__window.config_provider.config["Application"]["cacheDir"]
        if not os.path.exists(self.__cache_path):
            os.mkdir(self.__cache_path)  # If not create it
        self.__ready = False
        self.book_name = ""
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
            self.__ready = False
            return False

        # Sets permissions
        os.system("chmod 700 " + self.__cache_path)

        # Finds opf file
        if os.path.exists(os.path.join(self.__cache_path, "META-INF/container.xml")):

            # Gets metadata
            metadata = self.__get_metadata

            # Calculates MD5 of book (for use in bookmarks)
            md5 = self.__calculate_book_md5(file_path)

            # Sets metadata
            self.book_name = str(bytes.decode(str(metadata.metadata.dc_title).encode("utf-8")))
            raw_author = str(bytes.decode(str(metadata.metadata.dc_creator).encode("utf-8")))
            processed_author = ""
            first = True
            # Some magic to get nice list of authors names
            # TODO: Proper metadata and OPF data parsing, no dirty find_between tricks
            while "data:" in raw_author:
                if not first:
                    processed_author += ", "
                first = False
                processed_author += self.find_between(raw_author, "data:'", "'")
                raw_author = raw_author[raw_author.index("data:") + len("data:"):]
            if processed_author == "":
                self.book_author = str(bytes.decode(str(metadata.metadata.dc_creator).encode("utf-8")))
            else:
                self.book_author = processed_author
            self.book_md5 = md5.hexdigest()

            # Adds book to config (for use in bookmarks)
            if self.book_md5 not in self.__window.config_provider.config:
                self.__window.config_provider.add_book_to_config(self.book_md5)

            # Get oebps
            self.__oebps = self.__get_oebps

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
        container_data = xml2obj(open(os.path.join(self.__cache_path, "META-INF/container.xml"), "r"))
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
        return xml2obj(open(os.path.join(self.__cache_path, opf_file_path), "r"))

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
                return os.path.join(self.__cache_path, self.__get_oebps, x.href)

    def __calculate_book_md5(self, file_path):
        """
        Calculates and returns unique MD5 hash based on book content to be used in config
        :param file_path:
        :return MD5 hash of book content:
        """
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                piece = f.read(28 * md5.block_size)
                if not piece:
                    break
                md5.update(piece)
        f.close()
        return md5

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
            # TODO: This could use complete rewrite based on xml2obj, it sort of works but God help it's bad
            pat = re.compile('-(.*)-')
            for line in open(ncx_file_path):
                line = line.strip()
                # Find text elements witch chapter titles
                if "<text>" in line:
                    out = self.find_between(line, '<text>', '</text>')
                    self.titles.append(out)
                # Find content elements witch chapter links
                if "<content" in line:
                    out = self.find_between(line, '<content src="', '"')
                    self.chapter_links.append(out.split("#")[0])
                # Find ordering elements of chapters
                if "playOrder=" in line:
                    out = self.find_between(line, 'playOrder="', '"')
                    chapter_order.append(int(out))
            chapter_order = functools.reduce(lambda l, x: l.append(x) or l if x not in l else l, chapter_order, [])
            self.chapter_links = functools.reduce(lambda l, x: l.append(x) or l if x not in l else l,
                                                  self.chapter_links, [])

            # Remove unlinked chapter names, if there are more chapters then files it means
            # chapters use filepath.html#chapter1 type of navigation
            # TODO: Think of something better
            while not len(self.titles) <= len(self.chapter_links):
                self.titles.remove(self.titles[0])

            # Sort chapter links according to order
            if len(self.chapter_links) == len(chapter_order):
                sorted_chapters = list(chapter_order)
                sorted_chapters, self.chapter_links = (list(t) for t in
                                                       zip(*sorted(zip(sorted_chapters, self.chapter_links))))

            # Sort chapter names according to order
            if len(chapter_order) == len(self.titles):
                sorted_chapters = list(chapter_order)
                sorted_chapters, self.titles = (list(t) for t in zip(*sorted(zip(sorted_chapters, self.titles))))

            for i in range(len(self.titles)):
                self.titles[i] = [self.titles[i], self.chapter_links[i]]

            # If not all all files are chaptered append them
            # chater_number = 1;
            if len(__files) > len(self.chapter_links):
                for i in range(len(__files)):
                    if __files[i] not in self.chapter_links:
                        self.chapter_links.insert(i, __files[i])
                        # self.titles.insert(i, "Unnamed chapter" + " (" + str(chater_number) + ")")
                        # chater_number += 1;

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
        # TODO: This is the most terrible way to validate anything. Needs real re-write
        # Why is it checking only one path, why does it asume any of files links from manifest are correct?
        if not os.path.exists(os.path.join(self.__cache_path, self.__oebps, self.chapter_links[0])):
            # Reloads files
            self.chapter_links = []
            for x in metadata.manifest.item:
                if x.media_type == "application/xhtml+xml":
                    self.chapter_links.append(x.href)
            self.titles = []
            i = 1
            while not len(self.titles) == len(self.chapter_links):
                self.titles.append(_("Chapter %s") % (str(i)))
                i += 1

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

    def get_chapter_file(self, number):
        """
        Returns a chapter file to feed into viewer
        :param number:
        :return chapter file:
        """
        return os.path.join(self.__cache_path, self.__oebps, self.chapter_links[number].split("#")[0])

    def set_data_from_uri(self, uri):
        """
        Based on chapter uri finds current chapter number and tells UI elements to update
        :param uri:
        """
        for i in range(0, self.chapter_count + 1):
            if urllib.parse.unquote((os.path.split(uri)[-1]).split("#")[0]) == os.path.split(self.chapter_links[i])[-1]:
                self.current_chapter = i
                self.__window.header_bar_component.set_current_chapter(i + 1)
                self.__window.chapters_list_component.set_current_chapter(i + 1)
                break

    def find_between(self, s, first, last):
        """
        Help methods for parsing NCX files, finds first sub-string between two strings
        :param s: String to search in
        :param first: First sub-string
        :param last: Second sub-string
        :return: Sub-string from given string between first and second sub-string
        """
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""
