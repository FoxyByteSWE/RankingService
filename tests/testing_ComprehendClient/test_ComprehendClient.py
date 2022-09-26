import unittest
from unittest.mock import patch
import sys, os


sys.path.insert(1, (str(sys.path[0]))+"/../../src/")
from ComprehendClient import ComprehendClient


class TestS3Connection(unittest.TestCase):

	def setUp(self):
		self.client = ComprehendClient()

	def test1_parseTextResponse(self):
		response = self.client.analyzeText("Test")
		self.assertIsInstance(response, dict)
		self.assertIn("Sentiment", response)
		self.assertIn("Positive", response)
		self.assertIn("Negative", response)
		self.assertIn("Neutral", response)
		self.assertIn("Mixed", response)

	def test2_analyzeText(self):
		response = self.client.analyzeText("Molto bello")
		self.assertEqual(response["Sentiment"], "POSITIVE")
		response = self.client.analyzeText("Molto brutto")
		self.assertEqual(response["Sentiment"], "NEGATIVE")

	def test3_parseKeyPhrases(self):
		response = self.client.parseKeyPhrase({'KeyPhrases': [{'Score': 0.9997683167457581, 'Text': 'Test', 'BeginOffset': 0, 'EndOffset': 14}], 'ResponseMetadata': {'RequestId': 'a935c673-1076-4567-8d75-0f55ccb0754c', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'a935c673-1076-4567-8d75-0f55ccb0754c', 'content-type': 'application/x-amz-json-1.1', 'content-length': '100', 'date': 'Sat, 24 Sep 2022 12:54:04 GMT'}, 'RetryAttempts': 0}})
		self.assertIsInstance(response, list)
		for item in response:
			assertIsInstance(iitem, dict)
		self.assertIn("Confidence", response[0])
		self.assertIn("Text", response[0])

	def test4_KeyPhrases(self):
		response = self.client.keyPhrases("Frase di prova")
		self.assertEqual(response[0]["Text"], "Frase di prova")
		self.assertGreater(response[0]["Confidence"], 0.8)

unittest.main()
