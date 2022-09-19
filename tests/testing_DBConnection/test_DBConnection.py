import unittest
from unittest.mock import patch
import sys,os


sys.path.insert(1, (str(sys.path[0]))+"/../../src/")
from DBConnection import DBConnection



class TestDBConnection(unittest.TestCase):

	def setUp(self):
		self.connection = S3Connection("foxybyteswe")

	def test_createServerConnection(self):
		self.assertEqual(self.connection.list_buckets(), {"pk": 12345,
													 "username": "marcouderzo",
													 "isPrivate": False,
													 "lastPostCheckedCode": "12AB34CD" })

	def test_createDatabase(self):
		self.assertEqual(self.connection.createDatabase(), 12345)

	def test_createDatabaseConnection(self):
		self.assertEqual(self.connection.createDatabaseConnection(), "marcouderzo")

	def test_executeQuery(self):
		self.assertFalse(self.connection.executeQuery())

	def test_insertRestaurants(self):
		self.assertEqual(self.connection.insertRestaurants(), "12AB34CD")
	
	def test_createS3Connection(self):
		self.assertEqual(self.connection.createS3Connection(), "12AB34CD")

	def test_uploadDB(self):
		self.connection.uploadDB("newcode")

	def test_downloadDB(self):
		self.connection.downloadDB("newcode")

unittest.main()
