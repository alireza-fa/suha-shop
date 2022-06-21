SECRET_KEY = 'django-insecure-c*5@3vv0h_u0(=r2d+*)6ve8=ym2%do#rul8e2%v&-(w!9y5jy'

DEBUG = False

ALLOWED_HOSTS = ["*"]

DB_NAME = 'shop'
DB_USER = 'shop'
DB_PASS = 'shop'
DB_HOST = 'postgres'
DB_PORT = 5432

# ZARINPAL
ZARINPAL_MERCHANT = ''
ZARINPAL_CALLBACK_URL = 'http://shop.terangweb.com/order/verify/'
ZARINPAL_DESCRIPTION = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"

# KAVE_NEGAR
KAVE_API_KEY = ''
KAVE_SENDER = ''

URL_ROOT = 'http://shop.terangweb.com'


# S3 amazon, media storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''
AWS_SERVICE_NAME = 's3'
AWS_S3_ENDPOINT_URL = ''
AWS_S3_FILE_OVERWRITE = False
