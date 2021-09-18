FROM debian:buster-slim


RUN apt update
RUN apt upgrade
RUN apt dist-upgrade
RUN apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget

RUN mkdir ~/tmp
RUN cd ~/tmp
RUN wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
RUN tar -xvzf Python-3.9.0.tgz
RUN cd Python-3.9.0
RUN ./configure
RUN make install

RUN pip install pandas==1.3.3

WORKDIR /lombacovid
COPY . .
RUN chmod +x ./backend/timescript.sh
CMD ./backend/timescript.sh