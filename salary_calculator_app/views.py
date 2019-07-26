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
# GNU General Public License for more detailss.
#
# You should have received a copy of the GNU General Public License
# along with ADIUC Salary Calculator.  If not, see 
# <http://www.gnu.org/licenses/>.
#
#============= ================================

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from forms import *
from models import *

import datetime, pprint

# Debugger
import pdb

pp = pprint.PrettyPrinter(indent=4)
###############################################
# Hardcoded
###############################################

doc_code = '05/1'
doc_preuniv_code = '05/3'

master_code = '05/2'
master_preuniv_code = '05/5'

esp_code = '05/?'
esp_preuniv_code = '05/?'

garantia_code = '11/5'
garantia_name = u'Garantía Docentes Univ.'

garantia_preuniv_code = '10/7'
garantia_preuniv_name = u'Garantía Nivel Medio'

adic_118_code = '11/8'
#fondo_becas_code = '77/0'
#fondo_becas_name = u'Fondo de Becas'

daspu_code = '40/0'

afiliacion_code = '64/0'
afiliacion_name = u'ADIUC - Afiliacion'

sis_code = "DAS/1"
subsidio_fallecimiento_code = "DAS/2"
fs_code="DAS/4"


def add_values_from_contexts(context1, context2, key):
    """Return the plus between context1[key] and context2[key]."""
    v1 = 0.0
    v2 = 0.0
    if context1.has_key(key):
        v1 = context1[key]
    if context2.has_key(key):
        v2 = context2[key]

    return v1 + v2


##############################################
# Views
##############################################

def calculate(request):
    """Vista principal"""

    # Permite que aparezcan multiples formularios identicos.
    CargoUnivFormSet = formset_factory(CargoUnivForm, extra=0, max_num=5, can_delete=True)
    CargoPreUnivFormSet = formset_factory(CargoPreUnivForm, extra=0, max_num=5, can_delete=True)

    context = {}

    if request.method == 'POST':
        #print request
        # Sacamos la info del POST y bindeamos los forms.
        univformset = CargoUnivFormSet(request.POST, prefix='univcargo')
        preunivformset = CargoPreUnivFormSet(request.POST, prefix='preunivcargo')
        commonform = CommonForm(request.POST)
        #detailsform = DetailsForm(request.POST)
        #gananciasform = ImpuestoGananciasForm(request.POST)

        if univformset.is_valid() and preunivformset.is_valid() and commonform.is_valid():

            # Proceso los formularios de cargos.
            context_univ = processUnivFormSet(commonform, univformset)
            context_preuniv = processPreUnivFormSet(commonform, preunivformset)
            
            # Control de errores
            if context_univ.has_key('error_msg'):
                context['error_msg'] = context_univ['error_msg']
                return render_to_response('salary_calculated.html', context)
            if context_preuniv.has_key('error_msg'):
                context['error_msg'] = context_preuniv['error_msg']
                return render_to_response('salary_calculated.html', context)

            # Sumo los totales de remuneraciones y retenciones de ambos contexts.
            total_rem = add_values_from_contexts(context_univ, context_preuniv, 'total_rem')
            total_no_rem = add_values_from_contexts(context_univ, context_preuniv, 'total_no_rem')
            total_ret = add_values_from_contexts(context_univ, context_preuniv, 'total_ret')
            total_neto = add_values_from_contexts(context_univ, context_preuniv, 'total_neto')
            #total_bonificable = add_values_from_contexts(context_univ, context_preuniv, 'total_bonificable')

            fecha = datetime.date(int(commonform.cleaned_data['anio']), int(commonform.cleaned_data['mes']), 10)
            # Hago el merge de los dos contexts.
            context['total_rem'] = total_rem
            context['total_no_rem'] = total_no_rem
            context['total_ret'] = total_ret
            context['total_neto'] = total_neto
            context['total_bonificable_u'] = context_univ['total_bonificable']
            context['total_bonificable_pu'] = context_preuniv['total_bonificable']
            context['fecha'] = fecha

            context['lista_res'] = list()
            if context_univ.has_key('lista_res'):
                context['lista_res'].extend(context_univ['lista_res'])
                nro_forms_univ = len(context_univ['lista_res'])
            if context_preuniv.has_key('lista_res'):
                context['lista_res'].extend(context_preuniv['lista_res'])
                nro_forms_preuniv = len(context_preuniv['lista_res'])

            # Calculo de las remuneraciones y retenciones que son por persona.
            # Esto modifica el contexto.
            afiliacion_adiuc = commonform.cleaned_data['afiliado']
            #calcular_ganancias = commonform.cleaned_data['ganancias']
            context = calculateRemRetPorPersona(context, afiliacion_adiuc, commonform)
            #### Usando el neto, chequeo si hacen falta aplicar garantias salariales.
            #context = calculateGarantiasSalariales(context, context_univ['codigos_cargo'], context_preuniv['lista_res'], fecha)
            # Renderizo el template con el contexto.
            return render_to_response('salary_calculated.html', context)

        else:
            context['univformset'] = univformset
            context['preunivformset'] = preunivformset
            context['commonform'] = commonform
            #context['detailsform'] = detailsform

    else:

        # Creamos formularios vacios (sin bindear) y los mandamos.
        univformset = CargoUnivFormSet(prefix='univcargo')
        preunivformset = CargoPreUnivFormSet(prefix='preunivcargo')
        commonform = CommonForm()
        #detailsform = DetailsForm()

        context['univformset'] = univformset
        context['preunivformset'] = preunivformset
        context['commonform'] = commonform
        #context['detailsform'] = detailsform

    return render_to_response('calculate.html', context)

#Calcula montos por persona
def calculateRemRetPorPersona(context, afiliacion_adiuc, commonform):
    has_doctorado = commonform.cleaned_data['doctorado']
    has_master = commonform.cleaned_data['master']
    has_especialista = commonform.cleaned_data['especialista']
    es_afiliado = afiliacion_adiuc
    fecha = context['fecha']
    total_rem = context['total_rem']
    total_no_rem = context['total_no_rem']
    total_ret = context['total_ret']
    total_neto = context['total_neto']
    total_bonificable_u = context['total_bonificable_u']
    total_bonificable_pu = context['total_bonificable_pu']
    total_bonificaciones_u = 0.0
    total_bonificaciones_pu = 0.0
    form_bonif_u = {}
    form_bonif_pu = {}
    bonif_u ={}
    bonif_pu = {}
    form_ret_porc = {}
    form_ret = {}
    ret_porc_persona = list()
    ret_fijas_persona = list()
    rem_porc_persona = list()
    rem_fijas_persona = list()
    
    #Bonificaciones
    if (total_bonificable_u != 0): #Esta condicion se da en caso de haber 1 o mas univ forms
        bonif_u = get_bonificaciones(fecha, has_doctorado, has_master, has_especialista, 'U', total_bonificable_u)
        pp.pprint(bonif_u)
        form_bonif_u = {
        'bonificacion_u': bonif_u['bonificaciones_list'],
        'total_bonificaciones': bonif_u['total_bonificaciones']
        }    
        total_bonificaciones_u = bonif_u['total_bonificaciones']
        rem_porc_persona.append(form_bonif_u)
        
    if (total_bonificable_pu != 0): #Esta condicion se da en caso de haber 1 o mas preuniv forms
        bonif_pu = get_bonificaciones(fecha, has_doctorado, has_master, has_especialista, 'P', total_bonificable_pu)    
        form_bonif_pu = {
        'bonificacion_pu': bonif_pu['bonificaciones_list'],
        'total_bonificaciones': bonif_pu['total_bonificaciones']
        }            
        total_bonificaciones_pu = bonif_pu['total_bonificaciones']
        rem_porc_persona.append(form_bonif_pu)         
    
    #Retenciones porcentuales
    datos_desc_porc = get_retenciones_porcentuales(fecha, total_rem, es_afiliado)            
    form_ret_porc = {
            'retenciones_porcentuales': datos_desc_porc['ret_porc_calculadas'],
            'total_ret_porc' : datos_desc_porc['total_ret_porc']
            }
    ret_porc_persona.append(form_ret_porc)
    
    #retenciones fijas
    datos_desc = get_retenciones_fijas(fecha)    
    form_ret = {
            'retenciones_fijas': datos_desc['ret_fijas'],
            'total_ret_fijas': datos_desc['total_ret_fijas']
            }
    ret_fijas_persona.append(form_ret)
    
    total_ret = datos_desc_porc['total_ret_porc'] + datos_desc['total_ret_fijas']
    total_neto = total_rem + total_no_rem + total_bonificaciones_u + total_bonificaciones_pu - total_ret
    
    context['total_rem'] = total_rem
    context['total_no_rem'] = total_no_rem
    context['total_ret'] = total_ret
    context['total_neto'] = total_neto
    #context['total_bonificable'] = total_bonificable    
    context['ret_fijas_persona'] = ret_fijas_persona
    context['ret_porc_persona'] = ret_porc_persona
    context['rem_fijas_persona'] = rem_fijas_persona
    context['rem_porc_persona'] = rem_porc_persona
    
    pp.pprint(ret_fijas_persona)
    pp.pprint(ret_porc_persona)
    pp.pprint(rem_fijas_persona)
    pp.pprint(rem_porc_persona)
    
    return context    

# Retorna el porcentaje de aumento en base a la antiguedad
def get_antiguedad(antig, fecha, aplicacion):    
    antiguedad = Antiguedad.objects.filter(
            antig_desde__lte=antig,
            antig_hasta__gte=antig,
            desde__lte=fecha,
            hasta__gte=fecha,
            aplicado_a=aplicacion
            )
    if not antiguedad.exists():
        return False
    else:
        return antiguedad[0].porcentaje

# Retorna el basico
def get_basico(cargo_obj, fecha, antig):
    basico = ValoresRemuneracionFija.objects.filter(
            cargo = cargo_obj,
            remuneracion__nombre=u'Basico',
            remuneracion__desde__lte=fecha,
            remuneracion__hasta__gte=fecha
        )
    return False if not basico.exists() else basico[0].valor

#Funcion para obtener todos los datos referidos a un cargo
def get_data(cargo_obj, fecha, antig, horas, aplicacion):

    remunerativo = 0.0
    no_remunerativo = 0.0
    bonificable = 0.0       
    rem_list = list()  # Tuplas (obj remuneracion, importe).
    ret_list = list() # Tuplas (obj retencion, importe)
    result = {}
    context = {}    

    #Obtengo el porcentaje de antiguedad
    #Primero considero el caso de los preuniversitarios con menos de 1 año de anriguedad    
    if antig == u'0' and aplicacion == "P":
        antiguedad = 0
    else:
        antiguedad = get_antiguedad(antig, fecha, aplicacion)
        if not antiguedad:
            context['error_msg'] = u'No existe información de Salarios Básicos \
                para los datos ingresados. Por favor intente con otros datos.'
            return context
        
    # Obtengo el basico   
    basico = get_basico(cargo_obj, fecha, antig)
    if not basico:
        result['error_msg'] = u'No existe información de Salarios Básicos \
            para los datos ingresados. Por favor intente con otros datos.'
        return result
    
    if (cargo_obj.pago_por_hora):
        bonificable += basico * horas
    else:
        bonificable += basico 
    
    if (cargo_obj.pago_por_hora):
        remunerativo += basico * horas
    else:
        remunerativo += basico
    
     	
    #Obtengo otras remuneraciones fijas para el cargo, fecha y antiguedad
    rems_fijas = ValoresRemuneracionFija.objects.filter(
            cargo = cargo_obj,
            remuneracion__desde__lte=fecha,
            remuneracion__hasta__gte=fecha          
            ).exclude(remuneracion__nombre = u'Basico')
    if rems_fijas.exists():
        for rem_fija in rems_fijas:
            if (rem_fija.remuneracion.remunerativo):
                remunerativo += rem_fija.valor
            else:
                no_remunerativo += rem_fija.valor
            if (rem_fija.remuneracion.bonificable):
                bonificable += rem_fija.valor
            
            rem_list.append( (rem_fija, rem_fija.valor))
                
	# Obtengo las remuneraciones fijas relacionadas con un cargo y una antigüedad
    rems_fijas_cargo_antiguedad = ValoresRemuneracionFijaConAntig.objects.filter(
                        cargo = cargo_obj,
                        remuneracion__desde__lte=fecha,
                        remuneracion__hasta__gte=fecha,
                        antig_desde__lte = antig,
                        antig_hasta__gte = antig                                        
                        )
    if rems_fijas_cargo_antiguedad.exists():        
        for rem_fija in rems_fijas_cargo_antiguedad:
            if (rem_fija.remuneracion.remunerativo):
                remunerativo += rem_fija.valor
            else:
                no_remunerativo += rem_fija.valor
            if (rem_fija.remuneracion.bonificable):
                bonificable += rem_fija.valor
                
            rem_list.append( (rem_fija, rem_fija.valor))
    
    
    #Procedo al calculo de la antiguedad
    antiguedad_monto = bonificable * antiguedad / 100
    
    #Calculo de los descuentos
    # (actualmente no tenemos retenciones por cargo)
    
    #Lleno el context que devuelvo como resultado
    result['basico'] = basico
    result['rem_list'] = rem_list
    result['remunerativo'] = remunerativo + antiguedad_monto
    result['no_remunerativo'] = no_remunerativo
    result['bonificable'] = bonificable
    result['antiguedad'] = antiguedad
    result['antiguedad_monto'] = antiguedad_monto
    result['anios'] = antig
    if (cargo_obj.pago_por_hora):
        result['basico_horas'] = basico * horas
    else:
        result['basico_horas'] = 0.0
    return result

#Obtiene los descuentos fijos por PERSONA
def get_retenciones_fijas(fecha):
    ret_fijas = list()    
    fijas = 0.0
    result = {}    
    
    ret_fijas = RetencionFija.objects.filter(
            desde__lte=fecha,
            hasta__gte=fecha 
            )
    if ret_fijas:
        for ret_fija in ret_fijas:
            fijas += ret_fija.valor   
            
    result['ret_fijas'] = ret_fijas
    result['total_ret_fijas'] = fijas    
    return result

#Obtiene los descuentos porcentuales por PERSONA
def get_retenciones_porcentuales(fecha, remunerativo, es_afiliado):
    ret_porcentuales = list()
    ret_porc_calculadas = list()
    total_ret_porc = 0.0
    result = {}
    
    if (es_afiliado):
        ret_porcentuales = RetencionPorcentual.objects.filter(
                desde__lte=fecha,
                hasta__gte=fecha 
                )
    else:
        ret_porcentuales = RetencionPorcentual.objects.filter(
                desde__lte=fecha,
                hasta__gte=fecha               
                ).exclude( nombre = u'ADIUC')
    if ret_porcentuales:
        for ret_porc in ret_porcentuales:
            ret_porc_calculada = remunerativo * ret_porc.porcentaje / 100
            ret_porc_calculadas.append((ret_porc, ret_porc_calculada))
            total_ret_porc += ret_porc_calculada
        
    result['ret_porcentuales'] = ret_porcentuales
    result['ret_porc_calculadas'] = ret_porc_calculadas
    result['total_ret_porc'] = total_ret_porc
    return result

#Obtiene las bonificaciones por titulo de posgrado
def get_bonificaciones(fecha, has_doctorado, has_master, has_especialista, tipo_cargo, total_bonificable):
    bonificaciones = list()
    bonificaciones_list = list()
    bonif_calculada = 0.0
    total_bonificaciones = 0.0
    result = {}
    porcentaje_bonif = 0.0

    #Para cargos universitarios
    if(tipo_cargo == "U"):  
        if(has_doctorado):
           bonificaciones = Bonificacion.objects.filter(
                   desde__lte=fecha,
                   hasta__gte=fecha,
                   ref = u'AdicDoctorado'
                   )
        elif(has_master):
           bonificaciones = Bonificacion.objects.filter(
                   desde__lte=fecha,
                   hasta__gte=fecha,
                   ref = u'AdicMaestria'
                   )
        elif(has_especialista):
           bonificaciones = Bonificacion.objects.filter(
                   desde__lte=fecha,
                   hasta__gte=fecha,
                   ref = u'AdicEspec'
                   )
        if bonificaciones:
            for bonif in bonificaciones:
                bonif_calculada = total_bonificable * bonif.porcentaje / 100
                bonificaciones_list.append((bonif, bonif_calculada))
                total_bonificaciones += bonif_calculada
                
    #Para cargos preuniversitarios
    elif(tipo_cargo == "P"):
        if(has_doctorado):
           bonificaciones = Bonificacion.objects.filter(
                   desde__lte=fecha,
                   hasta__gte=fecha,
                   ref = u'AdicDoctoradoPU'
                   )
        elif(has_master):
           bonificaciones = Bonificacion.objects.filter(
                   desde__lte=fecha,
                   hasta__gte=fecha,
                   ref = u'AdicMaestriaPU'
                   )
        elif(has_especialista):
           bonificaciones = Bonificacion.objects.filter(
                   desde__lte=fecha,
                   hasta__gte=fecha,
                   ref = u'AdicEspecPU'
                   )           
        if bonificaciones:
            for bonif in bonificaciones:
                bonif_calculada = total_bonificable * bonif.porcentaje / 100
                bonificaciones_list.append((bonif, bonif_calculada))
                total_bonificaciones += bonif_calculada

    result['bonificaciones'] = bonificaciones
    result['bonificaciones_list'] = bonificaciones_list
    result['total_bonificaciones'] = total_bonificaciones
    return result
    

def processUnivFormSet(commonform, univformset):
    """Procesa un formset con formularios de cargos universitarios. Retorna un context"""

    antig = commonform.cleaned_data['antiguedad']
    fecha = datetime.date(int(commonform.cleaned_data['anio']), int(commonform.cleaned_data['mes']), 10)  
    has_doctorado = commonform.cleaned_data['doctorado']
    has_master = commonform.cleaned_data['master']
    has_especialista = commonform.cleaned_data['especialista']
    bonif_doctorado = 0.0
    bonif_master = 0.0
    bonif_especialista = 0.0    
    es_afiliado = commonform.cleaned_data['afiliado'] #Es afiliado a ADIUC?
    context = {}

    #Guardo en esta lista un diccionario para cada formulario procesado
    lista_res = list() 

    total_rem = 0.0
    total_no_rem = 0.0
    total_rem_cargo = 0.0
    total_remuneraciones = 0.0
    total_bonificable = 0.0
    total_ret = 0.0
    total_neto = 0.0
    horas = 0

    for univform in univformset:
        # No analizamos los forms que fueron borrados por el usuario.
        if univform in univformset.deleted_forms:
            continue
        # Obtengo el cargo
        cargo_obj = univform.cleaned_data['cargo']
        ###### Obtengo todo lo necesario en un dict.
        datos = get_data(cargo_obj, fecha, antig, horas, 'U')
        if datos.has_key('error_msg'):
            context['error_msg'] = datos['error_msg']
            return context
        #Remuneracion total para ese cargo
        total_rem_cargo = datos['remunerativo'] + datos['no_remunerativo']

        # Aqui iran los resultados del calculo para este cargo en particular.
        form_res = {
            'cargo': cargo_obj,
            'basico': datos['basico'],
            'remunerativo': datos['remunerativo'],
            'no_remunerativo': datos['no_remunerativo'],
            'remuneraciones' : datos['rem_list'],
            'bonificable': datos['bonificable'],
            'total_rem_cargo': total_rem_cargo,
            'antiguedad': datos['antiguedad'],
            'antiguedad_importe': datos['antiguedad_monto'],
            'anios' : datos['anios']
        }
        lista_res.append(form_res)

        # Calculo los acumulados de los salarios para todos los cargos univs.
        # y tambien los acumulados de las remuneraciones y retenciones.
        total_rem += datos['remunerativo']
        total_no_rem += datos['no_remunerativo']
        total_remuneraciones += total_rem_cargo
        total_bonificable += datos['bonificable']

    #Salario neto
    total_neto = total_rem + total_no_rem - total_ret
    
    context['total_rem'] = total_rem
    context['total_no_rem'] = total_no_rem
    context['total_ret'] = total_ret
    context['total_neto'] = total_neto
    context['total_bonificable'] = total_bonificable    
    context['lista_res'] = lista_res
    
    print("Univ")
    
    pp.pprint (lista_res)

    return context


def processPreUnivFormSet(commonform, preunivformset):
    """Procesa un formset con formularios de cargos preuniversitarios.
    Retorna un context."""

    antig = commonform.cleaned_data['antiguedad']
    #fecha = commonform.cleaned_data['fecha']
    fecha = datetime.date(int(commonform.cleaned_data['anio']), int(commonform.cleaned_data['mes']), 10)
    has_doctorado = commonform.cleaned_data['doctorado']
    has_master = commonform.cleaned_data['master']
    has_especialista = commonform.cleaned_data['especialista']
    es_afiliado = commonform.cleaned_data['afiliado']
    bonif_doctorado = 0.0
    bonif_master = 0.0
    bonif_especialista = 0.0
    context = {}

    #guardo en esta lista un diccionario para cada formulario procesado
    #en cada una de estas, los resultados para renderizar luego.
    lista_res = list()

    # Itero sobre todos los cargos.
    total_rem = 0.0
    total_no_rem = 0.0
    total_ret = 0.0
    total_neto = 0.0
    total_rem_cargo = 0.0
    total_remuneraciones = 0.0
    total_bonificable = 0.0

   
    for preunivform in preunivformset:

        if preunivform in preunivformset.deleted_forms:
            continue

        cargo_obj = preunivform.cleaned_data['cargo']
        horas = preunivform.cleaned_data['horas']

        datos = get_data(cargo_obj, fecha, antig, horas, 'P')
        if datos.has_key('error_msg'):
            context['error_msg'] = datos['error_msg']
            return context

        #Remuneracion total para ese cargo
        total_rem_cargo = datos['remunerativo'] + datos['no_remunerativo']

        # Calculo los acumulados de los salarios para todos los cargos preunivs.
        # y tambien los acumulados de las remuneraciones y retenciones.
        total_rem += datos['remunerativo']
        total_no_rem += datos['no_remunerativo']
        total_remuneraciones += total_rem_cargo
        total_bonificable += datos['bonificable']

        # Aqui iran los resultados del calculo para este cargo en particular.
        form_res = {
            'cargo': cargo_obj,
            'basico': datos['basico'],
            'basico_horas': datos['basico_horas'],
            'remunerativo': datos['remunerativo'],
            'no_remunerativo': datos['no_remunerativo'],
            'remuneraciones' : datos['rem_list'],
            'bonificable': datos['bonificable'],
            'total_rem_cargo': total_rem_cargo,
            'antiguedad': datos['antiguedad'],
            'antiguedad_importe': datos['antiguedad_monto'],
            'anios': datos['anios']
        }
        lista_res.append(form_res)
    
    #Salario neto
    total_neto = total_rem + total_no_rem - total_ret
    
    context['total_rem'] = total_rem
    context['total_no_rem'] = total_no_rem
    context['total_ret'] = total_ret
    context['total_neto'] = total_neto
    context['total_bonificable'] = total_bonificable 
    context['lista_res'] = lista_res

    print ("Preuniv")
    pp.pprint (lista_res)

    return context

