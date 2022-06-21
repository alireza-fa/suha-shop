# suha_shop
Suha shop is a online store.

Use:

part1: (run app)
  - docker volume create postgres_data
  - docker volume create static_volume
  - docker network create main
  - docker network create nginx_network
  - docker-compose up -d

part2: (set config)
  - docker exec -it app bash
  - python manage.py migrate
  - python manage.py collectstatic

part3: (required setting in A.local_settings.py)
  - enter ZARINPAL config
  - enter Kavenegar config
  - enter S3 amazon config (i use arvan cloud baket)

Optional:
  - if you want to translate, you should install gettex in app container.
  - you can use rosetta for translate, /rosetta/

Note:
   - This project has no template. Because his template is a premium template and if put it, this is not a good behavior. But you can see the full project at shop.terangweb.com

Technologies and tools:
  - Python
  - Django
  - Docker
  - S3 amazon
  - Arvan Cloud
  - Web serice sms(Kavenegar)
  - Nginx
  - Celery
  - i18n
