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

from django.db import models

from salary_calculator_app.validators import *

class Periodo(models.Model):
    """ Modelo para representar periodos de tiempo. """
    desde = models.DateField(u'Vigente desde',
            help_text=u'Comienzo del período de tiempo')
    hasta = models.DateField(u'Vigente hasta',
            help_text=u'Finalización del período de tiempo')

    class Meta:
        ordering = ['desde', 'hasta']

    def __unicode__(self):
        return 'De ' + unicode(self.desde.strftime("%d/%m/%y")) + ' a ' + unicode(self.hasta.strftime("%d/%m/%y"))

class GarantiaSalarialPreUniversitaria(models.Model):
    """ garantía salarial para cargos preuniversitarios """
    
    cargo = models.ManyToManyField('CargoPreUniversitario',
        help_text=u'Los cargos docentes sobre los que se aplica esta garantía.')
    
    garantia = models.FloatField(u'Garantía', validators=[validate_isgezero],
        help_text=u'Garantía salarial para el cargo.')

    vigencia = models.ForeignKey('Periodo',
        help_text=u'Período de tiempo en el cual esta garantía se encuentra vigente.')


class GarantiaSalarialUniversitaria(models.Model):
    """Representa el valor minimo que un Cargo puede cobrar."""

    cargo = models.ManyToManyField('CargoUniversitario',
        help_text=u'Los cargos docentes sobre los que se aplica esta garantía.')

    garantia = models.FloatField(u'Garantía', validators=[validate_isgezero],
        help_text=u'Garantía salarial para el cargo.')
    
    vigencia = models.ForeignKey('Periodo',
        help_text=u'Período de tiempo en el cual esta garantía se encuentra vigente.')

    def __unicode__(self):
        return unicode(self.cargo.values()[0]['dedicacion']) + " $" + unicode(self.garantia) + " [" + unicode(self.vigencia.desde) + " / " + unicode(self.vigencia.hasta) + "]"


class Cargo(models.Model):
    """Modelo que representa un Cargo, ya sea pre o universitario."""

    lu = models.PositiveSmallIntegerField(u'Código LU', validators=[validate_isgzero],
        help_text=u'El código L.U. del cargo que figura en la planilla de la UNC.')
    pampa = models.PositiveSmallIntegerField(u'Código PAMPA', unique=True, validators=[validate_isgzero],
        help_text=u'El código PAMPA del cargo que figura en la planilla de la UNC.')
    denominacion = models.ForeignKey('DenominacionCargo',
        help_text=u'El nombre del cargo asociado.')

    #rem_fijas = models.ManyToManyField('RemuneracionFija', blank=True)
    #rem_porcentuales = models.ManyToManyField('RemuneracionPorcentual', blank=True)
    #ret_fijas = models.ManyToManyField('RetencionFija', blank=True)
    #ret_porcentuales = models.ManyToManyField('RetencionPorcentual', blank=True)

    class Meta:
        ordering = ['denominacion']

    def __unicode__(self):
        return unicode(self.denominacion)


class DenominacionCargo(models.Model):
    """El nombre de un cargo docente. Ej: Profesor Adjunto, Ayudante Alumno, etc"""

    nombre = models.CharField(u'Denominacion del Cargo', max_length=50, unique=True,
        help_text=u'El nombre de un cargo docente. Ej: Profesor Titular, Profesor Asociado, etc')
    
    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre


class CargoUniversitario(Cargo):
    """Cargo de docente Universitario."""

    DEDICACION_OPCS = (
        ('D.E', u'Dedicación Exclusiva'),
        ('D.S.E', u'Dedicación Semi Exclusiva'),
        ('D.S', u'Dedicación Simple')
    )
    dedicacion = models.CharField(u'Dedicación', max_length=5, choices=DEDICACION_OPCS,
        help_text=u'El tipo de dedicación para el cargo. Pueden ser dedicación exclusiva, semi-exclusiva o simple.')
    #adic2003 = models.FloatField(u'Adic. 8% RHCS 153/03', blank=True, null=True,    
    #help_text=u'Es el adicional del 8% del salario básico del año 2003 que le corresponde a este cargo.')

    class Meta:
        ordering = ['pampa']

    def __unicode__(self):
        return super(CargoUniversitario, self).__unicode__() + " " + self.dedicacion


class CargoPreUniversitario(Cargo):
    """Cargo de docente Preuniversitario."""

    TIPOHORAS_OPCS = (
        ('C', u'Cátedra'),
        ('R', u'Reloj')
    )
    horas = models.FloatField(u'Cantidad de Horas Cátedra', validators=[validate_isgezero],
        help_text=u'La cantidad de horas para el cargo como figuran en la planilla de la UNC. Ej: Al cargo "Vice Director de 1°" le corresponden 25 horas.')
    tipo_horas = models.CharField(u'Tipo de Horas', max_length=1, choices=TIPOHORAS_OPCS,
        help_text=u'El tipo de horas del cargo.')
    pago_por_hora=models.BooleanField(u'Pago por hora?',
        help_text=u'Poner "Sí" si este cargo se paga por cantidad de horas. Poner "No" en caso contrario.')

    class Meta:
        ordering = ['pampa']

    def __unicode__(self):
        if self.pago_por_hora or self.horas <= 0.:
            return str(self.pampa) + " - " + super(CargoPreUniversitario, self).__unicode__()
        return str(self.pampa) + " - " + super(CargoPreUniversitario, self).__unicode__() + " - " + unicode(self.horas) + "hs"


class Retencion(models.Model):
    """Representa a una retencion."""

    MODO_OPCS = (
        ('P', u'Se aplica a la persona (solo una vez).'),
        ('C', u'Se aplica por cargo (una vez por cada cargo).'),
    )

    # Tuplas de opciones.
    APP_OPCS = (
        ('U', u'Cargos Universitarios'),
        ('P', u'Cargos Preuniversitarios'),
        ('T', u'Todos los cargos')
    )

    codigo = models.CharField(u'Código', max_length=5,
        help_text=u'El código de la retencion tal cual figura en la lista de la web de ADIUC.')
    nombre  = models.CharField(u'Nombre', max_length=50,
        help_text=u'El nombre de la retencion tal cual figura en la lista de la web de ADIUC.')
    aplicacion = models.CharField(u'Aplica a', max_length=1, choices=APP_OPCS,
        help_text=u'A qué tipo de cargo aplica esta retencion.')
    modo = models.CharField(u'Modo', max_length=1,choices=MODO_OPCS)

    class Meta:
        ordering = ['codigo', 'nombre', 'aplicacion']

    def __unicode__(self):
        return self.codigo + u" " + self.nombre


# Algunos conceptos importantes:
# Remuneracion REMUNERATIVA: se denomina así a todo aquel ítem del 
# salario que tiene DESCUENTOS DE LEY (Jubilación, Obra social, ART).
# Remuneracion BONIFICABLE: se denominan así a todos los ítems del salario al que se le aplican los
# porcentuales de ANTIGÜEDAD de la escala de Art. Nº de la Ley Nº 1820.
class Remuneracion(models.Model):
    """Representa un adicional, es decir, una remuneracion."""

    MODO_OPCS = (
        ('P', u'Se aplica a la persona (solo una vez).'),
        ('C', u'Se aplica por cargo (una vez por cada cargo).'),
    )

    # Tuplas de opciones.
    APP_OPCS = (
        ('U', u'Cargos Universitarios'),
        ('P', u'Cargos Preuniversitarios'),
        ('T', u'Todos los cargos')
    )

    codigo = models.CharField(u'Código', max_length=5,
        help_text=u'El código de la remuneracion tal cual figura en la lista de la web de ADIUC.')
    nombre  = models.CharField(u'Nombre', max_length=50,
        help_text=u'El nombre de la remuneracion tal cual figura en la lista de la web de ADIUC.')
    aplicacion = models.CharField(u'Aplica a', max_length=1, choices=APP_OPCS,
        help_text=u'A qué tipo de cargo aplica esta remuneracion.')
    modo = models.CharField(u'Modo', max_length=1,choices=MODO_OPCS)
    remunerativo = models.BooleanField(u'Remunerativa',
        help_text=u'Una remuneración es remunerativa cuando se le aplican descuentos de Ley (jubilación, obra social, art, etc.)')
    bonificable = models.BooleanField(u'Bonificable',
        help_text=u'Una remuneración es bonificable cuando se le aplican los porcentuales de Antiguedad.')

    class Meta:
        ordering = ['codigo', 'nombre', 'aplicacion']

    def __unicode__(self):
        result = self.codigo + u" " + self.nombre
        if self.remunerativo:
            result  += u' R'
        else:
            result +=  u' NR'
        if self.bonificable:
            result += u'B'
        else:
            result += u'NB'
        return result


class RetencionPorcentual(models.Model):
    """Una retencion que especifica el porcentaje del descuento que debe realizarse."""

    retencion = models.ForeignKey('Retencion',
        help_text = u'La retención relacionada con esta retención porcentual.')
    porcentaje = models.FloatField(u'Porcentaje de Descuento', validators=[validate_isgezero],
        help_text=u'El porcentaje del descuento. Ingresar un valor positivo.')
    vigencia = models.ForeignKey('Periodo',
        help_text=u'Período de tiempo en el cual esta garantía se encuentra vigente.')

    class Meta:
        ordering = ['retencion', 'porcentaje']

    def __unicode__(self):
        return unicode(self.retencion) + u" " + unicode(self.porcentaje) + u"%"


class RetencionDaspu(models.Model):
    """ Representa las retenciones para DASPU """
    
    #No usa retencion fija, porque necesita dos porcentajes.    
    retencion = models.ForeignKey('RetencionPorcentual',
        help_text = u'La retención relacionada con esta retención porcentual.')

    porcentaje_minimo = models.FloatField(u'Porcentaje tope mínimo',
        help_text='Porcentaje que al aplicarse al salario bruto indicara el tope mínimo para esta retención.')
        
    #cargo_referencia = models.OneToOneField(u'CargoUniversitario',
        #help_text='Se tomará como monto mínimo el porcentaje anterior sobre el salario bruto sin antiguedad de este cargo.')

    def __unicode__(self):
        return u"Retención DASPU: [" + unicode(self.retencion) + u" - " + unicode(self.porcentaje_minimo) + "%"


class RetencionFija(models.Model):
    """Una retencion que especifica un descuento fijo que debe realizarse."""

    retencion = models.ForeignKey('Retencion',
        help_text = u'La retención relacionada con esta retención porcentual.')
    valor = models.FloatField(u'Valor de Descuento', validators=[validate_isgezero],
        help_text=u'El valor fijo que debe descontarse.')
    vigencia = models.ForeignKey('Periodo',
        help_text=u'Período de tiempo en el cual esta garantía se encuentra vigente.')

    class Meta:
        ordering = ['retencion', 'valor']

    def __unicode__(self):
        return unicode(self.retencion) + u" $" + unicode(self.valor)


class FondoSolidario(RetencionFija):
    concepto = models.CharField(u'Concepto', max_length='80')


class RemuneracionPorcentual(models.Model):
    """Una remuneracion que especifica el porcentaje de aumento que debe realizarse."""

    remuneracion = models.ForeignKey('Remuneracion',
        help_text = u'La retención relacionada con esta remuneración porcentual.')
    porcentaje = models.FloatField(u'Porcentaje de Aumento', validators=[validate_isgezero],
        help_text=u'El porcentaje del aumento. Ingresar un valor positivo.')
    vigencia = models.ForeignKey('Periodo',
        help_text=u'Período de tiempo en el cual esta garantía se encuentra vigente.')
    sobre_referencia= models.BooleanField(u'Sobre salario de referencia?',
        help_text=u'La remuneración se calcula sobre el salario de referencia (caso aumentos de paritaria p.ej 30/8)?')
    nomenclador= models.BooleanField(u'Usa nomenclador?',
        help_text=u'A la remuneración hay que agregarle el porcentaje de nomenclador?')

    class Meta:
        ordering = ['remuneracion', 'porcentaje']

    def __unicode__(self):
        return unicode(self.porcentaje) + u"% - " + unicode(self.remuneracion)


class RemuneracionPorcentualAntiguedad(models.Model):
    remuneracion = models.ForeignKey(Remuneracion,
        help_text = u'La retención relacionada con esta remuneración porcentual.')
    porcentaje = models.FloatField(u'Porcentaje de Aumento', validators=[validate_isgezero],
        help_text=u'El porcentaje del aumento. Ingresar un valor positivo.')
    vigencia = models.ForeignKey(Periodo,
        help_text=u'Período de tiempo en el cual esta garantía se encuentra vigente.')
    cargo_universitario = models.ManyToManyField(CargoUniversitario,
        help_text=u'El cargo universitario sobre el que se aplica este porcentaje.',
        blank=True,
        null=True)

    class Meta:
        ordering = ['-vigencia', '-porcentaje', 'remuneracion__aplicacion']

    def __unicode__(self):
        return u'Depediente ' + unicode(self.porcentaje) + u"% - " + unicode(self.remuneracion)


class RemuneracionFija(models.Model):
    """Una remuneracion que especifica un aumento fijo sobre el salario basico."""

    remuneracion = models.ForeignKey('Remuneracion',
        help_text = u'La retención relacionada con esta remuneración fija.')
    valor = models.FloatField(u'Valor del Aumento', validators=[validate_isgezero],
        help_text=u'El valor fijo que se sumará al salario básico.')
    vigencia = models.ForeignKey('Periodo',
        help_text=u'Período de tiempo en el cual esta garantía se encuentra vigente.')

    class Meta:
        ordering = ['remuneracion', 'valor']

    def __unicode__(self):
        return u"$" + unicode(self.valor) + " - " + unicode(self.remuneracion)

class RemuneracionFijaCargoAntiguedad(RemuneracionFija):
    """ Una remuneración fija inherente a un cargo en particular."""
    
    anio = models.SmallIntegerField(u'Años de Antigüedad', validators=[validate_isgezero],
        help_text=u'La cantidad de años correspondiente a la antigüedad. Ej: 0, 1, 2, 5, 7, 9, 24, etc.')    

    cargo = models.ForeignKey('Cargo',
        help_text=u'Remuneración fija inherente a un cargo en particular, para una antiguedad dada.')    
    
    def __unicode__(self):
        return u"$" + unicode(self.valor) + " - " + unicode(self.remuneracion) + " - " + unicode(self.anio) + " - " + unicode(self.cargo) + u" - [" + unicode(self.vigencia.desde) + u" / " + unicode(self.vigencia.hasta) + u"]"


class RemuneracionFijaCargo(RemuneracionFija):
    """ Una remuneración fija inherente a un cargo en particular."""

    cargo = models.ForeignKey('Cargo',
        help_text=u'Remuneración fija inherente a un cargo en particular.')

class RemuneracionNomenclador(RemuneracionPorcentual):
    """ Una remuneración porcentual nomenclador inherente a un cargo en particular."""

    cargo = models.ForeignKey('Cargo',
        help_text=u'Remuneración porcentual inherente a un cargo en particular.')

class SalarioBasicoUniv(RemuneracionFija):
    """Representavalor_min = models.FloatField(u'Valor mínimo:',help_text=u'Valor mínimo de categoría.')
    valor_max = models.FloatField(u'Valor máximo:', help_text=u'Valor máximo de categoría.') un valor de un salario basico relacionado a un cargo."""

    cargo = models.ForeignKey('CargoUniversitario',
        help_text=u'El cargo docente sobre el que se aplica este salario.')

    salario_referencia = models.FloatField(u'Salario Básico de referencia', validators=[validate_isgezero],
             help_text=u'Salario de referencia sobre el cual se calculan los porcentajes de aumento de paritaria.')

    class Meta:
        ordering = ['cargo', 'valor']

    def __unicode__(self):
        return unicode(self.cargo) + u" - $" + unicode(self.valor) + u" - [" + unicode(self.vigencia.desde) + u" / " + unicode(self.vigencia.hasta) + u"]"


class SalarioBasicoPreUniv(RemuneracionFija):
    
    cargo = models.ForeignKey('CargoPreUniversitario',
        help_text=u'El cargo docente sobre el que se aplica este salario.')

    class Meta:
        ordering = ['cargo', 'valor']

    def __unicode__(self):
        return unicode(self.cargo) + u" - $" + unicode(self.valor) + u" - [" + unicode(self.vigencia.desde) + u" / " + unicode(self.vigencia.hasta) + u"]"

class AntiguedadUniversitaria(RemuneracionPorcentual):
    """Una entrada de la tabla de escala de antiguedad para los docentes Universitarios"""

    anio = models.SmallIntegerField(u'Años de Antigüedad', validators=[validate_isgezero],
        help_text=u'La cantidad de años correspondiente a la antigüedad. Ej: 0, 1, 2, 5, 7, 9, 24, etc.')

    class Meta:
        ordering = ['anio']

    def __unicode__(self):
        return unicode(self.anio) + u" años - " + unicode(self.porcentaje) + u"% - [" + unicode(self.vigencia.desde) + u" / " + unicode(self.vigencia.hasta) + u"]"

class AntiguedadPreUniversitaria(RemuneracionPorcentual):
    """Una entrada de la tabla de escala de antiguedad para los docentes Preuniversitarios"""

    anio = models.SmallIntegerField(u'Años de Antigüedad', validators=[validate_isgezero],
        help_text=u'La cantidad de años correspondiente a la antigüedad. Ej: 0, 1, 2, 5, 7, 9, 24, etc.')

    class Meta:
        ordering = ['anio']

    def __unicode__(self):
        return unicode(self.anio) + u" años - " + unicode(self.porcentaje) + u"% - [" + unicode(self.vigencia.desde) + u" / " + unicode(self.vigencia.hasta) + u"]"


class ImpuestoGananciasDeducciones(models.Model):
    """Este modelo guarda los montos de las deducciones personales para el estimativo del ingreso anual."""

    ganancia_no_imponible = models.FloatField(u'Ganancia no imponible', help_text=u'El monto de la ganancia no imponible.')
    desc_cuarta_cat = models.FloatField(u'Descuento cuarta categoría',
        help_text=u'Descuento que se aplica a trabajadores en relación de dependencia, por ejemplo UNC')
    por_conyuge = models.FloatField(u'Por cónyuge', help_text=u'El monto que se descuenta por cónyuge.')
    por_hijo = models.FloatField(u'Por cada hijo menor a 24 años',
        help_text=u'El monto que se descuenta por cada hijo/a')
    por_descendiente = models.FloatField(u'Por cada descendiente', 
        help_text=u'El monto que se descuenta por cada descendiente en línea recta (nieto/a, bisnieto/a)')
    por_ascendiente = models.FloatField(u'Por cada ascendiente',
        help_text=u'El monto que se descuenta por cada ascendiente (padre/madre, abuelo/a, bisabuelo/a, padrastro/madrastra)')
    por_suegro_yerno_nuera = models.FloatField(u'Por suegro, yerno o nuera',
        help_text=u'Por suegro/a y por cada yerno o nuera')
    deduccion_especial = models.FloatField(u'Deducción Especial',
        help_text=u'Deducción Especial')

    #max_por_intereses_creditos_hipotecarios = models.FloatField(u'Máx. a pagar por crédito hipotecarios',
        #help_text=u'Intereses pagados por créditos hipotecarios contraídos a partir del 01/01/2001 para la compra o construcción de su casa-habitación.')
    #max_por_seguro_de_vida = models.FloatField(u'Máx. a pagar por seguro de vida',
        #help_text=u'El monto que se descuenta por montos pagados en conceptos de seguro de vida.')
    #max_por_donaciones = models.FloatField(u'Máx. % a pagar por donaciones realizadas',
        #help_text=u'El % de la ganancia neta anual que se descuenta por donaciones realizadas a: org. nacionales, provinciales y municipales, instituciones sin fines de lucro con certificado emitido por AFIP.')

    vigencia = models.ForeignKey('Periodo',
        help_text=u'Período de tiempo en el cual esta garantía se encuentra vigente.')

    class Meta:
        ordering = ['vigencia']

    def __unicode__(self):
        return unicode(self.vigencia.desde.year)


class ImpuestoGananciasTabla(models.Model):

    ganancia_neta_min = models.FloatField(u'Ganancia neta mínima', help_text=u'El valor mínimo de la ganancia neta sujeta a impuesto.')
    ganancia_neta_max = models.FloatField(u'Ganancia neta máxima', help_text=u'El valor máximo de la ganancia neta sujeta a impuesto.')
    impuesto_porcentual = models.FloatField(u'Impuesto porcentual', help_text=u'El valor en porcentaje del impuesto a las ganancias que se aplica al exedente.')
    suma_anterior = models.FloatField(u'Suma anterior', help_text=u'El porcentaje anterior por el excedente más este valor darán el impuesto a las ganancias.')
    vigencia = models.ForeignKey('Periodo',
        help_text=u'Período de tiempo en el cual esta garantía se encuentra vigente.')

    class Meta:
        ordering = ['ganancia_neta_min', 'ganancia_neta_max']

    def __unicode__(self):
        return unicode(self.vigencia.desde.year) + " : De " + unicode(int(self.ganancia_neta_min)) + " a " + unicode(int(self.ganancia_neta_max))


