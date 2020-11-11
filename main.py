from prospecfun.functionsProspecAPI import *
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


authenticateProspec("daniel.mazucanti@skoposenergia.com.br", "Skopos2020")

listDecomp = getListOfDECOMPs()
listNewave = getListOfNEWAVEs()
listGevazp = getListOfGEVAZPs()


versionNewave = getVersion(listNewave)
versionDecomp = getVersion(listDecomp)
versionGevazp = getVersion(listGevazp)



studyID = createStudy("Isso é um teste", "Continua sendo um teste",
                      mostRecentVersion(versionDecomp), mostRecentVersion(versionNewave))
