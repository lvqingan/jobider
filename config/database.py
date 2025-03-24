import configparser


class Database:
    @staticmethod
    def get_config():
        config = configparser.ConfigParser()
        config.read('../config.ini')
        db_config = {
            'host': config.get('database', 'host'),
            'port': config.getint('database', 'port'),
            'user': config.get('database', 'user'),
            'password': config.get('database', 'password'),
            'database': config.get('database', 'database')
        }
        return db_config