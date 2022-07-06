import os, sys
import urllib.request
import logging
import boto3
from botocore.exceptions import ClientError
from S3Connection import S3Connection

# S3 bucket name
BUCKET_NAME = "foxybyteswe"

class RekognitionClient:

	def __init__(self):
		pass

	def detectLabels(self, url):
		urllib.request.urlretrieve(url, "tmp_image.jpg")

		s3 = S3Connection(BUCKET_NAME)
		s3.uploadFile("tmp_image.jpg")

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

		s3.deleteFile("tmp_image.jpg")
		os.remove("tmp_image.jpg")
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

		print(list)

		return list

	def detectFacesEmotions(self, url):
		urllib.request.urlretrieve(url, "tmp_image.jpg")

		s3 = S3Connection(BUCKET_NAME)
		s3.uploadFile("tmp_image.jpg")

		client = boto3.client('rekognition')
		response = client.detect_faces(
		Image = {
			'S3Object': {
				'Bucket': BUCKET_NAME,
				'Name': 'tmp_image.jpg',
			}
		},
		Attributes=[
			'ALL',
		]
		)

		s3.deleteFile("tmp_image.jpg")
		os.remove("tmp_image.jpg")
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

		print(list)

		return list

def main():

	rkn = RekognitionClient()

	#rkn.detectLabels("https://instagram.ffco2-1.fna.fbcdn.net/v/t51.2885-15/11249882_966261376755731_963030927_n.jpg?se=8&stp=dst-jpg_e35&_nc_ht=instagram.ffco2-1.fna.fbcdn.net&_nc_cat=111&_nc_ohc=9lNYboVO5K0AX90TSMu&edm=AKmAybEBAAAA&ccb=7-5&ig_cache_key=MTIyOTEzNTQ0NTAwMDU1ODY0Mg%3D%3D.2-ccb7-5&oh=00_AT-H5SGET-X6zx_j-GGayPMijixUZwQOB6Ssy4c_gdtQSQ&oe=62BFFD3D&_nc_sid=bcb96")
	#rkn.detectFacesEmotions("https://instagram.ffco2-1.fna.fbcdn.net/v/t51.2885-15/11249882_966261376755731_963030927_n.jpg?se=8&stp=dst-jpg_e35&_nc_ht=instagram.ffco2-1.fna.fbcdn.net&_nc_cat=111&_nc_ohc=9lNYboVO5K0AX90TSMu&edm=AKmAybEBAAAA&ccb=7-5&ig_cache_key=MTIyOTEzNTQ0NTAwMDU1ODY0Mg%3D%3D.2-ccb7-5&oh=00_AT-H5SGET-X6zx_j-GGayPMijixUZwQOB6Ssy4c_gdtQSQ&oe=62BFFD3D&_nc_sid=bcb96")
	rkn.detectLabels("https://thumbs.dreamstime.com/z/happy-little-boy-smiley-face-portrait-human-concept-freshness-133726078.jpg")
	rkn.detectFacesEmotions("https://thumbs.dreamstime.com/z/happy-little-boy-smiley-face-portrait-human-concept-freshness-133726078.jpg")

if __name__ == "__main__":
	main()
