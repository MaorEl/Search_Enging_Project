import os
import pathlib
import re
class ReadFile:

    def __init__(self, path):
        self.rootDir = path

    def create_maagar_meida(self):
        path_of_allDocs_file = self.rootDir + "\\allDocs"
        if os.path.exists(path_of_allDocs_file):
            os.remove(path_of_allDocs_file)
        #allDocs = open (name_of_allDocs_file, "a"); #creates new file for all the docs
        code = '<DOCNO> (.*?) </DOCNO>'
        for root, dirs, files in os.walk(self.rootDir):
            for name in files:
                #if name != "allDocs":
                list_of_files = self.create_list_of_information_by_regular_expression_tag_name(pathlib.PurePath(root, name), name, code)
                with open(path_of_allDocs_file, 'a') as f:
                    for mini_list in list_of_files:
                        f.write('%s\n' %mini_list)
                #allDocs.close()
        pass

    @staticmethod
    def create_list_of_information_by_regular_expression_tag_name(path, filename, regular_expression):
        result = []
        file = open(path, 'r')
        lines_of_doc = file.readlines()

        for i in range(len(lines_of_doc)):
            line = lines_of_doc.__getitem__(i)
            tmp_list = (re.findall(regular_expression, line))
            if len(tmp_list) != 0:  # if your find DOCNO tag
                tmp_list.insert(0, filename)
                tmp_list.append(i + 1)
                result.append(tmp_list)
        file.close()
        return result





