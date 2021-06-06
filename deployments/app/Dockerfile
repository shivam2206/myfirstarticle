FROM python:3.8-alpine3.13 as builder

WORKDIR /usr/src/app/


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk --update add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev python3-dev openssl-dev cargo
RUN pip3 install -U pip

COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


FROM python:3.8-alpine3.13


RUN addgroup -S app && adduser -S app -G app


ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

ENV FLASK_APP=app



EXPOSE 5000


HEALTHCHECK --interval=10s --timeout=10s \
  CMD curl -f http://localhost/ || exit 1


COPY . .

RUN chown -R app:app $APP_HOME && chmod 700 -R $APP_HOME

USER app

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]

