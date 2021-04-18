# FIO Automated Testing - Daniel Zhou
import yaml
import argparse
import os
import time
from dotenv import load_dotenv
load_dotenv()
#If you use -f argument, loads configuration from file, otherwise uses defaults
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="configuration file FIOTester should use")
parser.add_argument("-d", "--device", help="device name FIOTester should write to")
parser.add_argument("-n", "--test_name", help="names the test")
args = parser.parse_args()
if args.filename:
    try:
        with open(args.filename) as file:
            try:
                print(yaml.safe_load(file))

            except yaml.YAMLError as exc:
                print(exc)
    except FileNotFoundError:
        print("Error: System cannot find file specified")
elif args.device and args.test_name:
    f = open(os.getenv("kernel_version") + args.test_name + time.strftime("%H%M%S") + "-fio.csv", "w+")
    print("test")