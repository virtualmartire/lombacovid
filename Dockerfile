FROM python:3.9.7


RUN apt clean && apt-get update && apt-get upgrade
RUN pip install pandas==1.3.3

WORKDIR /lombacovid
COPY . .
RUN chmod +x ./backend/timescript.sh
CMD ./backend/timescript.sh