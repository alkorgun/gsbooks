FROM python:3.6
LABEL maintainer=alkorgun@gmail.com

WORKDIR /root

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY gsbooks gsbooks/
COPY scripts/* /bin/

RUN chmod a+x ./run.sh /bin/*

EXPOSE 80

CMD ./run.sh
