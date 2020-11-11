from src.functionsProspecAPI import *
import requests
from pathlib import Path
import json


def getVersion(resp):
    version = []
    for item in resp:
        version.append(item["Version"])
    version.sort()
    return version


def mostRecentVersion(versions):
    lastItem = len(versions) - 1
    mostRecent = versions[lastItem]
    return mostRecent


def main():
    controlFlow = input("create, modify or upload: ")

    authenticateProspec("daniel.mazucanti@skoposenergia.com.br", "Skopos2020")

    if controlFlow == "create":
        listDecomp = getListOfDECOMPs()
        listNewave = getListOfNEWAVEs()
        listGevazp = getListOfGEVAZPs()

        print(listDecomp)

        versionNewave = getVersion(listNewave)
        versionDecomp = getVersion(listDecomp)
        versionGevazp = getVersion(listGevazp)

        print(versionDecomp)

        studyId = createStudy("Isso é um teste", "Continua sendo um teste",
                              mostRecentVersion(versionDecomp), mostRecentVersion(versionNewave))
        
        print(studyId)



main()