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


#=============================================#
#           CARGOS PREUNIVERSITARIOS          #
#=============================================#

def add_cargo_preuniv(nombre, lu, pampa, horas, tipo_horas, pago_por_hora):
    """Agrega un cargo pre univ a la BD."""

    if DenominacionCargo.objects.filter(nombre=nombre).exists():
        den = DenominacionCargo.objects.get(nombre=nombre)
    else:
        den = DenominacionCargo(nombre=nombre)
        den.save()
 
    c = None
    if CargoPreUniversitario.objects.filter(
        lu=lu,
        pampa=pampa,
        denominacion=den,
        horas=horas,
        tipo_horas=tipo_horas,
        pago_por_hora=pago_por_hora
    ).exists():
        c = CargoPreUniversitario.objects.get(
            lu=lu,
            pampa=pampa,
            denominacion=den,
            horas=horas,
            tipo_horas=tipo_horas,
            pago_por_hora=pago_por_hora
        )
    else:
        c = CargoPreUniversitario(
            lu=lu,
            pampa=pampa,
            denominacion=den,
            horas=horas,
            tipo_horas=tipo_horas,
            pago_por_hora=pago_por_hora
        )
        c.save()

#    if c:
#        for rem in RemuneracionPorcentual.objects.filter(remuneracion__aplicacion='P', remuneracion__modo='C'):
#            c.rem_porcentuales.add(rem)
#        for rem in RemuneracionPorcentual.objects.filter(remuneracion__aplicacion='T', remuneracion__modo='C'):
#            c.rem_porcentuales.add(rem)
#        for ret in RetencionPorcentual.objects.filter(retencion__aplicacion='P', retencion__modo='C'):
#            c.ret_porcentuales.add(ret)
#        for ret in RetencionPorcentual.objects.filter(retencion__aplicacion='T', retencion__modo='C'):
#            c.ret_porcentuales.add(ret)

    return c


### Salario object
salario_obj = Remuneracion.objects.get(codigo="10/0")

def add_salario_basico(cargo, valor, vigencia_desde, vigencia_hasta):
    """Crea un salario basico nuevo si no existia ya en la BD con los 
    valores dados y la asocia al cargo que toma por parametro."""

    if SalarioBasico.objects.filter(remuneracion=salario_obj, cargo=cargo, valor=valor, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta).exists():
        g = SalarioBasico.objects.get(remuneracion=salario_obj, cargo=cargo, valor=valor, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta)
    else:
        g = SalarioBasico(remuneracion=salario_obj, cargo=cargo, valor=valor, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta)
        g.save()


rem = Remuneracion.objects.get(codigo="12/2")

def add_fonid(cargo, valor, vigencia_desde, vigencia_hasta):

    if not RemuneracionFijaCargo.objects.filter(
        cargo=cargo,
        valor=valor,
        remuneracion=rem,
        vigencia_desde=vigencia_desde,
        vigencia_hasta=vigencia_hasta).exists():

            r = RemuneracionFijaCargo(
                cargo=cargo,
                valor=valor,
                remuneracion=rem,
                vigencia_desde=vigencia_desde,
                vigencia_hasta=vigencia_hasta).save()


def add_garantia(cargo, valor, vigencia_desde, vigencia_hasta):
#def add_garantia(cargo, valor_minimo, valor_sin_titulo, valor_doctorado, valor_master, antiguedad_min, antiguedad_max, vigencia_desde, vigencia_hasta):
    """Crea una garantia salarial nueva si no existia ya en la BD con los 
    valores dados y la asocia al cargo que toma por parametro."""

#    if GarantiaSalarial.objects.filter(
#        cargo=cargo,
#        valor_minimo=valor_minimo,
#        valor_sin_titulo=valor_sin_titulo,
#        valor_doctorado=valor_doctorado,
#        valor_master=valor_master,
#        antiguedad_min=antiguedad_min,
#        antiguedad_max=antiguedad_max,
#        vigencia_desde=vigencia_desde,
#        vigencia_hasta=vigencia_hasta
#    ).exists():
#        g = GarantiaSalarial.objects.get(
#            cargo=cargo,
#            valor_minimo=valor_minimo,
#            valor_sin_titulo=valor_sin_titulo,
#            valor_doctorado=valor_doctorado,
#            valor_master=valor_master,
#            antiguedad_min=antiguedad_min,
#            antiguedad_max=antiguedad_max,
#            vigencia_desde=vigencia_desde,
#            vigencia_hasta=vigencia_hasta
#        )
#    else:
#        g = GarantiaSalarial(
#           cargo=cargo,
#           valor_minimo=valor_minimo,
#           valor_sin_titulo=valor_sin_titulo,
#           valor_doctorado=valor_doctorado,
#           valor_master=valor_master,
#           antiguedad_min=antiguedad_min,
#           antiguedad_max=antiguedad_max,
#           vigencia_desde=vigencia_desde,
#           vigencia_hasta=vigencia_hasta
#        )
#        g.save()
    return


############### VIGENCIAS
sep_vigencia_desde = date(2011, 9, 1)
sep_vigencia_hasta = date(2012, 2, 29)

mar_vigencia_desde = date(2012, 3, 1)
mar_vigencia_hasta = date(2012, 5, 31)

jun_vigencia_desde = date(2012, 6, 1)
jun_vigencia_hasta = date(2012, 8, 31)

sep12_vigencia_desde = date(2012, 9, 1)
sep12_vigencia_hasta = date(2012, 12, 31)


# Base: Copiar y pegar este
###############
#c = add_cargo_preuniv(
#    nombre = u'', 
#    lu = u'', 
#    pampa = u'', 
#    horas = , 
#    tipo_horas = '',
#    pago_por_hora = False
#)
## Septiembre 2011
#add_salario_basico(
#    cargo = c,
#    valor = ,
#    vigencia_desde = sep_vigencia_desde,
#    vigencia_hasta = sep_vigencia_hasta,
#)
## Marzo 2012
#add_salario_basico(
#    cargo = c,
#    valor = ,
#    vigencia_desde = mar_vigencia_desde,
#    vigencia_hasta = mar_vigencia_hasta
#)
## Junio 2012
#add_salario_basico(
#    cargo = c,
#    valor = ,
#    vigencia_desde = jun_vigencia_desde,
#    vigencia_hasta = jun_vigencia_hasta
#)
#add_garantia(
#    cargo = c,
#    valor_minimo = ,
#    valor_sin_titulo=valor_sin_titulo,
#    valor_doctorado=valor_doctorado,
#    valor_master=valor_master,
#    antiguedad_min=antiguedad_min,
#    antiguedad_max=antiguedad_max,
#    vigencia_desde = mar_vigencia_desde,
#    vigencia_hasta = jun_vigencia_hasta
#)
##############
c = add_cargo_preuniv(
    nombre = u'Vice Director de 1°', 
    lu = 1, 
    pampa = 201,
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 5079.60,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5689.15,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5993.93,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 6146.32,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
#add_garantia(
#    cargo = c,
#    valor_minimo = 5600,
#    valor_sin_titulo=5600,
#    valor_doctorado=5600,
#    valor_master=5600,
#    antiguedad_min=0,
#    antiguedad_max=1,
#    vigencia_desde = mar_vigencia_desde,
#    vigencia_hasta = jun_vigencia_hasta
#)
##############
c = add_cargo_preuniv(
    nombre = u'Regente de 1°', 
    lu = 2, 
    pampa = 202, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 4830.76,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5410.45,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5700.30,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 5845.22,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5600,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
##############
c = add_cargo_preuniv(
    nombre = u'Jefe Gral Ens.Práctica', 
    lu = 3, 
    pampa = 203, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 4442.50,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 4975.60,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5242.15,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 5375.43,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 189.26,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2464.76,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
##############
c = add_cargo_preuniv(
    nombre = u'Profesor TC', 
    lu = 4, 
    pampa = 204, 
    horas = 36, 
    tipo_horas = 'C',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 6092.64,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 6823.76,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 7189.32,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 7372.09,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5600,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)

###############
c = add_cargo_preuniv(
    nombre = u'Asesor Pedagógico', 
    lu = 10, 
    pampa = 205, 
    horas = 36, 
    tipo_horas = 'C',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 6092.64,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 6823.76,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 7189.32,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 7372.09,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5600,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)

###############
c = add_cargo_preuniv(
    nombre = u'Jefe Labor. Informática', 
    lu = 11, 
    pampa = 206, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 3427.00,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3838.24,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 4043.86,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 4146.67,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 215,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2800,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Asesor Psicopedagógico', 
    lu = 12, 
    pampa = 207, 
    horas = 18, 
    tipo_horas = 'C',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 3046.32,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3411.88,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3594.66,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3686.05,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 257.88,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 3358.47,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Director Escuela Superior', 
    lu = 15, 
    pampa = 208, 
    horas = 35, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2445.48,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2738.94,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2885.67,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2959.03,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)

###############
c = add_cargo_preuniv(
    nombre = u'Ayudante Clases Práct.(02)', 
    lu = 16, 
    pampa = 209, 
    horas = 12, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1988.92,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2227.58,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2346.92,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2406.59,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 129,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 1680,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Vice Director Escuela Superior', 
    lu = 17, 
    pampa = 210, 
    horas = 35, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2306.97,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2583.81,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2722.22,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2791.43,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Rector de 1° Categoría', 
    lu = 18, 
    pampa = 211, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 5394.50,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 6041.84,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 6365.51,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 6527.35,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5600,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)

###############
c = add_cargo_preuniv(
    nombre = u'Ayudante Clases Prácticas', 
    lu = 19, 
    pampa = 212, 
    horas = 21, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1749.70,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1959.66,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2064.65,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2117.14,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Director de 3° Categoría', 
    lu = 21, 
    pampa = 213, 
    horas = 35, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1994.97,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2234.37,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2354.06,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2413.91,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Prosecretario 1° (Esc.Com.)', 
    lu = 22, 
    pampa = 240, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 3300.25,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3696.28,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3894.30,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3993.30,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 215,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2800,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Regente de Esc.Superior', 
    lu = 23, 
    pampa = 214, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 3290.75,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3685.64,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3883.09,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3981.81,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 215,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2800,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Regente de 1° Esc.Superior', 
    lu = 24, 
    pampa = 215, 
    horas = 35, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2219.31,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2485.62,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2618.78,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2685.36,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2800,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Secret. de 1° Categoría', 
    lu = 25, 
    pampa = 216, 
    horas = 35, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1786.14,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2000.47,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2107.64,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2161.22,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Secretario Esc.Superior', 
    lu = 29, 
    pampa = 217, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 3617.50,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 4051.60,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 4268.65,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 4377.18,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 215,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2800,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. Jefe Trab.Prácticos', 
    lu = 30, 
    pampa = 218, 
    horas = 21, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1769.20,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1981.50,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2087.66,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2140.73,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Bibliot. Ley 22.416', 
    lu = 33, 
    pampa = 219, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2430.97,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2722.69,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2868.55,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2941.48,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 178.49,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2324.51,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. Jefe Trab.Prácticos', 
    lu = 35, 
    pampa = 220, 
    horas = 21, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1769.20,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1981.50,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2087.66,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2140.73,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. Centro Deportivo', 
    lu = 37, 
    pampa = 221, 
    horas = 17, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1621.95,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1816.58,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1913.90,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 1962.56,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Maestro Ayud.Ens.Práctico', 
    lu = 38, 
    pampa = 222, 
    horas = 18, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1497.01,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1676.65,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1766.47,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 1811.38,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Preceptores de 1°', 
    lu = 39, 
    pampa = 223, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2741.75,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3070.76,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3235.27,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3317.52,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 215,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2800,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Ayudante Trab.Prácticos', 
    lu = 40, 
    pampa = 224, 
    horas = 21, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1749.70,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1959.66,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2064.65,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2117.14,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Vice Rector Escuela Artes', 
    lu = 41, 
    pampa = 225, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2306.97,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2583.81,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2722.22,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2791.43,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Bibliot.Ens. Superior', 
    lu = 42, 
    pampa = 226, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2446.42,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2739.98,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2886.77,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2960.16,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 184.53,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2403.16,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Preceptores', 
    lu = 43, 
    pampa = 227, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2549.53,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2855.47,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3008.45,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3084.93,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 215,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2800,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Hs. Cátedra Terciario', 
    lu = 44, 
    pampa = 228, 
    horas = 1, 
    tipo_horas = 'C',
    pago_por_hora = True
)
add_salario_basico(
    cargo = c,
    valor = 211.55,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 236.94,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 249.63,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 255.98,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 17.92,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 233.42,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Hs. Cátedra Secundario', 
    lu = 45, 
    pampa = 229, 
    horas = 1, 
    tipo_horas = 'C',
    pago_por_hora = True
)
add_salario_basico(
    cargo = c,
    valor = 169.24,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 189.55,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 199.70,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 204.78,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 14.33,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 186.58,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Hs. Cát. Inherentes a cargos', 
    lu = 46, 
    pampa = 230, 
    horas = 12, 
    tipo_horas = 'C',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2030.88,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2274.59,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2396.44,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2457.36,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Rector Educación Artística', 
    lu = 49, 
    pampa = 231, 
    horas = 12, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2198.41,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2462.22,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2594.12,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2660.08,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Profesor T.P (4)', 
    lu = 50, 
    pampa = 239, 
    horas = 12, 
    tipo_horas = 'C',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2092.09,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2343.14,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2468.66,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2531.42,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 171.92,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2238.98,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Equipo Tec.Pedagógico', 
    lu = 51, 
    pampa = 232, 
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 3618.6,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 4052.83,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 4269.95,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 4378.51,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 215,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2800,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Secretario 1° Categoría', 
    lu = 52, 
    pampa = 233,
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 4511.53,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5052.91,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5323.61,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 5458.95,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5600,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Prosecretario Nivel Superior', 
    lu = 53, 
    pampa = 234,
    horas = 0, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1786.14,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2000.47,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2107.64,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2161.22,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'J.T.P T.C (Esc. Comercio)', 
    lu = 55, 
    pampa = 235,
    horas = 15, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2220.15,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2486.57,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2619.78,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2686.38,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 161.25,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2100,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. T.P (1)', 
    lu = 57, 
    pampa = 236,
    horas = 30, 
    tipo_horas = 'C',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 5077.2,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5686.46,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5991.10,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 6143.41,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 429.84,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5597.96,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. T.P (2)', 
    lu = 58, 
    pampa = 237,
    horas = 24, 
    tipo_horas = 'C',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 4061.76,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 4549.17,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 4792.88,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 4914.73,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 343.84,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 4477.96,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. T.P (3)', 
    lu = 59, 
    pampa = 238,
    horas = 18, 
    tipo_horas = 'C',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 3046.32,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3411.88,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3594.66,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3686.05,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 257.88,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 3358.47,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Auxiliar Docente', 
    lu = 80, 
    pampa = 241,
    horas = 25, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2856.00,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3198.72,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3370.08,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3455.76,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 208.71,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2718.04,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Director 1° D.E', 
    lu = 81, 
    pampa = 301,
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 9710.10,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 10875.31,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 11457.92,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 11749.22,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5600,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Vice Director 1° D.E', 
    lu = 82, 
    pampa = 302,
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 8568.00,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 9596.16,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 10110.24,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 10367.28,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5600,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Regente de 1° D.E', 
    lu = 83, 
    pampa = 303,
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 3039.92,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3404.71,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3587.11,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3678.30,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Sub Regente de 1° Cat. D.E', 
    lu = 84, 
    pampa = 304, 
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 5428.80,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 6080.26,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 6405.98,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 6568.85,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5600,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Sub Regente de 1° Categoría', 
    lu = 85, 
    pampa = 305, 
    horas = 27.3, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 3293.47,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3688.69,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3886.30,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 6568.85,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 215,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2800,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Secretario de 1° Categ.D.E', 
    lu = 86, 
    pampa = 306, 
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 6511.50,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 7292.88,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 7683.57,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 7878.92,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5600,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Dpto D.E', 
    lu = 87, 
    pampa = 307, 
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2309.53,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2586.67,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2725.24,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2794.53,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Gabinete Psicoped. D.E', 
    lu = 88, 
    pampa = 308, 
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2329.00,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2608.48,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2748.22,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2818.09,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Gabinetista D.E', 
    lu = 89, 
    pampa = 309, 
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2264.08,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2535.77,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2671.61,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2739.543,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Asesor Pedagógico', 
    lu = 90, 
    pampa = 310, 
    horas = 27.3, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1592.44,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1783.53,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 1879.08,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 1926.85,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Preceptores 1° D.E', 
    lu = 91, 
    pampa = 311, 
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 4935.15,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5527.37,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5823.48,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 5971.53,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5600,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Preceptores 1°', 
    lu = 92, 
    pampa = 312, 
    horas = 27.3, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2993.99,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3353.27,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3532.91,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3622.73,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 215,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2800,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Ayud. Gabinete Práctico D.E', 
    lu = 93, 
    pampa = 313, 
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2196.98,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2460.62,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2592.44,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2658.35,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Ayud. Gabinete Práctico', 
    lu = 94, 
    pampa = 314, 
    horas = 15, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2229.88,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2497.47,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2631.26,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2698.15,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 161.25,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2100,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Bibliotecario D.E', 
    lu = 95, 
    pampa = 315, 
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2230.53,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2498.19,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2632.02,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2698.94,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Preceptor D.E', 
    lu = 96, 
    pampa = 316, 
    horas = 45, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 4589.17,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5139.87,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 5415.22,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 5552.90,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 430,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 5600,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Preceptor', 
    lu = 97, 
    pampa = 317, 
    horas = 27.3, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2572.45,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2881.14,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 3035.49,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 3112.66,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 213.63,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 2782.18,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Hs Cát. Inherentes a cargos', 
    lu = 98, 
    pampa = 319, 
    horas = 12, 
    tipo_horas = 'C',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 2030.88,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2274.59,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2396.44,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2457.36,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Horas Cátedra Secundario', 
    lu = 98, 
    pampa = 318, 
    horas = 0, 
    tipo_horas = 'C',
    pago_por_hora = True
)
add_salario_basico(
    cargo = c,
    valor = 169.24,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 189.55,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 199.70,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 204.78,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 14.33,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 204.78,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
###############
c = add_cargo_preuniv(
    nombre = u'Ayudante Gab. Psicoped.', 
    lu = 99, 
    pampa = 242, 
    horas = 10, 
    tipo_horas = 'R',
    pago_por_hora = False
)
add_salario_basico(
    cargo = c,
    valor = 1896.14,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2123.68,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = mar_vigencia_hasta,
)
add_salario_basico(
    cargo = c,
    valor = 2237.45,
    vigencia_desde = jun_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
add_salario_basico(
    cargo = c,
    valor = 2294.33,
    vigencia_desde = sep12_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_fonid(
    cargo = c,
    valor = 107.5,
    vigencia_desde = sep_vigencia_desde,
    vigencia_hasta = sep12_vigencia_hasta
)
add_garantia(
    cargo = c,
    valor = 1400,
    vigencia_desde = mar_vigencia_desde,
    vigencia_hasta = jun_vigencia_hasta
)
