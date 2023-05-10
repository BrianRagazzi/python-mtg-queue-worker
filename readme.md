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



ver="202210211000"
docker build -t ragazzilab/mtgqueueworker:$ver -f ./Dockerfile .
docker tag ragazzilab/mtgqueueworker:$ver harbor.lab.brianragazzi.com/library/mtgqueueworker:$ver
docker tag ragazzilab/mtgqueueworker:$ver harbor.lab.brianragazzi.com/library/mtgqueueworker:latest
docker push harbor.lab.brianragazzi.com/library/mtgqueueworker:$ver
docker push harbor.lab.brianragazzi.com/library/mtgqueueworker:latest


docker run -e SLEEPTIME=5 ragazzilab/mtgqueueworker:$ver

docker build -t ragazzilab/mtgqueueworker:$ver -f ./Dockerfile .

docker rm worker

docker run --name worker \
  -e RABBITMQ_HOST="192.168.103.27" \
  -e RABBITMQ_QUEUE="cards" \
  -e RABBITMQ_USERNAME="myuser" \
  -e RABBITMQ_PASSWORD="mypass" \
  -e S3SERVER="minio.lab.brianragazzi.com" \
  -e S3BUCKET="cardimages" \
  -e S3ACCESSKEY="MCACCESS" \
  -e S3SECRETKEY="MCSECRET" \
  -e SLEEPTIME="5" \
  -e MAXRUNS="2" \
  harbor.lab.brianragazzi.com/library/mtgqueueworker:$ver \
  python -u /work/worker.py



## Run Local:
export RABBITMQ_HOST="192.168.103.10"
export RABBITMQ_QUEUE="cards"
export RABBITMQ_USERNAME="myuser"
export RABBITMQ_PASSWORD="mypass"
export S3SERVER="minio.lab.brianragazzi.com"
export S3BUCKET="cardimages"
export S3ACCESSKEY="MCACCESS"
export S3SECRETKEY="MCSECRET"
export SLEEPTIME="5"
export MAXRUNS="2"

python3 -u ./worker.py



## Deploy via TAP
Set apps.tanzu.vmware.com/workload-type to worker
--type=worker

tanzu apps workload create python-mtg-queue-worker \
  --git-repo https://github.com/BrianRagazzi/python-mtg-queue-worker \
  --git-branch main \
  --type worker \
  --label app.kubernetes.io/part-of=python-mtg-queue-worker \
  --label apps.tanzu.vmware.com/has-tests=false \
  --namespace default \
  --tail \
  --env "RABBITMQ_HOST=192.168.103.10" \
  --env "RABBITMQ_QUEUE=cards" \
  --env "RABBITMQ_USERNAME=myuser" \
  --env "RABBITMQ_PASSWORD=mypass" \
  --env S3SERVER="minio.lab.brianragazzi.com" \
  --env S3BUCKET="cardimages" \
  --env S3ACCESSKEY="MCACCESS" \
  --env S3SECRETKEY="MCSECRET" \
  --env SLEEPTIME="5" \
  --yes


tanzu apps workload delete python-mtg-queue-worker
