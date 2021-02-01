import calendar
import datetime as dt
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile

import numpy as np

from src import functionsProspecAPI as prospec
from src.arrFiles import main as prep_files


def prep_n_run():
    name, path = model_params()

    idServer = prospec.getIdOfServer("c5.24xlarge")
    idQueue = prospec.getIdOfFirstQueueOfServer("c5.24xlarge")

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
        monthStr = '0' + \
            str(initialMonth) if initialMonth < 10 else str(initialMonth)
        dateToFormat = (initialYear, monthStr)
        newaveFile = "NW%d%s.zip" % dateToFormat
        decompFile = "DC%d%s.zip" % dateToFormat
        configFile = "Dados_Prospectivo.xlsx"

    prospec.sendFileToStudy(studyId, path+'/'+configFile, configFile)

    path_prevs = path + "/prevs/"

    prospec.sendPrevsToStudy(studyId, path_prevs)

    send_gevazp(path, studyId)

    prospec.runExecution(studyId, idServer, idQueue, '', '0', '0', '2')
    prospec.generateNextRev(studyId, newaveFile, decompFile, configFile, [])

    # prospec.generateStudyDecks(studyId, initialYear, initialMonth, [duration], month, year, [False, False], [
    #                            True, True], newaveFile, [newaveFile, newaveFile], [decompFile, decompFile], [configFile, configFile], [])


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
    revision = np.where(x == day)[0][0]
    return(revision)


def send_decks(path, uploadId):
    # TODO #7 corrigir o upload de decks
    path_decks = path + "/Decks/"
    file = get_decomp_files(path_decks)
    for file in Path(path_decks).glob("**/*"):
        if file.is_file() and file.suffix == "zip":
            prospec.sendFileToStudy(uploadId, file, file.name)


def get_decomp_files(path_decks):
    for file in Path(path_decks).glob("**/*"):
        if file.suffix == ".zip" and "DC" in file.name:
            with ZipFile(file) as zp:
                zp.extractall(path_decks)
            file.unlink()


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


def main():
    prospec.authenticateProspec(
        "daniel.mazucanti@skoposenergia.com.br", "Skopos2020")

    numRequests = prospec.getNumberOfRequests()

    print("Foram feitas %s requisições até o momento." % numRequests)

    while True:
        control_flow = input(
            '1- Criar estudo\n2- Rodar estudo\n3- Abortar execução\n4- Informações do estudo\n0- Sair\n')
        if control_flow == "1":

            nameStudy, path_opt = model_params()

            create_study(nameStudy)

        elif control_flow == "2":

            prep_n_run()

        elif control_flow == "3":
            display_studies()
            stopId = int(input("Qual estudo deseja parar?\n"))
            prospec.abortExecution(stopId)

        elif control_flow == "4":
            studiesInfo()

        else:
            print("Programa encerrado.")
            break


main()
