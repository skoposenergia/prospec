from src.functionsProspecAPI import *
import requests
from pathlib import Path
import json


# def getVersion(resp):
#     version = []
#     for item in resp:
#         version.append(item["Version"])
#     version.sort()
#     return version


# def mostRecentVersion(versions):
#     lastItem = len(versions) - 1
#     mostRecent = versions[lastItem]
#     return mostRecent


def main():

    authenticateProspec("daniel.mazucanti@skoposenergia.com.br", "Skopos2020")

    numRequests = getNumberOfRequests()

    print("Foram feitas %s requisições até o momento." % numRequests)

    controlFlow = input("create, modify or upload: ")

    if controlFlow == "create":

        idStudy = createStudy(
            "Isso é um teste", "Continua sendo um teste", 0, 0)

        print(idStudy)
        
    elif controlFlow == "modify":

        idStudy = 271

        studies = getInfoFromStudy(0)
        print(studies)

    else:
        print("Programa encerrado.")


main()
