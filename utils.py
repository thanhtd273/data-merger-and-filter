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
    def extend_and_remove_duplicate(origin: list, data: list):
        origin.extend(data)
        return list(set(origin))