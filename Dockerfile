FROM python:3-alpine

LABEL MAINTANER "mongi3@gmail.com"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt && rm -rf ~/.cache/pip

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "code.py" ]
