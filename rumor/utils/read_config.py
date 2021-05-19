import configparser


def get_config(path='rumor-config.ini', encoding="utf-8"):
    config = configparser.ConfigParser()
    config.read(path, encoding=encoding)
    return config
