from Location import Location

class LocationFactory:

	@staticmethod
	def buildFromDB(dbLocation: dict) -> Location:
		return Location(dbLocation["pk"],
						dbLocation["name"],
						dbLocation["category"],
						dbLocation["address"],
						dbLocation["website"],
						dbLocation["phone"],
						dbLocation["main_image_url"],
						dbLocation["coordinates"],
						dbLocation["latest_post_partial_url_checked"])
