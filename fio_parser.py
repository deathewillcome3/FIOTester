import json
import argparse
import os
import time
import platform
import csv

def parse(path):
    cwd = os.getcwd()
    params = {filename: yaml_parse(filename) for filename in os.listdir(cwd+"\\main_run_test")}
    try:
        os.listdir("graphs")
        os.chdir("graphs")
    except FileNotFoundError:
        os.mkdir("graphs")
        # os.chdir("graphs")
    try:
        f = open("results.csv", "x")
    except FileExistsError:
        print("File Exists")
    with open("results.csv") as results:
        csv_writer = csv.writer(results, delimiter=',')
        print(get_metrics("read", "iops", params))

    os.chdir(cwd)


def yaml_parse(filename):
    with open(filename) as output:
        return json.load(output)


def get_metrics(iotype, metric, data):
    all_data = data.get('2-2-30-16.json')
    return all_data.get("jobs")[0].get(iotype).get(metric)

parse("Hello")


