FROM python:3.10

RUN apt update -y && apt upgrade -y

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend /app

ADD start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]
