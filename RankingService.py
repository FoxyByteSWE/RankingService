import sys

from DBConnection import DBConnection

sys.path.insert(1, (str(sys.path[0]))+"/../IGCrawlerService/crawler/")

from Restaurant import Restaurant, json2Restaurants, removeOldMedias, rank

# S3 bucket name
BUCKET_NAME = "foxybyteswe"

def main():

	db = DBConnection()

	db.createServerConnection()
	db.createDatabase("Restaurants")

	db.createDatabaseConnection("Restaurants")
	db.insertRestaurants()

	db.uploadDB()
	db.downloadDB()

if __name__ == "__main__":
	main()
