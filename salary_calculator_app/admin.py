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
#from import_export.admin import ImportExportModelAdmin
from salary_calculator_app.models import *
from django.contrib import admin



class CargoAdmin(admin.ModelAdmin):
    list_display = ('denominacion', 'pampa', 'tipo_cargo', 'horas', 'pago_por_hora')

class RetencionPorcentualAdmin(admin.ModelAdmin):
    list_display = ('ref','codigo', 'nombre', 'porcentaje', 'desde', 'hasta')

class RetencionFijaAdmin(admin.ModelAdmin):
    list_display = ('ref','codigo', 'nombre', 'valor', 'desde', 'hasta', 'por_cargo', 'cargo')

class RemuneracionFijaAdmin(admin.ModelAdmin):
    list_display = ('ref','codigo', 'nombre', 'remunerativo', 'bonificable', 'desde', 'hasta')

class ValoresRemuneracionFijaAdmin(admin.ModelAdmin):
    list_display = ('remuneracion', 'cargo', 'valor')

class ValoresRemuneracionFijaConAntigAdmin(admin.ModelAdmin):
    list_display = ('remuneracion', 'cargo', 'valor', 'antig_desde', 'antig_hasta')

class BonificacionAdmin(admin.ModelAdmin):
    list_display = ('ref','codigo', 'nombre', 'tipo_bonificacion', 'porcentaje', 'desde', 'hasta')
    
class AntiguedadAdmin(admin.ModelAdmin):
    list_display = ('ref','codigo', 'nombre', 'aplicado_a', 'antig_desde', 'antig_hasta', 'porcentaje', 'desde', 'hasta')


admin.site.register(Cargo, CargoAdmin)
admin.site.register(RetencionPorcentual, RetencionPorcentualAdmin)
admin.site.register(RetencionFija, RetencionFijaAdmin)
admin.site.register(RemuneracionFija, RemuneracionFijaAdmin)
admin.site.register(ValoresRemuneracionFija, ValoresRemuneracionFijaAdmin)
admin.site.register(ValoresRemuneracionFijaConAntig, ValoresRemuneracionFijaConAntigAdmin)
admin.site.register(Bonificacion, BonificacionAdmin)
admin.site.register(Antiguedad, AntiguedadAdmin)


