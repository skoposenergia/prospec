from pathlib import Path
from os import unlink
from datetime import timedelta, date
from sincrawl.implementa import RunGEVAZP
from hashlib import sha1


def get_files():
    spider_gevazp = RunGEVAZP()
    spider_gevazp.run()


def files_rvs():
    get_files()
    zip_gen = Path("full/").glob("**/*")
    zips_gevazp = [item for item in zip_gen if item.stat().st_size > 100000]
    num_files = len(zips_gevazp)
    rvs = ["PMO"] + ["RV%d" % rv for rv in range(1, num_files)]

    return num_files, rvs


def get_newer_file(rv):
    _, rvs = files_rvs()
    rv = rvs.pop()
    h = sha1()

    data = date.today() + timedelta(weeks=1)
    dias = 5 - int(data.isoweekday())
    data = data - timedelta(days=dias)
    mes = '0' + str(data.month) if data.month < 10 else str(data.month)
    infos = (data.year, mes, rv)
    url = "https://sintegre.ons.org.br/sites/9/13/79/_layouts/download.aspx?SourceUrl=/sites/9/13/79/Produtos/237" \
          "/Gevazp_%d%s_%s.zip" % infos
    h.update(url.encode('utf-8'))
    newer_rv_file = h.hexdigest()

    return "full/" + newer_rv_file + ".zip"

