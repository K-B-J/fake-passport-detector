// SPDM-Liscence-Identifier: MIT

pragma experimental ABIEncoderV2;

pragma solidity >=0.6.0 <0.9.0;

contract PassportContract {
    struct Info {
        bool exists;
        string passnum;
        PersonalDetailInfo personalDetails;
        ImagesInfo images;
        PassportInfo passportInformation;
    }

    struct PersonalDetailInfo {
        string surname;
        string name;
        string nationality;
        string sex;
        string dob;
        string placeOfBirth;
        string father;
        string mother;
        string spouse;
        string currentAddress;
    }

    struct ImagesInfo {
        string facePhoto;
        string signaturePhoto;
    }

    struct PassportInfo {
        string ptype;
        string countryCode;
        string placeOfIssue;
        string dateOfIssue;
        string dateOfExpiry;
        string oldPassNumDateAndIssue;
        string fileNum;
    }

    mapping(string => Info) public passportMap;

    function storePassport(
        string memory _passnum,
        PersonalDetailInfo memory personalInfo,
        ImagesInfo memory imagesInfo,
        PassportInfo memory passportInfo
    ) public {
        require(
            passportMap[_passnum].exists == false,
            "Passport Already Exists!"
        );
        passportMap[_passnum] = Info(
            true,
            _passnum,
            personalInfo,
            imagesInfo,
            passportInfo
        );
    }

    function getPassportDetails(string memory _passnum)
        public
        view
        returns (string[20] memory)
    {
        return [
            passportMap[_passnum].passnum,
            passportMap[_passnum].personalDetails.surname,
            passportMap[_passnum].personalDetails.name,
            passportMap[_passnum].personalDetails.nationality,
            passportMap[_passnum].personalDetails.sex,
            passportMap[_passnum].personalDetails.dob,
            passportMap[_passnum].personalDetails.placeOfBirth,
            passportMap[_passnum].personalDetails.father,
            passportMap[_passnum].personalDetails.mother,
            passportMap[_passnum].personalDetails.spouse,
            passportMap[_passnum].personalDetails.currentAddress,
            passportMap[_passnum].images.facePhoto,
            passportMap[_passnum].images.signaturePhoto,
            passportMap[_passnum].passportInformation.ptype,
            passportMap[_passnum].passportInformation.countryCode,
            passportMap[_passnum].passportInformation.placeOfIssue,
            passportMap[_passnum].passportInformation.dateOfIssue,
            passportMap[_passnum].passportInformation.dateOfExpiry,
            passportMap[_passnum].passportInformation.oldPassNumDateAndIssue,
            passportMap[_passnum].passportInformation.fileNum
        ];
    }

    function updateDetails(
        string memory _passnum,
        PersonalDetailInfo memory personalInfo,
        ImagesInfo memory imagesInfo,
        PassportInfo memory passportInfo
    ) public {
        require(
            passportMap[_passnum].exists == true,
            "Passport Doesn't Exist!"
        );
        passportMap[_passnum] = Info(
            true,
            _passnum,
            personalInfo,
            imagesInfo,
            passportInfo
        );
    }
}
