import logging
import boto3

class ComprehendClient:

	def __init__(self):
		pass

	def analyzeText(self, text):
		client = boto3.client('comprehend')

		lang = client.detect_dominant_language(
			Text = text
		)
		lang = lang["Languages"][0]["LanguageCode"]
		#print(lang)
		if lang not in ["ar", "hi", "ko", "zh-TW", "ja", "zh", "de", "pt", "en", "it", "fr", "es"]:
			response = {}
			response["Sentiment"] = "Neutral"
			response["Positive"] = 0
			response["Negative"] = 0
			response["Neutral"] = 1
			response["Mixed"] = 0
			print("Unknown language")
			#print(text)
			#print(response)
		else:
			response = client.detect_sentiment(
				Text = text,
				LanguageCode = lang
			)
			response = self.parseTextResponse(response)
			#print(text)
			#print(response)

		return response

	def parseTextResponse(self, response):
		dict = {}

		dict["Sentiment"] = response["Sentiment"]
		dict["Positive"] = response["SentimentScore"]["Positive"]
		dict["Negative"] = response["SentimentScore"]["Negative"]
		dict["Neutral"] = response["SentimentScore"]["Neutral"]
		dict["Mixed"] = response["SentimentScore"]["Mixed"]

		return dict

	def keyPhrases(self, text):
		client = boto3.client('comprehend')

		lang = client.detect_dominant_language(
			Text = text
		)
		lang = lang["Languages"][0]["LanguageCode"]
		#print(lang)

		response = client.detect_key_phrases(
			Text = text,
			LanguageCode = lang
		)
		response = self.parseKeyPhrase(response)
		return response
		#print(text)
		#print(response)

	def parseKeyPhrase(self, response):
		list = []

		for item in response["KeyPhrases"]:
			dict = {}
			dict["Confidence"] = item["Score"]
			dict["Text"] = item["Text"]
			list.append(dict)

		return list
