Techniques
==========

Several techniques are used to extract all data and metadata hidden in
digital images. They are briefly described in this chapter.

MIME information
================

Multipurpose Internet Mail Extensions (MIME) is a standard to describe
content type of a file, MIME is detected using magic number inside the image.
Magic numbers implement strongly typed data and are a form of in-band signaling
to the controlling program that reads the data type(s) at program run-time. Many
files have such constants that identify the contained data.
Detecting such constants in files is a simple and effective way of distinguishing
between many file formats and can yield further run-time information.
The image MIME type is detected to know the image type your are dealing with, in
both contacted (example: image/jpeg) and extended form.

Metadata information
====================

Metadata may be written into a digital photo file that will identify who owns it,
copyright and contact information, what camera created the file, along with exposure
information and descriptive information such as keywords about the photo, making the
file searchable on the computer and/or the Internet.
Some metadata are written by the camera and some is input by the photographer and/or
software after downloading to a computer.
Metadata are divided in several categories depending on the standard they come from.
The following categories are extracted and analyzed:

 * EXIF metadata extraction
    * Standard Exif tags
    * Canon MakerNote tags
    * Fujifilm MakerNote tags
    * Minolta MakerNote tags
    * Nikon MakerNote tags
    * Olympus MakerNote tags
    * Panasonic MakerNote tags
    * Pentax MakerNote tags
    * Samsung MakerNote tags
    * Sigma/Foveon MakerNote tags
    * Sony MakerNote tags
 * IPTC metadata extraction
    * IPTC datasets
 * XMP metadata extraction
    * Dublin Core schema (dc)
    * XMP Basic schema (xmp)
    * XMP Rights Management schema (xmpRights)
    * XMP Media Management schema (xmpMM)
    * XMP Basic Job Ticket schema (xmpBJ)
    * XMP Paged-Text schema (xmpTPg)
    * XMP Dynamic Media schema (xmpDM)
    * Adobe PDF schema (pdf)
    * Photoshop schema (photoshop)
    * Camera Raw schema (crs)
    * Exif schema for TIFF Properties (tiff)
    * Exif schema for Exif-specific Properties (exif)
    * Exif schema for Additional Exif Properties (aux)
    * IPTC Core schema (Iptc4xmpCore)
    * IPTC Extension schema (Iptc4xmpExt)
    * PLUS License Data Format schema (plus)
    * digiKam Photo Management schema (digiKam)
    * KDE Image Program Interface schema (kipi)
    * Microsoft Photo schema (MicrosoftPhoto)
    * iView Media Pro schema (mediapro)
    * Microsoft Expression Media schema (expressionmedia)
    * Microsoft Photo 1.2 schema (MP)
    * Microsoft Photo RegionInfo schema (MPRI)
    * Microsoft Photo Region schema (MPReg)
    * Metadata Working Group Regions schema (mwg-rs)

Preview thumbnail extraction
============================

Most digital camera and phones write a preview, called thumbnail, in image metadata.
The thumbnails and data related to them are extracted from image metadata and stored for review.

Preview thumbnail consistency
=============================

Sometimes when a photo is edited, if the image editing software does not support image preview,
the original image is edited but the thumbnail not. A simple comparison between the original image and
the thumbnail could detect image edits.

GPS Localization
================

Embedded in the image metadata sometimes there is a geotag, a bit of GPS data providing the longitude and
latitude of where the photo was taken.
Geotagging is when a device such as an iPhone, Android smartphone or digital camera stores your location
or geographical information, such as your GPS coordinates, within a photo.
A geotagged photograph is a photograph which is associated with a geographical location by geotagging.
Geotags are useful in helping people find a wide variety of location-specific information.
For example, one can find images taken near a given location by entering latitude and longitude coordinates
into a suitable image search engine.
The geotag inside image metadata is read and the position where the photo was taken is displayed on a map.

ELA (Error Level Analysis)
==========================

`Error Level Analysis`_ (ELA) is a technique aimed to detect if an image is edited or not.
It can be applied to compressed images, i.e. JPEG or PNG. The main idea is that an image in his original form has unique levels of compression.
The analyzed image is resaved and differences in compression levels are calculated, if differences are detected a probability of edits is high.
Ghiro calculates error levels and detects differences between them.

.. _`Error Level Analysis`: http://blackhat.com/presentations/bh-dc-08/Krawetz/Whitepaper/bh-dc-08-krawetz-WP.pdf

Hash digest generation
======================

Most common hash are calculated for the image, to create an unique identifier of it.
The calculated hashes are:

 * CRC32
 * MD5
 * SHA1
 * SHA224
 * SHA256
 * SHA384
 * SHA512

Hash list matching
==================

Suppose you are searching for an image and you have only the hash.
You can provide a list of hashes and all images matching are reported.

Strings extraction
==================

All text strings contained in the analyzed image are extracted, like in the unix
strings tool. The more interesting (i.e. URLs) are highlighted.

Signature engine
================

Signature provides evidence about most critical data to highlight focal points and common exposures.
Signature engine to highlight common exposure on over 120 signatures