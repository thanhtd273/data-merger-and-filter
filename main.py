import json
import argparse

from utils import Util
from supplier import Acme, Patagonia, Paperflies
from service.hotel import HotelService


def fetch_hotels(hotel_ids: list[str], destination_ids: list[str]):
    suppliers = [Acme(), Patagonia(), Paperflies()]

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
    print(json_data)


if __name__ == "__main__":
    main()
