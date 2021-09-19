FROM arm32v6/python:3.6-alpine3.13

RUN pip install pandas==1.3.3

WORKDIR /lombacovid
COPY . .
RUN chmod +x ./backend/timescript.sh
CMD ./backend/timescript.sh