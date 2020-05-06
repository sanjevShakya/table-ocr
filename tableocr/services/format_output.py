
import os
import json
import csv
from tableocr.util.object import nested_list_to_json
from tableocr.util.file import get_csv_filename, get_json_filename

def nested_array_to_formated_file(nestedList, columns, fileFormat, filePath=''): 
    basedir = os.path.abspath(os.path.dirname(__file__))
    if fileFormat == 'json':
        if not filePath:
            filePath = os.path.join("output/json")
        jsonValue = nested_list_to_json(nestedList, columns)
        with open(get_json_filename(filePath), 'w') as outputFile:
              json.dump(jsonValue, outputFile, indent=2)
        return True
    elif(fileFormat == 'csv'):
        if(not filePath):
            filePath = os.path.join("output/csv")
        with open(get_csv_filename(filePath), 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(columns)
            for value in nestedList:
                csv_writer.writerow(value)
        return True
    else:
        return False
