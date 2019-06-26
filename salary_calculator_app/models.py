# -*- coding: utf-8 -*-

#=============================================
#
# Copyright 2012 David Racca and Matias Molina.
# Copyright 2019 Araceli Acosta and Luis Romano
#
# The following code is a derivative work of the code from the ADIUC 
# Salary Calculator made by David Racca and Matias Molina and licensed GPLv3. 
# This code therefore is also licensed under the terms of the GNU Public 
# License, verison 3.
#
# This file is part of ADIUC Salary Calculator.
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

from django.db import models

from salary_calculator_app.validators import *



class Cargo(models.Model):
    """Modelo que representa un Cargo, ya sea pre o universitario."""
    TIPO_CARGO = (
        ('U', u'Universitario'),
        ('P', u'Preuniversitario')
    )

    pampa = models.PositiveSmallIntegerField(u'Código PAMPA', unique=True, validators=[validate_isgzero],
        help_text=u'El código PAMPA del cargo que figura en la planilla de la UNC.')
    denominacion = models.CharField(u'Denominacion del cargo y dedicación', max_length=50, unique=True,
        help_text=u'El nombre de un cargo. Ej: Profesor Titular, Profesor Asociado, etc')
    tipo_cargo = models.CharField(u'Tipo de cargo', max_length=1, choices=TIPO_CARGO,
        help_text=u'El tipo de cargo. Puede ser Universitario o Preuniversitario.')
    horas = models.FloatField(u'Dedicación horaria', validators=[validate_isgezero],
        help_text=u'La dedicación o cantidad de horas reloj correspondiente al cargo de la UNC.')
    pago_por_hora=models.BooleanField(u'Pago por hora?',
        help_text=u'Poner "Sí" si este cargo se paga por cantidad de horas. Poner "No" en caso contrario.')
    class Meta:
        ordering = ['pampa', 'tipo_cargo', 'denominacion']

    def __unicode__(self):
        return unicode(str(self.pampa) + " - " +self.denominacion)




class RetencionPorcentual(models.Model):
    """Retencion porcentual de descuento sobre el total remunerativo de la persona."""

    ref  = models.CharField(u'Referencia', max_length=30,
        help_text=u'Referencia interna')
    codigo = models.CharField(u'Código', max_length=5,
        help_text=u'Código de la retención')
    nombre  = models.CharField(u'Nombre', max_length=30,
        help_text=u'Nombre de la retención')
    porcentaje = models.FloatField(u'Porcentaje de Descuento', validators=[validate_isgezero],
        help_text=u'El porcentaje del descuento. Ingresar un valor positivo.')
    desde = models.DateField(u'Vigente desde',
            help_text=u'Comienzo del período de tiempo')
    hasta = models.DateField(u'Vigente hasta',
            help_text=u'Finalización del período de tiempo')
    '''
    por_cargo = models.BooleanField(u'Por cargo?',
            help_text=u'Indica si la retencion se efectúa por cargo o por persona')
    cargo = models.ForeignKey('Cargo',
        help_text=u'Cargo al cual se aplica la retencion (en el caso q sea por cargo).')
    '''

    class Meta:
        ordering = ['codigo', 'nombre', 'desde', 'hasta']

    def __unicode__(self):
        return unicode(self.ref) 


#class RetencionDaspu(models.Model):
#    """ Representa las retenciones para DASPU """
#    
#    #No usa retencion fija, porque necesita dos porcentajes.    
#    retencion = models.ForeignKey('RetencionPorcentual',
#        help_text = u'La retención relacionada con esta retención porcentual.')
#
#    porcentaje_minimo = models.FloatField(u'Porcentaje tope mínimo',
#        help_text='Porcentaje que al aplicarse al salario bruto indicara el tope mínimo para esta retención.')
#        
#    #cargo_referencia = models.OneToOneField(u'CargoUniversitario',
#        #help_text='Se tomará como monto mínimo el porcentaje anterior sobre el salario bruto sin antiguedad de este cargo.')
#
#    def __unicode__(self):
#        return u"Retención DASPU: [" + unicode(self.retencion) + u" - " + unicode(self.porcentaje_minimo) + "%"


class RetencionFija(models.Model):
    """Retencion fija que debe realizarse a la persona."""

    ref  = models.CharField(u'Referencia', max_length=30,
        help_text=u'Referencia interna o descripción corta')
    codigo = models.CharField(u'Código', max_length=5,
        help_text=u'El código de la retencion tal cual figura en la lista de la web de ADIUC.')
    nombre  = models.CharField(u'Nombre', max_length=30,
        help_text=u'El nombre de la retencion tal cual figura en la lista de la web de ADIUC.')
    valor = models.FloatField(u'Valor de Descuento', validators=[validate_isgezero],
        help_text=u'El valor fijo que debe descontarse.')
    desde = models.DateField(u'Vigente desde',
            help_text=u'Comienzo del período de tiempo')
    hasta = models.DateField(u'Vigente hasta',
            help_text=u'Finalización del período de tiempo')
    por_cargo = models.BooleanField(u'Por cargo?',
            help_text=u'Indica si la retencion se efectúa por cargo o por persona')
    cargo = models.ForeignKey('Cargo',
        help_text=u'Cargo al cual se aplica la retencion (en el caso q sea por cargo).')
    class Meta:
        ordering = ['codigo', 'nombre', 'desde', 'hasta']

    def __unicode__(self):
        return unicode(self.ref) 






class RemuneracionFija(models.Model):
    """Remuneracion fija por cargo y antigüedad."""

    ref  = models.CharField(u'Referencia', max_length=30,
        help_text=u'Referencia interna')
    codigo = models.CharField(u'Código', max_length=5,
        help_text=u'Código de la remuneracion')
    nombre  = models.CharField(u'Nombre', max_length=30,
        help_text=u'Nombre de la remuneracion')
    remunerativo = models.BooleanField(u'Remunerativa',
        help_text=u'Una remuneración es remunerativa cuando se le aplican descuentos de Ley (jubilación, obra social, art, etc.)')
    bonificable = models.BooleanField(u'Bonificable',
        help_text=u'Una remuneración es bonificable cuando se le aplican los porcentuales de Antiguedad y las bonificaciones.')
    desde = models.DateField(u'Vigente desde',
            help_text=u'Comienzo del período de tiempo')
    hasta = models.DateField(u'Vigente hasta',
            help_text=u'Finalización del período de tiempo')


    class Meta:
        ordering = ['codigo', 'nombre', 'desde', 'hasta']

    def __unicode__(self):
        if self.remunerativo:
            opc = u' R '
        else:
            opc =  u' NR '
        if self.bonificable:
            opc += u' B '
        else:
            opc += u' NB '
        return unicode(self.ref) + opc + unicode(self.nombre)


class ValoresRemuneracionFija(models.Model):
    """Datos de cargo de la remuneracion fija."""

    remuneracion = models.ForeignKey('RemuneracionFija',
        help_text = u'Remuneración fija.')

    cargo = models.ForeignKey('Cargo',
        help_text=u'Cargo al cual se aplica la remuneración.')

    valor = models.FloatField(u'Valor del Aumento', validators=[validate_isgezero],
        help_text=u'El valor fijo que se sumará al salario básico.')

    class Meta:
        ordering = ['cargo', 'valor']

    def __unicode__(self):
        return unicode(self.remuneracion) + unicode(self.cargo)


class ValoresRemuneracionFijaConAntig(models.Model):
    """Datos de cargo y antigüedad de la remuneracion fija."""

    remuneracion = models.ForeignKey('RemuneracionFija',
        help_text = u'Remuneración fija.')

    cargo = models.ForeignKey('Cargo',
        help_text=u'Cargo al cual se aplica la remuneración.')

    valor = models.FloatField(u'Valor del Aumento', validators=[validate_isgezero],
        help_text=u'El valor fijo que se sumará al salario básico.')

    antig_desde = models.SmallIntegerField(u'Desde Antigüedad', validators=[validate_isgezero], default=0,
        help_text=u'Desde qué antigüedad se aplica.')

    antig_hasta = models.SmallIntegerField(u'Hasta Antigüedad', validators=[validate_isgezero], default=24,
        help_text=u'Hasta qué antigüedad se aplica.')

    class Meta:
        ordering = ['cargo', 'antig_desde', 'valor']

    def __unicode__(self):
        return unicode(self.remuneracion) + unicode(self.cargo) 




class Bonificacion(models.Model):
    """Bonificaciones porcentuales sobre total remunerativo bonificable."""

    TIPO_BONIFICACION = (
        ('D', u'Doctorado'),
        ('M', u'Maestría'),
        ('E', u'Especialización')
    )

    ref  = models.CharField(u'Referencia', max_length=30,
        help_text=u'Referencia interna')
    codigo = models.CharField(u'Código', max_length=5,
        help_text=u'Código de la bonificación')
    nombre  = models.CharField(u'Nombre', max_length=30,
        help_text=u'Nombre de la bonificación')
    tipo_bonificacion = models.CharField(u'Tipo de bonificación', max_length=1, choices=TIPO_BONIFICACION,
        help_text=u'El tipo de bonificacion, Por Ej. Doctorado, Maestría, etc.')
    porcentaje = models.FloatField(u'Porcentaje de Bonificación', validators=[validate_isgezero],
        help_text=u'El porcentaje del bonificación. Ingresar un valor positivo.')
    desde = models.DateField(u'Vigente desde',
            help_text=u'Comienzo del período de tiempo')
    hasta = models.DateField(u'Vigente hasta',
            help_text=u'Finalización del período de tiempo')


    class Meta:
        ordering = ['codigo', 'nombre', 'desde', 'hasta']

    def __unicode__(self):
        return unicode(self.ref)



class Antiguedad(models.Model):
    """Antigüedad. Se aplica como un porcentaje sobre total remunerativo bonificable según la antig."""

    APLICADO_A = (
        ('U', u'Cargos Universitarios'),
        ('P', u'Cargos Preuniversitarios'),
        ('T', u'Todos los Cargos')
    )

    ref  = models.CharField(u'Referencia', max_length=30,
        help_text=u'Referencia interna')
    codigo = models.CharField(u'Código', max_length=5,
        help_text=u'Código de la bonificación')
    nombre  = models.CharField(u'Nombre', max_length=30,
        help_text=u'Nombre de la bonificación. En este caso Antigüedad')
    aplicado_a = models.CharField(u'Aplicado a', max_length=1, choices=APLICADO_A,
        help_text=u'A qué cargos se deben aplicar, i.e. Universitarios o Preuniversitarios.')
    antig_desde = models.SmallIntegerField(u'Desde Antigüedad', validators=[validate_isgezero], default=0,
        help_text=u'Desde qué antigüedad se aplica.')
    antig_hasta = models.SmallIntegerField(u'Hasta Antigüedad', validators=[validate_isgezero], default=24,
        help_text=u'Hasta qué antigüedad se aplica.')
    porcentaje = models.FloatField(u'Porcentaje de Bonificación', validators=[validate_isgezero],
        help_text=u'El porcentaje del bonificación. Ingresar un valor positivo.')
    desde = models.DateField(u'Vigente desde',
            help_text=u'Comienzo del período de tiempo')
    hasta = models.DateField(u'Vigente hasta',
            help_text=u'Finalización del período de tiempo')


    class Meta:
        ordering = ['codigo', 'nombre', 'desde', 'hasta', 'antig_desde', 'antig_hasta']

    def __unicode__(self):
        return unicode(self.ref) + " - " + unicode(str(self.porcentaje))


