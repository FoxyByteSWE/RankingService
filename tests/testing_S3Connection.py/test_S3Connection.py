import unittest
from unittest.mock import patch
import sys, os


sys.path.insert(1, (str(sys.path[0]))+"/../../src/")
from S3Connection import S3Connection


class TestS3Connection(unittest.TestCase):

	def setUp(self):
		self.connection = S3Connection("foxybytetestbucket")

	def test1_listBuckets(self):
		test_bucket_exists = False
		response = self.connection.listBuckets()
		for bucket in response["Buckets"]:
			if "foxybytetestbucket" in bucket["Name"]:
				test_bucket_exists = True
		self.assertTrue(test_bucket_exists)
		#self.assertTrue("foxybytetestbucket" in str(self.connection.listBuckets()))

	def test2_listBucketObjects(self):
		response = self.connection.listBucketObjetcs("foxybytetestbucket")
		list = []
		for dict in response["Contents"]:
			list.append(dict["Key"])
		self.assertTrue("test_file" in list)

	def test3_uploadFile(self):
		file = open('test_upload','a+')
		self.connection.uploadFile("test_upload", "foxybytetestbucket")
		response = self.connection.listBucketObjetcs("foxybytetestbucket")
		list = []
		for dict in response["Contents"]:
			list.append(dict["Key"])
		self.assertTrue("test_upload" in list)
		os.remove("test_upload")

	def test4_downloadFile(self):
		self.connection.downloadFile("test_upload", "test_download")
		self.assertTrue(os.path.isfile("test_download"))
		os.remove("test_download")

	def test5_deleteFIle(self):
		self.connection.deleteFile("test_upload")
		response = self.connection.listBucketObjetcs("foxybytetestbucket")
		list = []
		for dict in response["Contents"]:
			list.append(dict["Key"])
		self.assertTrue("test_upload" not in list)
	
	def test6_readFIle(self):
		self.assertEqual(self.connection.readFile("test_file"), b"Test\n")

	def test7_writeFile(self):
		self.connection.writeFile("Testing writeFile", "test_write")
		self.assertEqual(self.connection.readFile("test_write"), b"Testing writeFile")
		self.connection.deleteFile("test_write")

unittest.main()
