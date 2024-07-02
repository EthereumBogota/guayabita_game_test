// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TestContract {

    string saludo = "Saludos desde Colombia";


    function leerSaludo() public view returns (string memory) {
        return saludo;
    }


    function guardarSaludo(string memory nuevoSaludo) public {
        saludo = nuevoSaludo;
    }
}
