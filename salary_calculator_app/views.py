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

import datetime

# Debugger
import pdb

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

            fecha = datetime.date(int(commonform.cleaned_data['anio']), int(commonform.cleaned_data['mes']), 10)
            # Hago el merge de los dos contexts.
            context['total_rem'] = total_rem
            context['total_no_rem'] = total_no_rem
            context['total_ret'] = total_ret
            context['total_neto'] = total_neto
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
            #afiliacion_daspu = commonform.cleaned_data['daspu']
            #afiliacion_daspu = ""
            afiliacion_adiuc = commonform.cleaned_data['afiliado']
            #calcular_ganancias = commonform.cleaned_data['ganancias']
            context = calculateRemRetPorPersona(
                context,
                afiliacion_adiuc,
                nro_forms_univ,
                nro_forms_preuniv
                )
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
'''
def calculateDASPU(fecha,remunerativo):
    
    daspu_context={}
    daspu_importe = 0.0
    daspu_extra = 0.0

    rets_porc_daspu = RetencionPorcentual.objects.filter(
        codigo =daspu_code,
        desde__lte=fecha,
        hasta__gte=fecha
        )
    if rets_porc_daspu.exists():
        r = rets_porc_daspu.order_by('hasta')[rets_porc_daspu.count()-1]

        daspu_objs = RetencionDaspu.objects.filter(
            retencion=r,
            )
        if not daspu_objs.exists():
            context["error_msg"] = "No existe informacion sobre afiliaciones para DASPU.\n"
        else:
            daspu_obj = daspu_objs[daspu_objs.count()-1]
            p = daspu_obj.retencion.porcentaje # 3%
            p_min = daspu_obj.porcentaje_minimo # 8%

            # Corroborar si no cubre el minimo de del cargo ayudante D.S.E. sin antiguedad.
            basicos = SalarioBasicoUniv.objects.filter(
                cargo=daspu_obj.cargo_referencia,
                vigencia__desde__lte=fecha,
                vigencia__hasta__gte=fecha
                )
            if not basicos.exists():
                context['error_msg']='No se encuentra la información salarial requerida para el cálculo.'
            else:
                basico = basicos.order_by('vigencia__hasta')[basicos.count()-1]
                basico = basico.valor
                daspu_importe += remunerativo * p / 100.0
                tope_min = basico * p_min / 100.0
            
                daspu_context['daspu_importe'] = daspu_importe                
            
                if daspu_importe < tope_min:
                    daspu_extra = tope_min - daspu_importe
                    daspu_context['daspu_extra'] = daspu_extra
                    daspu_context['daspu_importe'] = tope_min
                    daspu_importe = tope_min

                daspu_context['daspu'] = daspu_obj
        
    return daspu_context
'''

'''

def get_retenciones_clase(clase, aplicacion, modo, fecha):
    return clase.objects.filter(
        retencion__aplicacion=aplicacion,
        retencion__modo=modo,
        vigencia__desde__lte=fecha,
        vigencia__hasta__gte=fecha
    )

def get_remuneraciones_clase(clase, aplicacion, modo, fecha):
    return clase.objects.filter(
        remuneracion__aplicacion=aplicacion,
        remuneracion__modo=modo,
        vigencia__desde__lte=fecha,
        vigencia__hasta__gte=fecha
    )

def get_retenciones_remuneraciones(aplicacion, modo, fecha):
    """Devuelve en un dict las ret fijas, ret porc, rem fijas, rem porc
    que matchean la aplicacion, modo y fecha dadas."""
    get_retenciones = lambda clase: get_retenciones_clase(clase,
                                                          aplicacion,
                                                          modo,
                                                          fecha)
    get_remuneraciones = lambda clase: get_remuneraciones_clase(clase,
                                                                aplicacion,
                                                                modo,
                                                                fecha)


    result = dict()
    result['ret_fijas'] = get_retenciones(RetencionFija)
    result['ret_porcentuales'] = get_retenciones(RetencionPorcentual)
    result['rem_fijas'] = get_remuneraciones(RemuneracionFija)
    result['rem_porcentuales'] = get_remuneraciones(RemuneracionPorcentual)
    return result
'''

def get_remuneraciones_fijas(cargo_obj, fecha, antig):
    result = dict()
    #Obtengo las remuneraciones fijas
    result['rem_fijas'] = ValoresRemuneracionFija.objects.filter(
            desde__lte = fecha,
            hasta__gte = fecha,
            cargo = cargo_obj
            )
    result['rem_fijas_cargo_antig'] = ValoresRemuneracionFija.objects.filter(
            desde__lte = fecha,
            hasta__gte = fecha,
            cargo = cargo_obj
            )
    return result





def filter_doc_masters_from_rem_porcentuales(rem_porcentuales, has_doctorado, has_master, has_especialista, aplicacion):
    """Elimina las remuneraciones porcentuales asociadas a titulos adicionales segun
    lo que haya especificado el usuario."""

    m_code = ""
    d_code = ""

    if aplicacion == 'U':
        m_code = master_code
        d_code = doc_code
        e_code = esp_code
    elif aplicacion == 'P':
        m_code = master_preuniv_code
        d_code = doc_preuniv_code
        e_code = esp_preuniv_code

    if has_doctorado:
        rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=m_code)
        rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=e_code)
    elif has_master:
        rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=d_code)
        rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=e_code)
    elif has_especialista:
        rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=d_code)
        rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=m_code)
    else:
        rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=d_code)
        rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=m_code)
        rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=e_code)

    return rem_porcentuales

'''
def get_antiguedad(antiguedad, fecha):
    antiguedades = Antiguedad.objects.filter(
        anio=antiguedad,
        desde__lte=fecha,
        hasta__gte=fecha
    )
    return False if not antiguedades.exists() else antiguedades[0]

'''
# Retorna el porcentaje de aumento en base a la antiguedad
def get_antiguedad(antig, fecha, aplicacion):
    antiguedad = Antiguedad.objects.filter(
            antig_desde__lte=antig,
            antig_hasta__gte=antig,
            desde__lte=fecha,
            hasta__gte=fecha,
            aplicado_a=aplicacion
            )
    return False if not antiguedad.exists() else antiguedad.porcentaje


# Retorna el basico
def get_basico(cargo_obj, fecha, antig):
    basico = ValoresRemuneracionFija.objects.filter(
            cargo = cargo_obj,
            antig_desde__lte = antig,
            antig_hasta__gte = antig,
            vigencia__desde__lte=fecha,
            vigencia__hasta__gte=fecha,
            remuneracion__nombre=u'Basico'
        )
    return False if not basico.exists() else basico.valor


def get_data(cargo_obj, fecha, antig, horas, aplicacion):
    ###### Salario Bruto.
    # Registro el bonificable, el remunerativo y el no remunerativo
    # Es por CARGO
    remunerativo = 0.0
    no_remunerativo = 0.0
    bonificable = 0.0       
    rem_list = list()  # Tuplas (obj remuneracion, importe).
    ret_list = list() # Tuplas (obj retencion, importe)
    result = {}    

    #Obtengo el porcentaje de antiguedad
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
    
    bonificable += basico.valor # Sumo el basico al bonificable.
    remunerativo += basico.valor # Sumo el basico al remunerativo
    
     	
    #Obtengo otras remuneraciones fijas para el cargo, fecha y antiguedad
    rems_fijas = ValoresRemuneracionFija.objects.filter(
            cargo = cargo_obj,
            antig_desde__lte = antig,
            antig_hasta__gte = antig,
            vigencia__desde__lte=fecha,
            vigencia__hasta__gte=fecha,
            remuneracion__nombre!=u'Basico'            
            )
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
                        antig_desde__lte = antig,
                        antig_hasta__gte = antig,
                        vigencia__desde__lte=fecha,
                        vigencia__hasta__gte=fecha                                                
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
    result['remunerativo'] = remunerativo
    result['no_remunerativo'] = no_remunerativo
    result['bonificable'] = bonificable
    result['antiguedad'] = antiguedad
    result['antiguedad_monto'] = antiguedad_monto
    return result


def get_retenciones_fijas(fecha):
    #Obtiene los descuentos por PERSONA
    ret_fijas = list()    
    fijas = 0.0    
    
    ret_fijas = RetencionFija.objects.filter(
            vigencia__desde__lte=fecha,
            vigencia__hasta__gte=fecha 
            )
    if ret_fijas.exists():
        for ret_fija in ret_fijas:
            fijas += ret_fija.valor    
   
            
    result['ret_fijas'] = ret_fijas
    result['total_ret_fijas'] = fijas    
    return result

    

def processUnivFormSet(commonform, univformset):
    """Procesa un formset con formularios de cargos universitarios. Retorna un context"""

    antig = commonform.cleaned_data['antiguedad']
    fecha = datetime.date(int(commonform.cleaned_data['anio']), int(commonform.cleaned_data['mes']), 10)
    has_doctorado = commonform.cleaned_data['doctorado']
    has_master = commonform.cleaned_data['master']
    has_especialista = commonform.cleaned_data['especialista']
    #afiliacion adiuc:
    es_afiliado = commonform.cleaned_data['afiliado']
    context = {}

    #Guardo en esta lista un diccionario para cada formulario procesado
    lista_res = list() 

    total_rem = 0.0
    total_no_rem = 0.0
    total_remuneraciones = 0.0
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
        }
        lista_res.append(form_res)

        # Calculo los acumulados de los salarios para todos los cargos univs.
        # y tambien los acumulados de las remuneraciones y retenciones.
        total_rem += datos['remunerativo']
        total_no_rem += datos['no_remunerativo']
        total_remuneraciones += total_rem_cargo

    #Calculo los descuentos
    datos_desc = get_retenciones_fijas(fecha)
    
    #Aqui van las retenciones
    form_ret = {
            'descuentos': datos_desc['ret_list'],
            'total_ret_fijas': datos_desc['total_ret_fijas']
            }
    lista_res.append(form_ret)
    total_ret = datos_desc['total_ret_fijas']
    
    #Salario neto
    total_neto = total_rem + total_no_rem - total_ret
    
    context['total_rem'] = total_rem
    context['total_no_rem'] = total_no_rem
    context['total_ret'] = total_ret
    context['total_neto'] = total_neto
    context['lista_res'] = lista_res

    return context



def processPreUnivFormSet(commonform, preunivformset):
    """Procesa un formset con formularios de cargos preuniversitarios.
    Retorna un context."""

    antiguedad = commonform.cleaned_data['antiguedad']
    #fecha = commonform.cleaned_data['fecha']
    fecha = datetime.date(int(commonform.cleaned_data['anio']), int(commonform.cleaned_data['mes']), 10)
    has_doctorado = commonform.cleaned_data['doctorado']
    has_master = commonform.cleaned_data['master']
    has_especialista = commonform.cleaned_data['especialista']
    es_afiliado = commonform.cleaned_data['afiliado']
    context = {}

    #guardo en esta lista un diccionario para cada formulario procesado
    #en cada una de estas, los resultados para renderizar luego.
    lista_res = list()

    # Itero sobre todos los cargos.
    total_rem = 0.0
    total_no_rem = 0.0
    total_ret = 0.0
    total_neto = 0.0

   
    for preunivform in preunivformset:

        if preunivform in preunivformset.deleted_forms:
            continue

        cargo_obj = preunivform.cleaned_data['cargo']
        horas = preunivform.cleaned_data['horas']

        datos = get_data(cargo_obj, fecha, antig, horas, 'U')
        if datos.has_key('error_msg'):
            context['error_msg'] = datos['error_msg']
            return context


        ###### Salario Neto.
        salario_neto = remunerativo + no_remunerativo - descuentos

        # Aqui iran los resultados del calculo para este cargo en particular.
        form_res = {
            'cargo': cargo_obj,
            'basico_horas': basico.valor * horas,
            'basico': basico.valor,
            'retenciones': ret_list,
            'remuneraciones': rem_list,
            'descuentos': descuentos,
            'remunerativo': remunerativo,
            'no_remunerativo': no_remunerativo,
            'salario_neto': salario_neto,
            'antiguedad': antiguedad,
            'antiguedad_importe': antiguedad_importe
        }
        lista_res.append(form_res)

        #print form_res

        # Calculo los acumulados de los salarios para todos los cargos.
        # y tambien los acumulados de las remuneraciones y retenciones.
        total_rem += remunerativo
        total_no_rem += no_remunerativo
        total_ret += descuentos
        total_neto += salario_neto

    context['total_rem'] = total_rem
    context['total_no_rem'] = total_no_rem
    context['total_ret'] = total_ret
    context['total_neto'] = total_neto
    context['lista_res'] = lista_res

    return context

def ganancias(request):
#def ganancias(anio, cargo, antig, doct, master, afiliado):
    context = {}
    if request.method == 'POST':
        rem1, rem2 = 0.0 , 0.0
        desc1, desc2 = 0.0, 0.0
        descuentos = 0.19

        commonform = CommonForm(request.POST)
        ganancias_form = ImpuestoGananciasForm(request.POST)
        cargo_univ = CargoUnivForm(request.POST)

        if commonform.is_valid() and ganancias_form.is_valid() and cargo_univ.is_valid():
            anio = int(commonform.cleaned_data['anio'])
            cargo = cargo_univ.cleaned_data['cargo']
            antig = commonform.cleaned_data['antiguedad']
            doct = commonform.cleaned_data['doctorado']
            master = commonform.cleaned_data['master']
            afiliado = commonform.cleaned_data['afiliado']
            caja_compl = float(commonform.cleaned_data['caja_compl'])/100.

            descuentos += .015 if afiliado else 0.0
            descuentos += caja_compl
            # Calculo el neto anual.
            for mes in range(1,7):
                fecha = datetime.date(anio, mes, 10)
                datos = get_data(cargo, fecha, antig, doct, master, afiliado)
                rem1 += datos['remunerativo']
                desc1 += datos['remunerativo'] * descuentos
            sac1 = (rem1/6.0)/2.0
            desc1 += sac1 * descuentos
            rem1 += sac1
            for mes in range (7, 13):
                fecha = datetime.date(anio, mes, 10)
                datos = get_data(cargo, fecha, antig, doct, master, afiliado)
                rem2 += datos['remunerativo']
                desc2 += datos['remunerativo'] * descuentos
            sac2 = (rem2/6.0)/2.0
            desc2 += sac2 * descuentos
            rem2 += sac2

            neto_anual = rem1 + rem2 - desc1 - desc2

            context['neto_anual'] = neto_anual
            context['cargo'] = cargo
            context['anio'] = anio

            # Empiezo a descontar.
            lista_deduc = list()
            deducciones_total = 0.0
            conyuge = int(ganancias_form.cleaned_data['conyuge']) == 1
            nro_hijos = int(ganancias_form.cleaned_data['nro_hijos_menores_24'])
            nro_desc = int(ganancias_form.cleaned_data['nro_descendientes'])
            nro_asc = int(ganancias_form.cleaned_data['nro_ascendientes'])
            nro_suegros = int(ganancias_form.cleaned_data['nro_suegros_yernos_nueras'])
            otras_deduc = int(ganancias_form.cleaned_data['otros_descuentos'])

            deducciones = ImpuestoGananciasDeducciones.objects.filter(
                            vigencia__desde__lte=fecha,
                            vigencia__hasta__gte=fecha
                        )
            if not deducciones.exists():
                context['error_msg'] = u'No se encontró información para el año solicitado.'
                return context
            else:
                deducciones = deducciones[0]
            if deducciones.ganancia_no_imponible > 0.0:
                lista_deduc.append((u'Mínimo no imponible', deducciones.ganancia_no_imponible))
                deducciones_total += deducciones.ganancia_no_imponible
            if deducciones.desc_cuarta_cat > 0.0:
                lista_deduc.append((u'Descuento 4ta categoría', deducciones.desc_cuarta_cat))
                deducciones_total += deducciones.desc_cuarta_cat
            if conyuge:
                lista_deduc.append((u'Descuento por cónyuge', deducciones.por_conyuge))
                deducciones_total += deducciones.por_conyuge
            if nro_hijos > 0:
                lista_deduc.append((u'Descuento por hijo (*' + str(nro_hijos) + u')', deducciones.por_hijo*nro_hijos))
                deducciones_total += deducciones.por_hijo*nro_hijos
            if nro_desc > 0:
                lista_deduc.append((u'Descuento por descendiente (*' + str(nro_desc) + u')', deducciones.por_descendiente*nro_desc))
                deducciones_total += deducciones.por_descendiente*nro_desc
            if nro_asc > 0:
                lista_deduc.append((u'Descuento por ascendiente (*' + str(nro_asc) + u')', deducciones.por_ascendiente*nro_asc))
                deducciones_total += deducciones.por_ascendiente*nro_asc
            if nro_suegros > 0:
                lista_deduc.append((u'Descuento por suegro, yerno o nuera (*' + str(nro_suegros) + u')', deducciones.por_suegro_yerno_nuera*nro_suegros))
                deducciones_total += deducciones.por_suegro_yerno_nuera*nro_suegros
            if otras_deduc > 0:
                lista_deduc.append((u'Otras deducciones', otras_deduc))
                deducciones_total += otras_deduc
            context['lista_deduc'] = lista_deduc
            context['total_deduc'] = deducciones_total
            # Ingreso neto sujeto a impuestos.
            insai = neto_anual - deducciones_total
            context['insai'] = insai if insai > 0.0 else 0.0
            print context['insai'], neto_anual, deducciones_total
            if insai > 0.0:
                tabla = ImpuestoGananciasTabla.objects.filter(
                            vigencia__desde__lte=fecha,
                            vigencia__hasta__gte=fecha,
                            ganancia_neta_min__lte=insai,
                            ganancia_neta_max__gte=insai
                        )
                if not tabla.exists():
                    context['error_msg'] = u'No se encontró información para el año solicitado.'
                    return context
                else:
                    tabla = tabla[0]
                impuesto = tabla.suma_anterior + (insai - tabla.ganancia_neta_min)*tabla.impuesto_porcentual
            else:
                impuesto = 0.0
            context['impuesto'] = impuesto
            context['mensual'] = impuesto/13.0
            return render_to_response('ganancias_calculated.html', context)
        else:
            context['commonform'] = commonform
            context['univform'] = cargo_univ
            context['gananciasform'] = ganancias_form
    else:
        commonform = CommonForm()
        ganancias_form = ImpuestoGananciasForm()
        cargo_univ = CargoUnivForm()
        context['commonform'] = commonform
        context['univform'] = cargo_univ
        context['gananciasform'] = ganancias_form
    return render_to_response('ganancias.html', context)
