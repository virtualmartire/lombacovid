FROM python:3.8-slim

RUN apt-get update
RUN apt-get -y dist-upgrade
RUN pip3 install pandas==1.3.3

WORKDIR /lombacovid
COPY . .
RUN chmod +x ./backend/timescript.sh
CMD ./backend/timescript.sh