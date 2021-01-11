from src import functionsProspecAPI as prospec
from src.arrFiles import main as prep_files


def create_study(nameStudy):
    idStudy = prospec.createStudy(nameStudy, "", 0, 0)

    with open("estudos criados", 'a') as fp:
        fp.write("ID: %d, Nome: %s\n" % (idStudy, nameStudy))

    print("O estudo %s foi criado com ID %d" % (nameStudy, idStudy))


def upload_files(idStudy, path):
    prospec.sendAllPrevsToStudy(idStudy, path)


def display_studies():
    print("Esses são os estudos criados até então:")
    with open("estudos criados", 'r') as fp:
        for line in fp:
            print(line)


def model_params():
    nameStudy = ""
    path_of_opt = ""
    choice = input("Qual o tipo de estudo que deseja?\n1- Curtísimo prazo\n2- ONS CP\n3- Matriz CP")
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
    prospec.authenticateProspec("daniel.mazucanti@skoposenergia.com.br", "Skopos2020")

    numRequests = prospec.getNumberOfRequests()

    print("Foram feitas %s requisições até o momento." % numRequests)

    control_flow = input("<criar>, fazer <upload> de arquivos, <parar> ou <rodar> estudo: ")
    if control_flow == "criar":

        nameStudy, path_opt = model_params()

        create_study(nameStudy)

    elif control_flow == "upload":

        nameStudy, path_model = model_params()
        path_prevs = path_model + "/prevs/"
        display_studies()

        uploadId = int(input("Para qual estudo deseja enviar os arquivos?\n"))
        prep_files()
        upload_files(uploadId, path_prevs)

    elif control_flow == "rodar":
        name, path = model_params()

        display_studies()

        runId = int(input("Qual estudo deseja rodar?\n"))

        prospec.generateNextRev(runId, "", "", path + "Dados_Prospectivo.xlsx")



    elif control_flow == "parar":
        display_studies()
        stopId = int(input("Qual estudo deseja parar?\n"))
        prospec.abortExecution(stopId)

    else:
        print("Programa encerrado.")


main()
