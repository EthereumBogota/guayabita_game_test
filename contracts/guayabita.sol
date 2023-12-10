// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract JuegoDado {
    address public jugador1;
    address public jugador2;
    uint256 public sumaJugador1;
    uint256 public sumaJugador2;
    uint256 public caseMinima;
    bool public juegoActivo;
    address public ganador;

    event NuevoTurno(address jugador, uint256 resultadoDado, uint256 sumaApostada, uint256 nuevaSuma);

    modifier soloJugadores() {
        require(msg.sender == jugador1 || msg.sender == jugador2, "No eres un jugador");
        _;
    }

    modifier juegoEnCurso() {
        require(juegoActivo, "El juego ha terminado");
        _;
    }

    constructor(address _jugador2, uint256 _sumaInicialJugador1, uint256 _sumaInicialJugador2, uint256 _caseMinima) {
        jugador1 = msg.sender;
        jugador2 = _jugador2;
        sumaJugador1 = _sumaInicialJugador1;
        sumaJugador2 = _sumaInicialJugador2;
        caseMinima = _caseMinima;
        juegoActivo = true;
    }

    function lanzarDado() public soloJugadores juegoEnCurso {
        uint256 resultadoDado = (uint256(keccak256(abi.encodePacked(block.difficulty, block.timestamp, msg.sender))) % 6) + 1;

        emit NuevoTurno(msg.sender, resultadoDado, caseMinima, 0);

        if (resultadoDado == 1) {
            // Jugador pierde y coloca el valor del case en la mesa
            colocarEnMesa(msg.sender, caseMinima);
        } else if (resultadoDado == 6) {
            // Jugador toma el valor mínimo del case y cambia de turno
            uint256 valorGanado = caseMinima;
            cambiarTurno(msg.sender, valorGanado);
        } else {
            // Jugador tiene un segundo turno
            emit NuevoTurno(msg.sender, 0, caseMinima, 0);
        }
    }

    function segundoTurno(uint256 apuesta) public soloJugadores juegoEnCurso {
        require(apuesta >= caseMinima, "La apuesta debe ser al menos el valor del case");

        uint256 resultadoDado = (uint256(keccak256(abi.encodePacked(block.difficulty, block.timestamp, msg.sender))) % 6) + 1;

        emit NuevoTurno(msg.sender, resultadoDado, apuesta, 0);

        if (resultadoDado > 1) {
            // Jugador gana la apuesta
            uint256 valorGanado = apuesta * 2;
            cambiarTurno(msg.sender, valorGanado);
        } else {
            // Jugador pierde la apuesta y se cambia de turno
            colocarEnMesa(msg.sender, apuesta);
        }
    }

    function colocarEnMesa(address jugador, uint256 cantidad) internal {
        if (jugador == jugador1) {
            sumaJugador1 -= cantidad;
        } else {
            sumaJugador2 -= cantidad;
        }

        if (sumaJugador1 <= 0 || sumaJugador2 <= 0) {
            // El juego ha terminado
            juegoActivo = false;
            if (sumaJugador1 > 0) {
                ganador = jugador1;
            } else if (sumaJugador2 > 0) {
                ganador = jugador2;
            } else {
                // Empate
                ganador = address(0);
            }
        }
    }

    function cambiarTurno(address jugador, uint256 valorGanado) internal {
        if (jugador == jugador1) {
            sumaJugador1 += valorGanado;
        } else {
            sumaJugador2 += valorGanado;
        }
    }
}