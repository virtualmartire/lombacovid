FROM balenalib/raspberry-pi-python:3


RUN apt-get update && apt-get upgrade
RUN pip install pandas==1.1.5

WORKDIR /lombacovid
COPY . .
RUN chmod +x ./backend/timescript.sh
CMD ./backend/timescript.sh