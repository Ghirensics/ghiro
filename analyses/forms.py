# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import os
import magic

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from analyses.models import Case, Analysis, Comment
from ghiro.common import check_allowed_content

class CaseForm(forms.ModelForm):
    """Case form."""
    class Meta:
        model = Case

class CommentForm(forms.ModelForm):
    """Comment form."""
    class Meta:
        model = Comment

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
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(image.temporary_file_path())
            if not check_allowed_content(file_type):
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
            raise ValidationError("URL field is mandatory.")

class UrlForm(forms.Form):
    """Image url form."""
    url = forms.CharField(required=True)

    def clean_url(self):
        url = self.cleaned_data.get("url", False)
        if url:
            validate = URLValidator()
            try:
                validate(url)
            except ValidationError:
                raise ValidationError("Please enter a valid URL")
        else:
            raise ValidationError("Path field is mandatory.")
