import json
import argparse

from base import Hotel
from utils import Util
from supplier import BaseSupplier, Acme, Patagonia, Paperflies

class HotelService:
    @staticmethod
    def get_data(suppliers: list[BaseSupplier]):
        result = []
        for supplier in suppliers:
            result.extend(supplier.fetch())
        return result
    
    @staticmethod
    def merge_data(data: list[Hotel]):
        result: list[Hotel] = []
        length = len(data)
        for i in range(length):
            id = data[i].id
            destination_id = data[i].destination_id
            index = Util.find_index(result, id, destination_id)
            if index == -1:
                result.append(data[i])
                continue

            existed = result[index]
            if data[i].name is not None:
                existed.name = data[i].name

            if data[i].description is not None:
                existed.description = data[i].description

            if existed.location is None:
                existed.location = data[i].location
            else:
                location = data[i].location
                if location.address is not None:
                    existed.location.address = location.address
                if location.city is not None:
                    existed.location.city = location.city
                if location.country is not None:
                    existed.location.country = location.country
                if location.lat is not None:
                    existed.location.lat = location.lat
                if location.lng is not None:
                    existed.location.lng = location.lng
            
            if existed.amenities is None:
                existed.amenities = data[i].amenities
            elif data[i].amenities is not None:
                general = data[i].amenities.general
                if general is not None:
                    existed.amenities.general = Util.merge_list(existed.amenities.general, general)

                room = data[i].amenities.room
                if room is not None:
                    existed.amenities.room = Util.merge_list(existed.amenities.room, room)
            
            if existed.images is None:
                existed.images = data[i].images
            elif data[i].images is not None:
                existed.images.rooms = Util.merge_list(existed.images.rooms, data[i].images.rooms)
                existed.images.site = Util.merge_list(existed.images.site, data[i].images.site)
                existed.images.amenities = Util.merge_list(existed.images.amenities, data[i].images.amenities)

            
            if existed.booking_conditions is None or len(existed.booking_conditions) == 0:
                existed.booking_conditions = data[i].booking_conditions
            elif data[i].booking_conditions is not None and len(data[i].booking_conditions) != 0:
                existed.booking_conditions = Util.merge_list(existed.booking_conditions, data[i].booking_conditions)

        return result

    @staticmethod
    def filter(data: list[Hotel], hotel_ids: list[str], destination_ids: list[str]) -> list[Hotel]:
        result = []
        for info in data:
            if info.id in hotel_ids and str(info.destination_id) in destination_ids:
                result.append(info)
        
        return result

def fetch_hotels(hotel_ids: list[str], destination_ids: list[str]):
    suppliers = [
        Acme(), 
        Patagonia(), 
        Paperflies()
    ]

    svc = HotelService()
    all_supplier_data = svc.get_data(suppliers)
    
    merged_data = svc.merge_data(all_supplier_data)

    if len(hotel_ids) == 0 or len(destination_ids) == 0:
        return merged_data
    
    filtered_data = svc.filter(merged_data, hotel_ids, destination_ids)
    
    return filtered_data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hotel_ids", type=str, help="Hotel IDs")
    parser.add_argument("destination_ids", type=str, help="Destination IDs")

    args = parser.parse_args()
    hotel_ids = Util.split_ids(args.hotel_ids)
    destination_ids = Util.split_ids(args.destination_ids)

    data = fetch_hotels(hotel_ids, destination_ids)
    json_data = json.dumps(data, default=lambda o: o.__dict__, indent=4)
    # with open("hotels.json", "w") as outfile:
    #     outfile.write(json_data)
    print(json_data) 

if __name__ == "__main__":
    main()