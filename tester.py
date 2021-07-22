import itertools
import subprocess
import processor as p
from itertools import product


def populate_args(arg, parent_file, head, tail):
    return arg + str(parent_file.get(arg[head:tail])) if arg[head:tail] in parent_file else arg


def run_test_from_file(os, device, name, yaml_conf, defaults):
    params = {param: value for (param, value) in defaults.items()}
    params.update(yaml_conf)
    arguments = ["--filename=" + device, "--size=", "--direct=", "--rw=", "--refill_buffers", "--norandommap",
                 "--randrepeat=", "--ioengine=", "--bs=", "--rwmixread=", "--iodepth=", "--numjobs=", "--time_based",
                 "--runtime=", "--group_reporting", "--name=", "--output="]
    eqdepths = []
    arguments = [populate_args(arg, params, 2, -1) for arg in arguments]
    for eqdepth in product(params.get("qdepths"), params.get("threads")):
        False if eqdepth[0] * eqdepth[1] in eqdepths else eqdepths.append(eqdepth[0] * eqdepth[1])

    for coordinate in product(eqdepths, params.get("blocksizes"), params.get("threads"), params.get("qdepths"),
                              params.get("readpcts")):
        if coordinate[2] * coordinate[3] == coordinate[0]:
            arguments[8] += str(coordinate[1])
            arguments[9] += str(coordinate[4])
            arguments[10] += str(coordinate[3])
            arguments[11] += str(coordinate[2])
            f_name = str(coordinate[2]) + "-" + str(coordinate[3]) + "-" + str(coordinate[4]) +\
                "-" + str(coordinate[1]) + ".json"
            arguments[len(arguments) - 1] += f_name
            arguments[len(arguments) - 2] += str(coordinate[2]) + "-" + str(coordinate[3]) + "-" + str(coordinate[4]) +\
                "-" + str(coordinate[1])
            print("Running this command" + str(arguments))
            if os == "Windows":
                f = open("error.txt", "w+")
                output = subprocess.Popen(["powershell.exe", "fio", "--output-format=json+", "--thread"] + arguments,
                                          cstdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #p.parse(f_name, name, params)
            else:
                f = open("error.txt", "w+")
                output = subprocess.Popen(["fio", "--output-format=json"] + arguments, stdout=subprocess.PIPE,
                                          stderr=f)
                #p.parse(f_name, name, params)