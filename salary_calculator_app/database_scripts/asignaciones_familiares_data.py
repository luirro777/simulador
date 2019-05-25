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

#### Objeto Remuneracion Asignación Familiar.
rem_obj = Remuneracion.objects.get(codigo="---")

def addAFamiliar(concepto, valor_min, valor_max, valor, vigencia_desde, vigencia_hasta):

    if valor_min != 'blank' and valor_max != 'blank' and valor != 'blank':
        if not AsignacionFamiliar.objects.filter(valor=valor, concepto=concepto,vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta,valor_min=valor_min, valor_max=valor_max).exists():
        
            AsignacionFamiliar(
                        remuneracion=rem_obj,
                        valor=valor,
                        concepto=concepto,
                        valor_min=valor_min,
                        valor_max=valor_max,
                        vigencia_desde=vigencia_desde,
                        vigencia_hasta=vigencia_hasta
                    ).save()

    elif valor_min!='blank' and valor_max=='blank' and valor=='blank':
        if not AsignacionFamiliar.objects.filter(concepto=concepto, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta, valor_min=valor_min).exists():
            AsignacionFamiliar(
                        remuneracion=rem_obj,
                        concepto=concepto,
                        valor_min=valor_min,
                        vigencia_desde=vigencia_desde,
                        vigencia_hasta=vigencia_hasta
                    ).save()
        
        
    elif valor_min!='blank' and valor_max!='blank' and valor=='blank':
        if not AsignacionFamiliar.objects.filter(concepto=concepto, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta, valor_min=valor_min, valor_max=valor_max).exists():
            AsignacionFamiliar(
                        remuneracion=rem_obj,
                        concepto=concepto,
                        valor_min=valor_min,
                        valor_max=valor_max,
                        vigencia_desde=vigencia_desde,
                        vigencia_hasta=vigencia_hasta
                    ).save
                
    elif valor_min!='blank' and valor_max=='blank' and valor!='blank':
        if not AsignacionFamiliar.objects.filter(valor=valor, concepto=concepto, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta, valor_min=valor_min,valor_max=NULL).exists():
            AsignacionFamiliar(
                        remuneracion=rem_obj,
                        valor=valor,
                        concepto=concepto,
                        valor_min=valor_min,
                        vigencia_desde=vigencia_desde,
                        vigencia_hasta=vigencia_hasta
                    ).save


    elif valor_min=='blank' and valor_max!='blank' and valor!='blank':
        if not AsignacionFamiliar.objects.filter(valor=valor, concepto=concepto, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta, valor_max=valor_max).exists():
            AsignacionFamiliar(
                        remuneracion=rem_obj,
                        valor=valor,
                        concepto=concepto,
                        valor_max=valor_max,
                        vigencia_desde=vigencia_desde,
                        vigencia_hasta=vigencia_hasta
                    ).save
                
    elif valor_min=='blank' and valor_max=='blank' and valor!='blank':
        if not AsignacionFamiliar.objects.filter(valor=valor, concepto=concepto, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta).exists():

            AsignacionFamiliar(
                        remuneracion=rem_obj,
                        valor=valor,
                        concepto=concepto,
                        vigencia_desde=vigencia_desde,
                        vigencia_hasta=vigencia_hasta
                    ).save
                
    elif valor_min=='blank' and valor_max!='blank' and valor=='blank':
        if not AsignacionFamiliar.objects.filter(concepto=concepto, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta, valor_max=valor_max).exists():
            AsignacionFamiliar(
                        remuneracion=rem_obj,
                        valor_max=valor_max,
                        concepto=concepto,
                        vigencia_desde=vigencia_desde,
                        vigencia_hasta=vigencia_hasta
                    ).save
    else:
        if not AsignacionFamiliar.objects.filter(concepto=concepto, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta).exists():
            AsignacionFamiliar(
                remuneracion=rem_obj,
                concepto=concepto,
                vigencia_desde=vigencia_desde,
                vigencia_hasta=vigencia_hasta
            ).save()

#lista de asignaciones:(concepto, min, max, valor, desde, hasta)
inf = 50000
asignaciones =[
('Nacimiento','100','5200','600',date(2012, 1, 1),date(2012, 12, 31)),
('Adopción','100','5200','3600',date(2012, 1, 1),date(2012, 12, 31)),
('Matrimonio','100','5200','900',date(2012, 1, 1),date(2012, 12, 31)),
('Prenatal','100','2800','270',date(2012, 1, 1),date(2012, 12, 31)),
('Prenatal','2800.01','4000','204',date(2012, 1, 1),date(2012, 12, 31)),
('Prenatal','4000.01','5200','136',date(2012, 1, 1),date(2012, 12, 31)),
('Ayuda escolar por hijo con discapacidad',0,inf,'170',date(2012, 1, 1),date(2012, 12, 31)),
('Hijo','100','2800','270',date(2012, 1, 1),date(2012, 12, 31)),
('Hijo','2800.01','4000','204',date(2012, 1, 1),date(2012, 12, 31)),
('Hijo','4000.01','5200','136',date(2012, 1, 1),date(2012, 12, 31)),
('Hijo con discapacidad','0','2800','1080',date(2012, 1, 1),date(2012, 12, 31)),
('Hijo con discapacidad','2800.01','4000','810',date(2012, 1, 1),date(2012, 12, 31)),
('Hijo con discapacidad','4000.01',0,'540',date(2012, 1, 1),date(2012, 12, 31)),
]

for a in asignaciones:
    addAFamiliar(a[0],a[1],a[2],a[3],a[4],a[5])
