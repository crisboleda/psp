
from decouple import config


# Si la variable de entorno es verdadera toma las configuraciones de producción
if config('DJANGO_PRODUCTION_ENV', default=False, cast=bool):
    from psp.config.production_env import *
elif config('DJANGO_PRE_PRODUCTION_ENV', default=False, cast=bool):
    from psp.config.pre_production_env import *
else:
    from psp.config.local_env import *

