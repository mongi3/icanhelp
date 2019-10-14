FROM python:2.7-alpine

LABEL MAINTANER "mongi3@gmail.com"

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt && rm -rf ~/.cache/pip

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "code.py" ]

