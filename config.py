import json
import re
import os
import yaml
from configparser import ConfigParser, MissingSectionHeaderError, ParsingError

from yaml.loader import SafeLoader


class ImproperlyConfigured(Exception):
    pass


CONFIG_FILE =  r"config/server.yml"

class ConfigReader:
    
    token_pattern =  "_start_([A-Z]+_?[A-Z]+)+_end_"

    def __init__(self, config_file=None):
        self._config = self.loadFile(config_file or CONFIG_FILE)
        self._configure(self._config)
        for entry in self._config:
            setattr(self,entry,self._config[entry])

    def loadFile(self, file):
        self.parser = ConfigParserSelector().get_parser(file)
        with open(file) as config_file:
            try:
                if isinstance(self.parser,ConfigParser):
                   self.parser.read_file(config_file)
                   _config = self.parser._sections
                else:
                    _config = self.parser.load(config_file,Loader=SafeLoader)
            except (yaml.YAMLError, MissingSectionHeaderError, ParsingError, json.decoder.JSONDecodeError) as e:
                raise ImproperlyConfigured(str(e))
        return _config
    
    def is_token(self, token):
        return re.match(self.token_pattern,token) or False
    
    def _configure(self, config):
        """
        recursively traverse the config file and substitutes
        value from env variable if any token is found
        """
        for key, value in config.items():
            if isinstance(value,dict):
                self._configure(value)
            else:
                if isinstance(value,str) and self.is_token(value):
                    if not os.environ.get(value[7:-5]):
                        raise ImproperlyConfigured("Couldn't find {} in environment " 
                              "variables to substitute in token {}".format(value[7:-5],value))
                    config[key] = os.environ.get(value[7:-5]) #to truncate _start_ and _end_ from the token

    def __getitem__(self,key):
        #getattr is slower than self.__dict__[key] but it's acceptable
        #and required to throw RuntimeError
        __ = getattr(self,key,None)
        if __:
            return __
        raise RuntimeError("{} is not configured".format(key))
    
    @property
    def config(self):
        return self._config


class ConfigParserSelector:

    pattern = '\.[^.\\/:*?"<>|\r\n]+$'

    def extract_file_type(self,filename):
        _type = re.search(self.pattern,filename)
        return _type.group(0) if _type else _type #returns None 

    def select_parser(self,file_type):
        #selects parser based on the file type
        if file_type == ".ini" or file_type == ".cfg" :
            return ConfigParser()
        elif file_type == ".yaml" or file_type == ".yml":
           return yaml
        elif file_type == ".json":
           return json
        else:
            raise ImproperlyConfigured("Couldn't load configuration file of type {}".format(file_type))

    def get_parser(self,filename):
        file_type = self.extract_file_type(filename)
        return self.select_parser(file_type)
        


config = ConfigReader(CONFIG_FILE)





                    


