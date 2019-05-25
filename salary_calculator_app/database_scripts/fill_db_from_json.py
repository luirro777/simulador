#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: Franco Rodriguez (ffrodriguez@famaf.unc.edu.ar)
# date: 18/03/2013

from pprint import pprint
import json
import sys
import os
import pdb
from datetime import date
sys.path.append(os.getcwd() + '/../../')

try:
        from salary_calculator import settings
except ImportError:
        import sys
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
        sys.exit(1)

from django.core.management import setup_environ
setup_environ(settings)

from salary_calculator_app.models import *

BASE_FILE = "../fixtures/"
PERIODO_FILE = BASE_FILE + "initial_data_periodo.json"
DENOMINACION_FILE = BASE_FILE +"initial_data_denominacion.json"
CARGO_FILE = BASE_FILE + "initial_data_cargo.json"
CARGOUNIV_FILE = BASE_FILE + "initial_data_cargouniv.json"
CARGOPREUNIV_FILE = BASE_FILE +"initial_data_cargopreuniv.json"
RETENCION_FILE = BASE_FILE + "initial_data_retencion.json"
REMUNERACION_FILE = BASE_FILE + "initial_data_remuneracion.json"
RETENCIONPORCENTUAL_FILE = BASE_FILE + "initial_data_retencion_porcentual.json"
REMUNERACIONPORCENTUAL_FILE = BASE_FILE + "initial_data_remuneracion_porcentual.json"
RETENCIONFIJA_FILE = BASE_FILE + "initial_data_retencion_fija.json"
REMUNERACIONFIJA_FILE = BASE_FILE + "initial_data_remuneracion_fija.json"
FONDOSOLIDARIO_FILE = BASE_FILE + "initial_data_fondo_solidario.json"
REMUNERACIONFIJACARGO_FILE = BASE_FILE + "initial_data_remuneracion_fija_cargo.json"
REMUNERACIONNOMENCLADOR_FILE = BASE_FILE + "initial_data_remuneracion_nomenclador.json"
BASICOUNIV_FILE = BASE_FILE + "initial_data_basico_univ.json"
BASICOPREUNIV_FILE = BASE_FILE + "initial_data_basico_preuniv.json"
ANTIGUEDADUNIV_FILE = BASE_FILE + "initial_data_antiguedad_univ.json"
ANTIGUEDADPREUNIV_FILE = BASE_FILE +"initial_data_antiguedad_preuniv.json"

def fill_periodo():
    print "Periodo"
    json_data = open(PERIODO_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not Periodo.objects.filter(pk=item['pk']).exists():
            Periodo(pk=item['pk'], **item['fields']).save()

def fill_denominacion():
    print "Denominacion"
    json_data = open(DENOMINACION_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not DenominacionCargo.objects.filter(pk=item['pk']).exists():
            DenominacionCargo(pk=item['pk'], **item['fields']).save()

def fill_cargo():
    print "Cargo"
    json_data = open(CARGO_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not Cargo.objects.filter(pk=item['pk']).exists():
            denominacion = DenominacionCargo.objects.get(pk=item['fields']['denominacion'])
            Cargo(pk=item['pk'], denominacion=denominacion,
                  pampa=item['fields']['pampa'], lu=item['fields']['lu']).save()

def fill_cargo_univ():
    print "Cargo Universitario"
    json_data = open(CARGOUNIV_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not CargoUniversitario.objects.filter(pk=item['pk']).exists():
            cargo = Cargo.objects.get(pk=item['pk'])
            CargoUniversitario(pk=item['pk'], dedicacion=item['fields']['dedicacion'],
                lu=cargo.lu, pampa=cargo.pampa, denominacion=cargo.denominacion).save()


def fill_cargo_preuniv():
    print "Cargo PreUniversitario"
    json_data = open(CARGOPREUNIV_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not CargoPreUniversitario.objects.filter(pk=item['pk']).exists():
            cargo = Cargo.objects.get(pk=item['pk'])
            CargoPreUniversitario(pk=item['pk'], lu=cargo.lu, pampa=cargo.pampa,
                denominacion=cargo.denominacion, **item['fields']).save()

def fill_retencion():
    print "Retencion"
    json_data = open(RETENCION_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not Retencion.objects.filter(pk=item['pk']).exists():
            Retencion(pk=item['pk'], **item['fields']).save()

def fill_remuneracion():
    print "Remuneracion"
    json_data = open(REMUNERACION_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not Remuneracion.objects.filter(pk=item['pk']).exists():
            Remuneracion(pk=item['pk'], **item['fields']).save()

def fill_retencion_porcentual():
    print "Retencion Porcentual"
    json_data = open(RETENCIONPORCENTUAL_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not RetencionPorcentual.objects.filter(pk=item['pk']).exists():
            retencion = Retencion.objects.get(pk=item['fields']['retencion'])
            vigencias = Periodo.objects.get(pk=item['fields']['vigencia'])
            RetencionPorcentual(pk=item['pk'], retencion=retencion, vigencia=vigencias,
                                porcentaje=item['fields']['porcentaje']).save()

def fill_remuneracion_porcentual():
    print "Remuneracion Porcentual"
    json_data = open(REMUNERACIONPORCENTUAL_FILE, 'r')

    data = json.load(json_data)
    json_data.close()
    #pprint(data)
    for item in data:
        if not RemuneracionPorcentual.objects.filter(pk=item['pk']).exists():
            remuneracion = Remuneracion.objects.get(pk=item['fields']['remuneracion'])
            vigencia = Periodo.objects.get(pk=item['fields']['vigencia'])
            print "vigencia : " + str(item['fields']['vigencia'])
            pprint(vigencia)
            RemuneracionPorcentual(pk=item['pk'], remuneracion=remuneracion,
                                porcentaje=item['fields']['porcentaje'],
                                sobre_referencia=item['fields']['sobre_referencia'],
                                nomenclador=item['fields']['nomenclador']).save()

def fill_retencion_fija():
    print "Retencion Fija"
    json_data = open(RETENCIONFIJA_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not RetencionFija.objects.filter(pk=item['pk']).exists():
            retencion = Retencion.objects.get(pk=item['fields']['retencion'])
            #vigencia = Periodo.objects.get(pk=item['fields']['vigencia'])
            RetencionFija(pk=item['pk'], retencion=retencion,
                                valor=item['fields']['valor']).save()

def fill_remuneracion_fija():
    print "Remuneracion Fija"
    json_data = open(REMUNERACIONFIJA_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not RemuneracionFija.objects.filter(pk=item['pk']).exists():
            remuneracion = Remuneracion.objects.get(pk=item['fields']['remuneracion'])
            #vigencia = Periodo.objects.get(pk=item['fields']['vigencia'])
            RemuneracionFija(pk=item['pk'], remuneracion=remuneracion,
                                valor=item['fields']['valor']).save()

def fill_fondo_solidario():
    print "Fondo Solidario"
    json_data = open(FONDOSOLIDARIO_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not FondoSolidario.objects.filter(pk=item['pk']).exists():
            ret = RetencionFija.objects.get(pk=item['pk'])
            FondoSolidario(pk=item['pk'], concepto=item['fields']['concepto'],
                           retencion=ret.retencion, valor=ret.valor).save()

def fill_remuneracion_fija_cargo():
    print "Remuneracion fija cargo"
    json_data = open(REMUNERACIONFIJACARGO_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not RemuneracionFijaCargo.objects.filter(pk=item['pk']).exists():
            rem = RemuneracionFija.objects.get(pk=item['pk'])
            cargo = Cargo.objects.get(pk=item['fields']['cargo'])
            RemuneracionFijaCargo(pk=item['pk'], remuneracion=rem.remuneracion,
                    valor=rem.valor, cargo=cargo).save()


def fill_remuneracion_nomenclador():
    print "remuneracion nomenclador"
    json_data = open(REMUNERACIONNOMENCLADOR_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not RemuneracionNomenclador.objects.filter(pk=item['pk']).exists():
            rem = RemuneracionPorcentual.objects.get(pk=item['pk'])
            cargo = Cargo.objects.get(pk=item['fields']['cargo'])
            RemuneracionNomenclador(pk=item['pk'], remuneracion=rem.remuneracion,
                   porcentaje=rem.porcentaje,
                   sobre_referencia=item['fields']['sobre_referencia'],
                   nomenclador=item['fields']['nomenclador'], cargo=cargo).save()

def fill_basico_univ():
    print "basico univ"
    json_data = open(BASICOUNIV_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not SalarioBasicoUniv.objects.filter(pk=item['pk']).exists():
            rem = RemuneracionFija.objects.get(pk=item['pk'])
            cargo = CargoUniversitario.objects.get(pk=item['fields']['cargo'])
            SalarioBasicoUniv(pk=item['pk'], remuneracion=rem.remuneracion,
                   valor=rem.valor,
                   salario_referencia=item['fields']['salario_referencia'],
                   cargo=cargo).save()

def fill_basico_preuniv():
    print "basico pre univ"
    json_data = open(BASICOPREUNIV_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not SalarioBasicoPreUniv.objects.filter(pk=item['pk']).exists():
            rem = RemuneracionFija.objects.get(pk=item['pk'])
            cargo = CargoPreUniversitario.objects.get(pk=item['fields']['cargo'])
            SalarioBasicoPreUniv(pk=item['pk'], remuneracion=rem.remuneracion,
                   valor=rem.valor,
                   salario_referencia=item['fields']['salario_referencia'],
                   cargo=cargo).save()

def fill_antiguedad_univ():
    print "antiguedad univ"
    json_data = open(ANTIGUEDADUNIV_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not AntiguedadUniversitaria.objects.filter(pk=item['pk']).exists():
            rem = RemuneracionPorcentual.objects.get(pk=item['pk'])
            AntiguedadUniversitaria(pk=item['pk'], remuneracion=rem.remuneracion,
                   porcentaje=rem.porcentaje,
                   sobre_referencia=item['fields']['sobre_referencia'],
                   nomenclador=item['fields']['nomenclador']).save()

def fill_antiguedad_preuniv():
    print "antiguedad preuniv"
    json_data = open(ANTIGUEDADPREUNIV_FILE, 'r')

    data = json.load(json_data)
    json_data.close()

    for item in data:
        if not AntiguedadPreUniversitaria.objects.filter(pk=item['pk']).exists():
            rem = RemuneracionPorcentual.objects.get(pk=item['pk'])
            AntiguedadPreUniversitaria(pk=item['pk'], remuneracion=rem.remuneracion,
                   porcentaje=rem.porcentaje,
                   sobre_referencia=item['fields']['sobre_referencia'],
                   nomenclador=item['fields']['nomenclador']).save()

if __name__=="__main__":
#     fill_periodo()
    fill_denominacion()
#     fill_cargo()
#     fill_cargo_univ()
#     fill_cargo_preuniv()
#     fill_retencion()
#     fill_remuneracion()
    #fill_retencion_porcentual()
#     fill_remuneracion_porcentual()
#     fill_retencion_fija()
#     fill_remuneracion_fija()
#     fill_fondo_solidario()
#     fill_remuneracion_fija_cargo()
#     fill_remuneracion_nomenclador()
#     fill_basico_univ()
#     fill_basico_preuniv()
#     fill_antiguedad_univ()
#     fill_antiguedad_preuniv()
