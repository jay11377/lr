from django import forms
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    # User
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # You must return the original result.
        return user


