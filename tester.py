import itertools
import subprocess
from itertools import product


def run_test_from_file(os, device, name, yaml_conf, defaults):
    params = {param: value for (param, value) in defaults.items()}
    params.update(yaml_conf)

    def populate_args(arg, parent_file): return arg+str(parent_file.get(arg[2:-1])) if arg[2:-1] in parent_file \
        else arg

    arguments = ["--filename " + device, "--size ", "--thread ", "--direct ", "--rw ", "--refill_buffers ", "--norandommap",
                 "--randrepeat ", "--ioengine ", "--bs ", "--rwmixread ", "--iodepth ", "--numjobs ", "--time_based ",
                 "--runtime ", "--group_reporting ", "--name "]
    eqdepths = []
    arguments = [populate_args(arg, params) for arg in arguments]

    for eqdepth in product(params.get("qdepths"), params.get("threads")):
        False if eqdepth[0] * eqdepth[1] in eqdepths else eqdepths.append(eqdepth[0] * eqdepth[1])

    for coordinate in product(eqdepths, params.get("blocksizes"), params.get("threads"), params.get("qdepths"),
                              params.get("readpcts")):
        if coordinate[2]*coordinate[3] == coordinate[0]:
            arguments[9] += str(coordinate[1])
            arguments[10] += str(coordinate[4])
            arguments[11] += str(coordinate[3])
            arguments[12] += str(coordinate[2])
            arguments[len(arguments)-1] += str(coordinate[1])+"-"+str(coordinate[2])+"-"+str(coordinate[3])+"-"+\
                                          str(coordinate[4])

            print("Running this command" + str(arguments))
            if os == "Windows":
                output = subprocess.run(["powershell.exe", "fio", "--output-format=json"] + arguments, capture_output=
                True)
            else:
                output = subprocess.run(["fio", "--output-format=json"], capture_output=True)

    print(output)