FROM python:3.8.13

RUN apt-get -y update && apt-get -y upgrade
RUN pip install --upgrade pip
RUN pip install pandas==1.1.5

WORKDIR /lombacovid
COPY . .
CMD while true; do python ./backend/macinino.py; sleep 86400; done