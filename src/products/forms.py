from django import forms


class CreateAccountForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()
    address_title = forms.CharField()
    company = forms.CharField(required=False)
    address_first_name = forms.CharField()
    address_last_name = forms.CharField()
    address = forms.CharField()
    address_2 = forms.CharField(required=False)
    zip_code = forms.CharField()
    city = forms.CharField()
    phone = forms.CharField()
    entrance_code = forms.CharField(required=False)
    intercom = forms.CharField(required=False)
    stairs = forms.CharField(required=False)
    floor = forms.CharField(required=False)
    apartment_number = forms.CharField(required=False)
    comment = forms.CharField(required=False)

