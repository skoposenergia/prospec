from datetime import timedelta, date
from hashlib import sha1
from os import unlink
from pathlib import Path
from shutil import copy
from zipfile import ZipFile
from getpass import getpass

from sincrawl.implementa import RunGEVAZP
from src.gpl import get_pluv, get_dates


def get_files(): # Executa a classe do sincrawl que faz o download dos GEVAZP
    spider_gevazp = RunGEVAZP() # Instancia a classe
    spider_gevazp.run() # Executa método da classe


def files_rv():
    zip_gen = Path("full/").glob("**/*") # Lista todos os diretórios em full
    zips_gevazp = [item for item in zip_gen if item.stat().st_size > 100000] # Filtra os arquivos válidos checando o tamanho deles
    num_files = len(zips_gevazp) # Conta quantos arquivos válidos existem
    if num_files != 0: # Checa se o número de arquivos válidos não é zero
        rvs = ["PMO"] + ["RV%d" % rv for rv in range(1, num_files)] # Se for o caso, ele monta a pilha de revisões
    else:
        return "" # Senão ele retorna uma lista vazia
    return rvs.pop() # Ele retorna a revisão mais recente


def get_newer_file(rv): # Usa uma hash table para achar o arquivo de acordo com a revisão
    h = sha1() # Instancia o objeto do hash sha1 (o que o scrapy usa no download para garantir que os arquivos não se sobreponham)
    rv = rv.replace("RV", "REV") # Correção do texto para a formatação da URL
    data = date.today() + timedelta(weeks=1) # Cria um objeto de data da semana seguinte (referência para as revisões)
    dias = 5 - int(data.isoweekday()) # Conta quantos dias faltam para sexta (dia de referência para revisões)
    data = data - timedelta(days=dias) # Edita a data original para o objeto corresponder a sexta
    mes = '0' + str(data.month) if data.month < 10 else str(data.month) # Formata string de mês
    infos = (data.year, mes, rv) # Cria tupla de formatação

    url = "https://sintegre.ons.org.br/sites/9/13/79/_layouts/download.aspx?SourceUrl=/sites/9/13/79/Produtos/237" \
          "/Gevazp_%d%s_%s.zip" % infos # Cria string da url do arquivo desejado

    h.update(url.encode('utf-8')) # Correção de encoding para evitar infortúnios e alimentando a classe para o hash

    newest_file = h.hexdigest() # Criação do hash baseado na url 

    return "full/" + newest_file + ".zip" # Retorono do endereço do arquivo mais recente


def extract_zip(file_dir): # Extrai o endereço dado na pasta full
    with ZipFile(file_dir) as zp: # Instancia a classe
        zp.extractall('full')


def files_cp(files, dst): # Copia arquivos em lotes, criado só para mais fácil reaproveitamento de código
    for item in files:
        copy(item, dst)


def send_gevazp(rv): # Organiza e manda os GEVAZP para cada tipo de previsão
    matriz = ["REGRAS.DAT", "VAZOES.DAT", "MODIF.DAT", "POSTOS.DAT"] # Arquivos pertinentes ao Matriz
    rv = rv.replace("PMO", "RV0") # Correção de indicador de revisão para formatação dos nomes dos arquivos
    ons_cp = ["REGRAS.DAT", "VAZOES.DAT", "MODIF.DAT",
              "POSTOS.DAT", "prevs.%s" % rv] # Arquivos pertinentes a ONS de curto prazo

    matriz = ["full/Gevazp/" + x for x in matriz] # Criação da lista de diretórios de Matriz
    ons_cp = ["full/Gevazp/" + x for x in ons_cp] # Criação da lista de diretórios de ONS Curto Prazo

    # Chamada das funções de cópia de arquivo
    files_cp(ons_cp, "CP/ONS/GEVAZP/")
    files_cp(ons_cp, "CP/Curtissimo/GEVAZP/")
    files_cp(matriz, "CP/Matriz/GEVAZP/")
    files_cp(matriz, "CP/Matriz/GEVAZP/")
    files_cp(ons_cp, "CP/Curtissimo/GEVAZP/")


def extract_prevs(): # Baixa e extrai os prevs
    dir_download = get_dates()
    pluvia_zips = [file for file in dir_download[1].glob("**/*") if file.suffix == ".zip"]
    for pzip in pluvia_zips:
        extract_zip(pzip)


def clear_full(): # Remove os arquivos da pasta de download
    files = Path("full/").glob("**/*")
    files_dir = [item for item in files if item.is_file()]
    for item in files_dir:
        unlink(item)


def send_prevs(): # Copia os prevs extraídos para a pasta do curtíssimo prazo
    dst = "CP/Curtissimo/prevs"
    prevs_files = [file for file in Path("full").glob("**/*") if "rv" in file.suffix]
    for prev in prevs_files:
        copy(prev, dst)


def main():
    user = input("Usuário Pluvia: ")
    password = getpass("Senha: ")
    get_files() # Baixa arquivos do sintegre
    rv = files_rv() # Recebe revisão mais recente dos arquivos disponíveis ou "" se não existe arquivo para o mês alvo

    if rv == "": # Tratamento para o mês alvo faltante
        print("Ainda não existem GEVAZPs desse mês operativo disponíveis no momento")
    else:
        file_dir = get_newer_file(rv) # Recebe o diretório do arquivo da revisão mais recente
        extract_zip(file_dir) # Extrai arquivo
        send_gevazp(rv) # Coloca o arquivo na pasta do curtíssimo prazo
    clear_full() # Remove arquivos temporários
    get_pluv(user, password) # Baixa os arquivos do pluvia com as credenciais fornecidas
    extract_prevs() # Extrai os arquivos baixados do pluvia
    send_prevs() # Copia para a pasta do curtíssimo prazo
    clear_full() # Limpa os arquivos temporários novamente
