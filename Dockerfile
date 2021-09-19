FROM python@sha256:eec73d7e9ace1e12242b9612726e31e2f463e5f50c128a53a5621e9694299fda

RUN apt update && apt full-upgrade

RUN pip install pandas==1.3.3

WORKDIR /lombacovid
COPY . .
RUN chmod +x ./backend/timescript.sh
CMD ./backend/timescript.sh