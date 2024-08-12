import configparser


class ConfigManager:
    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()

    def read_config(self):
        self.config.read(self.filename)

    def save_config(self):
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

    def get_value(self, section, key):
        self.read_config()
        return self.config.get(section, key)

    def set_value(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        self.save_config()
