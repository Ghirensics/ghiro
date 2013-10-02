# Ghiro - Copyright (C) 2013 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import os
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from analyses.models import Case, Analysis

class CaseForm(forms.ModelForm):
    """Case form."""
    class Meta:
        model = Case

class UploadImageForm(forms.ModelForm):
    """Image upload form."""
    image = forms.FileField(required=True)

    class Meta:
        model = Analysis
        fields = ["image"]

    def clean_image(self):
        image = self.cleaned_data.get("image", False)
        if image:
            # File check.
            if image._size > settings.MAX_FILE_UPLOAD:
                raise ValidationError("Image file too large")
            # Type check.
            file_type = image.content_type
            if not file_type in settings.ALLOWED_EXT:
                raise ValidationError("Image type not supported.")
        else:
            raise ValidationError("Image field is mandatory.")

class ImageFolderForm(forms.Form):
    """Folder upload form."""
    path = forms.CharField(required=True)

    def clean_image(self):
        path = self.cleaned_data.get("path", False)
        if path:
            # Checks if it exist.
            if not os.path.exists(path):
                raise ValidationError("Specified path not found.")
            # Checks if is a directory.
            if not os.path.isdir(path):
                raise ValidationError("Specified path is not a directory.")
        else:
            raise ValidationError("Path field is mandatory.")