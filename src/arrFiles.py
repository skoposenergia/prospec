from pathlib import Path
from os import unlink
from datetime import timedelta, date


def filesNRvs():
    zipGen = Path("full/").glob("**/*")
    zipsGevazp = [item for item in zipGen if item.stat().st_size > 100000]
    numFiles = len(zipsGevazp)
    rvs = ["PMO"] + ["RV%d" % rv for rv in range(1, numFiles)]

    return numFiles, rvs


def get_hash(rv):
    _, rvs = filesNRvs()
    rv = rvs.pop()

    data = date.today() + timedelta(weeks=1)
    dias = 5 - int(data.isoweekday())
    data = data - timedelta(days=dias)
    mes = '0' + str(data.month) if data.month < 10 else str(data.month)
    infos = (data.year, mes, rv)
    url = "https://sintegre.ons.org.br/sites/9/13/79/_layouts/download.aspx?SourceUrl=/sites/9/13/79/Produtos/237" \
          "/Gevazp_%d%s_%s.zip" % infos
    print(url)


getHash("PMO")
