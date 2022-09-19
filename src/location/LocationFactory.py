import sys

sys.path.insert(1, (str(sys.path[0]))+"/location/")

from Location import Location


class LocationFactory:

    @staticmethod
    def buildFromInstagrapi(instagrapiLocation: InstagrapiLocation, main_image_url, coordinates, latest_post_partial_url_checked) -> Location:
        return Location(instagrapiLocation.pk,
                        instagrapiLocation.name,
                        instagrapiLocation.category,
                        instagrapiLocation.address,
                        instagrapiLocation.website,
                        instagrapiLocation.phone,
                        main_image_url,
                        coordinates,
                        latest_post_partial_url_checked)


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
