import unittest
from unittest.mock import patch
import sys,os


sys.path.insert(1, (str(sys.path[0]))+"/../../src/")
sys.path.insert(1, (str(sys.path[0]))+"/../../src/location")
from DBConnection import DBConnection



class TestDBConnection(unittest.TestCase):

	def setUp(self):
		#self.connection = DBConnection("michelinsocial.ctr0m4f2rgau.eu-west-1.rds.amazonaws.com", "admin", "#g7ct=MD")
		self.connection = DBConnection()

	def test1_createServerConnection(self):
		conn = self.connection.createServerConnection();
		self.assertNotEqual(conn, None)

	def test2_createDatabase(self):
		self.connection.createDatabase("test");
		conn = self.connection.server_connection
		cursor = conn.cursor(buffered=True)
		cursor.execute("show schemas;")
		response = cursor.fetchall()
		print(response)
		self.assertTrue(('test',) in response)

	def test3_createDatabaseConnection(self):
		conn = self.connection.createDatabaseConnection("test");
		self.assertNotEqual(conn, None)

	def test4_executeQuery(self):
		response = self.connection.executeQuery("show tables;")
		self.assertEqual(response, [])

	#def test5_insertLocations(self):
		#self.assertEqual(self.connection.insertRestaurants(), "12AB34CD")
	
	def test6_createS3Connection(self):
		self.assertNotEqual(self.connection.createS3Connection(), None)

unittest.main()
