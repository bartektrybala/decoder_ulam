FROM python:3.9-slim-bullseye

WORKDIR /weirdtext

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

COPY ./entrypoint.sh /weirdtext


ENTRYPOINT [ "/bin/bash", "/weirdtext/entrypoint.sh"]