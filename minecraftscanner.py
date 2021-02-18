#!/usr/bin/python3

from subprocess import Popen, PIPE
import sys
from mcstatus import MinecraftServer

def main(argv):
    ip = []
    version = []
    if "-version" in argv:
        version = [argv[x+1] for x in range(len(argv)) if argv[x] == "-version" or argv[x] == "-v"]
    ip += [argv[x] for x in range(len(argv)) if argv[x] != "-version" or argv[x] != "-v" or argv[x-1] != "-version" or argv[x-1] != "-v"]

    for i in ip:
        proc = Popen(["nmap", "-sT", "-Pn", f"{i}", "-p-"], stdout=PIPE)
        (out, err) = proc.communicate()
        print(len(out)*"\b")
        outs = []
        for j in out.split("\n"):
            try:
                port = int(j[:5])
                server = MinecraftServer.lookup(f"{i}:{port}")
                outs += {"ipfull":f"{i}:{port}", "version":server.status().version.name}
            except ValueError:
                pass
    if ip != []:
        for i in outs:
            if i["version"] in version or version == []:
                print(i["ipfull"], i["version"])



if __name__ == "__main__":
    main(sys.argv[1:])
