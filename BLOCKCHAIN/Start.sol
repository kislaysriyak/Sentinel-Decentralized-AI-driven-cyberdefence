// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;
contract Start {
    uint256 public number;
    struct Person {
        uint256 number;
        string name;
    }

    Person[] public people;

    function store(uint256 _number) public {
        number = _number;
    }
    mapping(string => uint256) public nametonumber;

    function retrieve() public view returns (uint256) {
        return number;
    }

    function addperson(string memory _name, uint256 _number) public {
        people.push(Person({number: _number, name: _name}));
        nametonumber[_name] = number;
    }
}
