import logging
import boto3
from botocore.exceptions import ClientError

# S3 bucket name
BUCKET_NAME = "foxybyteswe"

class S3Connection:

	def __init__(self, default_bucket = ""):
		self.default_bucket = default_bucket

	def listBuckets(self):
		s3 = boto3.client('s3')
		response = s3.list_buckets()

		print('Existing buckets:')
		for bucket in response['Buckets']:
			print(f'  {bucket["Name"]}')

	def listBucketObjetcs(self, bucket = None):

		if bucket is None:
			bucket = self.default_bucket

		s3 = boto3.client('s3')
		for key in s3.list_objects(Bucket=bucket)['Contents']:
			print(key['Key'])

	def uploadFile(self, file_name, bucket = None, object_name=None):

		if bucket is None:
			bucket = self.default_bucket

		# If S3 object_name was not specified, use file_name
		if object_name is None:
			object_name = os.path.basename(file_name)

		# Upload the file
		s3 = boto3.client('s3')
		try:
			response = s3.upload_file(file_name, bucket, object_name)
		except ClientError as e:
			logging.error(e)
			return False
		return True

	def downloadFile(self, object_name, file_name, bucket = None):

		if bucket is None:
			bucket = self.default_bucket

		s3 = boto3.client('s3')
		s3.download_file(bucket, object_name, file_name)

	def deleteFile(self, file_name, bucket = None):

		if bucket is None:
			bucket = self.default_bucket

		s3_client = boto3.client('s3')
		response = s3_client.delete_object(
			Bucket = bucket,
			Key = file_name
		)

	def readFile(self, file_name, bucket = None):

		if bucket is None:
			bucket = self.default_bucket

		s3_client = boto3.client('s3')
		response = s3_client.get_object(
			Bucket = bucket,
			Key = file_name
		)["Body"].read()

		return response
