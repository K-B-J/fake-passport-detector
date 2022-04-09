// SPDM-Liscence-Identifier: MIT
pragma experimental ABIEncoderV2;

pragma solidity >=0.6.0 <0.9.0;

contract PassportContract {
    struct Info {
        bool exists;
        string passnum;
        string name;
        string dob;
    }

    mapping(string => Info) public passportMap;

    function storePassport(
        string memory _passnum,
        string memory _name,
        string memory _dob
    ) public {
        require(
            passportMap[_passnum].exists == false,
            "Passport Already Exists!"
        );
        passportMap[_passnum] = Info(true, _passnum, _name, _dob);
    }

    function getPassportDetails(string memory _passnum)
        public
        view
        returns (Info memory)
    {
        return passportMap[_passnum];
    }

    function updateDetails(string memory _passnum, string memory _name) public {
        require(
            passportMap[_passnum].exists == true,
            "Passport Doesn't Exist!"
        );
        passportMap[_passnum].passnum = _passnum;
        passportMap[_passnum].name = _name;
    }
}
