import os, sys
from s3 import uploadFile, deleteFile
import urllib.request
import logging
import boto3
from math import exp
import pprint
from botocore.exceptions import ClientError
import datetime

from restaurant import Restaurant, Media, json2Restaurants

BUCKET_NAME = "foxybyteswe"

def analyzeText(text):
	client = boto3.client('comprehend')
	response = client.detect_sentiment(
		Text = text,
		LanguageCode = 'it'
	)
	response = parseTextResponse(response)
	#print(response)
	return response

def parseTextResponse(response):
	dict = {}
	dict["Sentiment"] = response["Sentiment"]
	dict["Positive"] = response["SentimentScore"]["Positive"]
	dict["Negative"] = response["SentimentScore"]["Negative"]
	dict["Neutral"] = response["SentimentScore"]["Neutral"]
	dict["Mixed"] = response["SentimentScore"]["Mixed"]
	return dict

def parseImageResponse(response):
	list = []
	for i in response["Labels"]:
		dict = {}
		dict["Name"] = i["Name"]
		dict["Confidence"] = i["Confidence"]
		dict["Parents"] = i["Parents"]
		list.append(dict)
	print(list)
	return dict

def detectLabels(url):
	urllib.request.urlretrieve(url, "tmp_image.jpg")

	uploadFile("tmp_image.jpg", BUCKET_NAME)

	client = boto3.client('rekognition')
	response = client.detect_labels(
    Image = {
        'S3Object': {
            'Bucket': BUCKET_NAME,
            'Name': 'tmp_image.jpg',
        },
    },
    MaxLabels = 5,
    MinConfidence = 0.5
	)
	deleteFile(BUCKET_NAME, "tmp_image.jpg")
	os.remove("tmp_image.jpg")
	response = parseImageResponse(response)
	return response

def rank(restaurants):

	for r in restaurants:
		pos = neg = neu = mix = 0
		weight_list = []
		#print("Comments for restaurant " + r.pk)

		for m in r.medias:
			now = datetime.datetime.now()
			post_taken_at = datetime.datetime(m.TakenAtTime[0], m.TakenAtTime[1], m.TakenAtTime[2], m.TakenAtTime[3], m.TakenAtTime[4], m.TakenAtTime[5])
			age = (now - post_taken_at).days
			#print(age)

			if age <= 30:
				weight = 1
			elif age <= 90:
				weight = 0.9
			elif age <= 180:
				weight = 0.7
			elif age <= 360:
				weight = 0.5
			elif age <= 720:
				weight = 0.2
			else:
				weight = 0

			if m.CaptionText != "":
				#print(m.CaptionText)
				score = analyzeText(m.CaptionText)
				pos += score["Positive"] * weight
				neg += score["Negative"] * weight
				#neu += score["Neutral"] * weight
				#mix += score["Mixed"] * weight
				weight_list.append(weight)

		if sum(weight_list) == 0:
			pos = neg = 0
		else:
			pos /= sum(weight_list)
			neg /= sum(weight_list)
			#neu /= sum(weight_list)
			#mix /= sum(weight_list)

		ranking = pos-neg
		ranking = linearRanking(ranking)
		#ranking = sigmoidRanking(ranking)
		ranking = round(ranking, 1)

		r.ranking = ranking

	return dict

def linearRanking(x):
	x = 5*x + 5
	return x

def sigmoidRanking(x):
	x = 1 / (1 + exp(-5*x))
	x = 10*x
	return x

def main():
	test = []
	test.append(analyzeText("Molto bello!"))
	test.append(analyzeText("Brutto"))

	restaurants = json2Restaurants((str(sys.path[0]))+"/../IGCrawlerService/crawler/data/locationsData.json")
	for r in restaurants:
		r.assignValues()

	rank(restaurants)
	for r in restaurants:
		print(r.pk)
		print(r.name)
		r.printFormattedRanking()
		print('\n')

	detectLabels("https://instagram.ffco2-1.fna.fbcdn.net/v/t51.2885-15/11249882_966261376755731_963030927_n.jpg?se=8&stp=dst-jpg_e35&_nc_ht=instagram.ffco2-1.fna.fbcdn.net&_nc_cat=111&_nc_ohc=9lNYboVO5K0AX90TSMu&edm=AKmAybEBAAAA&ccb=7-5&ig_cache_key=MTIyOTEzNTQ0NTAwMDU1ODY0Mg%3D%3D.2-ccb7-5&oh=00_AT-H5SGET-X6zx_j-GGayPMijixUZwQOB6Ssy4c_gdtQSQ&oe=62BFFD3D&_nc_sid=bcb96")

if __name__ == "__main__":
	main()
