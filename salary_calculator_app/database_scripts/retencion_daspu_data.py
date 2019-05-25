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


ret_obj = Retencion.objects.get(codigo="40/0")

def addDASPU(porcentaje_minimo,porcentaje,vigencia_desde,vigencia_hasta,cargo):
    r = RetencionPorcentual.objects.get(retencion=ret_obj,porcentaje=porcentaje,vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta)
    
    if not RetencionDaspu.objects.filter(porcentaje_minimo=porcentaje_minimo, retencion=r).exists():
        RetencionDaspu(
            retencion=r,
            porcentaje_minimo=porcentaje_minimo,
            cargo_referencia=cargo
            ).save()

c = CargoUniversitario.objects.get(lu='28')
data =[(8.0,3.0,date(2012, 1, 1),date(2012, 12, 31), c)]

for d in data:
    addDASPU(d[0],d[1],d[2],d[3],d[4])

