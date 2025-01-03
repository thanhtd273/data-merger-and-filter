from supplier import BaseSupplier
from base import Hotel
from utils import Util


class HotelService:

    @staticmethod
    def get_data(suppliers: list[BaseSupplier]):
        result = []
        for supplier in suppliers:
            data = supplier.fetch()
            if data is not None:
                result.extend(data)
        return result

    @staticmethod
    def merge_data(data: list[Hotel]):
        result: list[Hotel] = []
        length = len(data)
        for i in range(length):
            hotel_id = data[i].id
            destination_id = data[i].destination_id
            index = Util.find_index(result, hotel_id, destination_id)
            if index == -1:
                result.append(data[i])
                continue

            existed = result[index]
            if data[i].name is not None:
                existed.name = data[i].name
            if data[i].description is not None:
                existed.description = data[i].description

            existed.location = HotelService.merge_location(
                existed.location, data[i].location)
            existed.amenities = HotelService.merge_amenities(
                existed.amenities, data[i].amenities)
            existed.images = HotelService.merge_images(existed.images,
                                                       data[i].images)
            existed.booking_conditions = HotelService.merge_booking_condition(
                existed.booking_conditions, data[i].booking_conditions)

        return result

    @staticmethod
    def filter(data: list[Hotel], hotel_ids: list[str],
               destination_ids: list[str]) -> list[Hotel]:
        result = []
        for info in data:
            if info.id in hotel_ids and str(
                    info.destination_id) in destination_ids:
                result.append(info)

        return result

    @staticmethod
    def merge_location(origin, data):
        if origin is None:
            return data
        else:
            if data.address is not None:
                origin.address = data.address
            if data.city is not None:
                origin.city = data.city
            if data.country is not None:
                origin.country = data.country
            if data.lat is not None:
                origin.lat = data.lat
            if data.lng is not None:
                origin.lng = data.lng
        return origin

    @staticmethod
    def merge_amenities(origin, data):
        if origin is None:
            return data
        elif data is not None:
            general = data.general
            if general is not None:
                origin.general = Util.merge_str_list(origin.general, general)

            room = data.room
            if room is not None:
                origin.room = Util.merge_str_list(origin.room, room)
        return origin

    @staticmethod
    def merge_images(origin, data):
        if origin is None:
            return data
        elif data is not None:
            origin.rooms = Util.merge_list(origin.rooms, data.rooms)
            origin.site = Util.merge_list(origin.site, data.site)
            origin.amenities = Util.merge_list(origin.amenities,
                                               data.amenities)
        return origin

    @staticmethod
    def merge_booking_condition(origin, data):
        if origin is None or len(origin) == 0:
            return data
        elif data is not None and len(data) != 0:
            origin = Util.merge_list(origin, data)
        return origin
