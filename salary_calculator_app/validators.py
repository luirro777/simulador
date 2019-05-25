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

from django.core.exceptions import ValidationError

def validate_isdigit(string):
	"""string es valido si no es vacio y si todos sus caracteres son digitos
	(0..9).
	Pre: string es una cadena de caracteres de python"""

	if not string.isdigit():
		raise ValidationError(u'Debe ingresar caracteres numéricos: "0", "1", "2", ... , "7", "8", "9".')

def validate_isgezero(number):
    """number es valido si es mayor o igual a 0."""

    if number<0:
        raise ValidationError(u'Debe ingresar un número positivo.')

def validate_isgzero(number):
	"""number es valido si es mayor estricto que 0."""

	if number<=0:
		raise ValidationError(u'Debe ingresar un número mayor a 0.')
