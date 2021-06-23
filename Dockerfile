FROM python:latest

WORKDIR /bot
COPY . . 

RUN pip3 install -r requirements.txt --quiet

ENTRYPOINT ["python3", "bot.py"]
