# based on ubuntu 16.04 lts
FROM tiangolo/meinheld-gunicorn-flask:python3.7

# Install dependencies and tools, last libs are for freeview
RUN \
  pip install flask_bootstrap flask_sqlalchemy flask_wtf numpy scipy && \
  rm -rf /app/* && \
  git clone https://github.com/elenhinan/XNucCalc.git /app && \
  mkdir /app/app/static && \
  wget https://code.jquery.com/jquery-3.3.1.min.js -P /app/app/static && \
  wget https://cdn.plot.ly/plotly-latest.min.js -P /app/app/static  && \
  echo -ne "#! /usr/bin/env bash\n#cd /app\n#git pull" > /app/prestart.sh && \
  chmod +x /app/prestart.sh /app/main.py