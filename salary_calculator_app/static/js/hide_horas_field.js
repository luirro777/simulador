/*=============================================
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
==============================================*/

function show_horas(cargoObj)
{
    //console.debug("START: show_horas : " + cargoObj);

    var id = cargoObj.getAttribute("id").split("-");
    var formsetprefix = id[0] + "-" + id[1];
    var horasInfoObj = document.getElementById(formsetprefix + "-horas");
    var cargoPorHoraObj = document.getElementById(formsetprefix + "-pago_por_horas_info");
    var selectedCargo = cargoObj.options[cargoObj.selectedIndex].getAttribute("value");

    var cantHorasRowObj = horasInfoObj.parentElement.parentElement;

    var cargo_por_hora = false;
    for (var i=0; i<cargoPorHoraObj.options.length; i++) {
        var optObj = cargoPorHoraObj.options[i];
        if (optObj.getAttribute("value") == selectedCargo && optObj.innerHTML == "True") {
            cargo_por_hora = true;
            break;
        }
    }

    horasInfoObj.value = "1.0";

    if (cargo_por_hora) {
        cantHorasRowObj.style.display = "table-row";
        //console.debug("Showing horas field");
    }
    else {
        cantHorasRowObj.style.display = "none";
        //console.debug("Hidding horas field");
        var errorRowObj = document.getElementById(formsetprefix + "-horas-errors");
        if (errorRowObj != null) {
            //console.debug("Showing horas-errors row");
            errorRowObj.style.display = "none";
        }
    }

    //console.debug("END: show_horas");
}

function initial_show_horas(formsetPrefix)
{
    //console.debug("START: initial_show_horas() : " + formsetPrefix);
    id = "id_" + formsetPrefix;
    id = id + "-" + (get_total_forms(preunivPrefix)-1) + "-cargo";
    show_horas(document.getElementById(id));
    //console.debug("END: initial_show_horas");
}
