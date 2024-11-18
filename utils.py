import re
from base import Hotel

class Util:

    @staticmethod
    def split_ids(arg) -> list:
        if arg == None or arg == "" or arg == "none":
            return []
        return arg.split(",")

    @staticmethod
    def find_index(data: list[Hotel], id: str, destination_id: str) -> bool:
        length = len(data)
        for i in range(length):
            if data[i].id == id and data[i].destination_id == destination_id:
                return i
        return -1
    
    @staticmethod
    def merge_list(origin: list, data: list):
        origin.extend(data)
        return list(set(origin))
    
    @staticmethod
    def format_str(s: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', ' ', s).lower().strip()