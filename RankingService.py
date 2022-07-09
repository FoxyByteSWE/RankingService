import sys, os

from DBConnection import DBConnection

sys.path.insert(1, (str(sys.path[0]))+"/../IGCrawlerService/crawler/")

from Restaurant import Restaurant, json2Restaurants, removeOldMedias, rank

# S3 bucket name
BUCKET_NAME = "foxybyteswe"

def main():

	db = DBConnection()

	db.createServerConnection()
	db.createDatabase("michelinsocial")

	db.createDatabaseConnection("michelinsocial")
	db.insertRestaurants()

	db.uploadDB("michelinsocial")
	db.downloadDB("michelinsocial")

if __name__ == "__main__":
	main()
