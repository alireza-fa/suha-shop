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
  - enter S3 amazon config

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

#بسم الله الرحمن الرحیم

توضیحات:

  این پروژه بک اند یک وب سایت با استفاده از زبان پایتون و فریم ورک جنگو است.
  
  در این پروژه لاگین و رجیستر کردن کاربران با استفاده از شماره موبایل میسر میگردد. همچنین برای ارسال اس ام اس از سلری استفاده شده است تا کاربران در شرایطی که ممکن است پیش آید، معطل نشوند.
  
  یکی از مشکلات در فروشگاه های آنلاین این است که کاربر ممکن است خریدش را انجام بدهد اما اینترنتش قطع شود و ... در نهایت به صفحه تایید سفارش منتقل نشود و وضعیت سفارش بر روی پرداخت نشده باقی بماند.
  
  برای حل این مشکل در این پروژه تسکی نوشته شده است که با استفاده از سلری بیت بصورت اتوماتیک ران میشود و تمامی سفارشاتی که نیمه کاره مانده اند را چک میکند و اگر مشکلی نداشت وضعیت آن را به پرداخت شده تغییر می دهد. اما اگر مشکلی داشت(برای مثال پرداخت شده، اما مبلغ پرداخت شده کمتر و یا بیشتر است) وضعیت آن را بر روی (نیاز به بازبینی) قرار میدهد. با این آپشن سود فروشگاه آنلاین بیشتر میشود، چک کردن سفارشات راحت تر میشود و از همه مهم تر کاربران تجربه بهتری از خرید کردن می برند.
  
نکات:

  پروژه ای که در گیت قرار داده شده است، قالبی ندارد. زیرا قالب آن رایگان نیست. اما میتوانید پروژه کامل را در وب سایت shop.terangweb.com مشاهده کنید.
