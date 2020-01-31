FROM markadams/chromium-xvfb-py3 

WORKDIR /app

ENV DISPLAY=:9527

ADD requirement.txt /app

RUN pip3 install -r /app/requirement.txt

ADD main.py /app
