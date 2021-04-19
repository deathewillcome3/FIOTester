import itertools
import subprocess
from itertools import product

def run_test_from_file(os, device, name, yaml_conf):
    qdepths = yaml_conf.get("qdepths", "Item not Found")
    threads = yaml_conf.get("threads", "Item not Found")
    blocksizes = yaml_conf.get("blocksizes", "Item not Found")
    readpcts = yaml_conf.get("readpcts", "Item not Found")
    ioengine = yaml_conf.get("ioengine", "Item Not Found")
    eqdepths = []

    for eqdepth in product(qdepths, threads):
        False if eqdepth[0]*eqdepth[1] in eqdepths else eqdepths.append(eqdepth[0]*eqdepth[1])

    for coordinate in product(eqdepths, blocksizes, threads, qdepths, readpcts):
        if coordinate[2]*coordinate[3] == coordinate[0]:
            command = []
            if(os == "Windows"):
                output = subprocess.run(["powershell.exe", "fio", "--help"] + command, capture_output=True)
            else:
                output = subprocess.run(["fio", "--help"], capture_output=True)

    print(output)
