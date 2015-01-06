# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class ProfileForm(forms.ModelForm):
    """Edit profile form."""
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "last_name", "first_name", "is_active", "is_superuser", "is_staff"]

class ProfileCreationForm(UserCreationForm):
    """New profile form."""
    class Meta:
        model = get_user_model()
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages["duplicate_username"])