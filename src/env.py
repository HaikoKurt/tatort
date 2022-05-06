import os

class Environment :
    ENV_DB_HOST = 'FM_DB_HOST'
    ENV_DB_USER = 'FM_DB_USER'
    ENV_DB_PASSWD = 'FM_DB_PASSWD'
    ENV_DATABASE = 'FM_DATABASE'
    
    def __init__(self) -> None:
        self.db_host = self._get_env(self.ENV_DB_HOST, 'malmstrom')
        self.db_user = self._get_env(self.ENV_DB_USER, 'xxx')
        self.db_passwd = self._get_env(self.ENV_DB_PASSWD, 'zzz')
        self.database = self._get_env(self.ENV_DATABASE, 'xxx_dev')

    def _get_env(self, name, default) :
        value = os.environ.get(name)
        if value is None :
            return default
        else :
            return value

if __name__ == "__main__" :
    env = Environment()
    print(env.registration_time)