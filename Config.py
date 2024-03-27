import configparser

class Config:
    def __init__(self, filename) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def get_configurations(self):
        return self.config


# cnf = Config("db_config.env")
# params = cnf.get_configurations()

# print(params.get("DB", "host"))
# print(params.get("DB", "password"))
