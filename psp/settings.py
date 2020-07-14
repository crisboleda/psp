
ENVIOROMENTS = ['local', 'production']

ENV = 'production'


if ENV == ENVIOROMENTS[0]:
    from psp.config.local_env import *
elif ENV == ENVIOROMENTS[1]:
    from psp.config.production_env import *
