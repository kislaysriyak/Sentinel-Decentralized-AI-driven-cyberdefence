// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract logs {
    // ==============================================================================
    // struct to store log details
    // ==============================================================================
    struct Log {
        string attackType;
        string ipAddress;
        string macAddress;
    }
    Log[] public loglist;
    // ==============================================================================
    // event to be emitted when a new log is added
    // ==============================================================================
    event Logadded(
        string attackType,
        string ipAddress,
        string macAddress,
        address sender
    );
    // ==============================================================================
    // function to add a new log
    // ==============================================================================
    function addlog(
        string memory _attackType,
        string memory _ipAddress,
        string memory _macAddress
    ) public {
        Log memory newLog = Log(_attackType, _ipAddress, _macAddress);
        loglist.push(newLog);
        emit Logadded(_attackType, _ipAddress, _macAddress, msg.sender);
    }
    // ==============================================================================
    // function to get the log at a particular index
    // ==============================================================================
    function getlog(
        uint256 _index
    ) public view returns (string memory, string memory, string memory) {
        require(_index <= loglist.length - 1, "index out of bound");
        Log memory l = loglist[_index];
        return (l.attackType, l.ipAddress, l.macAddress);
    }
}
