# -*- coding: utf-8 -*-
"""
Created on Jun 2020 by Norus
"""
import os
import time

from src.requestsPluviaAPI import getToken
from src.requestsPluviaAPI import getInfoFromAPI
from src.requestsPluviaAPI import getFileFromAPI

# -----------------------------------------------------------------------------
# Global variables | Variáveis globais
# -----------------------------------------------------------------------------

global token

# -----------------------------------------------------------------------------
# Get token | Obter token
# -----------------------------------------------------------------------------


def authenticatePluvia(username, password):
    global token
    token = getToken(username, password)
    return token

# -----------------------------------------------------------------------------
# Get list of Precitation Data Source | Obter lista de Fonte de Dados de Precipitação
# -----------------------------------------------------------------------------


def getIdsOfPrecipitationsDataSource():
    return getInfoFromAPI(token, '/api/valoresParametros/mapas')


def getIdOfPrecipitationDataSource(precipitationDataSource):
    "Possible values: MERGE, ETA, GEFS, CFS, ONS NT0156, Usuário, Prec. Zero, ONS, ONS SOMBRA, ECMWF_ENS or ECMWF_ENS_EXT"
    return next(item for item in getIdsOfPrecipitationsDataSource() if item["descricao"] == precipitationDataSource)['id']


# -----------------------------------------------------------------------------
# Get list of Forecast Modelos | Obter lista dos Modelos de Previsão
# -----------------------------------------------------------------------------


def getIdsOfForecastModels():
    return getInfoFromAPI(token, '/api/valoresParametros/modelos')

def getIdOfForecastModel(forecastModel):
    "Possible values: IA, IA+SMAP or SMAP "
    return next(item for item in getIdsOfForecastModels() if item["descricao"] == forecastModel)['id']

# -----------------------------------------------------------------------------
# Get list of Precitation Data Source | Obter lista de Fonte de Dados de Precipitação
# -----------------------------------------------------------------------------


def getForecasts(forecastDate, forecastSources, forecastModels, bias, preliminary, years, members):
    "forecastDate mandatory"

    if forecastDate == '':
        print('Data de Previsão não pode ser nula')
        return []

    params = "dataPrevisao=" + forecastDate
   
    for forecastSource in forecastSources:
        params += "&mapas=" + str(forecastSource)
    
    for forecastModel in forecastModels:
        params += "&modelos=" + str(forecastModel)
    
    if bias != '':
        params += "&semVies=" + str.lower(bias)
    
    if preliminary != '':
        params += "&preliminar=" + str.lower(preliminary)
    
    for year in years:
        params += "&anos=" + str(year)

    for member in members:
        params += "&membros=" + str(member)

    return getInfoFromAPI(token, '/api/previsoes?' + params)

def downloadForecast(idForecast, pathToDownload, fileName):
    response = getFileFromAPI(token, '/api/resultados/' + str(idForecast), fileName, pathToDownload)