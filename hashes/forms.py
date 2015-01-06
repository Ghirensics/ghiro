# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import re
from django import forms

from hashes.models import List

class ListForm(forms.ModelForm):
    """Hash list form."""
    hash_list = forms.FileField(required=True)

    class Meta:
        model = List

    def clean_hash_list(self):
        file = self.cleaned_data["hash_list"]
        cipher = self.cleaned_data["cipher"].lower()

        # Checks file for validation line by line.
        for row in file.readlines():
            # Skip comments.
            if row.startswith("#"):
                continue
            # Skip empty lines.
            if len(row) == 0:
                continue
            # MD5.
            if cipher == "md5":
                if not re.match(r"^([a-fA-F\d]{32})$", row):
                    raise forms.ValidationError("Uploaded file does not met MD5 hash format: [a-fA-F\\d]{32}")
            # CRC32
            elif cipher == "crc32":
                if not re.match(r"^([a-fA-F\d]{8})$", row):
                    raise forms.ValidationError("Uploaded file does not met CRC32 hash format: [a-fA-F\\d]{8}")
            # SHA1.
            elif cipher == "sha1":
                if not re.match(r"^([a-fA-F\d]{40})$", row):
                    raise forms.ValidationError("Uploaded file does not met SHA1 hash format: [a-fA-F\\d]{40}")
            # SHA224.
            elif cipher == "sha224":
                if not re.match(r"^([a-fA-F\d]{56})$", row):
                    raise forms.ValidationError("Uploaded file does not met SHA224 hash format: [a-fA-F\\d]{56}")
            # SHA384.
            elif cipher == "sha384":
                if not re.match(r"^([a-fA-F\d]{96})$", row):
                    raise forms.ValidationError("Uploaded file does not met SHA386 hash format: [a-fA-F\\d]{96}")
            # SHA256.
            elif cipher == "sha256":
                if not re.match(r"^([a-fA-F\d]{64})$", row):
                    raise forms.ValidationError("Uploaded file does not met SHA256 hash format: [a-fA-F\\d]{64}")
            # SHA512.
            elif cipher == "sha512":
                if not re.match(r"^([a-fA-F\d]{128})$", row):
                    raise forms.ValidationError("Uploaded file does not met SHA512 hash format: [a-fA-F\\d]{128}")

        return file