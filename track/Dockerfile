FROM python:3.8

RUN mkdir /opt/track
COPY . /opt/track
WORKDIR /opt/track

RUN pip install -r requirements.txt

CMD [ "python",  "src/main.py" ]
