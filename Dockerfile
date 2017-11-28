FROM ubuntu 14:04
MAINTAINER sanghee <sanghee.lee1992@gmail.com>

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
