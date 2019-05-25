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

from salary_calculator_app.models import *
from django.contrib import admin


def show_porc(obj):
    return unicode(obj.porcentaje) + u'%'
show_porc.short_description = u'Porcentaje de aumento'

def show_valor(obj):
    return unicode(obj.valor) + u'%'
show_porc.short_description = u'Valor del aumento'

def vigencia_desde(obj):
    return unicode(obj.vigencia.desde.strftime("%d/%m/%y"))
vigencia_desde.short_description = u'Válido desde'
    
def vigencia_hasta(obj):
    return unicode(obj.vigencia.hasta.strftime("%d/%m/%y"))
vigencia_hasta.short_description = u'Hasta'

class AntiguedadUniversitariaAdmin(admin.ModelAdmin):
    list_display = ('show_years', show_porc, vigencia_desde, vigencia_hasta)

    def show_years(self, obj):
        return unicode(obj.anio) + u' años'
    show_years.short_description = u'Años'
    show_years.admin_order_field = 'anio'

class AntiguedadPreUniversitariaAdmin(admin.ModelAdmin):
    list_display = ('show_years', show_porc, vigencia_desde, vigencia_hasta)

    def show_years(self, obj):
        return unicode(obj.anio) + u' años'
    show_years.short_description = u'Años'
    show_years.admin_order_field = 'anio'

def show_cargo(obj):
    return unicode(obj.denominacion.nombre)
show_cargo.short_description = u'Nombre del cargo'
show_cargo.admin_order_field = 'denominacion'

class CargoUniversitarioAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'pampa', 'lu')
    list_filter = ('dedicacion',)

class CargoPreUniversitarioAdmin(admin.ModelAdmin):
    list_display = (show_cargo, 'pampa', 'lu', 'show_horas', 'horas_catedra', 'pago_hora')
    list_filter = ('pago_por_hora', 'horas')

    def show_horas(self, obj):
        return obj.horas
    show_horas.short_description = u'Cantidad de horas'

    def horas_catedra(self, obj):
        return obj.tipo_horas == 'C'
    horas_catedra.short_description = u'Horas cátedra?'
    horas_catedra.boolean = True

    def pago_hora(self, obj):
        return obj.pago_por_hora
    pago_hora.short_description = u'Pago por hora?'
    pago_hora.boolean = True

def codigo_nombre(obj):
    return unicode(obj.codigo) + " " + unicode(obj.nombre)
codigo_nombre.short_description = u'Código y nombre'
codigo_nombre.admin_order_field = 'codigo'

def show_modo(obj):
    return u'Persona' if obj.modo == 'P' else u'Cargo'
show_modo.short_description = u'Persona o cargo?'

def is_remun(obj):
    return obj.remunerativo
is_remun.short_description = u'Remunerativo?'
is_remun.boolean = True

def is_bonif(obj):
    return obj.bonificable
is_bonif.short_description = u'Bonificable?'
is_bonif.boolean = True

class RemuneracionAdmin(admin.ModelAdmin):
    list_display = (codigo_nombre, 'aplicacion', show_modo, is_remun, is_bonif)
    list_filter = ('aplicacion', 'modo', 'remunerativo', 'bonificable')

def rem_codigo_nombre(obj):
    return unicode(obj.remuneracion.codigo) + " " + unicode(obj.remuneracion.nombre)
rem_codigo_nombre.short_description = u'Código y nombre'
rem_codigo_nombre.admin_order_field = 'codigo'

def rem_aplicacion(obj):
    return unicode(obj.remuneracion.aplicacion)

def rem_show_modo(obj):
    return u'Persona' if obj.remuneracion.modo == 'P' else u'Cargo'
rem_show_modo.short_description = u'Persona o cargo?'

def show_anios(obj):
    return unicode(obj.anio) + u' años'

def rem_is_remun(obj):
    return obj.remuneracion.remunerativo
rem_is_remun.short_description = u'Remunerativo?'
rem_is_remun.boolean = True

def rem_is_bonif(obj):
    return obj.remuneracion.bonificable
rem_is_bonif.short_description = u'Bonificable?'
rem_is_bonif.boolean = True

def ret_codigo_nombre(obj):
    return unicode(obj.retencion.codigo) + " " + unicode(obj.retencion.nombre)
ret_codigo_nombre.short_description = u'Código y nombre'
ret_codigo_nombre.admin_order_field = 'codigo'

def ret_aplicacion(obj):
    if obj.retencion.aplicacion == 'U':
        return u'Universitarios'
    elif obj.retencion.aplicacion == 'P':
        return u'Preuniversitarios'
    else:
        return u'Todos'

def ret_show_modo(obj):
    return u'Persona' if obj.retencion.modo == 'P' else u'Cargo'
ret_show_modo.short_description = u'Persona o cargo?'

class RemuneracionPorcentualAdmin(admin.ModelAdmin):
    list_display = (rem_codigo_nombre, rem_aplicacion, rem_show_modo, rem_is_remun, rem_is_bonif)
    #list_filter = ('aplicacion', 'modo', 'remunerativo', 'bonificable')

class RemuneracionFijaAdmin(admin.ModelAdmin):
    list_display = (rem_codigo_nombre, rem_aplicacion, rem_show_modo)

class RemuneracionFijaCargoAdmin(admin.ModelAdmin):
    list_display = (rem_codigo_nombre, 'valor' , rem_aplicacion, rem_show_modo, 'cargo')

class RemuneracionFijaCargoAntiguedadAdmin(admin.ModelAdmin):
    list_display = (rem_codigo_nombre, 'valor' , rem_aplicacion, rem_show_modo, 'cargo', show_anios, vigencia_desde, vigencia_hasta)

class RemuneracionNomencladorAdmin(admin.ModelAdmin):
    list_display = (rem_codigo_nombre, 'porcentaje' , vigencia_desde, vigencia_hasta, 'cargo')

class RetencionAdmin(admin.ModelAdmin):
    list_display = (codigo_nombre, 'aplicacion', show_modo)
    list_filter = ('aplicacion', 'modo')

class RetencionFijaAdmin(admin.ModelAdmin):
    list_display = (ret_codigo_nombre, ret_aplicacion, ret_show_modo)

class RetencionPorcentualAdmin(admin.ModelAdmin):
    list_display = (ret_codigo_nombre, ret_aplicacion, ret_show_modo)
    
class SalarioBasicoUnivAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'valor', 'vigencia')
    list_filter = ('cargo__dedicacion',)

class SalarioBasicoPreUnivAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'valor', 'vigencia')
    list_filter = ('cargo__horas',)

# ver alguna forma de hacerlo
class RemuneracionPorcentualAntiguedadAdmin(admin.ModelAdmin):
    fields = (
        'remuneracion',
        'porcentaje',
        'vigencia',
        'cargo_universitario',
    )

admin.site.register(SalarioBasicoUniv, SalarioBasicoUnivAdmin)
admin.site.register(SalarioBasicoPreUniv, SalarioBasicoPreUnivAdmin)
admin.site.register(DenominacionCargo)
admin.site.register(RemuneracionFijaCargoAntiguedad, RemuneracionFijaCargoAntiguedadAdmin)
admin.site.register(CargoUniversitario, CargoUniversitarioAdmin)
admin.site.register(CargoPreUniversitario, CargoPreUniversitarioAdmin)
admin.site.register(Periodo)
# admin.site.register(GarantiaSalarialUniversitaria)
# admin.site.register(GarantiaSalarialPreUniversitaria)
admin.site.register(AntiguedadUniversitaria, AntiguedadUniversitariaAdmin)
admin.site.register(AntiguedadPreUniversitaria, AntiguedadPreUniversitariaAdmin)
admin.site.register(Retencion, RetencionAdmin)
admin.site.register(Remuneracion, RemuneracionAdmin)
admin.site.register(RetencionPorcentual, RetencionPorcentualAdmin)
admin.site.register(RetencionFija, RetencionFijaAdmin)
admin.site.register(RemuneracionPorcentual, RemuneracionPorcentualAdmin)
admin.site.register(RemuneracionFija, RemuneracionFijaAdmin)
admin.site.register(RemuneracionFijaCargo, RemuneracionFijaCargoAdmin)
admin.site.register(RemuneracionNomenclador, RemuneracionNomencladorAdmin)
admin.site.register(FondoSolidario)
admin.site.register(RetencionDaspu)
admin.site.register(ImpuestoGananciasTabla)
admin.site.register(ImpuestoGananciasDeducciones)
admin.site.register(RemuneracionPorcentualAntiguedad, RemuneracionPorcentualAntiguedadAdmin)
