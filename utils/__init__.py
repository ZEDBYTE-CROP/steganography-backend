import os

#helper lambdas
quote = lambda s: "'" + s + "'"
double_quote = lambda s: '"' + s + '"'

class ErrorFormatter:
    def __init__(self,data):
        self.parse(data)
    
    def parse(self,errors):
        self.formatted_errors = []
        for error in errors:
            error = {"message": error['msg'] + ": " + double_quote(error['loc'][0]), "type": "validation error"}
            self.formatted_errors.append(error)

def tryParseFloat(value):
    try:
        return float(value)
    except:
        return str(value)

def tryParseInt(value):
    try:
        return int(value)
    except:
        return str(value)

            
def split_all_paths(path):
    #paths should start with '\'
    paths = []
    while path != "\\":
      path = os.path.normpath(path + os.sep + os.pardir)
      paths.append(path)
    return paths
            