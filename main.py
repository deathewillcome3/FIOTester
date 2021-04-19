# FIO Automated Testing - Daniel Zhou
import yaml
import argparse
import os
import time
import platform
import tester

from dotenv import load_dotenv
load_dotenv()
#If you use -f argument, loads configuration from file, otherwise uses defaults
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="configuration file FIOTester should use")
parser.add_argument("-d", "--device", help="device name FIOTester should write to")
parser.add_argument("-n", "--test_name", help="names the test")
args = parser.parse_args()
if args.filename and args.device and args.test_name:
    with open(args.filename) as file:
        config = yaml.safe_load(file)
        tester.run_test_from_file(platform.system(), args.device, args.test_name, config)
elif args.device and args.test_name:
    defaults = yaml.safe_load("defaults.yml")
    tester.run_test_from_file(platform.system(), args.device, args.test_name, args.filename)

else:
    print(" Please select a device name using the -d flag and a test name using the -n flag")

