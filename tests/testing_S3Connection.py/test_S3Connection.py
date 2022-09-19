import unittest
from unittest.mock import patch
import sys,os


sys.path.insert(1, (str(sys.path[0]))+"/../../src/")
from S3Connection import S3Connection



class TestS3Connection(unittest.TestCase):

	def setUp(self):
		self.connection = S3Connection("foxybyteswe")

	def test_listBuckets(self):
		self.assertEqual(self.connection.list_buckets(), {"pk": 12345,
													 "username": "marcouderzo",
													 "isPrivate": False,
													 "lastPostCheckedCode": "12AB34CD" })

	def test_listBucketObjects(self):
		self.assertEqual(self.connection.list_bucketObjects(), 12345)

	def test_uploadFile(self):
		self.assertEqual(self.connection.uploadFIle(), "marcouderzo")

	def test_downloadFile(self):
		self.assertFalse(self.connection.downloadFile())

	def test_deleteFIle(self):
		self.assertEqual(self.connection.deleteFile(), "12AB34CD")
	
	def test_readFIle(self):
		self.assertEqual(self.connection.readFile(), "12AB34CD")

	def test_writeFile(self):
		self.assertTrue(self.connection.writeFile() == "newcode")

unittest.main()
