FROM amancevice/pandas:1.3.2
WORKDIR /lombacovid
COPY . .
CMD ["python", "macinino.py"]