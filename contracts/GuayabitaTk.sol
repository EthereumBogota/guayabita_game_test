// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";

contract GuayabitaTk is ERC20, ERC20Burnable, ERC20Permit {
    constructor(address initialOwner)
        ERC20("GuayabitaTk", "GU")
        ERC20Permit("GuayabitaTk")
    {}

    function mint(address to, uint256 amount) public  {
        _mint(to, amount);
    }
}
