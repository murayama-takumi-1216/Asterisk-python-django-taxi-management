from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(SignupForm):
    """
    Form for user registration on the public registration page.
    Extends allauth's SignupForm to ensure proper email verification flow.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

        # Update placeholders
        if "username" in self.fields:
            self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        if "email" in self.fields:
            self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        if "password1" in self.fields:
            self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        if "password2" in self.fields:
            self.fields["password2"].widget.attrs.update(
                {"placeholder": "Confirm Password"}
            )
