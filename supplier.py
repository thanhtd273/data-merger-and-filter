import requests
from base import Hotel, Images, Amenities, Link, Location
from utils import Util

class BaseSupplier:
    
    def endpoint():
     """URL to fetch supplier data"""

    def parse(obj: dict) -> Hotel:
        """Parse supplier-provided data into Hotel object"""
    
    def fetch(self):
        url = self.endpoint()
        resp = requests.get(url)
        return [self.parse(dto) for dto in resp.json()]
    
class Acme(BaseSupplier):
    @staticmethod
    def endpoint():
        return "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme"
    
    @staticmethod
    def parse(dto: dict) -> Hotel:
        location = Location(lng=dto["Longitude"], 
                            lat=dto["Latitude"],
                            address=dto["Address"],
                            city=dto["City"],
                            country=dto["Country"]
                            )
        general = dto["Facilities"]
        if (general != None):
            general = list(map(lambda item: Util.format_str(item), general))

        return Hotel(id=dto["Id"], 
                     destination_id=dto["DestinationId"],
                     name=dto["Name"],
                     location=location,
                     description=dto["Description"],
                     amenities=Amenities(general=general),
                     images=None,
                     booking_conditions=[]
                     )

class Patagonia(BaseSupplier):
    @staticmethod
    def endpoint():
        return "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia"
    
    @staticmethod
    def parse(dto: dict) -> Hotel:
        location = Location(lat=dto["lat"], lng=dto["lng"], address=dto["address"])
        room = dto["amenities"]
        if (room != None):
            room = list(map(lambda item: Util.format_str(item), room))

        images = Images()
        image_data = dto["images"]
        room_images = image_data["rooms"]
        if room_images != None and isinstance(room_images, list) :
            for room in room_images:
                link = Link(link=room["url"], description=room["description"])
                images.rooms.append(link)

        amenity_images = image_data["amenities"]
        if amenity_images != None and isinstance(amenity_images, list):
            for amenity_image in amenity_images:
                link = Link(link=amenity_image["url"], description=amenity_image["description"])
                images.amenities.append(link)
                
        return Hotel(id = dto["id"],
                    destination_id=dto["destination"],
                    name=dto["name"],
                    location=location,
                    description=dto["info"],
                    amenities=Amenities(room=room),
                    images=images
                    )

class Paperflies(BaseSupplier):
    @staticmethod
    def endpoint():
        return "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies"
    
    @staticmethod
    def parse(dto: dict) -> Hotel:
        location = Location(address=dto["location"]["address"], country=dto["location"]["country"])

        origin_amenities = dto["amenities"]
        if origin_amenities != None:
            amenities = Amenities()

            room = origin_amenities["room"]
            if room != None:
                room = list(map(lambda item: Util.format_str(item), room))
                amenities.room = room
            
            general = origin_amenities["general"]
            if general != None:
                general = list(map(lambda item: Util.format_str(item), general))
                amenities.general = general

        images = Images()
        image_data = dto["images"]
        room_images = image_data["rooms"]
        if room_images != None and isinstance(room_images, list) :
            for room_image in room_images:
                link = Link(link=room_image["link"], description=room_image["caption"])
                images.rooms.append(link)

        site_images = image_data["site"]
        if site_images != None and isinstance(site_images, list):
            for site_image in site_images:
                link = Link(link=site_image["link"], description=site_image["caption"])
                images.site.append(link)
        
        return Hotel(id = dto["hotel_id"],
                    destination_id=dto["destination_id"],
                    name=dto["hotel_name"],
                    location=location,
                    description=dto["details"],
                    amenities=amenities,
                    images=images,
                    booking_conditions=dto["booking_conditions"]
                    )