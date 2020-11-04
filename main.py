from prospecfun.functionsProspecAPI import *
import requests
from pathlib import Path
from getpass import getpass
import json


authenticateProspec("daniel.mazucanti@skoposenergia.com.br", "omIJjk37")

dc = getIdOfDECOMP(28)
nw = getIdOfNEWAVE(28)
gv = getIdOfGEVAZP(28)

with open("dc.json", 'w') as fp:
    fp.write(json.dumps(dc))

with open("nw.json", 'w') as fp:
    fp.write(json.dumps(nw))

with open("gv.json", 'w') as fp:
    fp.write(json.dumps(gv))
