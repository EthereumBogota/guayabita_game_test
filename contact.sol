// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

contract MiPrimerContrato {

    string saludo = "Saludos desde Bogota";


    function leerSaludo() public view returns (string memory) {
        return saludo;
    }


    function guardarSaludo(string memory nuevoSaludo) public {
        saludo = nuevoSaludo;
    }
}