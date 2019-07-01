#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 11:56:19 2019

@author: lromano
"""

from models import *
import csv

with open('cargo.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        denominacion = row[0]
        pampa = row[1]
        aplicacion = row [2]
        horas = row[3]
        por_hora = row[4]
        cargo = Cargo(denominacion, pampa, aplicacion, horas, por_hora)
        cargo.save()
        
        
        