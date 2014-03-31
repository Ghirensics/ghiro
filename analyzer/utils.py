# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import StringIO

from PIL import Image
from django.db.models import Q

import analyzer.db as db
from hashes.models import List
from analyses.models import AnalysisMetadataDescription


class HashComparer():
    """Compares hashes with hashes lists."""
    @staticmethod
    def run(hashes, analysis):
        for key, value in hashes.iteritems():
            # Get all lists matching hash type.
            hash_lists = List.objects.filter(cipher=key).filter(Q(owner=analysis.owner) | Q(public=True))
            # Check hashes.
            for hash_list in hash_lists:
                if List.objects.filter(pk=hash_list.pk).filter(hash__value=value).exists():
                    hash_list.matches.add(analysis)



def str2image(data):
    """Converts binary data to PIL Image object.
    @param data: binarydata
    @return: PIL Image object
    """
    output = StringIO.StringIO()
    output.write(data)
    output.seek(0)
    return Image.open(output)

def image2str(img):
    """Converts PIL Image object to binary data.
    @param img: PIL Image object
    @return:  binary data
    """
    f = StringIO.StringIO()
    img.save(f, "JPEG")
    return f.getvalue()

def create_thumb(file_path):
    """Create thumbnail
    @param file_path: file path
    @return: GridFS ID
    """
    try:
        thumb = Image.open(file_path)
        thumb.thumbnail([200, 150], Image.ANTIALIAS)
        return db.save_file(data=image2str(thumb), content_type="image/jpeg")
    except:
        return None

def add_metadata_description(key, description):
    """Adds key metadata description to lookup table.
    @param key: fully qualified metadata key
    @param description: key description
    """
    # Skip if no description is provided.
    if description:
        try:
            AnalysisMetadataDescription.objects.get(key=key.lower())
        except AnalysisMetadataDescription.DoesNotExist:
            obj = AnalysisMetadataDescription(key=key.lower(), description=description)
            obj.save()
