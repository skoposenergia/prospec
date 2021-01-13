from src import functionsProspecAPI as prospec
from src.arrFiles import main as prep_files
from pathlib import Path


def create_study(nameStudy):
    idStudy = prospec.createStudy(nameStudy, "", 0, 0)

    with open("estudos criados", 'a') as fp:
        fp.write("ID: %d, Nome: %s\n" % (idStudy, nameStudy))

    print("O estudo %s foi criado com ID %d" % (nameStudy, idStudy))


def display_studies():
    print("Esses são os estudos criados até então:")
    with open("estudos criados", 'r') as fp:
        for line in fp:
            print(line)


def get_paths(path_model):
    path_prevs = path_model + "/prevs/"
    path_gevazp = path_model + "/GEVAZP/"
    return path_prevs, path_gevazp


def model_params():
    nameStudy = ""
    path_of_opt = ""
    choice = input(
        "Qual o tipo de estudo que deseja?\n1- Curtísimo prazo\n2- ONS CP\n3- Matriz CP")
    choice = int(choice)
    if choice == 1:
        nameStudy = "Curtíssimo prazo"
        path_of_opt = "CP/Curtissimo"

    elif choice < 4:
        print("Opção em implementação.")

    else:
        print("Opção inválida.")

    return nameStudy, path_of_opt


def main():
    prospec.authenticateProspec(
        "daniel.mazucanti@skoposenergia.com.br", "Skopos2020")

    numRequests = prospec.getNumberOfRequests()

    print("Foram feitas %s requisições até o momento." % numRequests)

    idServer = prospec.getIdOfServer("c5.24xlarge")
    idQueue = prospec.getIdOfFirstQueueOfServer("c5.24xlarge")

    while True:
        control_flow = input('1- Criar estudo\n2- Upload de arquivos\n3- Rodar estudo\n4- Abortar execução\n5- '
                             'Informações do estudo\n0- Sair\n')
        if control_flow == "1":

            nameStudy, path_opt = model_params()

            create_study(nameStudy)

        elif control_flow == "2":

            nameStudy, path_model = model_params()
            path_prevs, path_gevazp = get_paths(path_model)

            display_studies()

            uploadId = int(
                input("Para qual estudo deseja enviar os arquivos?\n"))
            prep_files()
            prospec.sendPrevsToStudy(uploadId, path_prevs)
            for file in Path(path_gevazp).glob("**/*"):
                prospec.sendFileToDeck(uploadId, "", file, file.name)
            prospec.sendFileToDeck()

        elif control_flow == "3":
            name, path = model_params()

            display_studies()

            runId = int(input("Qual estudo deseja rodar?\n"))

            prospec.generateNextRev(
                runId, "", "", path + "Dados_Prospectivo.xlsx", "")

        elif control_flow == "4":
            display_studies()
            stopId = int(input("Qual estudo deseja parar?\n"))
            prospec.abortExecution(stopId)

        elif control_flow == "5":
            display_studies()
            infoId = input("Qual estudo deseja?\n")
            infoStudy = prospec.getInfoFromStudy(infoId)
            print(infoStudy)

        else:
            print("Programa encerrado.")
            break


main()
