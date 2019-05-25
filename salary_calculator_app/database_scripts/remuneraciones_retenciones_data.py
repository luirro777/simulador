#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=============================================
#
# Copyright 2012 David Racca and Matias Molina.
#
# This file is part of ADIUC Salary Calculator.
#
# ADIUC Salary Calculator is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published 
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ADIUC Salary Calculator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ADIUC Salary Calculator.  If not, see 
# <http://www.gnu.org/licenses/>.
#
#=============================================

import sys
import os
import pdb
from datetime import date
from antiguedad_data import complete_antiguedad
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


#################################
# Tabla de periodos #
#################################

def addPeriodo(desde, hasta):
    if not Periodo.objects.filter(desde=desde, hasta=hasta).exists():
        r = Periodo(desde=desde, hasta=hasta)
        r.save()
    return r

p1 = addPeriodo(
    desde=date(2011, 9, 01),
    hasta=date(2012, 2, 29)
)

p2 = addPeriodo(
    desde=date(2012, 3, 01),
    hasta=date(2012, 5, 31)
)

p3 = addPeriodo(
    desde=date(2012, 6, 01),
    hasta=date(2012, 8, 31)
)

p4 = addPeriodo(
    desde=date(2012, 9, 01),
    hasta=date(2020, 12, 31)
)

p5 = addPeriodo(
    desde=date(2011, 9, 01),
    hasta=date(2020, 12, 31)
)


def add_retencion(codigo, nombre, aplicacion, modo):

    r = None
    if not Retencion.objects.filter(codigo=codigo, nombre=nombre, aplicacion=aplicacion, modo=modo).exists():
        r = Retencion(codigo=codigo, nombre=nombre, aplicacion=aplicacion, modo=modo)
        r.save()
    else:
        r = Retencion.objects.get(codigo=codigo, nombre=nombre, aplicacion=aplicacion, modo=modo)
    return r


def add_remuneracion(codigo, nombre, aplicacion, modo, remunerativo, bonificable):

    r = None
    if not Remuneracion.objects.filter(
        codigo=codigo,
        nombre=nombre,
        aplicacion=aplicacion,
        modo=modo,
        remunerativo=remunerativo,
        bonificable=bonificable).exists():
        r = Remuneracion(
            codigo=codigo,
            nombre=nombre,
            aplicacion=aplicacion,
            modo=modo,
            remunerativo=remunerativo,
            bonificable=bonificable)
        r.save()
    else:
        r = Remuneracion.objects.get(
                codigo=codigo,
                nombre=nombre,
                aplicacion=aplicacion,
                modo=modo,
                remunerativo=remunerativo,
                bonificable=bonificable
        )
    return r


def add_retencion_porcentual(retencion, porcentaje, vigencia):

    if not RetencionPorcentual.objects.filter(
        retencion=retencion,
        porcentaje=porcentaje,
        vigencia=vigencia).exists():
        r = RetencionPorcentual(
            retencion=retencion,
            porcentaje=porcentaje,
            vigencia=vigencia
        )
        r.save()


def add_remuneracion_porcentual(remuneracion, porcentaje, vigencia, sobre_referencia, nomenclador):

    if not RemuneracionPorcentual.objects.filter(
        remuneracion=remuneracion,
        porcentaje=porcentaje,
        vigencia=vigencia,
        sobre_referencia=sobre_referencia,
        nomenclador=nomenclador).exists(
    ):
        r = RemuneracionPorcentual(
            remuneracion=remuneracion,
            porcentaje=porcentaje,
            vigencia=vigencia,
            sobre_referencia=sobre_referencia,
            nomenclador=nomenclador
        )
        r.save()


def add_retencion_fija(retencion, valor, vigencia):

    if not RetencionFija.objects.filter(
        retencion=retencion,
        valor=valor,
        vigencia=vigencia).exists(
    ):
        r = RetencionFija(
            retencion=retencion,
            valor=valor,
            vigencia=vigencia
        )
        r.save()


def add_remuneracion_fija(remuneracion, valor, vigencia):

    if not RemuneracionFija.objects.filter(
        remuneracion=remuneracion,
        valor=valor,
        vigencia=vigencia).exists(
    ):
        r = RemuneracionFija(
            remuneracion=remuneracion,
            valor=valor,
            vigencia=vigencia
        )
        r.save()

def add_remuneracion_fija_cargo(remuneracion, valor, vigencia, cargo):

    if not RemuneracionFijaCargo.objects.filter(
        remuneracion=remuneracion,
        valor=valor,
        vigencia=vigencia,
        cargo=cargo).exists(
    ):
        r = RemuneracionFijaCargo(
            remuneracion=remuneracion,
            valor=valor,
            vigencia=vigencia,
            cargo=cargo
        )
        r.save()

def add_remuneracion_nomenclador(remuneracion, porcentaje, vigencia, sobre_referencia, nomenclador, cargo):

    if not RemuneracionNomenclador.objects.filter(
        remuneracion=remuneracion,
        porcentaje=porcentaje,
        vigencia=vigencia,
        sobre_referencia=sobre_referencia,
        nomenclador=nomenclador,
        cargo=cargo).exists(
    ):
        r = RemuneracionNomenclador(
            remuneracion=remuneracion,
            porcentaje=porcentaje,
            vigencia=vigencia,
            sobre_referencia=sobre_referencia,
            nomenclador=nomenclador,
            cargo=cargo
        )
        r.save()

def add_retencion_daspu(retencion, porcentaje_minimo):
    
    if not RetencionDaspu.objects.filter(retencion=retencion, porcentaje_minimo=porcentaje_minimo).exists:
        r= RetencionDaspu(retencion=retencion, porcentaje_minimo=porcentaje_minimo)
        r.save()

def add_fondosolidario(retencion, valor, vigencia, concepto):

    if not RetencionFija.objects.filter(
        retencion=retencion,
        valor=valor,
        vigencia=vigencia,
        concepto=concepto).exists(
    ):
        r = RetencionFija(
            retencion=retencion,
            valor=valor,
            vigencia=vigencia,
            concepto=concepto
        )
        r.save()


##### Retenciones Porcentuales

# Retencion DASPU
r = add_retencion(
    codigo=u"40/0",
    nombre= u"DASPU",
    aplicacion=u"T",
    modo=u"P"
)
add_retencion_porcentual(
    retencion=r,
    porcentaje= 3.0,
    vigencia=p5
)

####
r = add_retencion(
    codigo=u"20/3",
    nombre= u"Aporte Fondo Adic. Universitario",
    aplicacion=u"U",
    modo=u"C"
)
add_retencion_porcentual(
    retencion = r,
    porcentaje = 2.0,
    vigencia=p5
)
####
r = add_retencion(
    codigo=u"20/9",
    nombre= u"Jubilación Régimen Especial",
    aplicacion=u"T",
    modo=u"C"
)
add_retencion_porcentual(
    retencion = r,
    porcentaje = 11.0,
    vigencia=p5
)
####
r = add_retencion(
    codigo="21/0",
    nombre= u"Caja Complementaria de Jub.",
    aplicacion=u"T",
    modo=u"C"
)
add_retencion_porcentual(
    retencion = r,
    porcentaje = 4.5,
    vigencia=p5
)
####
r = add_retencion(
    codigo=u"22/0",
    nombre= u"Ley 19032 Obra Soc. Jubilados",
    aplicacion=u"T",
    modo=u"C"
)
add_retencion_porcentual(
    retencion = r,
    porcentaje = 3.0,
    vigencia=p5
)
####
r = add_retencion(
    codigo=u"64/0",
    nombre= u"ADIUC - Afiliación",
    aplicacion=u"T",
    modo=u"P"
)
add_retencion_porcentual(
    retencion = r,
    porcentaje = 1.5,
    vigencia=p5
)

##### Retenciones Fijas

r = add_retencion(
    codigo=u"DAS/1",
    nombre= u"Sistema Integral de Sepelio (SIS)",
    aplicacion=u"T",
    modo=u"P"
)
add_retencion_fija(
    retencion = r,
    valor = 7.0,
    vigencia=p5
)

###
r = add_retencion(
    codigo=u"DAS/4",
    nombre= u"Fondo Solidario",
    aplicacion=u"T",
    modo=u"P"
)
add_retencion_fija(
    retencion = r,
    valor = 7.0,
    vigencia=p5
)
###
r = add_retencion(
    codigo=u"DAS/2",
    nombre= u"Subsidio por fallecimiento",
    aplicacion=u"T",
    modo=u"P"
)
add_retencion_fija(
    retencion = r,
    valor = 7.0,
    vigencia=p5
)

###
r = add_retencion(
    codigo=u"70/0",
    nombre= u"Seguro de vida Ley 13003",
    aplicacion=u"T",
    modo=u"P"
)
add_retencion_fija(
    retencion = r,
    valor = 3.8,
    vigencia=p5
)

###### Remuneraciones Porcentuales
r = add_remuneracion(
    codigo=u"03/0",
    nombre= u"Adicional por Antigüedad",
    aplicacion=u"T",
    modo=u"C",
    remunerativo=True,
    bonificable=False
)
# Call antiuedad_data function.
complete_antiguedad(r, p5)
## Ver: antiguedad_data.py
####
r = add_remuneracion(
    codigo=u"05/1",
    nombre= u"Adicional Título Doctorado",
    aplicacion=u"U",
    modo=u"C",
    remunerativo=True,
    bonificable=True
)
add_remuneracion_porcentual(
    remuneracion = r,
    porcentaje = 15.0,
    vigencia=p5,
    sobre_referencia=False,
    nomenclador=False
)
####
r = add_remuneracion(
    codigo=u"05/3",
    nombre= u"Adic. Tít. Doctorado Nivel Medio",
    aplicacion=u"P",
    modo=u"C",
    remunerativo=True,
    bonificable=True
)
add_remuneracion_porcentual(
    remuneracion = r,
    porcentaje = 15.0,
    vigencia=p5,
    sobre_referencia=False,
    nomenclador=False
)
####
r = add_remuneracion(
    codigo=u"05/2",
    nombre= u"Adicional Título Maestría",
    aplicacion=u"U",
    modo=u"C",
    remunerativo=True,
    bonificable=False
)
add_remuneracion_porcentual(
    remuneracion = r,
    porcentaje = 5.0,
    vigencia=p5,
    sobre_referencia=False,
    nomenclador=False
)
####
r = add_remuneracion(
    codigo=u"05/5",
    nombre= u"Adic. Tít. Maestría Nivel Medio",
    aplicacion=u"P",
    modo=u"C",
    remunerativo=True,
    bonificable=False
)
add_remuneracion_porcentual(
    remuneracion = r,
    porcentaje = 5.0,
    vigencia=p5,
    sobre_referencia=False,
    nomenclador=False
)
####

###### Remuneraciones Fijas
r = add_remuneracion(
    codigo=u"01/0",
    nombre= u"Sueldo Básico",
    aplicacion=u"T",
    modo=u"C",
    remunerativo=True,
    bonificable=True
)

r = add_remuneracion(
    codigo = "12/2",
    nombre = "FONID",
    aplicacion = 'P',
    modo = 'C',
    remunerativo = False,
    bonificable = False
)
