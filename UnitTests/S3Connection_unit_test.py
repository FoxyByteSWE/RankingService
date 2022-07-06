import os, sys, inspect
from os.path import exists
import logging
import boto3
from botocore.exceptions import ClientError

sys.path.insert(0, (str(sys.path[0]))+"/../") 

from S3Connection import S3Connection

BUCKET_NAME = "foxybyteswe"

def testListBuckets(s3):
	s3.listBuckets()

def testListBucketObjetcs(s3, bucket = None):
	s3.listBucketObjetcs(bucket)

def testUploadFile(s3, file_name, bucket = None, object_name=None):

	if not exists(file_name):
		open(file_name, 'x').close()

	s3.uploadFile(file_name, bucket)

	s3.listBucketObjetcs(bucket)

	os.remove('test_file')

def testDownloadFile(s3, object_name, file_name, bucket = None):
	s3.downloadFile(object_name, file_name, bucket)
	print(os.listdir())
	os.remove(file_name)

def testDeleteFile(s3, file_name, bucket = None):
	s3.deleteFile(file_name, bucket)
	s3.listBucketObjetcs(bucket)

def main():

	s3 = S3Connection(BUCKET_NAME)

	print("Listing existing buckets...")
	testListBuckets(s3)
	print('\n')
	print("Listing existing objects in " + BUCKET_NAME + "...")
	testListBucketObjetcs(s3)
	print('\n')
	print("Listing existing objects in "+ BUCKET_NAME + " after uploading a test file...")
	testUploadFile(s3, 'test_file')
	print('\n')
	print("Listing existing objects in local dir after downloading the test file...")
	testDownloadFile(s3, 'test_file', 'downloaded_test_file')
	print('\n')
	print("Listing existing objects in " + BUCKET_NAME + " after deleting the test file...")
	testDeleteFile(s3, 'test_file')
	print('\n')

if __name__ == "__main__":
	main()
