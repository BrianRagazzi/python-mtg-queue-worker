#!/usr/bin/env python

from minio import Minio
from minio.error import S3Error
import pathlib
import os

S3SERVER="minio.lab.brianragazzi.com"
S3BUCKET="cardimages"
S3ACCESSKEY="MCACCESS"
S3SECRETKEY="MCSECRET"


def openBucket():
    global client
    client = Minio(S3SERVER,
    access_key=S3ACCESSKEY,
    secret_key=S3SECRETKEY)

    

    if client.bucket_exists(S3BUCKET):
        objects = client.list_objects(S3BUCKET)
        for obj in objects:
            #print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,obj.etag, obj.size, obj.content_type)
            #print(obj.object_name)
            print("https://" + S3SERVER + "/" + str(obj.bucket_name) + "/" + str(obj.object_name))
    else:
        print("Bucket " + S3BUCKET + " is not found")


#openBucket()

# client.fput_object(S3BUCKET,"testfile","/Users/bragazzi/Documents/github/homelab/jobpatterns/scryfall/images/worker/readme.md")

def imagesinBucket():
    client = Minio(S3SERVER,
    access_key=S3ACCESSKEY,
    secret_key=S3SECRETKEY)
    objcnt=0
    if client.bucket_exists(S3BUCKET):
        objects = client.list_objects(S3BUCKET)
        for obj in objects:
            objcnt=objcnt+1
        return int(objcnt)
    else:
        return int(0)


print("images in bucket:" + str(imagesinBucket()))
