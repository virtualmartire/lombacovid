FROM python:3.6-buster

RUN apt-get -y update && apt-get -y upgrade
RUN pip install --upgrade pip

RUN pip install pandas==1.1.5

WORKDIR /lombacovid
COPY . .
RUN chmod +x ./backend/timescript.sh
CMD ./backend/timescript.sh
