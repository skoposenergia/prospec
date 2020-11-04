from prospecfun.functionsProspecAPI import *
import requests
from pathlib import Path
from getpass import getpass


token = authenticateProspec("daniel.mazucanti@skoposenergia.com.br", "omIJjk37")

dc = getListOfDECOMPs()
print(dc)