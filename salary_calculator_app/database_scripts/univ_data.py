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

from preuniv_data import add_salario_basico
from preuniv_data import add_garantia


#=============================================#
#       CARGOS UNIVERSITARIOS                 #
#=============================================#

def add_cargo_univ(nombre, lu, pampa, dedicacion):
    """Agrega un cargo univ a la BD y le asigna todas las remuneraciones y 
    retenciones cuya aplicacion sean los cargos univs y que tengan modo
    'por cargo'."""

    if DenominacionCargo.objects.filter(nombre=nombre).exists():
        den = DenominacionCargo.objects.get(nombre=nombre)
    else:
        den = DenominacionCargo(nombre=nombre)
        den.save()
 
    c = None
    if CargoUniversitario.objects.filter(
        lu=lu,
        pampa=pampa,
        denominacion=den,
        dedicacion=dedicacion
    ).exists():
        c = CargoUniversitario.objects.get(
            lu=lu,
            pampa=pampa,
            denominacion=den,
            dedicacion=dedicacion
        )
    else:
        c = CargoUniversitario(
            lu=lu,
            pampa=pampa,
            denominacion=den,
            dedicacion=dedicacion
        )
        c.save()

#    if c:
#        for rem in RemuneracionPorcentual.objects.filter(remuneracion__aplicacion='U', remuneracion__modo='C'):
#            c.rem_porcentuales.add(rem)
#        for rem in RemuneracionPorcentual.objects.filter(remuneracion__aplicacion='T', remuneracion__modo='C'):
#            c.rem_porcentuales.add(rem)
#        for ret in RetencionPorcentual.objects.filter(retencion__aplicacion='U', retencion__modo='C'):
#            c.ret_porcentuales.add(ret)
#        for ret in RetencionPorcentual.objects.filter(retencion__aplicacion='T', retencion__modo='C'):
#            c.ret_porcentuales.add(ret)

    return c


############### VIGENCIAS
sep_vigencia_desde = date(2011, 9, 1)
sep_vigencia_hasta = date(2012, 2, 29)

mar_vigencia_desde = date(2012, 3, 1)
mar_vigencia_hasta = date(2012, 5, 31)

jun_vigencia_desde = date(2012, 6, 1)
jun_vigencia_hasta = date(2012, 8, 31)

sep12_vigencia_desde = date(2012, 9, 1)
sep12_vigencia_hasta = date(2012, 12, 31)


######################
c = add_cargo_univ(
    nombre="Profesor Titular",
    lu=5,
    pampa=101,
    dedicacion="D.E"
)
add_salario_basico(
    cargo = c,
    valor = 6929.41,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 7749.22,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 8159.13,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 8438.55,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre="Profesor Titular",
    lu=13,
    pampa=102,
    dedicacion="D.S.E"
)
add_salario_basico(
    cargo = c,
    valor = 3444.34,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3854.25,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 4059.20,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 4198.91,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre="Profesor Titular",
    lu=27,
    pampa=103,
    dedicacion="D.S"
)
add_salario_basico(
    cargo = c,
    valor = 1716.98,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1921.93,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2024.41,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2094.26,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre="Profesor Asociado",
    lu=6,
    pampa=105,
    dedicacion="D.E"
)
add_salario_basico(
    cargo = c,
    valor = 6238.57,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 6976.15,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 7344.95,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 7585.28,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre="Profesor Asociado",
    lu=8,
    pampa=106,
    dedicacion="D.S.E"
)
add_salario_basico(
    cargo = c,
    valor = 3100.69,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3469.48,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3653.88,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3774.04,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre="Profesor Asociado",
    lu=54,
    pampa=107,
    dedicacion="D.S"
)
add_salario_basico(
    cargo = c,
    valor = 1545.25,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1729.65,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1821.84,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 1881.93,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre="Profesor Adjunto",
    lu=7,
    pampa=109,
    dedicacion="D.E"
)
add_salario_basico(
    cargo = c,
    valor = 5541.07,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 6196.43,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 6524.11,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 6725.08,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre="Profesor Adjunto",
    lu=20,
    pampa=110,
    dedicacion="D.S.E"
)
add_salario_basico(
    cargo = c,
    valor = 2755.95,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3083.63,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3247.47,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3347.96,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre="Profesor Adjunto",
    lu=31,
    pampa=111,
    dedicacion="D.S"
)
add_salario_basico(
    cargo = c,
    valor = 1373.02,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1536.86,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1618.78,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 1669.02,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre="Profesor Asistente",
    lu=9,
    pampa=113,
    dedicacion="D.E"
)
add_salario_basico(
    cargo = c,
    valor = 4844.37,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5417.50,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5704.07,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 5865.98,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre="Profesor Asistente",
    lu=26,
    pampa=114,
    dedicacion="D.S.E"
)
add_salario_basico(
    cargo = c,
    valor = 2411.57,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2698.14,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2841.42,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2922.37,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre="Profesor Asistente",
    lu=32,
    pampa=115,
    dedicacion="D.S"
)
add_salario_basico(
    cargo = c,
    valor = 1200.91,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1344.19,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1415.83,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 1456.31,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre='Profesor Ayudante "A"',
    lu=14,
    pampa=117,
    dedicacion="D.E"
)
add_salario_basico(
    cargo = c,
    valor = 4153.76,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 4644.66,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 4890.12,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 5012.84,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre='Profesor Ayudante "A"',
    lu=28,
    pampa=118,
    dedicacion="D.S.E"
)
add_salario_basico(
    cargo = c,
    valor = 2067.70,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2313.15,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2435.88,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2497.24,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre='Profesor Ayudante "A"',
    lu=34,
    pampa=119,
    dedicacion="D.S"
)
add_salario_basico(
    cargo = c,
    valor = 1029.07,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1151.80,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1213.16,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 1243.84,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
######################
c = add_cargo_univ(
    nombre='Profesor Ayudante "B"',
    lu=36,
    pampa=121,
    dedicacion="D.S"
)
add_salario_basico(
    cargo = c,
    valor = 823.93,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 922.11,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 971.20,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 995.75,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
