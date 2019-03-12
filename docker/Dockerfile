# based on ubuntu 16.04 lts
FROM tiangolo/meinheld-gunicorn-flask:python3.7

# Install dependencies and tools, last libs are for freeview
RUN \
  pip install flask_bootstrap4 flask_sqlalchemy flask_wtf numpy scipy

# Clone newest version of XNucCalc and prepare for docker
RUN \
  rm -rf /app/* && \
  git clone https://github.com/elenhinan/XNucCalc.git /app && \
  mkdir /app/app/static && \
  wget -nv https://code.jquery.com/jquery-3.3.1.min.js -P /app/app/static && \
  wget -nv https://cdn.plot.ly/plotly-latest.min.js -P /app/app/static  && \
  echo "#! /usr/bin/env bash\ncd /app\ngit pull" > /app/prestart.sh && \
  chmod +x /app/prestart.sh /app/main.py

  VOLUME [ "/data" ]