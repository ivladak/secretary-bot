from configparser import SafeConfigParser
import os.path

SECTION = "bot"

prefixes = [os.path.expanduser(p) for p in ["./", "~/"]]
config_filenames = [p + "bot-secretary.config" for p in prefixes]
config_parser = None


def add_file(file):
    global config_filenames
    config_filenames = [file] + config_filenames


def setup_parser():
    global config_parser
    config_parser = SafeConfigParser()
    config_parser.read(config_filenames)


def get(option):
    if not config_parser:
        setup_parser()
    return config_parser.get(SECTION, option)