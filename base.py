from dataclasses import dataclass

@dataclass
class Location:
    lat: float
    lng: float
    address: str
    city: str
    country: str

    def __init__(self, lat: float = None, lng: float = None, address: str = None, city: str = None, country: str = None):
        self.lat = lat
        self.lng = lng
        self.address = address
        self.city = city
        self.country = country
    

@dataclass
class Amenities:
    general: list[str]
    room: list[str]

    def __init__(self, general: list[str] = [], room: list[str] = []):
        self.general = general
        self.room = room

@dataclass
class Link:
    link: str
    description: str

    def __init__(self, link: str, description: str):
        self.link = link
        self.description = description
    
    def __hash__(self):
        return hash((self.link, self.description))

@dataclass
class Images:
    rooms: list[Link]
    amenities: list[Link]
    site: list[Link]

    def __init__(self):
        self.rooms = []
        self.amenities = []
        self.site = []

@dataclass
class Hotel:
    id: str
    destination_id: str
    name: str
    description: str
    location: Location
    amenities: Amenities
    images: Images
    booking_conditions: list[str]

    def __init__(self, id: str, destination_id: str, name: str, description: str, location: Location, amenities: Amenities, images: Images, booking_conditions: list[str] = []):
        self.id = id
        self.destination_id = destination_id
        self.name = name
        self.description = description
        self.location = location
        self.amenities = amenities
        self.images = images
        self.booking_conditions = booking_conditions