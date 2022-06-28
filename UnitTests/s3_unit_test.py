import os, sys
from os.path import exists
import logging
import boto3
from botocore.exceptions import ClientError

from s3 import listBuckets, listBucketObjetcs, uploadFile, downloadFile, deleteFile

BUCKET_NAME = "foxybyteswe"

def testListBuckets():
	listBuckets()

def testListBucketObjetcs(bucket):
	listBucketObjetcs(bucket)

def testUploadFile(file_name, bucket, object_name=None):
	if not exists(file_name):
		open(file_name, 'x').close()
	uploadFile(file_name, bucket)
	listBucketObjetcs(bucket)
	os.remove('test_file')

def testDownloadFile(bucket, object_name, file_name):
	downloadFile(bucket, object_name, file_name)
	print(os.listdir())
	os.remove(file_name)

def testDeleteFile(bucket, file_name):
	deleteFile(bucket, file_name)
	listBucketObjetcs(bucket)

def main():
	print("Listing existing buckets...")
	testListBuckets()
	print('\n')
	print("Listing existing objects in " + BUCKET_NAME + "...")
	testListBucketObjetcs(BUCKET_NAME)
	print('\n')
	print("Listing existing objects in "+ BUCKET_NAME + " after uploading a test file...")
	testUploadFile('test_file', BUCKET_NAME)
	print('\n')
	print("Listing existing objects in local dir after downloading the test file...")
	testDownloadFile(BUCKET_NAME, 'test_file', 'downloaded_test_file')
	print('\n')
	print("Listing existing objects in " + BUCKET_NAME + " after deleting the test file...")
	testDeleteFile(BUCKET_NAME, 'test_file')
	print('\n')

if __name__ == "__main__":
	main()
