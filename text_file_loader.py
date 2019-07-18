"""
Loads different formats of files which can contain text
and provides functions for obtaining the raw text strings

Current supported formats:
*.pdf -> load_pdf_text
*.txt -> load_txt_text

"""


from conditional_print import ConditionalPrint
from configuration_handler import ConfigurationHandler
from tika import parser  # care contacts a web service, used for pdf parsing atm

# import PyPDF2
import shutil
import os


class TextFileLoader(object):

    def __init__(self):
        config_handler = ConfigurationHandler(first_init=False)

        self.config = config_handler.get_config()
        self.cpr = ConditionalPrint(self.config.PRINT_TXT_FILE_LOADER, self.config.PRINT_EXCEPTION_LEVEL,
                                    self.config.PRINT_WARNING_LEVEL, leading_tag=self.__class__.__name__)

        self.cpr.print("init text_file_loader")

    def delete_directory_tree(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)

    def create_directory_tree(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def load_pdf_text(self, file_path):
        """
        Loads a *.pdf file returns the text for it
        :param file_path: path of the pdf file to load
        :return:
        """

        # this contacts a web server and obtains *.pdf methods
        raw = parser.from_file(file_path)
        return raw['content'], raw['metadata']

        """ didn't work well still worth a try in some time 
        pdfFileObj = open(file_path, 'rb')  # 'rb' for read binary mode
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        pageObj = pdfReader.getPage(4)  # '9' is the page number
        text = pageObj.extractText()
        pdfFileObj.close()
        return text
        """

    def load_multiple_txt_paths_from_folder(self, folder_path, extension=None):
        """
        Loads all filepaths within a folder
        :param folder_path: path to folder
        :param extension: extension filter, if applied only these file come in list
        :return: list of full file  paths
        """

        from os import listdir
        from os.path import isfile, join
        if extension is not None:
            onlyfiles = [join(folder_path, f) for f in listdir(folder_path) if f.endswith(extension) and isfile(join(folder_path, f))]
        else:
            onlyfiles = [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]

        return onlyfiles


    def load_txt_text(self, file_path, encoding = None):
        """
        loads a *.txt file returns the text of it
        :param file_path: path of the txt file
        :return:
        """

        if encoding is None:
            f = open(file_path, "r")
        else:
            f = open(file_path, "r", encoding=encoding)
        text = f.read()
        f.close()
        return text

    def check_file_format(self, file_path):
        """
        Checks the file format and returns convenient check
        object
        :param file_path: file to check
        :return: object for checking
        """
        class return_object(object):
            is_pdf = False
            is_txt = False

        ro = return_object

        if file_path.endswith(".txt"):
            ro.is_txt = True
        elif file_path.endswith(".pdf"):
            ro.is_pdf = True

        return ro
