from src.arrFiles import main as prep_files
from src.functionsProspecAPI import *


def main():
    authenticateProspec("daniel.mazucanti@skoposenergia.com.br", "Skopos2020")

    numRequests = getNumberOfRequests()

    print("Foram feitas %s requisições até o momento." % numRequests)

    prep_files()

    control_flow = input("<criar>, fazer <upload> de arquivos ou <rodar> estudo: ")

    if control_flow == "criar":
        choice = input("Qual o estudo que deseja?\n1- Curtísimo prazo\n")
        choice = int(choice)
        if choice == 1:
            idStudy = 0
            nameStudy = "Curtíssimo prazo"

            with open("estudos_criados", 'a') as fp:
                fp.write("ID: %d, Nome: %s\n" % (idStudy, nameStudy))

            print("O estudo %s foi criado com ID %d" % (nameStudy, idStudy))

    elif control_flow == "upload":
        print("Esses são os estudos criados até então:")
        with open("estudos criados", 'r') as fp:
            for line in fp:
                print(line)

        int(input("Qual o estudo que deseja enviar os arquivos?\n"))


    else:
        print("Programa encerrado.")


main()
