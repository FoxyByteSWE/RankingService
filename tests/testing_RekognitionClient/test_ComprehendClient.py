import unittest
from unittest.mock import patch
import sys, os


sys.path.insert(1, (str(sys.path[0]))+"/../../src/")
from RekognitionClient import RekognitionClient


class TestS3Connection(unittest.TestCase):

	def setUp(self):
		self.client = RekognitionClient()

	def test1_parseImageResponse(self):
		response = self.client.detectLabels("https://thumbs.dreamstime.com/z/happy-little-boy-smiley-face-portrait-human-concept-freshness-133726078.jpg")
		self.assertIsInstance(response, list)
		for item in response:
			self.assertIsInstance(item, dict)
			self.assertIn("Name", item)
			self.assertIn("Confidence", item)
			self.assertIn("Parents", item)

	def test2_detectLabels(self):
		response = self.client.detectLabels("https://thumbs.dreamstime.com/z/happy-little-boy-smiley-face-portrait-human-concept-freshness-133726078.jpg")
		self.assertEqual(response[0]["Name"], "Face")
		self.assertGreater(response[0]["Confidence"], 0.8)
		self.assertEqual(response[0]["Parents"], [{'Name': 'Person'}])

	def test3_parseEmotions(self):
		response = self.client.detectFacesEmotions("https://thumbs.dreamstime.com/z/happy-little-boy-smiley-face-portrait-human-concept-freshness-133726078.jpg")
		self.assertIsInstance(response, list)
		for item in response:
			self.assertIsInstance(item, dict)
			self.assertIn("Emotion", item["Emotions"][0])
			self.assertIn("EmotionConfidence", item["Emotions"][0])

	def test4_detectFacesEmotions(self):
		response = self.client.detectFacesEmotions("https://thumbs.dreamstime.com/z/happy-little-boy-smiley-face-portrait-human-concept-freshness-133726078.jpg")
		self.assertEqual(response[0]["Emotions"][0]["Emotion"], "HAPPY")
		self.assertGreater(response[0]["Emotions"][0]["EmotionConfidence"], 0.8)

unittest.main()
