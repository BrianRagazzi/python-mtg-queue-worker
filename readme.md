Use mc (minio client) cli to copy items to S3

Python things:

python3 -m pip install urllib3



Go get data blob from RabbitMQ
Parse for image URL
 image_uri.large
Get image
Push image to S3 bucket
  use multiverse_id ?
  folder for set



  wget https://dl.min.io/client/mc/release/linux-amd64/mc
  chmod +x mc
  ./mc --help


  check ../scratch/mc-job



Do while 1=1

  Do while Queue is not empty
    Get item from queue
      get image url
      download image
      copy image to S3
  Loop
  Sleep 60 seconds
Loop


amgp-get - output to std

amqp-get -u=$BROKER_URL -q=job1
carddata=$(amqp-get -u=$BROKER_URL -q=job1 | base64 -d)
status=$?
if [$status -eq 0] then;
  #successful pull
else
  # queue empty

fi
amqp-get -u=$BROKER_URL -q=job1 | base64 -d | jq -r '.image_uris.large'




docker build -t ragazzilab/scryfallwork:dev -f ./Dockerfile .
docker tag ragazzilab/scryfallwork:dev harbor.lab.brianragazzi.com/library/scryfallwork:latest
docker push harbor.lab.brianragazzi.com/library/scryfallwork:latest


docker run -e SLEEPTIME=5 ragazzilab/scryfallwork:002

docker build -t ragazzilab/scryfallwork:dev -f ./Dockerfile .


docker run --name worker \
  -e RABBITMQ_HOST="192.168.103.33" \
  -e  RABBITMQ_QUEUE="job2" \
  -e  S3SERVER="minio.lab.brianragazzi.com" \
  -e  S3BUCKET="mctest" \
  -e  S3ACCESSKEY="MCACCESS" \
  -e  S3SECRETKEY="MCSECRET" \
  -e  SLEEPTIME="5" \
  -e  MAXRUNS="2" \
  ragazzilab/scryfallwork:dev \
  python -u /work/worker.py
