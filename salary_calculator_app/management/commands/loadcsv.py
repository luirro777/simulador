from django.core.management.base import BaseCommand
from salary_calculator_app.models import *
import csv

# Importa datos a un modelo desde un csv
class Command(BaseCommand):
    help = 'runs your code in the django environment'     
    def handle(self, *args, **options):
        for model_id in args:
            if model_id == 'Cargo':
                with open('Cargo.csv', 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for row in spamreader:
                        deno = row[0]
                        pa = row[1]
                        apli = row [2]
                        hor = row[3]
                        por_hor = row[4]
                        cargo = Cargo(denominacion = deno, pampa = pa, tipo_cargo = apli, horas = hor, pago_por_hora = por_hor)
                        cargo.save()
            elif model_id == 'RetencionPorcentual':
                with open('RetencionPorcentual.csv', 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for row in spamreader:
                        refe = row[0]
                        codi = row[1]
                        nom = row[2]
                        porce = row[3]
                        des = row[4]
                        has = row[5]
                        retpor = RetencionPorcentual(ref = refe, codigo = codi, nombre = nom,
                                                 porcentaje = porce, desde = des, hasta = has)
                        retpor.save()
            elif model_id == 'RetencionFija':
                with open('RetencionFija.csv', 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for row in spamreader:
                        refe = row[0]
                        codi = row[1]
                        nom = row[2]
                        val = row[3]
                        des = row[4]
                        has = row[5]
                        por_c = row[6]
                        car = row[7]
                        retfi = RetencionFija(ref = refe, codigo = codi, nombre = nom,
                                          valor = val, desde = des, hasta = has, por_cargo = por_c, cargo = car)
                        retfi.save()
            elif model_id == 'RemuneracionFija':
                with open('RemuneracionFija.csv', 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for row in spamreader:
                        refe = row[0]
                        codi = row[1]
                        nom = row[2]
                        remu = row[3]
                        boni = row[4]
                        des = row[5]
                        has = row[6]
                        remufi = RemuneracionFija(ref = refe, codigo = codi, nombre = nom, 
                                              remunerativo = remu, bonificable = boni, desde = des, hasta = has)                    
                        remufi.save()
            elif model_id == 'ValoresRemuneracionFija':
                with open('ValoresRemuneracionFija.csv', 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for row in spamreader:
                        remu = row[0]
                        car = row[1]
                        val = row[2]
                        valremufi = ValoresRemuneracionFija(remuneracion = remu, cargo = car, valor = val)
                        valremufi.save()
            elif model_id == 'ValoresRemuneracionFijaConAntig':
                with open('ValoresRemuneracionFijaConAntig.csv', 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for row in spamreader:
                        
                        remu = RemuneracionFija.objects.get(ref = row[0])                       
                        car = Cargo.objects.get(pampa = row[1])
                        val = row[2]
                        antig_des = row[3]
                        antig_has = row[4]
                        valremuficonantig = ValoresRemuneracionFijaConAntig(remuneracion = remu, cargo = car, valor = val,
                                                        antig_desde = antig_des, antig_hasta = antig_has)     
                        valremuficonantig.save()
                        
                        
            elif model_id == 'Bonificacion':
                with open('Bonificacion.csv', 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for row in spamreader:
                        refe = row[0]
                        codi = row[1]
                        nom = row[3]
                        tipo = row[4]
                        porce = row[5]
                        des = row[6]
                        has = row[7]
                        bonificacion = Bonificacion(ref = refe, codigo = codi, nombre = nom, tipo_bonificacion = tipo,
                                                    porcentaje = porce, desde = des, hasta = has)
                        bonificacion.save()
            elif model_id == 'Antiguedad':
                with open('Antiguedad.csv', 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for row in spamreader:
                        refe = row[0]
                        codi = row[1]
                        nom = row[3]
                        apli = row[4]
                        antig_des = row[5]
                        antig_has = row[6]
                        porce = row[7]
                        des = row[8]
                        has = row[9]
                        antiguedad = Antiguedad(ref = refe, codigo = codi, nombre = nom, aplicado_a = apli,
                                                antig_desde = antig_des, antig_hasta = antig_has, porcentaje = porce,
                                                desde = des, hasta = has)
                        antiguedad.save()
            else:
                print("""
                      Opcion no valida. Las opciones son:
                    Cargo
                    RetencionPorcentual
                    RetencionFija
                    RemuneracionFija
                    ValoresRemuneracionFija
                    ValoresRemuneracionFijaConAntig
                    Bonificacion
                    Antiguedad                    
                    """)
                    

                    
