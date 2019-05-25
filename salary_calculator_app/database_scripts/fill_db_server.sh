#!/bin/bash

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

# Especifica bien el orden en que deben ejecutarse los scripts que llenan
# la base de datos con los datos basicos.

# Correr con:
# bash salary_calculator_app/database_scripts/fill_db_server.sh

export PYTHONPATH=`pwd`

scripts=(
    "remuneraciones_retenciones_data.py"
    "univ_data.py"
    "preuniv_data.py"
    "antiguedad_data.py"
    "fondo_solidario_data.py"
    "retencion_daspu_data.py"
    "impuesto_ganancias_data.py"
)

prefix="salary_calculator_app/database_scripts/"

for s in "${scripts[@]}"
do 
    echo "Running $s ..."
    python2.7  $prefix$s
done
