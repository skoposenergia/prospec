from src.arrFiles import main as prep_files
from src.functionsProspecAPI import *


def main():
    authenticateProspec("daniel.mazucanti@skoposenergia.com.br", "Skopos2020")

    numRequests = getNumberOfRequests()

    print("Foram feitas %s requisições até o momento." % numRequests)

    prep_files()

    control_flow = input("create, modify or upload: ")

    if control_flow == "create":
        choice = input("Qual o estudo que deseja?\n1- Curtísimo prazo\n")
        choice = int(choice)
        if choice == 1:
            idStudy = 0
            nameStudy = "Curtíssimo prazo"
            # idStudy = createStudy(
            #     "Curtíssimo prazo", "", 0, 0)
            with open("estudos_criados", 'a') as fp:
                fp.write("ID: %d, Nome: %s\n" % (idStudy, nameStudy))

            print("O estudo %s foi criado com ID %d" % (nameStudy, idStudy))

    elif control_flow == "modify":

        idStudy = 271

        studies = getInfoFromStudy(0)
        print(studies)

    else:
        print("Programa encerrado.")


main()
