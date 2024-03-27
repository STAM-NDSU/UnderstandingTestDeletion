usuage = """
USAGE: python3 tools/analyzer/results_json_to_csv.py 
"""

""" 
Converts analyzer files for individual projects in both strict and loose setting to csv
"""

import sys

sys.path.append("../")

import json
import csv
from FAST.config import PROJECTS, ARTIFACTS_DIR, SETTINGS


def flatten_json(nested_json):
    flattened_json = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        else:
            flattened_json[name[:-1]] = x

    flatten(nested_json)
    return flattened_json


def convert_json_to_csv(input_file, output_file, project, setting):
    # Opening JSON file and loading the data
    # into the variable data
    with open(input_file) as json_file:
        data = json.load(json_file)

    analyzer_detail_data = map(lambda x: flatten_json(x), data["details"])

    # now we will open a file for writing
    data_file = open(output_file, "w")

    # create the csv writer object
    csv_writer = csv.writer(data_file)

    # Counter variable used for writing
    # headers to the CSV file
    count = 0

    for each in analyzer_detail_data:
        if count == 0:
            # Writing headers of CSV file
            header = each.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(each.values())

    print("Converted to csv successfully for " + project + " in setting " + setting)
    data_file.close()


for setting in SETTINGS:
    for project in PROJECTS:
        input_file = ARTIFACTS_DIR + "/" + setting + "/" + project + ".json"
        output_file = ARTIFACTS_DIR + "/" + setting + "/" + project + ".csv"
        convert_json_to_csv(input_file, output_file, project, setting)
