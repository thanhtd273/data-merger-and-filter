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

            existed_item = result[index]
            if existed_item.name == None:
                existed_item.name = data[i].name

            if existed_item.description == None:
                existed_item.description = data[i].description

            if existed_item.location == None:
                existed_item.location = data[i].location
            else:
                location = data[i].location
                if existed_item.location.address == None:
                    existed_item.location.address = location.address
                elif existed_item.location.city == None:
                    existed_item.location.city = location.city
                elif existed_item.location.country == None:
                    existed_item.location.country = location.country
                elif existed_item.location.lat == None:
                    existed_item.location.lat = location.lat
                elif existed_item.location.lng == None:
                    existed_item.location.lng = location.lng
            
            if existed_item.amenities == None:
                existed_item.amenities = data[i].amenities
            elif data[i].amenities != None:
                general = data[i].amenities.general
                if general != None:
                    existed_item.amenities.general.extend(general)
                    existed_item.amenities.general = list(set(existed_item.amenities.general))
                room = data[i].amenities.room
                if room != None:
                    existed_item.amenities.room.extend(room)
                    existed_item.amenities.room = list(set(existed_item.amenities.room))
            
            if existed_item.images == None:
                existed_item.images = data[i].images
            elif data[i].images != None:
                existed_item.images.rooms = Util.extend_and_remove_duplicate(existed_item.images.rooms, data[i].images.rooms)
                existed_item.images.site = Util.extend_and_remove_duplicate(existed_item.images.site, data[i].images.site)
                existed_item.images.amenities = Util.extend_and_remove_duplicate(existed_item.images.amenities, data[i].images.amenities)

            
            if existed_item.booking_conditions == None or len(existed_item.booking_conditions) == 0:
                existed_item.booking_conditions = data[i].booking_conditions
            elif data[i].booking_conditions != None and len(data[i].booking_conditions) != 0:
                existed_item.booking_conditions = Util.extend_and_remove_duplicate(existed_item.booking_conditions, data[i].booking_conditions)

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