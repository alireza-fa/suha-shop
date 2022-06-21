# terang_shop
terang shop is a production project for a business

create volume 
create networks

docker-compose up -d
dokcer exec -it app bash
python manage.py migrate
python manage.py collectstatic
