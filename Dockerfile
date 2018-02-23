FROM python:2

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install .

CMD [ "python", "osso/api.py" ]
