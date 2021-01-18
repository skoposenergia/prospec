from src import functionsProspecAPI as prospec
from src.arrFiles import main as prep_files
from pathlib import Path
import datetime as dt


def main():
    prospec.authenticateProspec(
        "daniel.mazucanti@skoposenergia.com.br", "Skopos2020")

    numRequests = prospec.getNumberOfRequests()

    print("Foram feitas %s requisições até o momento." % numRequests)

    idServer = prospec.getIdOfServer("c5.24xlarge")
    idQueue = prospec.getIdOfFirstQueueOfServer("c5.24xlarge")

    while True:
        control_flow = input(
            '1- Criar estudo\n2- Rodar estudo\n3- Abortar execução\n4- Informações do estudo\n0- Sair\n')
        if control_flow == "1":

            nameStudy, path_opt = model_params()

            create_study(nameStudy)

        elif control_flow == "2":

            prep_run()

        elif control_flow == "3":
            display_studies()
            stopId = int(input("Qual estudo deseja parar?\n"))
            prospec.abortExecution(stopId)

        elif control_flow == "4":
            studiesInfo()

        else:
            print("Programa encerrado.")
            break


def prep_run():
    name, path = model_params()

    display_studies()

    uploadId = int(
        input("Para qual estudo deseja enviar os arquivos?\n"))

    prep_files()

    send_decks(uploadId)

    if name == "Curtíssimo prazo":
        dateStudy = dt.date.today()
        initialYear = dateStudy.year
        initialMonth = dateStudy.month

    prospec.generateStudyDecks(
        # uploadId, initialYear, initialMonth, 0, initialMonth, initialYear, False, True, )
        # TODO #1 parametros das funções de gerar decks, antes de enviar os arquivos

    path_prevs = path_model + "/prevs/"

    prospec.sendPrevsToStudy(uploadId, path_prevs)

    runId = int(input("Qual estudo deseja rodar?\n"))


def send_decks(uploadId):
    path_decks = path_model + "/Decks/"
    for file in Path(path_decks).glob("**/*"):
        if file.suffix == ".zip":
            prospec.sendFileToStudy(uploadId, file, file.name)


def send_gevazp(path_model, uploadId):
    path_gevazp = path_model + "/GEVAZP/"
    for file in Path(path_gevazp).glob("**/*"):
        prospec.sendFileToDeck(uploadId, "", file, file.name)


def studiesInfo():
    display_studies()
    infoId = input("Qual estudo deseja?\n")
    infoStudy = prospec.getInfoFromStudy(infoId)
    if infoStudy == None:
        print("Esse estudo não está mais na plataforma!")
    else:
        print(infoStudy)


def create_study(nameStudy):
    idStudy = prospec.createStudy(nameStudy, "", 0, 0)

    with open("estudos criados", 'a') as fp:
        fp.write("ID: %s, Nome: %s\n" % (idStudy, nameStudy))

    print("O estudo %s foi criado com ID %s" % (nameStudy, idStudy))


def display_studies():
    print("Esses são os estudos criados até então:")
    with open("estudos criados", 'r') as fp:
        for line in fp:
            print(line)


def model_params():
    nameStudy = ""
    path = ""
    choice = input(
        "Qual o tipo de estudo que deseja?\n1- Curtísimo prazo\n2- ONS CP\n3- Matriz CP\n")
    choice = int(choice)
    if choice == 1:
        nameStudy = "Curtíssimo prazo"
        path = "CP/Curtissimo"

    elif choice < 4:
        #TODO #4 Tratamento de caso para CP ONS
        #TODO #5 Tratamento de caso para CP Matriz
        #TODO #2 Tratamento de caso para MP Matriz
        print("Opção em implementação.")

    else:
        print("Opção inválida.")

    return nameStudy, path


main()
