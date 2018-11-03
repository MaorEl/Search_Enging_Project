import os
import pathlib
import json
import re

class ReadJson:
    def __init__(self, path):
        self.rootDir = path

    def create_maagar_meida (self):
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
                    #f.write('%s\n' % list_of_files)
                    for mini_list in list_of_files:
                        f.write('%s\n' %mini_list)
                #allDocs.close()
        pass

    def create_list_of_information_by_regular_expression_tag_name(self, path, filename, regular_expression):
        result = []
        file = open(path, 'r')
        lines_of_doc = file.readlines()

        for i in range(len(lines_of_doc)):
            line = lines_of_doc.__getitem__(i)
            tmp_list = (re.findall(regular_expression, line))
            if len(tmp_list) != 0:  # if your find DOCNO tag
                doc = {}
                doc['filename'] = filename
                doc['docname'] = tmp_list[0]
                doc['rownumber'] = i + 1
                doc_json = json.dumps(doc)
                result.append(doc_json)
        file.close()
        return result





