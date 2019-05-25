#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: Franco Rodriguez (ffrodriguez@famaf.unc.edu.ar)
# date: 18/03/2013

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
#       CARGOS UNIVERSITARIOS                 #
#=============================================#

def add_denominacion(nombre):

    if DenominacionCargo.objects.filter(nombre=nombre).exists():
        return DenominacionCargo.objects.get(nombre=nombre)
    else:
        den = DenominacionCargo(nombre=nombre)
        den.save()
        return den



{
        "pk": 5,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Asesor Pedagógico"
        }
    },
    {
        "pk": 7,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Asesor Psicopedagógico"
        }
    },
    {
        "pk": 40,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Auxiliar Docente"
        }
    },
    {
        "pk": 53,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Ayud. Gabinete Práctico"
        }
    },
    {
        "pk": 52,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Ayud. Gabinete Práctico D.E"
        }
    },
    {
        "pk": 9,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Ayudante Clases Práct.(02)"
        }
    },
    {
        "pk": 12,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Ayudante Clases Prácticas"
        }
    },
    {
        "pk": 59,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Ayudante Gab. Psicoped."
        }
    },
    {
        "pk": 24,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Ayudante Trab.Prácticos"
        }
    },
    {
        "pk": 20,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Bibliot. Ley 22.416"
        }
    },
    {
        "pk": 26,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Bibliot.Ens. Superior"
        }
    },
    {
        "pk": 54,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Bibliotecario D.E"
        }
    },
    {
        "pk": 41,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Director 1º D.E"
        }
    },
    {
        "pk": 8,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Director Escuela Superior"
        }
    },
    {
        "pk": 13,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Director de 3º Categoría"
        }
    },
    {
        "pk": 49,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Gabinetista D.E"
        }
    },
    {
        "pk": 58,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Horas Cátedra Secundario"
        }
    },
    {
        "pk": 57,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Hs Cát. Inherentes a cargos"
        }
    },
    {
        "pk": 30,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Hs. Cát. Inherentes a cargos"
        }
    },
    {
        "pk": 29,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Hs. Cátedra Secundario"
        }
    },
    {
        "pk": 28,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Hs. Cátedra Terciario"
        }
    },
    {
        "pk": 36,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "J.T.P T.C (Esc. Comercio)"
        }
    },
    {
        "pk": 47,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Jefe Dpto D.E"
        }
    },
    {
        "pk": 33,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Jefe Equipo Tec.Pedagógico"
        }
    },
    {
        "pk": 48,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Jefe Gabinete Psicoped. D.E"
        }
    },
    {
        "pk": 3,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Jefe Gral Ens.Práctica"
        }
    },
    {
        "pk": 6,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Jefe Labor. Informática"
        }
    },
    {
        "pk": 51,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Jefe Preceptores 1º"
        }
    },
    {
        "pk": 50,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Jefe Preceptores 1º D.E"
        }
    },
    {
        "pk": 23,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Jefe Preceptores de 1º"
        }
    },
    {
        "pk": 22,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Maestro Ayud.Ens.Práctico"
        }
    },
    {
        "pk": 56,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Preceptor"
        }
    },
    {
        "pk": 55,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Preceptor D.E"
        }
    },
    {
        "pk": 27,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Preceptores"
        }
    },
    {
        "pk": 21,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Prof. Centro Deportivo"
        }
    },
    {
        "pk": 19,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Prof. Jefe Trab.Prácticos"
        }
    },
    {
        "pk": 37,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Prof. T.P (1)"
        }
    },
    {
        "pk": 38,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Prof. T.P (2)"
        }
    },
    {
        "pk": 39,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Prof. T.P (3)"
        }
    },
    {
        "pk": 62,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Profesor Adjunto"
        }
    },
    {
        "pk": 63,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Profesor Asistente"
        }
    },
    {
        "pk": 61,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Profesor Asociado"
        }
    },
    {
        "pk": 64,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Profesor Ayudante \"A\""
        }
    },
    {
        "pk": 65,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Profesor Ayudante \"B\""
        }
    },
    {
        "pk": 32,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Profesor T.P (4)"
        }
    },
    {
        "pk": 4,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Profesor TC"
        }
    },
    {
        "pk": 60,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Profesor Titular"
        }
    },
    {
        "pk": 14,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Prosecretario 1º (Esc.Com.)"
        }
    },
    {
        "pk": 35,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Prosecretario Nivel Superior"
        }
    },
    {
        "pk": 31,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Rector Educación Artística"
        }
    },
    {
        "pk": 11,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Rector de 1º Categoría"
        }
    },
    {
        "pk": 2,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Regente de 1º"
        }
    },
    {
        "pk": 43,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Regente de 1º D.E"
        }
    },
    {
        "pk": 16,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Regente de 1º Esc.Superior"
        }
    },
    {
        "pk": 15,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Regente de Esc.Superior"
        }
    },
    {
        "pk": 17,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Secret. de 1º Categoría"
        }
    },
    {
        "pk": 34,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Secretario 1º Categoría"
        }
    },
    {
        "pk": 18,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Secretario Esc.Superior"
        }
    },
    {
        "pk": 46,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Secretario de 1º Categ.D.E"
        }
    },
    {
        "pk": 44,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Sub Regente de 1º Cat. D.E"
        }
    },
    {
        "pk": 45,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Sub Regente de 1º Categoría"
        }
    },
    {
        "pk": 42,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Vice Director 1º D.E"
        }
    },
    {
        "pk": 10,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Vice Director Escuela Superior"
        }
    },
    {
        "pk": 1,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Vice Director de 1º"
        }
    },
    {
        "pk": 25,
        "model": "salary_calculator_app.denominacioncargo",
        "fields": {
            "nombre": "Vice Rector Escuela Artes"
        }
    },