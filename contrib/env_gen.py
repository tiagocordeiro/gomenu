#!/usr/bin/env python

"""
Django SECRET_KEY generator.
"""
from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
sk = get_random_string(50, chars)

CONFIG_STRING = f"""# Basic config
SECRET_KEY={sk}
DEBUG=True
ALLOWED_HOSTS=localhost, 127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
# Se usar docker...
# DATABASE_URL=postgres://gomenu:gomenu@localhost/postgres

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=localhost
EMAIL_PORT=25
EMAIL_USE_TLS=False
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Codecov
CODECOV_TOKEN=

# Sentry
SENTRY_DSN=

# Cloudinary
CLOUDINARY_URL=

# AWS
DJANGO_AWS_ACCESS_KEY_ID=
DJANGO_AWS_SECRET_ACCESS_KEY=
DJANGO_AWS_STORAGE_BUCKET_NAME=

# WooCommerce
WC_CK=
WC_CS=
WC_URL=
"""

# Writing our configuration file to '.env'
with open('.env', 'w') as configfile:
    configfile.write(CONFIG_STRING)
