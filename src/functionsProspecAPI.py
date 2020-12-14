# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 13:06:40 2018
Plan4
@author: Vitor
"""
import os

from src.requestsProspecAPI import getToken
from src.requestsProspecAPI import getInfoFromAPI
from src.requestsProspecAPI import postInAPI
from src.requestsProspecAPI import sendFileToAPI
from src.requestsProspecAPI import getFileFromAPI
from src.requestsProspecAPI import getCompilationFromAPI
from src.requestsProspecAPI import getFileFromS3viaAPI
from src.requestsProspecAPI import sendFiles
from src.requestsProspecAPI import patchInAPI

# -----------------------------------------------------------------------------
# Global variables | Variáveis globais
# -----------------------------------------------------------------------------

token = ''

# -----------------------------------------------------------------------------
# Get token | Obter token
# -----------------------------------------------------------------------------


def authenticateProspec(username, password):
    global token
    token = getToken(username, password)

# -----------------------------------------------------------------------------
# Update Password | Atualizar Senha
# -----------------------------------------------------------------------------


def updatePassword(oldPassword, newPassword):
    parameter = ''
    data = {
        "OldPassword": oldPassword,
        "NewPassword": newPassword,
        "ConfirmPassword": newPassword
    }
    postInAPI(token, '/api/Account/ChangePassword', parameter,
              data)

    return 0

# -----------------------------------------------------------------------------
# Get number of total requests | Buscar quantidade de requests já usados
# -----------------------------------------------------------------------------


def getNumberOfRequests():
    numberOfRequests = getInfoFromAPI(token, '/api/Account/Requests')
    return numberOfRequests

# -----------------------------------------------------------------------------
# Get list of NEWAVES | Obter lista de NEWAVES
# -----------------------------------------------------------------------------


def getListOfNEWAVEs():
    return getInfoFromAPI(token, '/api/CepelModels/Newaves')

# -----------------------------------------------------------------------------
# Get list of NEWAVES and choose one | Obter lista de NEWAVES e escolher um
# -----------------------------------------------------------------------------


def getIdOfNEWAVE(version):
    listOfNewave = getListOfNEWAVEs()

    idNewave = ''
    for newave in listOfNewave:
        if newave['Version'] == version:
            idNewave = newave['Id']
            return idNewave

    return 0

# -----------------------------------------------------------------------------
# Get list of DECOMPs | Obter lista de DECOMPs
# -----------------------------------------------------------------------------


def getListOfDECOMPs():
    return getInfoFromAPI(token, '/api/CepelModels/Decomps')

# -----------------------------------------------------------------------------
# Get list of NEWAVES and choose one | Obter lista de NEWAVES e escolher um
# -----------------------------------------------------------------------------


def getIdOfDECOMP(version):
    listOfDecomps = getListOfDECOMPs()

    idDecomp = ''
    for decomp in listOfDecomps:
        if decomp['Version'] == version:
            idDecomp = decomp['Id']
            return idDecomp

    return 0

# -----------------------------------------------------------------------------
# Get list of DESSEM | Obter lista de DESSEM
# -----------------------------------------------------------------------------


def getListOfDESSEMs():
    return getInfoFromAPI(token, '/api/CepelModels/Dessems')

# -----------------------------------------------------------------------------
# Get list of DESSEM and choose one | Obter lista de DESSEM e escolher um
# -----------------------------------------------------------------------------


def getIdOfDESSEM(version):
    listOfDessem = getListOfDESSEMs()

    idDessem = ''
    for dessem in listOfDessem:
        if dessem['Version'] == version:
            idDessem = dessem['Id']
            return idDessem

    return 0

# -----------------------------------------------------------------------------
# Get list of GEVAZP | Obter lista de GEVAZP
# -----------------------------------------------------------------------------


def getListOfGEVAZPs():
    return getInfoFromAPI(token, '/api/CepelModels/Gevazps')

# -----------------------------------------------------------------------------
# Get list of GEVAZP and choose one | Obter lista de GEVAZP e escolher um
# -----------------------------------------------------------------------------


def getIdOfGEVAZP(version):
    listOfGevazp = getListOfGEVAZPs()

    idGevazp = ''
    for gevazp in listOfGevazp:
        if gevazp['Version'] == version:
            idGevazp = gevazp['Id']
            return idGevazp

    return 0

# -----------------------------------------------------------------------------
# Get list of Tags | Obter lista de marcadores
# -----------------------------------------------------------------------------


def getListOfTags():
    return getInfoFromAPI(token, '/api/prospectiveStudies/Tags')

# -----------------------------------------------------------------------------
# Get list of Spot Instances Types | Obter lista de tipos de instâncias SPOT
# -----------------------------------------------------------------------------


def getListOfSpotInstancesTypes():
    return getInfoFromAPI(token, '/api/Servers/SpotInstances')

# -----------------------------------------------------------------------------
# Get list of Spot Instances Types    and choose one
# Obter lista de tipos de instâncias SPOT e escolher um
# -----------------------------------------------------------------------------


def getIdOfSpotInstancesType(serverType):
    listOfSpotInstances = getListOfSpotInstancesTypes()

    idSpotInstances = ''
    for spotInstances in listOfSpotInstances:
        if spotInstances['InstanceType'] == serverType:
            idSpotInstances = spotInstances['Id']
            return idSpotInstances

    return 0

# -----------------------------------------------------------------------------
# Get list of servers - this is necessary to add studies in a given queue
# Obter lista de servidores - necessário para adicionar um estudo em uma fila
# -----------------------------------------------------------------------------


def getListOfServers():
    return getInfoFromAPI(token, '/api/Servers')


def getIdOfServer(serverName):
    listOfServers = getListOfServers()

    for server in listOfServers:
        if server['Name'] == serverName:
            idServer = server['Id']
            return idServer

    return 0


def getIdOfFirstQueueOfServer(serverName):

    listOfServers = getListOfServers()

    for server in listOfServers:
        if server['Name'] == serverName:
            listOfQueues = server['Queues']
            firsQueue = listOfQueues[0]
            return firsQueue['Id']

    return 0

# -----------------------------------------------------------------------------
# Create one study | Criar um estudo
# -----------------------------------------------------------------------------


def createStudy(title, description, idDecomp, idNewave):
    parameter = ''
    data = {
        "Title": title,
        "Description": description,
        "DecompVersionId": int(idDecomp),
        "NewaveVersionId": int(idNewave)
    }

    print("Creating study with the following configuration:")
    print(data)

    prospecStudyId = postInAPI(token, '/api/prospectiveStudies', parameter,
                               data)
    return prospecStudyId

# -----------------------------------------------------------------------------
# Get info from a specific study | Obter informações de um estudo específico
# -----------------------------------------------------------------------------


def getInfoFromStudy(idStudy):
    prospecStudy = getInfoFromAPI(token, '/api/prospectiveStudies/'
                                  + str(idStudy))
    return prospecStudy

# -----------------------------------------------------------------------------
# Get status from a specific study | Obter o status de um estudo específico
# -----------------------------------------------------------------------------


def getStatusFromStudy(idStudy):
    prospecStudy = getInfoFromAPI(token, '/api/prospectiveStudies/'
                                  + str(idStudy))
    return prospecStudy['Status']

# -----------------------------------------------------------------------------
# Send files to a study | Enviar arquivos para um estudo
# -----------------------------------------------------------------------------


def sendFileToStudy(idStudy, pathToFile, fileName):
    prospecStudy = sendFileToAPI(token, '/api/prospectiveStudies/'
                                 + str(idStudy) + '/UploadFiles',
                                 pathToFile, fileName)
    return prospecStudy

# -----------------------------------------------------------------------------
# Send files to a deck of a study | Enviar arquivos para um deck de um estudo
# -----------------------------------------------------------------------------


def sendFileToDeck(idStudy, idDeck, pathToFile, fileName):
    prospecStudy = sendFileToAPI(token, '/api/prospectiveStudies/'
                                 + str(idStudy) + '/UploadFiles?deckId='
                                 + str(idDeck), pathToFile, fileName)
    return prospecStudy

# -----------------------------------------------------------------------------
# Generate decks to a prospective study
# Gerar decks para um estudo prospectivo
# -----------------------------------------------------------------------------


def generateStudyDecks(idStudy, initialYear, initialMonth, duration, month,
                       year, multipleStages, multipleRevision, firstNewaveFile,
                       otherNewaveFiles, decompFile, spreadsheetFile, tags):

    listOfDeckConfiguration = []
    listOfTags = []

    i = 0
    for deck in month:
        deckConfiguration = {}
        deckConfiguration['Year'] = year[i]
        deckConfiguration['Month'] = month[i]
        deckConfiguration['MultipleStages'] = multipleStages[i]
        deckConfiguration['MultipleRevisions'] = multipleRevision[i]
        if (i > 0):
            if (otherNewaveFiles[i] != ''):
                deckConfiguration['NewaveUploaded'] = otherNewaveFiles[i]
        listOfDeckConfiguration.append(deckConfiguration)
        i = i + 1

    for tag in tags:
        tagsConfiguration = {}
        tagsConfiguration['Text'] = tag
        listOfTags.append(tagsConfiguration)

    parameter = ''
    data = {
        "InitialYear": initialYear,
        "InitialMonth": initialMonth,
        "Duration": duration,
        "DeckCreationConfigurations": listOfDeckConfiguration,
        "Tags": listOfTags,
        "InitialFiles": {
            "NewaveFileName": firstNewaveFile,
            "DecompFileName": decompFile,
            "SpreadsheetFileName": spreadsheetFile
        }
    }

    print("Gerando decks com as seguintes configuracoes para o estudo: ",
          str(idStudy))
    print(data)

    postInAPI(token, '/api/prospectiveStudies/' + str(idStudy) + '/Generate',
              parameter, data)

# -----------------------------------------------------------------------------
# Generate next revision
# Gerar próxima revisão
# -----------------------------------------------------------------------------


def generateNextRev(idStudy, newaveFile, decompFile, spreadsheetFile, tags):

    listOfTags = []

    for tag in tags:
        tagsConfiguration = {}
        tagsConfiguration['Text'] = tag
        listOfTags.append(tagsConfiguration)

    parameter = ''
    data = {
        "InitialFiles": {
            "NewaveFileName": newaveFile,
            "DecompFileName": decompFile,
            "SpreadsheetFileName": spreadsheetFile
        },
        "Tags": listOfTags
    }

    print("Gerando a próxima revisão para o estudo: ",
          str(idStudy))
    print(data)

    patchInAPI(token, '/api/prospectiveStudies/' + str(idStudy) + '/NextRev',
               parameter, data)

# -----------------------------------------------------------------------------
# Generate study with complete decks | Gerando estudo com decks completos
# -----------------------------------------------------------------------------


def completeStudyDecks(idStudy, fileName, tags):

    listOfTags = []

    for tag in tags:
        tagsConfiguration = {}
        tagsConfiguration['Text'] = tag
        listOfTags.append(tagsConfiguration)

    parameter = ''
    data = {
        "Tags": listOfTags,
        "FileName": fileName
    }

    print("Usando a seguinte configuracao para o estudo: ", str(idStudy))
    print(data)

    postInAPI(token, '/api/prospectiveStudies/' + str(idStudy) + '/Complete',
              parameter, data)

# -----------------------------------------------------------------------------
# Duplicate a study | Duplicar um estudo
# -----------------------------------------------------------------------------


def duplicateStudy(idStudy, title, description, tags, vazoesDat, vazoesRvx, prevsCondition):

    listOfTags = []

    for tag in tags:
        tagsConfiguration = {}
        tagsConfiguration['Text'] = tag
        listOfTags.append(tagsConfiguration)

    parameter = ''
    data = {
        "Title": title,
        "Description": description,
        "Tags": listOfTags,
        "VazoesDatCondition": vazoesDat,
        "VazoesRvxCondition": vazoesRvx,
        "PrevsCondition": prevsCondition
    }

    # VazoesDatCondition(integer)
    # 0 - padrão, não faz nenhuma mudança no decks.
    # 1 - exclui todos os vazoes.dat de todos os decks DECOMP do estudo.
    # 2 - exclui os vazoes.dat do segundo deck DECOMP em diante.

    # VazoesRvxCondition(integer)
    # 0 - Modo padrão
    # 1 - exclui todos os vazoes.rvX de todos os decks DECOMP do estudo.
    # 2 - exclui os vazoes.rvX do segundo deck DECOMP em diante.

    # PrevsCondition(integer)
    # 0 - Modo padrão
    # 1 - exclui todos os prevs, inclusive sensibilidade, de todos os decks DECOMP do estudo.
    # 2 - exclui somente os prevs sensibilidade do primeiro deck DECOMP e dos demais decks exclui todos os prevs, inclusive sensibilidade

    print("Usando a seguinte configuracao para o estudo: ", str(idStudy))
    print(data)

    prospecStudyId = postInAPI(token, '/api/prospectiveStudies/'
                               + str(idStudy) + '/Duplicate', parameter, data)
    return prospecStudyId

# -----------------------------------------------------------------------------
# Adding tags to a study | Adicionar tags em um estudos
# -----------------------------------------------------------------------------


def addTags(idStudy, tags):

    listOfTags = []

    for tag in tags:
        tagsConfiguration = {}
        tagsConfiguration['Text'] = tag
        listOfTags.append(tagsConfiguration)

    parameter = ''

    data = listOfTags

    print("Adicionando tags ao estudo: ", str(idStudy))
    print(data)

    patchInAPI(token, '/api/prospectiveStudies/' + str(idStudy) + '/AddTags',
               parameter, data)

# -----------------------------------------------------------------------------
# Removing tags to a study | Remover tags em um estudos
# -----------------------------------------------------------------------------


def removeTags(idStudy, tags):

    listOfTags = []

    for tag in tags:
        tagsConfiguration = {}
        tagsConfiguration['Text'] = tag
        listOfTags.append(tagsConfiguration)

    parameter = ''

    data = listOfTags

    print("Removendo tags do estudo: ", str(idStudy))
    print(data)

    patchInAPI(token, '/api/prospectiveStudies/' + str(idStudy) + '/RemoveTags',
               parameter, data)


# -----------------------------------------------------------------------------
# Send prevs file to each deck | Enviar o arquivo prevs para cada deck
# -----------------------------------------------------------------------------

def sendPrevsToStudy(idStudy, pathToPrevs):

    prospecStudy = getInfoFromStudy(idStudy)
    listOfDecks = prospecStudy['Decks']
    listOfFiles = []
    listOfPaths = []
    listOfDecksIds = []

    for deck in listOfDecks:

        if ((deck['Model'] == 'DECOMP') and (deck['SensibilityInfo'] == 'Original')):

            mes = deck['Month']
            revision = ".rv" + str(deck['Revision'])

            if mes < 10:
                pathToFile = pathToPrevs + '/0' + str(mes) + '/'
            else:
                pathToFile = pathToPrevs + '/' + str(mes) + '/'

            print('Arquivo em ' + pathToFile)
            for file in os.listdir(pathToFile):
                if file.lower().startswith('prevs'):
                    if file.lower().endswith(revision):
                        prospecStudy = sendFileToDeck(idStudy,
                                                      str(deck['Id']),
                                                      (pathToFile + file),
                                                      file)

# -----------------------------------------------------------------------------
# Send all prevs files to a deck | Enviar todos os arquivos prevs de um deck
# -----------------------------------------------------------------------------


def sendAllPrevsToEachDeck(idStudy, pathToPrevs):

    prospecStudy = getInfoFromStudy(idStudy)
    listOfDecks = prospecStudy['Decks']

    for deck in listOfDecks:

        if ((deck['Model'] == 'DECOMP') and (deck['SensibilityInfo'] == 'Original')):

            listOfFiles = {}
            mes = deck['Month']
            revision = ".rv" + str(deck['Revision'])

            if mes < 10:
                pathToFile = pathToPrevs + '/0' + str(mes) + '/'
            else:
                pathToFile = pathToPrevs + '/' + str(mes) + '/'

            print('Arquivos em ' + pathToFile)
            for file in os.listdir(pathToFile):
                if file.lower().startswith('prevs'):
                    if file.lower().endswith(revision):
                        listOfFiles[file] = [file, open((pathToFile + file), 'rb'),
                                             'multipart/form-data', {'Expires': '0'}]

            sendFiles(token, '/api/prospectiveStudies/' + str(idStudy)
                      + '/UploadFiles?deckId=' + str(deck['Id']), listOfFiles)

# -----------------------------------------------------------------------------
# Send all prevs files to a study | Enviar todos os arquivos prevs de um estudo
# -----------------------------------------------------------------------------


def sendAllPrevsToStudy(idStudy, pathToAllPrevs):

    listOfPrevs = {}

    for file in os.listdir(pathToAllPrevs):
        if 'prevs' in file.lower():
            listOfPrevs[file] = [file, open((pathToAllPrevs + file), 'rb'),
                                 'multipart/form-data', {'Expires': '0'}]

    sendFiles(token, '/api/prospectiveStudies/' + str(idStudy)
              + '/UploadMultiplePrevs', listOfPrevs)

# -----------------------------------------------------------------------------
# Run a study | Executar um estudo
# -----------------------------------------------------------------------------


def runExecution(idStudy, idServer, idQueue, spotInstanceType, executionMode,
                 infeasibilityHandling, maxRestarts):
    parameter = ''

    if idServer == 0:
        if spotInstanceType == '':
            prospecStudy = getInfoFromStudy(idStudy)
            listOfDecks = prospecStudy['Decks']
            containsNEWAVE = False
            for deck in listOfDecks:
                if deck['Model'] == 'NEWAVE':
                    containsNEWAVE = True
                    break

            if containsNEWAVE:
                data = {
                    "SpotInstanceType": 'c5.9xlarge',
                    "ExecutionMode": executionMode,
                    "InfeasibilityHandling": infeasibilityHandling,
                    "MaxTreatmentRestarts": maxRestarts
                }
            else:
                data = {
                    "SpotInstanceType": 'm5.4xlarge',
                    "ExecutionMode": executionMode,
                    "InfeasibilityHandling": infeasibilityHandling,
                    "MaxTreatmentRestarts": maxRestarts
                }

        else:
            data = {
                "SpotInstanceType": spotInstanceType,
                "ExecutionMode": executionMode,
                "InfeasibilityHandling": infeasibilityHandling,
                "MaxTreatmentRestarts": maxRestarts
            }
    elif idQueue == 0:
        data = {
            "ServerId": int(idServer),
            "ExecutionMode": executionMode,
            "InfeasibilityHandling": infeasibilityHandling,
            "MaxTreatmentRestarts": maxRestarts
        }
    else:
        data = {
            "ServerId": int(idServer),
            "QueueId": int(idQueue),
            "ExecutionMode": executionMode,
            "InfeasibilityHandling": infeasibilityHandling,
            "MaxTreatmentRestarts": maxRestarts
        }

    print("A seguinte configuracao sera usada para iniciar a execucao o estudo: ", str(idStudy))
    print(data)

    response = postInAPI(token, '/api/prospectiveStudies/' + str(idStudy)
                         + '/Run', parameter, data)

    # print(response)

# -----------------------------------------------------------------------------
# Abort execution | Abortar execução
# -----------------------------------------------------------------------------


def abortExecution(idStudy):
    parameter = ''
    data = ''

    response = postInAPI(token, '/api/prospectiveStudies/' + str(idStudy)
                         + '/Stop', parameter, data)
    print(response)

# -----------------------------------------------------------------------------
# Download study | Download de um estudo
# -----------------------------------------------------------------------------


def downloadDecksOfStudy(idStudy, pathToDownload, fileName):
    response = getFileFromAPI(token, '/api/prospectiveStudies/' + str(idStudy)
                              + '/DeckDownload', fileName, pathToDownload)

# -----------------------------------------------------------------------------
# Download File From Deck Results | Download de um arquivo de um resultado do deck
# -----------------------------------------------------------------------------


def downloadFileFromDeck(idDeck, pathToDownload, fileNameDownload, fileNames):
    filesToGet = 'fileNames=' + '&fileNames='.join(fileNames)
    response = getFileFromS3viaAPI(token, '/api/prospectiveStudies/DownloadResultFiles/' + str(idDeck)
                                   + '?' + filesToGet, fileNameDownload, pathToDownload)

# -----------------------------------------------------------------------------
# Download compilation | Download da compilação
# -----------------------------------------------------------------------------


def downloadCompilationOfStudy(idStudy, pathToDownload, fileName):
    response = getCompilationFromAPI(token, '/api/prospectiveStudies/'
                                     + str(idStudy) + '/CompilationDownload',
                                     fileName, pathToDownload)

# -----------------------------------------------------------------------------
# Associate cuts | Reaproveitar (associar) cortes
# -----------------------------------------------------------------------------


def cutAssociation(idStudy, destinationIds, sourceStudyId):
    listOfAssociation = []

    for deck in destinationIds:
        associationConfiguration = {}
        associationConfiguration['DestinationDeckId'] = deck
        associationConfiguration['SourceStudyId'] = sourceStudyId
        listOfAssociation.append(associationConfiguration)

    parameter = ''
    data = {
        "cortesAssociation": listOfAssociation,
    }

    print("Usando a seguinte configuracao do estudo: ", str(idStudy))
    print(data)

    postInAPI(token, '/api/prospectiveStudies/' + str(idStudy)
              + '/Associate', parameter, data)

# -----------------------------------------------------------------------------
# Associate Volume and GNL | Reaproveitamento (associação) de volumes e GNL
# -----------------------------------------------------------------------------


def volumeAssociation(idStudy, destinationIds, previsouStage, sourceStudyId):
    listOfAssociation = []

    i = 0
    for deck in destinationIds:
        associationConfiguration = {}
        associationConfiguration['DestinationDeckId'] = deck
        associationConfiguration['SourceStudyId'] = sourceStudyId
        if (len(previsouStage) > i):
            associationConfiguration['PreviousStage'] = previsouStage[i]
        listOfAssociation.append(associationConfiguration)
        i = i + 1

    parameter = ''
    data = {
        "volumeAssociation": listOfAssociation,
    }

    print("Usando a seguinte configuracao do estudo: ", str(idStudy))
    print(data)

    postInAPI(token, '/api/prospectiveStudies/' + str(idStudy)
              + '/Associate', parameter, data)
