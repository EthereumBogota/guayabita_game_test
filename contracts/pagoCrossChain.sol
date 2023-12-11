// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import {CCIPReceiver} from "@chainlink/contracts-ccip/src/v0.8/ccip/applications/CCIPReceiver.sol";
import {IRouterClient} from "@chainlink/contracts-ccip/src/v0.8/ccip/interfaces/IRouterClient.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";
import {LinkTokenInterface} from "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";
import {GuayabitaTk} from "./GuayabitaTk.sol";

/**
 * THIS IS AN EXAMPLE CONTRACT THAT USES HARDCODED VALUES FOR CLARITY.
 * THIS IS AN EXAMPLE CONTRACT THAT USES UN-AUDITED CODE.
 * DO NOT USE THIS CODE IN PRODUCTION.
 */
contract pagoCrossChain is CCIPReceiver  {

    GuayabitaTk public token;

	// Custom errors to provide more descriptive revert messages.
	error NotEnoughBalance(uint256 currentBalance, uint256 calculatedFees); // Used to make sure contract has enough balance to cover the fees.
	error NothingToWithdraw(); // Used when trying to withdraw Ether but there's nothing to withdraw.
	error FailedToWithdrawEth(address owner, address target, uint256 value); // Used when the withdrawal of Ether fails.

	IRouterClient public router;
	LinkTokenInterface public linkToken;
	uint64 public destinationChainSelector;
	address public owner;

	event MessageSent(bytes32 messageId);

	constructor(
        address routerAddressSource,
        address routerAddressTarget,
        address linkAddress,
        uint64 _destinationChainSelector) 
          CCIPReceiver(routerAddressTarget) {
    	owner = msg.sender;    	
    	router = IRouterClient(routerAddressSource);
    	linkToken = LinkTokenInterface(linkAddress);
    	linkToken.approve(routerAddressSource, type(uint256).max);

    	// to Sepolia
    	// https://docs.chain.link/ccip/supported-networks#ethereum-sepolia
    	destinationChainSelector = _destinationChainSelector;
	}

	function transferOnSepolia(
        address destinationAddress,
        address spender,
        uint256 value) external {
    	Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
        	receiver: abi.encode(destinationAddress),
        	data: abi.encodeWithSignature("payment(address,address,uint256,uint256,uint8,bytes32,bytes32)", 
			        spender, value),
        	tokenAmounts: new Client.EVMTokenAmount[](0),
        	extraArgs: Client._argsToBytes(
            	Client.EVMExtraArgsV1({gasLimit: 500_000})
        	),
        	feeToken: address(linkToken)
    	});

    	// Get the fee required to send the message
    	uint256 fees = router.getFee(destinationChainSelector, message);

    	if (fees > linkToken.balanceOf(address(this)))
        	revert NotEnoughBalance(linkToken.balanceOf(address(this)), fees);

    	bytes32 messageId;
    	// Send the message through the router and store the returned message ID
    	messageId = router.ccipSend(destinationChainSelector, message);
    	emit MessageSent(messageId);
	}

	modifier onlyOwner() {
    	require(msg.sender == owner);
    	_;
	}

    function _ccipReceive(
    	Client.Any2EVMMessage memory message
	) internal override {
    	(bool success, ) = address(token).call(message.data);
    	require(success);
    	
	}

	function linkBalance (address account) public view returns (uint256) {
    	return linkToken.balanceOf(account);
	}

	function withdrawLINK(
    	address beneficiary
	) public onlyOwner {
    	uint256 amount = linkToken.balanceOf(address(this));
    	if (amount == 0) revert NothingToWithdraw();
    	linkToken.transfer(beneficiary, amount);
	}
}