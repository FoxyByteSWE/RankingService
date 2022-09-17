import json
import logging
import boto3

# S3 bucket name
BUCKET_NAME = "foxybyteswe"

class RekognitionClient:

	def __init__(self):
		pass

	def detectLabels(self):
		client = boto3.client('rekognition')
		response = client.detect_labels(
		Image = {
			'S3Object': {
			'Bucket': BUCKET_NAME,
				'Name': 'images/tmp_image.jpg',
			},
		},
		MaxLabels = 5,
		MinConfidence = 0.5
		)

		#s3.deleteFile("tmp_image.jpg")
		response = self.parseImageResponse(response)

		return response

	def parseImageResponse(self, response):
		list = []

		for item in response["Labels"]:
			dict = {}
			dict["Name"] = item["Name"]
			dict["Confidence"] = item["Confidence"]
			dict["Parents"] = item["Parents"]
			list.append(dict)

		return list

	def detectFacesEmotions(self):
		client = boto3.client('rekognition')
		response = client.detect_faces(
		Image = {
			'S3Object': {
				'Bucket': BUCKET_NAME,
				'Name': 'images/tmp_image.jpg',
			}
		},
		Attributes=[
			'ALL',
		]
		)

		#s3.deleteFile("tmp_image.jpg")
		response = self.parseEmotions(response)

		return response

	def parseEmotions(self, response):
		list = []

		for item in response["FaceDetails"]:
			dict = {}
			emotions_list = []
			dict["SmileConfidence"] = item["Smile"]["Confidence"]
			dict["Smile"] = item["Smile"]["Value"]
			for em in item["Emotions"]:
				emotions_dict = {}
				emotions_dict["EmotionConfidence"] = em["Confidence"]
				emotions_dict["Emotion"] = em["Type"]
				emotions_list.append(emotions_dict)
				dict["Emotions"] = emotions_list

			list.append(dict)

		return list

def lambda_handler(event, context):
	
	rkn = RekognitionClient()
	ret = rkn.detectLabels()

	return {
		'statusCode': 200,
		#'body': json.dumps(ret)
		'body': ret
	}
