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

def addAntiguedadUniv(remuneracion, anio, porcentaje, vigencia):
    if not AntiguedadUniversitaria.objects.filter(anio=anio, porcentaje=porcentaje, vigencia).exists():
        AntiguedadUniversitaria(
            remuneracion=remuneracion,
            anio=anio,
            porcentaje=porcentaje,
            vigencia=vigencia
        ).save()

def addAntiguedadPreUniv(remuneracion, anio, porcentaje, vigencia):
    if not AntiguedadUniversitaria.objects.filter(anio=anio, porcentaje=porcentaje, vigencia).exists():
        AntiguedadUniversitaria(
            remuneracion=remuneracion,
            anio=anio,
            porcentaje=porcentaje,
            vigencia=vigencia
        ).save()

def complete_antiguedad(remuneracion, periodo):
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=0,
        porcentaje=20.,
        vigencia=periodo
    )
    ###########
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=1,
        porcentaje=20.,
        vigencia=periodo
    )
    ###########
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=2,
        porcentaje=20.,
        vigencia=periodo
    )
    ###########
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=5,
        porcentaje=30.,
        vigencia=periodo
    )
    ###########
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=7,
        porcentaje=40.,
        vigencia=periodo
    )
    ###########
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=10,
        porcentaje=50.,
        vigencia=periodo
    )
    ###########
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=12,
        porcentaje=60.,
        vigencia=periodo
    )
    ###########
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=15,
        porcentaje=70.,
        vigencia=periodo
    )
    ###########
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=17,
        porcentaje=80.,
        vigencia=periodo
    )
    ###########
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=20,
        porcentaje=100.,
        vigencia=periodo
    )
    ###########
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=22,
        porcentaje=110.,
        vigencia=periodo
    )
    ###########
    addAntiguedadUniv(
        remuneracion=remuneracion,
        anio=24,
        porcentaje=120.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=0,
        porcentaje=0.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=1,
        porcentaje=10.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=2,
        porcentaje=15.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=5,
        porcentaje=30.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=7,
        porcentaje=40.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=10,
        porcentaje=50.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=12,
        porcentaje=60.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=15,
        porcentaje=70.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=17,
        porcentaje=80.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=20,
        porcentaje=100.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=22,
        porcentaje=110.,
        vigencia=periodo
    )
    ###########
    addAntiguedadPreUniv(
        remuneracion=remuneracion,
        anio=24,
        porcentaje=120.,
        vigencia=periodo
    )
