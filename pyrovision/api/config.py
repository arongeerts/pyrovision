import yaml
import os


class Config:
    def __init__(self, config_file=None):
        if not config_file:
            config_file = os.environ.get("PYROVISION_CONFIG_FILE", "config.yaml")
        try:
            with open(config_file) as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            self.config = {}
        print(self.config, type(self.config))

    def __setitem__(self, key, value):
        return self.__set_item(self.config, key, value)

    def __getitem__(self, key):
        return self.__get_item(self.config, key)

    def get(self, key, default=None):
        try:
            return self.__get_item(self.config, key)
        except KeyError:
            return default

    @staticmethod
    def __set_item(d, keys, item):
        if "." in keys:
            key, rest = keys.split(".", 1)
            if key not in d:
                d[key] = {}
            Config.__set_item(d[key], rest, item)
        else:
            d[keys] = item

    @staticmethod
    def __get_item(d, keys):
        if "." in keys:
            key, rest = keys.split(".", 1)
            return Config.__get_item(d[key], rest)
        else:
            return d[keys]


config = Config()
