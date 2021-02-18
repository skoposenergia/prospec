import calendar
import datetime as dt
from pathlib import Path
from zipfile import ZipFile

import numpy as np

from src import functionsProspecAPI as prospec
from src.arrFiles import main as prep_files


def prep_n_run():
    name, path = model_params() # Recebe nome do modelo e caminho para os arquivos

    idServer = prospec.getIdOfServer("c5.24xlarge") # define o servidor que vai ser usado
    idQueue = prospec.getIdOfFirstQueueOfServer("c5.24xlarge") # define a fila que será usada

    display_studies() # mostra os arquivos criados desde então registrado no arquivo "estudos criados" 
 
    studyId = int(
        input("Para qual estudo deseja enviar os arquivos?\n")) # recebe id do estudo

    prep_files() # baixa os gevazp e as ENAs do pluvia para o tratamento dos dados e os coloca nas pastas apropriadas

    # os decks devem ser inseridos manualmente na pasta de decks do estudo desejado
    # TODO #13 automatizar o download dos decks
    send_decks(path, studyId) # função que organiza e manda um zip com todos os decks necessários para rodar o estudo

    if name == "Curtíssimo prazo": # controle de fluxo para cada modelo 

        todayDate, multipleRevision, targetDates = treat_dates() # recebe as datas tratadas para usar de parâmetro

        initialYear = todayDate.year # ano do parâmetro
        initialMonth = todayDate.month # mês do parâmetro
        duration = str(todayDate.month - targetDates[1].month) 
        month = [targetDates[0].month, targetDates[1].month] # lista de parâmetros de mês
        year = [targetDates[0].year, targetDates[1].year] # lista de parâmetros de ano
        monthStr = '0' + \
            str(initialMonth) if initialMonth < 10 else str(initialMonth) #formatação da string de mês
        dateToFormat = (initialYear, monthStr) 
        newaveFile = "NW%d%s.zip" % dateToFormat # nome do deck newave
        decompFile = "DC%d%s.zip" % dateToFormat # nome do deck decomp

        configFile = "Dados_Prospectivo.xlsx" # arquivo de configuração. obrigatoriamente colocado de forma manual na pasta do modelo

    prospec.sendFileToStudy(studyId, path+'/'+configFile, configFile) # manda arquivo de configuração para a plataforma

    path_prevs = path + "/prevs/" # cria a string de caminho para os prevs

    prospec.sendPrevsToStudy(studyId, path_prevs) # evia os prevs para a plataforma

    send_gevazp(path, studyId) # envia os arquivos do GEVAZP para a plataforma

    prospec.runExecution(studyId, idServer, idQueue, '', '0', '0', '2') # solicita a execução do estudo
    

# TODO #14 fazer o download dos resultados dos estudos da plataforma
    # prospec.generateNextRev(studyId, newaveFile, decompFile, configFile, [])

    # prospec.generateStudyDecks(studyId, initialYear, initialMonth, [duration], month, year, [False, False], [
    #                            True, True], newaveFile, [newaveFile, newaveFile], [decompFile, decompFile], [configFile, configFile], [])


def treat_dates(): # função que organiza as datas de acordo com a revisão do curtíssimo prazo
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


def get_rev(date_value): # calcula a revisão de interesse baseado num calendário
    day = date_value.day
    month = date_value.month
    year = date_value.year
    x = np.array(calendar.monthcalendar(year, month))
    revision = np.where(x == day)[0][0]
    return(revision)


def send_decks(path, uploadId): # envia arquivos de decks para a plataforma

    path_decks = path + "/Decks/" # cria caminho para a pasta de decks
    create_folder_structure(path_decks) # cria as pastas com os conteúdos no formato que o zip precisa ter
    completeStudyZip = "CompleteStudy.zip" # nome do zip final
    zip_path = path_decks+completeStudyZip # criação do caminho para o zip na pasta

    # TODO #11 criação do zip apropriado para upload
    # os caminhos dentro do zip se referem à pasta raiz do projeto. Eles têm que se referir à pasta study
    # do modelo (e.g. CP/Curtíssimo/study/<pasta>/<arquivo> deveria ser somente /<pasta>/<arquivo>)
    decks = [item for item in Path(path_decks).glob(
        "**/*") if item.suffix == ".zip"] #lista os arquivos zip da pasta de decks

    create_zip(zip_path, path_decks) # função que cria o zip a ser enviado

    prospec.sendFileToStudy(uploadId, zip_path, completeStudyZip) # envia o zip para o estudo de interesse
    zipDecks = Path(zip_path) # cria objeto de caminho
    prospec.completeStudyDecks(uploadId, zipDecks.name, []) # solicita o tratamento do zip na plataforma com os decks completos
    zipDecks.unlink() # remove zip enviado para evitar um zip recursivo

def create_zip(zip_path, path_decks):
    studyFiles = Path(path_decks+'/study') # cria endereço para os arquivos do zip
    
    # with ZipFile(zip_path, 'w') as zp:
    #     for deck in decks:
    #         if "decomp" in deck.parts:
    #             arcName = "/DECOMP/%s" % deck.name

    #         else:
    #             arcName = "/NEWAVE/%s" % deck.name
    #         zp.write(deck, arcName)


def create_folder_structure(path_decks):
    extract_dc(path_decks) # extrai os arquivos do decomp para a criação de pastas individuais para eles
    folders(path_decks) # extrai os arquivos pertinentes aos decks a serem enviados
    rm_tmp(path_decks) # limpa arquivos temporários

def folders(path_decks):
    files = [item for item in Path(path_decks).glob("**/*") if item.suffix == ".zip"] # lista os zips da pasta de decks
    for file in files:
        if ("sem" in file.name or "NW" in file.name) and not ("Relatorio" in file.name): # acha os zips que não são de relatório
            with ZipFile(file, 'r') as zp:
                zp.extractall(path_decks+"/study/"+file.stem) # extrai para a pasta do zip

def extract_dc(path_decks):
    for file in Path(path_decks).glob("**/*"): # itera arquivos da pasta de decks
        if file.suffix == ".zip" and "DC" in file.name: # condicional para pegar somente os arquivos do DECOMP
            with ZipFile(file) as zp:
                zp.extractall(path_decks+'/tmp') # extração para uma pasta temporária

def rm_tmp(path_decks): # remoção da pasta temporária
    tmp = Path(path_decks+"/tmp")
    for file in tmp.glob('**/*'):
        file.unlink()
    tmp.rmdir()
        
        


def send_gevazp(path, uploadId): # envio dos arquivos do GEVAZP para o estudo
    path_gevazp = path + "/GEVAZP/"
    for file in Path(path_gevazp).glob("**/*"):
        if file.is_file():
            prospec.sendFileToDeck(uploadId, "", file, file.name)


def studiesInfo(): # retorna informações de um estudo
    display_studies() # disponibiliza o histórico de estudos criados
    infoId = input("Qual estudo deseja?\n") # recebe id do estudo
    infoStudy = prospec.getInfoFromStudy(infoId) # solicita à plataforma as infos do estudo
    if infoStudy == None: # tratamento de resposta de um estudo que não está mais presente na plataforma
        print("Esse estudo não está mais na plataforma!")
    else:
        print(infoStudy)


def create_study(nameStudy): # cria um estudo
    idStudy = prospec.createStudy(nameStudy, "", 0, 0) # cria um estudo na plataforma com o nome dado bno parâmetro

    with open("estudos criados", 'a') as fp: # registra no histórico a criação do estudo
        fp.write("ID: %s, Nome: %s\n" % (idStudy, nameStudy))

    print("O estudo %s foi criado com ID %s" % (nameStudy, idStudy))


def display_studies(): # imprime na tela o histórico de estudos
    print("Esses são os estudos criados até então:")
    with open("estudos criados", 'r') as fp:
        for line in fp:
            print(line)


def model_params(): # escolhe o nome e caminho do estudo
    nameStudy = "" # recebe o nome apropriado ou continua vazio em caso de erro
    path = "" # mesmo que o nome
    choice = input(
        "Qual o tipo de estudo que deseja?\n1- Curtísimo prazo\n2- ONS CP\n3- Matriz CP\n") # recebe o tipo de estudo a ser feito
    choice = int(choice)
    if choice == 1:
        nameStudy = "Curtíssimo prazo" # define o nome do estudo
        path = "CP/Curtissimo" # define o caminho para os arquivos do estudo

    elif choice < 4:
        # TODO #15 Controle de nomes e caminhos dos demais estudos

        print("Opção em implementação.")

    else:
        print("Opção inválida.")

    return nameStudy, path


def main():
    prospec.authenticateProspec(
        "daniel.mazucanti@skoposenergia.com.br", "Skopos2020") # segurança em primeiro lugar, não é mesmo?

    numRequests = prospec.getNumberOfRequests() # recebe o número de requisições feitas

    print("Foram feitas %s requisições até o momento." % numRequests) # imprime o número de requisições feitas

    while True: # cria laço para impressão do menu
        control_flow = input(
            '1- Criar estudo\n2- Rodar estudo\n3- Abortar execução\n4- Informações do estudo\n0- Sair\n') 
            # recebe opção do menu
        if control_flow == "1": # criar estudo

            nameStudy, path_opt = model_params() # recebe os parâmetros do estudo desejado
            

            create_study(nameStudy) # cria estudo na plataforma

        elif control_flow == "2": # rodar estudo

            prep_n_run() # prepara os arquivos, os envia para a plataforma e solicita a execução

        elif control_flow == "3": # pelo direito de escolher
            display_studies() # mostra histórico de estudos criados
            stopId = int(input("Qual estudo deseja parar?\n")) # recebe id do estudo a ser abortado
            prospec.abortExecution(stopId) # solicita o interrupção do estudo na plataforma

        elif control_flow == "4": # infos do estudo
            studiesInfo() # duh

        else: # qualquer coisa que não esteja nos casos anteriores para aqui
            print("Programa encerrado.")
            break


# create_folder_structure("CP/Curtissimo/Decks/")
# isso aqui era para debugar essa função
