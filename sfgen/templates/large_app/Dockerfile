FROM python:3.7

RUN pip3 install virtualenv

WORKDIR /usr/src/app

COPY requirements.txt .
RUN virtualenv env && . env/bin/activate && pip3 install -r requirements.txt


COPY src .

EXPOSE 8000

CMD ["./deploy.sh", "test"]
