import os

class Environment :
    ENV_XXX = 'XXX'
    
    def __init__(self) -> None:
        self.xxx = self._get_env(self.ENV_XXX, 'yyy')

    def _get_env(self, name, default) :
        value = os.environ.get(name)
        if value is None :
            return default
        else :
            return value

if __name__ == "__main__" :
    env = Environment()
    print(env.registration_time)