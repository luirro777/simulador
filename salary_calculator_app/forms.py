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

from django import forms
from models import *
import datetime


class ImpuestoGananciasForm(forms.Form):
    """Formulario para que el usuario ingrese datos referidos al calculo del impuesto a las ganancias"""

    conyuge = forms.ChoiceField(
        label=u'¿Tiene a su cónyuge a cargo?',
        choices=[(2, 'No'), (1, u'Sí')]
    )
    nro_hijos_menores_24 = forms.ChoiceField(
        label=u'N° de hijos a cargo',
        choices=[(i, i) for i in range(15)]
    )
    nro_descendientes = forms.ChoiceField(
       label=u'N° de nietos/bisnietos a cargo',
        choices=[(i, i) for i in range(15)]
    )
    nro_ascendientes = forms.ChoiceField(
       label=u'N° de padres, padrastros y abuelos a cargo',
        choices=[(i, i) for i in range(6)]
    )
    nro_suegros_yernos_nueras = forms.ChoiceField(
        label=u'N° de suegros/as, yernos/nueras a cargo',
        choices=[(i, i) for i in range(6)]
    )
    otros_descuentos = forms.IntegerField(label=u'Otros gastos deducibles (Form. 572)',
                        min_value=0, max_value=50000, initial=0, required=False,
                        widget=forms.TextInput(attrs={'maxlength':'5', 'style':'width: 50px;'}),
                        help_text=u'Otros gastos deducibles especificados en el formulario 572')


class CommonForm(forms.Form):
    """Formulario para el cálculo de salario docente. Contiene todos los valores
    que dependen de la persona y no de cada cargo por separado."""

    mes = forms.ChoiceField(
        label=u'Mes',
        #initial=str(datetime.date.today().month) + "/" + str(datetime.date.today().year),
        choices=[(i, unicode(i)) for i in range(1,13)],
        widget = forms.Select(),
        required = False,
        help_text=u'Seleccione una fecha para hacer el cálculo del salario.'
    )

    anio = forms.ChoiceField(
        label=u'Año',
        choices=[(i, unicode(i)) for i in range(2012,datetime.datetime.now().year+1)],
        #initial=str(datetime.date.today().month) + "/" + str(datetime.date.today().year),
        widget = forms.Select(),
        help_text=u'Seleccione una fecha para hacer el cálculo del salario.'
    )

    antiguedad = forms.ChoiceField(
        label=u'Antigüedad', 
        choices=[(i, unicode(i)) for i in range(0,24)],
        widget = forms.Select(),       
        help_text=u'Ingrese su antigüedad docente'
    )

    caja_compl = forms.FloatField(
        label=u'Caja complementaria de Jub.',
        min_value=0.0, max_value=10., initial=4.5, required=False,
        widget=forms.TextInput(attrs={'maxlength':'3', 'style':'width: 40px;'}),
        help_text=u'Porcentaje de caja complementaria de Jubilación'
    )
    doctorado = forms.BooleanField(label=u'Añadir Título de Doctorado', required=False)
    master = forms.BooleanField(label=u'Añadir Título de Maestría', required=False)
    especialista = forms.BooleanField(label=u'Añadir Título de Especialista', required=False)

    afiliado = forms.BooleanField(label=u'Afiliado a ADIUC', required=False)
    
    #daspu = forms.BooleanField(label=u'Considerar servicios DASPU', required=False)

class CargoUnivForm(forms.Form):
    """Formulario de calculo de salario docente para docentes universitarios."""

    cargo = forms.ModelChoiceField(
        label=u'Cargo',
        queryset=Cargo.objects.filter(
                tipo_cargo = u'Universitario'
                ),
        empty_label=None,
        help_text=u'Ingrese el nombre del cargo.'
    )


class CargoPreUnivForm(forms.Form):
    """Formulario de calculo de salario docente para docentes Pre-universitarios."""

    cargo = forms.ModelChoiceField(label=u'Cargo', queryset=CargoPreUniversitario.objects.filter(tipo_cargo = u'Preuniversitario'), empty_label=None,
       widget=forms.Select(attrs={'onChange': 'this.horas', 'onLoad':'this.horas', 'onKeyUp':'this.blur();this.focus();'}),
       help_text=u'Ingrese el nombre del cargo.'
    )

    horas = forms.FloatField(label=u'Horas de trabajo', min_value=0., max_value=99., initial=1., required=True,
        widget=forms.TextInput(attrs={'maxlength':'5', 'style':'width: 50px;'}),
        help_text=u'Ingrese la cantidad de horas asociadas al cargo.'
    )

'''
    pago_por_horas_info = forms.ChoiceField(
        required=False, 
        choices=[(unicode(c.id), unicode(c.pago_por_hora))  for c in CargoPreUniversitario.objects.all()],
        widget=forms.Select(attrs={'style':'display: none;'})

    )
'''