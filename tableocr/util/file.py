import uuid


def get_uuid():
    return uuid.uuid4().hex


def get_csv_filename(dirPath):
    return dirPath + "/tableocr-csv-" + get_uuid() + ".csv"


def get_json_filename(dirPath):
    return dirPath + "/tableocr-json-" + get_uuid() + ".json"
