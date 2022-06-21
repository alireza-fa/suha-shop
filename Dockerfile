FROM python:3.8
LABEL MAINTAINER='alireza faizi | https://alirezafaizi.ir'

RUN mkdir /code
WORKDIR /code
COPY . /code

ADD requirements.txt /code

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "--chdir", "A", "--bind", ":8000", "A.wsgi.application"]
