// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract logs {
    string[] private log;
    event Logadded(string log, address sender);

    function addlog(string memory _log, address _sender) public {
        log.push(_log);
        emit Logadded(_log, _sender);
    }

    function getlog(uint256 _index) public view returns (string memory) {
        require(_index <= log.length - 1, "index out of bound");
        return log[_index];
    }

    function getalllogs() public view returns (string[] memory) {
        return log;
    }
}
