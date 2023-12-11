from .base import *


DEBUG = True

# Databases
DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE', None),
        'NAME': env('DATABASE_NAME', None),
        'USER': env('DATABASE_USER', None),
        'PASSWORD': env('DATABASE_PASSWORD', None),
        'HOST': env('DATABASE_HOST', None),
        'PORT': env('DATABASE_PORT', None),
    },
}

# DATABASES['default'] = dj_database_url.parse("postgres://entireandfit_user:DrsQlVXQdn9OFEtzt9rprQSlpDcwc9b1@dpg-clrebtie9h4c73av1q6g-a.oregon-postgres.render.com/entireandfit")


# set admin
ADMINS = (
 ('Ejeh Faith', 'entireandfit@gmail.com'), ('Big Steve', 'mrejembistephen@gmail.com')
)
ALLOWED_HOSTS = ['*']