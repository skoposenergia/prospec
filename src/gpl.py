import datetime as dt
from getpass import getpass
from pathlib import Path

from src.functionsPluviaAPI import *


def get_pluv():
    auth()

    id_maps, id_models = get_ids()

    curr_day, dir_download, forecastdate = get_dates()

    if not (dir_download.exists()):
        Path.mkdir(dir_download)

    download_files(curr_day, dir_download, forecastdate, id_maps, id_models)


def auth():
    user = input("Usuário: ")
    psswd = getpass("Senha: ")
    authenticatePluvia(user, psswd)


def get_ids():
    precipitationDataSources = ["GEFS", "ECMWF_ENS", "ONS"]
    forecastModels = ['IA+SMAP']
    id_maps = []
    id_models = []
    for precipitationDataSource in precipitationDataSources:
        id_maps.append(getIdOfPrecipitationDataSource(precipitationDataSource))
    for forecastModel in forecastModels:
        id_models.append(getIdOfForecastModel(forecastModel))
    return id_maps, id_models


def download_files(curr_day, dir_download, forecastdate, id_maps, id_models):
    forecasts = getForecasts(forecastdate, id_maps,
                             id_models, '', '', [curr_day.year], ["ENSEMBLE"])
    for forecast in forecasts:
        downloadForecast(forecast['prevsId'], dir_download,
                         forecast['nome'] + ' - ' + forecast['membro'] + ' - Prevs.zip')
        # downloadForecast(forecast['enaId'], dir_download,
        #                  forecast['nome'] + ' - ' + forecast['membro'] + '- ENA.zip')
        # downloadForecast(forecast['vnaId'], dir_download, forecast['nome'] + ' - ' + forecast['membro'] + '- VNA.csv')
        # downloadForecast(forecast['strId'], dir_download, forecast['nome'] + ' - ' + forecast['membro'] + '- STR.zip')


def get_dates():
    curr_day = dt.datetime.today()
    forecastdate = curr_day.strftime("%d/%m/%Y")
    form_dir = curr_day.strftime("%Y-%m-%d")
    dir_download = Path('full/%s/' % form_dir)
    return curr_day, dir_download, forecastdate
