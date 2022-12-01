# based on uwsgi-nginx-flask
FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN \
  apt-get update && \
  apt-get install -y ca-certificates && \
  rm -rf /var/lib/apt/lists/*

# Clone newest version of XNucCalc and prepare for docker
RUN \
  rm -rf /app/* && \
  git clone https://github.com/elenhinan/XNucCalc.git /app && \
  wget -nv https://code.jquery.com/jquery-3.3.1.min.js -P /app/app/static && \
  wget -nv https://cdn.plot.ly/plotly-latest.min.js -P /app/app/static  && \
  echo "#! /usr/bin/env bash\ncd /app\ngit pull" > /app/prestart.sh && \
  echo "[uwsgi]\nmodule = app\ncallable=app" > /app/uwsgi.ini && \
  chmod +x /app/prestart.sh /app/main.py

# Install dependencies and tools
RUN \
  cd /app && pip install -r requirements.txt

ENV STATIC_PATH /app/app/static

VOLUME [ "/data" ]