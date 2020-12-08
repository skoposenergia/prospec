from datetime import timedelta, date
from hashlib import sha1
from os import unlink
from pathlib import Path
from shutil import copyfile
from sincrawl.implementa import RunGEVAZP
from zipfile import ZipFile


def get_files():
    spider_gevazp = RunGEVAZP()
    spider_gevazp.run()


def files_rv():
    zip_gen = Path("full/").glob("**/*")
    zips_gevazp = [item for item in zip_gen if item.stat().st_size > 100000]
    num_files = len(zips_gevazp)
    if num_files != 0:
        rvs = ["PMO"] + ["RV%d" % rv for rv in range(1, num_files)]
    else:
        return ""
    return rvs.pop()


def get_newer_file(rv):
    h = sha1()

    data = date.today() + timedelta(weeks=1)
    dias = 5 - int(data.isoweekday())
    data = data - timedelta(days=dias)
    mes = '0' + str(data.month) if data.month < 10 else str(data.month)
    infos = (data.year, mes, rv)

    url = "https://sintegre.ons.org.br/sites/9/13/79/_layouts/download.aspx?SourceUrl=/sites/9/13/79/Produtos/237" \
          "/Gevazp_%d%s_%s.zip" % infos
    h.update(url.encode('utf-8'))

    newest_file = h.hexdigest()

    return "full/" + newest_file + ".zip"


def extract_zip(file_dir):
    with ZipFile(file_dir) as zp:
        zp.extractall('full')


def files_cp(files, dst):
    for item in files:
        copyfile(item, dst)


def send_files(rv):
    matriz = ["REGRAS.DAT", "VAZOES.DAT", "MODIF.DAT", "POSTOS.DAT"]
    ons_cp = ["REGRAS.DAT", "VAZOES.DAT", "MODIF.DAT", "POSTOS.DAT", "prevs.%s" % rv.upper()]


def clear_full():
    files = Path("full/").glob("**/*")
    files_dir = [item for item in files if item.is_file()]
    for item in files_dir:
        unlink(item)


def main():
    get_files()
    rv = files_rv()
    if rv == "":
        print("Não existem GEVAZPs desse mês operativo disponíveis no momento")
    else:
        file_dir = get_newer_file(rv)
        extract_zip(file_dir)

    clear_full()


main()
