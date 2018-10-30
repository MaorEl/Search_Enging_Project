class ReadFile:

    def __init__(self, path):
        self.path = path

#Todo: to decide wheter to start with sepreate into different files or to work with those.
    def findBeginningOfDoc(self):
        return True


rf = ReadFile("maor")
print(rf.path)

