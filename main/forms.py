from django import forms
from django.core.validators import FileExtensionValidator, RegexValidator
from django.conf import settings
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .helper_functions import *


class passportDataForm(forms.Form):
    faceId = forms.ImageField(
        label="चेहरा छवि/Face Image",
    )
    sign = forms.ImageField(
        label="हस्ताक्षर/Signature",
    )
    type = forms.CharField(
        max_length=255,
        label="प्रकार/Type",
        validators=[RegexValidator("^[a-zA-Z]*$", message="Invalid Input")],
    )
    countryCode = forms.CharField(
        max_length=3,
        label="देश कोड/Country Code",
        validators=[RegexValidator("^[a-zA-Z]*$", message="Invalid Input")],
    )
    passNum = forms.CharField(
        max_length=255,
        label="पासपोर्ट संख्या/Passport No",
        validators=[RegexValidator("^[a-zA-Z0-9]*$", message="Invalid Input")],
    )
    surname = forms.CharField(
        max_length=255,
        label="उपनाम/Surname",
        validators=[RegexValidator("^[a-zA-Z' ]*$", message="Invalid Input")],
    )
    holderName = forms.CharField(
        max_length=255,
        label="प्रदत्त नाम/Given Name",
        validators=[RegexValidator("^[a-zA-Z' ]*$", message="Invalid Input")],
    )
    nationality = forms.CharField(
        max_length=255,
        label="राष्ट्रीयता/Nationality",
        validators=[RegexValidator("^[a-zA-Z]*$", message="Invalid Input")],
    )
    GENDER_CHOICES = [("M", "M"), ("F", "F"), ("O", "O")]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect, label="लिंग/Sex"
    )
    dob = forms.DateField(
        widget=DatePickerInput(format="%d/%m/%Y"),
        input_formats=settings.DATE_INPUT_FORMATS,
        label="जन्म की तारीख/ Date of Birth",
    )
    placeOfBirth = forms.CharField(
        max_length=255,
        label="जन्म स्थान/Place of Birth",
        validators=[RegexValidator("^[a-zA-Z0-9, ]*$", message="Invalid Input")],
    )
    placeOfIssue = forms.CharField(
        max_length=255,
        label="जारी करने का स्थान/Place of issue",
        validators=[RegexValidator("^[a-zA-Z0-9, ]*$", message="Invalid Input")],
    )
    dateOfIssue = forms.DateField(
        widget=DatePickerInput(format="%d/%m/%Y"),
        input_formats=settings.DATE_INPUT_FORMATS,
        label="जारी करने की तिथि/Date of issue",
    )
    dateOfExpiry = forms.DateField(
        widget=DatePickerInput(format="%d/%m/%Y"),
        input_formats=settings.DATE_INPUT_FORMATS,
        label="समाप्ति की तिथि/Date of expiry",
    )
    father = forms.CharField(
        max_length=255,
        label="पिता/कानूनी अभिभावक का नाम/Name of Father/Legal Guardian",
        validators=[RegexValidator("^[a-zA-Z' ]*$", message="Invalid Input")],
    )
    mother = forms.CharField(
        max_length=255,
        label="माता का नाम/Name of Mother",
        validators=[RegexValidator("^[a-zA-Z' ]*$", message="Invalid Input")],
    )
    spouse = forms.CharField(
        required=False,
        max_length=255,
        label="पति या पत्नी का नाम/Name of Spouse",
        validators=[RegexValidator("^[a-zA-Z' ]*$", message="Invalid Input")],
    )
    address_1 = forms.CharField(max_length=255, label="पता पंक्ति १/Address Line 1")
    address_2 = forms.CharField(max_length=255, label="पता पंक्ति २/Address Line 2")
    address_3 = forms.CharField(max_length=255, label="पता पंक्ति ३/Address Line 3")
    oldPassNum = forms.CharField(
        required=False,
        max_length=255,
        label="पुराना पासपोर्ट नंबर/Old Passport Number",
        validators=[RegexValidator("^[a-zA-Z0-9]*$", message="Invalid Input")],
    )
    oldPlaceIssue = forms.CharField(
        required=False,
        max_length=255,
        label="पुराना पासपोर्ट जारी करने का स्थान/Old Passport Place of Issue",
        validators=[RegexValidator("^[a-zA-Z0-9, ]*$", message="Invalid Input")],
    )
    oldDateIssue = forms.DateField(
        required=False,
        widget=DatePickerInput(format="%d/%m/%Y"),
        input_formats=settings.DATE_INPUT_FORMATS,
        label="जारी करने की पुरानी पासपोर्ट तिथि/Old Passport Date of Issue",
    )
    fileNum = forms.CharField(
        max_length=255,
        label="फाइल संख्या/File number",
        validators=[RegexValidator("^[a-zA-Z0-9]*$", message="Invalid Input")],
    )

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data["dob"]
        dateOfIssue = cleaned_data["dateOfIssue"]
        dateOfExpiry = cleaned_data["dateOfExpiry"]
        oldDateIssue = cleaned_data["oldDateIssue"]

        if dob == None or not any_date_before_today(str(dob)):
            raise forms.ValidationError({"dob": "Invalid Input"})
        if (
            dateOfIssue == None
            or dateOfExpiry == None
            or not issue_expiry_checker(str(dateOfIssue), str(dateOfExpiry))
        ):
            raise forms.ValidationError(
                {"dateOfIssue": "Invalid Input", "dateOfExpiry": "Invalid Input"}
            )
        if oldDateIssue != None and not any_date_before_today(str(oldDateIssue)):
            raise forms.ValidationError({"oldDateIssue": "Invalid Input"})

        return cleaned_data


class passportNumberForm(forms.Form):
    passNum = forms.CharField(
        max_length=255,
        label="पासपोर्ट संख्या/Passport No",
        validators=[RegexValidator("^[a-zA-Z0-9]*$", message="Invalid Input")],
    )
