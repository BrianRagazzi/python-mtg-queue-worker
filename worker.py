#!/usr/bin/env python




import os
import sys
import time
import json
import pika
import requests
from requests.exceptions import HTTPError
# import urllib3.request
from genericpath import isfile
from minio import Minio
from minio.error import S3Error
# import requests
# import hashlib



def main():
    print(" [*] Starting main")
    host = os.getenv("RABBITMQ_HOST")
    qname = os.getenv("RABBITMQ_QUEUE")
    rabbitmq_username = os.getenv("RABBITMQ_USERNAME") or "myuser"
    rabbitmq_password = os.getenv("RABBITMQ_PASSWORD") or "mypass"
    s3server = os.getenv("S3SERVER")
    s3bucket = os.getenv("S3BUCKET")
    s3accesskey = os.getenv("S3ACCESSKEY")
    s3secretkey = os.getenv("S3SECRETKEY")
    sleeptime = int(os.getenv("SLEEPTIME")) or 2
    #maxruns = int(os.getenv("MAXRUNS")) or 0
    print("  Rabbit host %r" % host)
    print("  Rabbit queue %r" %qname)
    print("  s3 server %r" % s3server)
    print("  sleeptime %r" % str(sleeptime))
    #print("  maxruns %r" % str(maxruns))

    # connect to RabbitMQ
    rabbit_credentials = pika.PlainCredentials(rabbitmq_username,rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,credentials=rabbit_credentials))
    channel = connection.channel()
    channel.queue_declare(queue=qname, durable=True)
    
    # connect to S3
    client=openBucket(s3server,s3bucket,s3accesskey, s3secretkey)
    global runCt
    runCt = 0
    print(' [*] Started - Waiting for messages.')


    def callback(ch, method, properties, body):
        global runCt
        # if int(maxruns)>0:
        #     runCt=runCt+1
        #     if int(runCt) > int(maxruns):
        #         print(" [*] Max interations:" + str(maxruns) + " reached, quitting")
        #         abort()      

        try:
            cardjson=body
            print(" [*] Message received, parsing")
            #cardjson = cardjson.replace("\'", "\"") #replace single-quote with proper doule-quotes
            #print(cardjson)
            #y = json.loads(body)
            
            #print("name: " + str(y['name']))



            imageurl=getImageURL(cardjson)
            if imageurl != "":
                print(" [*] Found imageURL: " + str(imageurl))
                imagefile=getSetCardNum(cardjson)+".jpg"
                print(" [*] Downloading " + imageurl + " to " + imagefile)
                downloadFile(imageurl,imagefile)
                if fileExists(imagefile):
                    print(" [*] File " + imagefile + " exists, attempt upload")
                    try:
                        client.fput_object(s3bucket,imagefile,imagefile)
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                        deleteFile(imagefile)
                        print(" [x] Done")
                        print(" [*] Sleeping " + str(sleeptime) + " seconds")
                        time.sleep(int(sleeptime))
                    except S3Error as exc:
                        print(" [!] ERROR: ", exc)
                else:
                    print(" [!] ERROR: image is missing:" + str(imagefile))
            else:
                print(" [!] ACK anyway to clear item from queue")
                ch.basic_ack(delivery_tag=method.delivery_tag)
        except HTTPError as http_err:
            print(" [!] HTTP error occurred: " + str(http_err))
        except Exception as e:
            print(" [!] ERROR: " + str(e))
                

        
        

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=qname, on_message_callback=callback)
    channel.start_consuming()
    # don't actually have to check whether queue is empty, do we?





def openBucket(s3server,s3bucket,s3accesskey,s3secretkey):
    global client
    client = Minio(s3server,
    access_key=s3accesskey,
    secret_key=s3secretkey)

    if client.bucket_exists(s3bucket):
        objects = client.list_objects(s3bucket) #iterator of object
        ct=0
        for obj in objects:
            ct=ct+1
        print(" [*] " + str(ct) + " objects in bucket already")
        #     print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
        #   obj.etag, obj.size, obj.content_type)
    else:
        print(" [!] ERROR - Bucket " + s3bucket + " is not found, quitting")
        abort()
    return client





def getImageURL(cardjson):
    y = json.loads(cardjson)
    # largeimageurl=y["image_uris"]["large"]
    # Yes there is an easier way to do this
    try:
        imageuris=y["image_uris"]
        largeimageurl=imageuris["large"]
    except Exception as e:
        print(" [!] ERROR: Unable to parse.")
        largeimageurl=""
    return largeimageurl

def getMultiverseID(cardjson):
    y = json.loads(cardjson)
    return y["multiverse_ids"][0]

def getSetCardNum(cardjson):
    y = json.loads(cardjson)
    set=y["set"]
    num=y["collector_number"]
    return set+str(num)

def getLayout(cardjson):
    y = json.loads(cardjson)
    layout=y["layout"]
    return layout


def downloadFile(url, filename):

    #return wget.download(url,filename)
    response = requests.get(url)
    with open(filename,"wb") as f:  #wb = write binary
        f.write(response.content)
    # urllib.request.urlretrieve(url, filename)

def fileExists(filename):
    return os.path.exists

def deleteFile(filename):
    if os.path.isfile(filename):
        os.remove(filename)
    else:
        print(" [!] ERROR: %s file not found" % filename)


def abort():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)