import json
import datetime
#from geopy.geocoders import Nominatim
from math import exp
import time

from Media import Media
from ComprehendClient import ComprehendClient
from RekognitionClient import RekognitionClient

class Restaurant:

	def __init__(self, pk = 0, medias = [], name = "", category = "", address = "", website = "", phone = "", main_image_url = "", coordinates = "", ranking = -1, comments = []):
		self.pk = pk
		self.medias = medias
		self.name = name
		self.category = category
		self.address = address
		self.website = website
		self.phone = phone
		self.main_image_url = main_image_url
		self.coordinates = coordinates
		self.ranking = ranking
		self.comments = comments

	def assignValues(self):
		for m in self.medias:
			if self.name == "" and m.TakenAtLocation["name"] != "":
				self.name = m.TakenAtLocation["name"]
			if self.category == "" and m.TakenAtLocation["category"] != "":
				self.category = m.TakenAtLocation["category"]
			#if self.address == "" and m.TakenAtLocation["address"] != "":
				#self.address = m.TakenAtLocation["address"]
			if self.website == "" and m.TakenAtLocation["website"] != "":
				self.website = m.TakenAtLocation["website"]
			if self.phone == "" and m.TakenAtLocation["phone"] != "":
				self.phone = m.TakenAtLocation["phone"]
			if self.coordinates == "" and m.TakenAtLocation["coordinates"] != "":
				self.coordinates = m.TakenAtLocation["coordinates"]
		#geolocator = Nominatim(user_agent="geoapiExercises")
		#self.address = geolocator.reverse(str(self.coordinates[1]) + "," + str(self.coordinates[0]))
		self.topComments()
		#self.main_image_url = self.getMainImageUrl()

	def returnFormattedRanking(self):
		return '{0:.1f}'.format(self.ranking)

	def printFormattedRanking(self):
		print('{0:.1f}'.format(self.ranking))

	def isOld(self, m):
		now = datetime.datetime.now()
		post_taken_at = datetime.datetime(m.TakenAtTime[0], m.TakenAtTime[1], m.TakenAtTime[2], m.TakenAtTime[3], m.TakenAtTime[4], m.TakenAtTime[5])
		age = (now - post_taken_at).days
		if age > 1800:
			return True
		else:
			return False
	
	def removeOldMedias(self):
		self.medias = [m for m in self.medias if not self.isOld(m)]

	def rank(self):

		comprehend = ComprehendClient()
		rekognition = RekognitionClient()

		pos = neg = neu = mix = 0
		weight_list = []
		#print("Comments for restaurant " + r.pk)

		for m in self.medias:
			now = datetime.datetime.now()
			post_taken_at = datetime.datetime(m.TakenAtTime[0], m.TakenAtTime[1], m.TakenAtTime[2], m.TakenAtTime[3], m.TakenAtTime[4], m.TakenAtTime[5])
			age = (now - post_taken_at).days
			#print(age)

			if age <= 90:
				weight = 1
			elif age <= 360:
				weight = 0.9
			elif age <= 720:
				weight = 0.7
			elif age <= 1080:
				weight = 0.5
			elif age <= 1800:
				weight = 0.2
			else:
				weight = 0

			if m.CaptionText != "":
				print(m.CaptionText)
				score = comprehend.analyzeText(m.CaptionText)
				print(score)
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
		ranking = self.linearRanking(ranking)
		#ranking = self.sigmoidRanking(ranking)
		ranking = round(ranking, 1)

		self.ranking = ranking

	def linearRanking(self, x):
		x = 5*x + 5
		return x

	def sigmoidRanking(self, x):
		x = 1 / (1 + exp(-5*x))
		x = 10*x
		return x

	def cubicRanking(self, x):
		x = 5 * x*x*x + 5
		return x

	def topComments(self):
		comprehend = ComprehendClient()
		list = []
		for m in self.medias:
			if len(m.CaptionText) > 0:
				score = comprehend.analyzeText(m.CaptionText)
				list.append([score["Positive"], score["Negative"], m.MediaURL, m.CaptionText])
		if len(list) > 0:
			list.sort(reverse = True, key = lambda x: x[0])
			if len(list[0][3]) > 1000:
				list[0][3] = list[0][3][:997] + "..."
			self.comments = [[list[0][2], list[0][3]]]
			list.sort(reverse = True, key = lambda x: x[1])
			if len(list[0][3]) > 1000:
				list[0][3] = list[0][3][:997] + "..."
			if list[0][2] != self.comments[0][0]:
				self.comments.append([list[0][2], list[0][3]])




#	def buildWebDriver(self):
#		chrome_options = webdriver.ChromeOptions()
#		chrome_options.add_experimental_option("useAutomationExtension", False)
#		chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#		driver = webdriver.Chrome(chromedriverDirectory, options=chrome_options)
#		return driver
#
#	def getMainLocationImageFromGMaps(self, locationName, driver):
#		driver.get("https://www.google.com/maps/search/?api=1&query="+locationName)
#		time.sleep(20)
#		try:
#			cover_img = driver.find_element(By.XPATH, "//img[@decoding='async']")
#		except Exception as e:
#			print(e)
#			return ""
#		src = cover_img.get_property("src")
#		return src
#
#	def getMainImageUrl(self):
#		driver = self.buildWebDriver()
#		source = self.getMainLocationImageFromGMaps(self.name + " " + str(self.address), driver)
#		return source





		
def json2Restaurants(input):

	data = json.loads(input)

	restaurant_list = []

	for restaurant in data:
		media_list = []

		for media in data[restaurant]:
			m = Media(media["PostPartialURL"], media["MediaType"], media["TakenAtTime"], media["TakenAtLocation"], media["LikeCount"], media["CaptionText"], media["MediaURL"])
			media_list.append(m)

		restaurant_list.append(Restaurant(restaurant, media_list))

	return restaurant_list

def Restaurants2json(restaurants):
	out = '{'
	for r in restaurants:
		out += '"' + r.pk + '": ['
		for m in r.medias:
			out += json.dumps(m.__dict__)
			out += ', '
		out = out[:-2]
		out += '], '

	out = out[:-2]
	out += '}'
	
    return out

def removeOldMedias(restaurants):
	for r in restaurants:
		r.removeOldMedias()
