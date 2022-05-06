FROM python:3

ENV TZ=Europe/Berlin
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

EXPOSE 10000
VOLUME [ "/data" ]

ENV FLASK_ENV=production

CMD [ "gunicorn" ]