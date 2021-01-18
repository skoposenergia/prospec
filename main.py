import datetime as dt
from pathlib import Path
import calendar
import numpy as np
from src import functionsProspecAPI as prospec
from src.arrFiles import main as prep_files


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
            prospec.runExecution(studyId, idServer, idQueue, '', '0', '0', '2')

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

    studyId = int(
        input("Para qual estudo deseja enviar os arquivos?\n"))

    prep_files()

    send_decks(path, studyId)

    if name == "Curtíssimo prazo":

        todayDate, multipleRevision, targetDates = treat_dates()

        initialYear = todayDate.year
        initialMonth = todayDate.month
        duration = str(todayDate.month - targetDates[1].month)
        month = [targetDates[0].month, targetDates[1].month]
        year = [targetDates[0].year, targetDates[1].year]
        dateToFormat = (initialYear, initialMonth)
        newaveFile = "NW%d%d" % dateToFormat
        decompFile = "DC%d%d" % dateToFormat
        configFile = "Dados_Prospectivo.xlsx"

    prospec.sendFileToStudy(studyId, path+'/'+configFile, configFile)

    prospec.generateStudyDecks(
        studyId, [initialYear], [initialMonth], [duration], month, year, [False, False], [True, True], newaveFile, "", decompFile, configFile, [])

    path_prevs = path + "/prevs/"

    prospec.sendPrevsToStudy(studyId, path_prevs)

    send_gevazp(path, studyId)


def treat_dates():
    targetDates = []
    multipleRevision = []
    todayDate = dt.date.today()
    firstRevDate = todayDate + dt.timedelta(weeks=1)
    secondRevDate = firstRevDate + dt.timedelta(weeks=1)
    daysDelta = 5 - int(firstRevDate.isoweekday())
    targetDates.append(firstRevDate - dt.timedelta(days=daysDelta))
    targetDates.append(secondRevDate - dt.timedelta(days=daysDelta))
    for target in targetDates:
        rev = get_rev(target)
        multipleRevision.append(rev)
    return todayDate, multipleRevision, targetDates


def get_rev(date_value):
    day = date_value.day
    month = date_value.month
    year = date_value.year
    x = np.array(calendar.monthcalendar(year, month))
    revision = np.where(x==day)[0][0]
    return(revision)


def send_decks(path, uploadId):
    path_decks = path + "/Decks/"
    for file in Path(path_decks).glob("**/*"):
        if file.suffix == ".zip":
            prospec.sendFileToStudy(uploadId, file, file.name)


def send_gevazp(path, uploadId):
    path_gevazp = path + "/GEVAZP/"
    for file in Path(path_gevazp).glob("**/*"):
        if file.is_file():
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
        
        print("Opção em implementação.")

    else:
        print("Opção inválida.")

    return nameStudy, path


main()
