import itertools
import subprocess
import os
from itertools import product


def populate_args(arg, parent_file, head, tail):
    return arg + str(parent_file.get(arg[head:tail])) if arg[head:tail] in parent_file else arg


def run_test_from_file(os, device, name, yaml_conf, defaults):
    # err = open("error.txt", "w+")
    # out = open("output.txt", "w+")
    params = {param: value for (param, value) in defaults.items()}
    params.update(yaml_conf)
    arguments = ["--filename=" + device, "--size=", "--rw=", "--refill_buffers", "--norandommap",
                 "--randrepeat=", "--ioengine=", "--bs=", "--rwmixread=", "--iodepth=", "--numjobs=", "--time_based",
                 "--runtime=", "--group_reporting", "--name=", "--output="]
    eqdepths = []
    arguments = [populate_args(arg, params, 2, -1) for arg in arguments]
    for eqdepth in product(params.get("qdepths"), params.get("threads")):
        False if eqdepth[0] * eqdepth[1] in eqdepths else eqdepths.append(eqdepth[0] * eqdepth[1])

    for coordinate in product(eqdepths, params.get("blocksizes"), params.get("threads"), params.get("qdepths"),
                              params.get("readpcts")):
        if coordinate[2] * coordinate[3] == coordinate[0]:
            arguments[7] += str(coordinate[1])
            arguments[8] += str(coordinate[4])
            arguments[9] += str(coordinate[3])
            arguments[10] += str(coordinate[2])
            arguments[len(arguments) - 1] += str(coordinate[2]) + "-" + str(coordinate[3]) + "-" + str(coordinate[4]) +\
                "-" + str(coordinate[1]) + ".json"
            arguments[len(arguments) - 2] += str(coordinate[2]) + "-" + str(coordinate[3]) + "-" + str(coordinate[4]) +\
                "-" + str(coordinate[1])
            print("Running this command" + str(arguments))
            if os == "Windows":
                output = subprocess.Popen(["powershell.exe", "fio", "--output-format=json", "--thread", "--direct=0"] +
                                          arguments)
            else:
                output = subprocess.Popen(["fio", "--output-format=json", "--direct=1"] + arguments)
                #, stdout=out, stderr=err