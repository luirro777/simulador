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

#### Objeto Retencion Fondo Solidario
ret_obj = Retencion.objects.get(codigo="DAS/4")

def addFondoSolidario(concepto,valor,vigencia_desde,vigencia_hasta):

    if not FondoSolidario.objects.filter(valor=valor, concepto=concepto, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta).exists():
    
        FondoSolidario(
                    retencion=ret_obj,
                    valor=valor,
                    concepto=concepto,
                    vigencia_desde=vigencia_desde,
                    vigencia_hasta=vigencia_hasta
                ).save()


#lista de asignaciones:(concepto, valor, desde, hasta)

fondos =[
('Fondo solidario para una persona (menor a 55 años)','13',date(2012, 1, 1),date(2012, 12, 31)),
('Fondo solidario para dos personas (menor a 55 años)','25',date(2012, 1, 1),date(2012, 12, 31)),
('Fondo solidario para tres personas (menor a 55 años)','34',date(2012, 1, 1),date(2012, 12, 31)),
('Fondo solidario para cuatro personas (menor a 55 años)','40',date(2012, 1, 1),date(2012, 12, 31)),
('Fondo solidario para cinco personas o más (menor a 55 años)','47',date(2012, 1, 1),date(2012, 12, 31)),
('Fondo solidario para una persona (mayor a 55 años)','55',date(2012, 1, 1),date(2012, 12, 31))
]

for a in fondos:
    addFondoSolidario(a[0],a[1],a[2],a[3])
