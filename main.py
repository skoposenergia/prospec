from src.functionsProspecAPI import *
import requests
from pathlib import Path
import json
from src.arrFiles import main as prep_files


def main():

    authenticateProspec("daniel.mazucanti@skoposenergia.com.br", "Skopos2020")

    numRequests = getNumberOfRequests()

    print("Foram feitas %s requisições até o momento." % numRequests)

    control_flow = input("create, modify or upload: ")

    if control_flow == "create":
        choice = input("Qual o estudo que deseja?\n1- Curtísimo prazo")
        choice = int(choice)
        if choice == 1:
            idStudy = 0
            # idStudy = createStudy(
            #     "Isso é um teste", "Continua sendo um teste", 0, 0)

            print("O estudo %s foi cirado com ID %d" % ("teste", idStudy))

    elif control_flow == "modify":

        idStudy = 271

        studies = getInfoFromStudy(0)
        print(studies)

    elif control_flow == "upload":
        prep_files()

    else:
        print("Programa encerrado.")


main()
