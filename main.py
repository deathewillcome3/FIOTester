# FIO Automated Testing - Daniel Zhou
import yaml
import argparse
import os
import time
import platform
import linux
import windows

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
        with open(args.filename) as file, yaml.safe_load(file) as yaml:
            if platform.system() == 'Linux':
                print(yaml)
                linux.run_test_from_file(yaml)
            elif platform.system() == 'Windows':
                print(yaml)
                windows.run_test_from_file(yaml)
    except FileNotFoundError:
        print("Error: System cannot find file specified")
    except yaml.YAMLError as exc:
        print(exc)
elif args.device and args.test_name
    if platform.system() == 'Linux':
        linux.run_test(args.device, args.test_name)

    elif platform.system() == 'Windows':
        windows.run_test(args.device, args.test_name)
