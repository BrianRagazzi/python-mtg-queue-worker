FROM python:latest

ENV BROKER_URL amqp://guest:guest@rabbitmq-service.rabbit.svc.cluster.local:5672
ENV QUEUE_NAME mtgcards
ENV HOST "192.168.103.33"
ENV QNAME "job2"
ENV S3SERVER="minio.lab.brianragazzi.com"
ENV S3BUCKET="job2"
ENV S3ACCESSKEY="MCACCESS"
ENV S3SECRETKEY="MCSECRET"
ENV SLEEPTIME=2

WORKDIR /work

RUN pip install pika minio wget

COPY worker.py /work/
CMD  ["python","-u","/work/worker.py"]
