import os
import numpy as np
from PIL import Image

path = r"E:\data5\val"

def class_convert(path):
    for path_name, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith("txt"):
                with open(path_name + "/" +filename, "r") as f:
                    datalist = f.readlines()

                with open(path_name + "/" +filename, "w") as f:
                    for data in datalist:
                        position = data.split()
                        if position[0] == "0":
                            position[0] = "0"
                        elif position[0] == "1":
                            position[0] = "0"
                        else:
                            print("[err] " + filename + "<< this file is not 0 or 1: " + position[0])
                        ns = f"{position[0]} {position[1]} {position[2]} {position[3]} {position[4]}\n"
                        print("[log] " + filename + " >> " + ns)
                        f.write(ns)

def file_check(path):
    for path_name, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith("txt"):
                with open(path_name + "/" + filename, "r") as f:
                    datalist = f.readlines()
                    for data in datalist:
                        position = data.split()
                        if position[0] == "2":
                            print("[msg] warning! this file has 'class2' >> " + filename)

def class2_to_0(path):
    for path_name, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith("txt"):
                with open(path_name + "/" + filename, "r") as f:
                    datalist = f.readlines()

                with open(path_name + "/" + filename, "w") as f:
                    for data in datalist:
                        position = data.split()
                        if position[0] == "2":
                            position[0] = "1"
                        ns = f"{position[0]} {position[1]} {position[2]} {position[3]} {position[4]}\n"
                        print("[log] " + filename + " >> " + ns)
                        f.write(ns)

def file_rename(path):
    for path_name, dirnames, filenames in os.walk(path):
        for filename in filenames:
            os.rename(path_name + "/" +filename, path_name + "/2_" +filename)

if __name__ == "__main__":
    class_convert(path)
    #file_rename(path)
    #file_check(path)
    #class2_to_0(path)