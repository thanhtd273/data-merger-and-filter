import re
from base import Hotel


class Util:

    @staticmethod
    def split_ids(arg) -> list:
        if arg is None or arg == "" or arg == "none":
            return []
        return arg.split(",")

    @staticmethod
    def find_index(data: list[Hotel], id: str, destination_id: str) -> int:
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
    def merge_slist(origin: list[str], data: list[str]) -> list[str]:
        if origin is None or len(origin) == 0:
            return data
        if data is None or len(data) == 0:
            return origin

        l2 = len(data)
        for i in range(l2):
            flag = False
            for item in origin:
                if item in data[i]:
                    origin[origin.index(item)] = data[i]
                    flag = True
                    break
                elif data[i] in item:
                    flag = True
                    break
            if not flag and data[i] not in origin:
                origin.append(data[i])
        return origin

    @staticmethod
    def format_str(s: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', ' ', s).lower().strip()
