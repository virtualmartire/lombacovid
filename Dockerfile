FROM python:3.6

RUN pip install pandas==1.1.5

WORKDIR /lombacovid
COPY . .
RUN chmod +x ./backend/timescript.sh
CMD ./backend/timescript.sh