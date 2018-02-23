FROM python:2

COPY . /usr/src/app
COPY etc /etc
WORKDIR /usr/src/app
RUN pip install .

CMD [ "python", "osso/api.py" ]
