FROM python:stretch

COPY . /dict_app
WORKDIR /dict_app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["gunicorn", "-b", ":5000", "app:app"]
