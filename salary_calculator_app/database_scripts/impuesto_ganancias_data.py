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

vigencia_desde = date(2011,1,1)
vigencia_hasta = date(2012,12,31)

retencion = Retencion.objects.get(codigo='42/0')

#######################
deduccion_data = ImpuestoGananciasDeducciones(
    ganancia_no_imponible = 12960,
    por_conyuge = 14400,
    por_hijo_menor_24_anios = 7200,
    por_descendiente = 5400,
    por_ascendiente = 5400,
    por_suegro_yerno_nuera = 5400,
    deduccion_especial = 62208,
    vigencia_desde = vigencia_desde,
    vigencia_hasta = vigencia_hasta
)
deduccion_data.save()
#######################
tabla = ImpuestoGananciasTabla(
    ganancia_neta_min = 0,
    ganancia_neta_max = 10000,
    impuesto_fijo = 0,
    impuesto_porcentual = 9,
    sobre_exedente_de = 0,
    vigencia_desde = vigencia_desde,
    vigencia_hasta = vigencia_hasta
)
tabla.save()
#######################
tabla = ImpuestoGananciasTabla(
    ganancia_neta_min = 10000,
    ganancia_neta_max = 20000,
    impuesto_fijo = 900,
    impuesto_porcentual = 14,
    sobre_exedente_de = 10000,
    vigencia_desde = vigencia_desde,
    vigencia_hasta = vigencia_hasta
)
tabla.save()
#######################
tabla = ImpuestoGananciasTabla(
    ganancia_neta_min = 20000,
    ganancia_neta_max = 30000,
    impuesto_fijo = 2300,
    impuesto_porcentual = 19,
    sobre_exedente_de = 20000,
    vigencia_desde = vigencia_desde,
    vigencia_hasta = vigencia_hasta
)
tabla.save()
#######################
tabla = ImpuestoGananciasTabla(
    ganancia_neta_min = 30000,
    ganancia_neta_max = 60000,
    impuesto_fijo = 4200,
    impuesto_porcentual = 23,
    sobre_exedente_de = 30000,
    vigencia_desde = vigencia_desde,
    vigencia_hasta = vigencia_hasta
)
tabla.save()
#######################
tabla = ImpuestoGananciasTabla(
    ganancia_neta_min = 60000,
    ganancia_neta_max = 90000,
    impuesto_fijo = 11100,
    impuesto_porcentual = 27,
    sobre_exedente_de = 60000,
    vigencia_desde = vigencia_desde,
    vigencia_hasta = vigencia_hasta
)
tabla.save()
#######################
tabla = ImpuestoGananciasTabla(
    ganancia_neta_min = 90000,
    ganancia_neta_max = 120000,
    impuesto_fijo = 19200,
    impuesto_porcentual = 31,
    sobre_exedente_de = 90000,
    vigencia_desde = vigencia_desde,
    vigencia_hasta = vigencia_hasta
)
tabla.save()
#######################
tabla = ImpuestoGananciasTabla(
    ganancia_neta_min = 120000,
    ganancia_neta_max = 99999999,
    impuesto_fijo = 28500,
    impuesto_porcentual = 35,
    sobre_exedente_de = 120000,
    vigencia_desde = vigencia_desde,
    vigencia_hasta = vigencia_hasta
)
tabla.save()
#######################
