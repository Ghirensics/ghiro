# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from lib.analyzer.base import BaseSignature

class ExifCanonOwnerName(BaseSignature):
    pk = 1001
    severity = 2
    category = "personal information"
    name = "EXIF Canon Owner name detected"
    description = "Owner name provided by Canon metadata"

    def check(self, data):
        if data['metadata']['Exif']['Canon']['OwnerName']:
            return 'EXIF OwnerName', data['metadata']['Exif']['Canon']['OwnerName']

class ExifImageSoftwareAvailable(BaseSignature):
    pk = 1002
    severity = 1
    category = "editing information"
    name = "Exif Image Software detected"
    description = "This tag records the name and version of the software or firmware of the camera or image input device used to generate the image. The detailed format is not specified, but it is recommended that the example shown below be followed. When the field is left blank, it is treated as unknown."

    def check(self, data):
        if data['metadata']['Exif']['Image']['Software']:
            return 'EXIF Image Software', data['metadata']['Exif']['Image']['Software']

class XMPCreatorToolSoftwareAvailable(BaseSignature):
    pk = 1003
    severity = 1
    category = "editing information"
    name = "XMP CreatorTool Software detected"
    description = "Photo editing software name is available in metadata"

    def check(self, data):
        if data['metadata']['Xmp']['xmp']['CreatorTool']:
            return 'XMP CreatorTool', data['metadata']['Xmp']['xmp']['CreatorTool']
        
class XMPPDFProducerSoftwareAvailable(BaseSignature):
    pk = 1004
    severity = 1
    category = "editing information"
    name = "XMP PDF Producer Software detected"
    description = "The name of the tool that created the PDF document."

    def check(self, data):
        if data['metadata']['Xmp']['pdf']['Producer']:
            return 'XMP PDF Producer', data['metadata']['Xmp']['pdf']['Producer']

class ExifImageModelAvailable(BaseSignature):
    pk = 1005
    severity = 1
    category = "hardware information"
    name = "Exif Image Model available"
    description = "The model name or model number of the equipment. This is the model name or number of the DSC, scanner, video digitizer or other equipment that generated the image. When the field is left blank, it is treated as unknown."

    def check(self, data):
        if data['metadata']['Exif']['Image']['Model']:
            return 'EXIF Image Model', data['metadata']['Exif']['Image']['Model']

class ExifCanonMeta(BaseSignature):
    pk = 1006
    severity = 1
    category = "hardware information"
    name = "Exif Canon metadata available"
    description = "Canon proprietary metadata are available"

    def check(self, data):
        if data['metadata']['Exif']['Canon']:
            return True

class ExifCanonSiMeta(BaseSignature):
    pk = 1007
    severity = 1
    category = "hardware information"
    name = "Exif CanonSi metadata available"
    description = "Canon proprietary metadata are available"

    def check(self, data):
        if data['metadata']['Exif']['CanonSi']:
            return True

class ExifCanonCsMeta(BaseSignature):
    pk = 1008
    severity = 1
    category = "hardware information"
    name = "Exif CanonCs metadata available"
    description = "Canon proprietary metadata are available"

    def check(self, data):
        if data['metadata']['Exif']['CanonCs']:
            return True

class ExifPhotoDateTimeOriginalAvailable(BaseSignature):
    pk = 1009
    severity = 2
    category = "time information"
    name = "Exif Photo DateTimeOriginal available"
    description = "The date and time when the original image data was generated. For a digital still camera the date and time the picture was taken are recorded."

    def check(self, data):
        if data['metadata']['Exif']['Photo']['DateTimeOriginal']:
            return 'EXIF Photo DateTimeOriginal', data['metadata']['Exif']['Photo']['DateTimeOriginal']

class ExifPhotoDateTimeDigitizedAvailable(BaseSignature):
    pk = 1010
    severity = 2
    category = "time information"
    name = "Exif Photo DateTimeDigitized available"
    description = "The date and time when the image was stored as digital data."

    def check(self, data):
        if data['metadata']['Exif']['Photo']['DateTimeDigitized']:
            return 'EXIF Photo DateTimeDigitized', data['metadata']['Exif']['Photo']['DateTimeDigitized']

class ExifImageDateTimeAvailable(BaseSignature):
    pk = 1011
    severity = 2
    category = "time information"
    name = "Exif Image DateTime available"
    description = "Photo date and time is available in metadata"

    def check(self, data):
        if data['metadata']['Exif']['Image']['DateTime']:
            return 'EXIF Image DateTime', data['metadata']['Exif']['Image']['DateTime']

class XMPCreateDateAvailable(BaseSignature):
    pk = 1012
    severity = 2
    category = "time information"
    name = "XMP CreateDate available"
    description = "Photo date and time is available in metadata"

    def check(self, data):
        if data['metadata']['Xmp']['xmp']['CreateDate']:
            return 'XMP CreateDate', data['metadata']['Xmp']['xmp']['CreateDate']

class XMPModifyDateAvailable(BaseSignature):
    pk = 1013
    severity = 2
    category = "time information"
    name = "XMP ModifyDate available"
    description = "Photo date and time is available in metadata"

    def check(self, data):
        if data['metadata']['Xmp']['xmp']['ModifyDate']:
            return 'XMP ModifyDate', data['metadata']['Xmp']['xmp']['ModifyDate']

class XMPMetadataDateAvailable(BaseSignature):
    pk = 1014
    severity = 2
    category = "time information"
    name = "XMP MetadataDate available"
    description = "Photo date and time is available in metadata"

    def check(self, data):
        if data['metadata']['Xmp']['xmp']['MetadataDate']:
            return 'XMP MetadataDate', data['metadata']['Xmp']['xmp']['MetadataDate']

class XMPPhotoshopDateCreatedAvailable(BaseSignature):
    pk = 1015
    severity = 2
    category = "time information"
    name = "XMP Photoshop DateCreated available"
    description = "Photo date and time is available in metadata"

    def check(self, data):
        if data['metadata']['Xmp']['photoshop']['DateCreated']:
            return 'XMP Photoshop DateCreated', data['metadata']['Xmp']['photoshop']['DateCreated']

class ExifPhotoUserCommentAvailable(BaseSignature):
    pk = 1016
    severity = 2
    category = "personal information"
    name = "Exif Photo UserComment available"
    description = "A tag for Exif users to write keywords or comments on the image besides those in <ImageDescription>, and without the character code limitations of the <ImageDescription> tag."

    def check(self, data):
        if data['metadata']['Exif']['Photo']['UserComment']:
            return 'EXIF Photo UserComment', data['metadata']['Exif']['Photo']['UserComment']

class ExifImageMakeAvailable(BaseSignature):
    pk = 1017
    severity = 1
    category = "hardware information"
    name = "Exif Image Make available"
    description = "The manufacturer of the recording equipment. This is the manufacturer of the DSC, scanner, video digitizer or other equipment that generated the image. When the field is left blank, it is treated as unknown."

    def check(self, data):
        if data['metadata']['Exif']['Image']['Make']:
            return 'EXIF Image Make', data['metadata']['Exif']['Image']['Make']

class ThumbAvailable(BaseSignature):
    pk = 1018
    severity = 1
    category = "editing information"
    name = "Exif preview available"
    description = "A thumbnail in exif metadata is available"

    def check(self, data):
        if data['metadata']['Exif']['Thumbnail']:
            return True

class ExifGPSInfoLatLongAvailable(BaseSignature):
    pk = 1019
    severity = 3
    category = "position information"
    name = "Exif GPSInfo GPSLatitude and GPSLongitude available"
    description = "EXIF GPS localization data are available"

    def check(self, data):
        if data['metadata']['Exif']['GPSInfo']['GPSLatitude'] and data['metadata']['Exif']['GPSInfo']['GPSLongitude']:
            return True

class XMPXmpmmAvailable(BaseSignature):
    pk = 1020
    severity = 3
    category = "editing information"
    name = "XMP XMPmm available"
    description = "Metadata contains history for changes related to image editing"

    def check(self, data):
        if data['metadata']['Xmp']['xmpMM']:
            for key in data['metadata']['Xmp']['xmpMM'].keys():
                if key.startswith('History'):
                    return True

class IPTCApplication2WriterAvailable(BaseSignature):
    pk = 1021
    severity = 2
    category = "personal information"
    name = "IPTC Application2 Writer available"
    description = "Identification of the name of the person involved in the writing."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['Writer']:
            return 'IPTC Application2 Writer', data['metadata']['Iptc']['Application2']['Writer']

class XMPPhotoshopCaptionWriterAvailable(BaseSignature):
    pk = 1022
    severity = 2
    category = "personal information"
    name = "XMP Photoshop CaptionWriter available"
    description = "Photo editor writer information are available"

    def check(self, data):
        if data['metadata']['Xmp']['photoshop']['CaptionWriter']:
            return 'XMP Photoshop CaptionWriter', data['metadata']['Xmp']['photoshop']['CaptionWriter']

class ExifImageArtistAvailable(BaseSignature):
    pk = 1023
    severity = 2
    category = "personal information"
    name = "Exif Image Artist available"
    description = "This tag records the name of the camera owner, photographer or image creator. The detailed format is not specified, but it is recommended that the information be written as in the example below for ease of Interoperability. When the field is left blank, it is treated as unknown. Ex.)"

    def check(self, data):
        if data['metadata']['Exif']['Image']['Artist']:
            return 'Exif Image Artist', data['metadata']['Exif']['Image']['Artist']

class ExifImageCopyrightAvailable(BaseSignature):
    pk = 1024
    severity = 2
    category = "personal information"
    name = "Exif Image Copyright available"
    description = "Copyright information. In this standard the tag is used to indicate both the photographer and editor copyrights. It is the copyright notice of the person or organization claiming rights to the image. The Interoperability copyright statement including date and rights should be written in this field; e.g., \"Copyright, John Smith, 19xx. All rights reserved.\". In this standard the field records both the photographer and editor copyrights, with each recorded in a separate part of the statement. When there is a clear distinction between the photographer and editor copyrights, these are to be written in the order of photographer followed by editor copyright, separated by NULL (in this case since the statement also ends with a NULL, there are two NULL codes). When only the photographer copyright is given, it is terminated by one NULL code . When only the editor copyright is given, the photographer copyright part consists of one space followed by a terminating NULL code, then the editor copyright is given. When the field is left blank, it is treated as unknown."

    def check(self, data):
        if data['metadata']['Exif']['Image']['Copyright']:
            return 'Exif Image Copyright', data['metadata']['Exif']['Image']['Copyright']

class IptcApplication2SubLocationAvailable(BaseSignature):
    pk = 1025
    severity = 3
    category = "position information"
    name = "IPTC Application2 SubLocation available"
    description = "Identifies the location within a city from which the object data originates."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['SubLocation']:
            return 'IPTC Application2 SubLocation', data['metadata']['Iptc']['Application2']['SubLocation']

class IptcApplication2CityAvailable(BaseSignature):
    pk = 1026
    severity = 3
    category = "position information"
    name = "IPTC Application2 City available"
    description = "Identifies city of object data origin according to guidelines established by the provider."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['City']:
            return 'IPTC Application2 City', data['metadata']['Iptc']['Application2']['City']

class IptcApplication2ProvinceAvailable(BaseSignature):
    pk = 1027
    severity = 3
    category = "position information"
    name = "IPTC Application2 Province available"
    description = "Province localization data are available"

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['Province']:
            return 'IPTC Application2 Province', data['metadata']['Iptc']['Application2']['Province']

class IptcApplication2ProvinceStateAvailable(BaseSignature):
    pk = 1028
    severity = 3
    category = "position information"
    name = "IPTC Application2 ProvinceState available"
    description = "Identifies Province/State of origin according to guidelines established by the provider."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['ProvinceState']:
            return 'IPTC Application2 ProvinceState', data['metadata']['Iptc']['Application2']['ProvinceState']

class IptcApplication2BylineAvailable(BaseSignature):
    pk = 1029
    severity = 2
    category = "personal information"
    name = "IPTC Application2 Byline available"
    description = "Photo author information is available"

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['Byline']:
            return 'IPTC Application2 Byline', data['metadata']['Iptc']['Application2']['Byline']

class IptcApplication2CountryCodeAvailable(BaseSignature):
    pk = 1030
    severity = 2
    category = "position information"
    name = "IPTC Application2 CountryCode available"
    description = "Indicates the code of the country/primary location where the intellectual property of the object data was created."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['CountryCode']:
            return 'IPTC Application2 CountryCode', data['metadata']['Iptc']['Application2']['CountryCode']

class IptcApplication2DateCreatedAvailable(BaseSignature):
    pk = 1031
    severity = 2
    category = "time information"
    name = "IPTC Application2 DateCreated available"
    description = "Represented in the form CCYYMMDD to designate the date the intellectual content of the object data was created rather than the date of the creation of the physical representation. Follows ISO 8601 standard."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['DateCreated']:
            return 'IPTC Application2 DateCreated', data['metadata']['Iptc']['Application2']['DateCreated']

class IptcApplication2TimeCreatedAvailable(BaseSignature):
    pk = 1031
    severity = 2
    category = "time information"
    name = "IPTC Application2 TimeCreated available"
    description = "Photo date and time is available in metadata"

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['TimeCreated']:
            return 'IPTC Application2 TimeCreated', data['metadata']['Iptc']['Application2']['TimeCreated']

class IptcApplication2CopyrightAvailable(BaseSignature):
    pk = 1032
    severity = 2
    category = "personal information"
    name = "IPTC Application2 Copyright available"
    description = "Photo author information is available"

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['Copyright']:
            return 'IPTC Application2 Copyright', data['metadata']['Iptc']['Application2']['Copyright']

class IptcApplication2DigitizationDateAvailable(BaseSignature):
    pk = 1033
    severity = 2
    category = "time information"
    name = "IPTC Application2 DigitizationDate available"
    description = "Photo date and time is available in metadata"

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['DigitizationDate']:
            return 'IPTC Application2 DigitizationDate', data['metadata']['Iptc']['Application2']['DigitizationDate']

class IptcApplication2DigitizationTimeAvailable(BaseSignature):
    pk = 1034
    severity = 2
    category = "time information"
    name = "IPTC Application2 DigitizationTime available"
    description = "Photo date and time is available in metadata"

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['DigitizationTime']:
            return 'IPTC Application2 DigitizationTime', data['metadata']['Iptc']['Application2']['DigitizationTime']

class IptcApplication2CountryNameAvailable(BaseSignature):
    pk = 1035
    severity = 2
    category = "position information"
    name = "IPTC Application2 CountryName available"
    description = "Country name localization data is available"

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['CountryName']:
            return 'IPTC Application2 CountryName', data['metadata']['Iptc']['Application2']['CountryName']

class XMPPhotoshopCountryAvailable(BaseSignature):
    pk = 1036
    severity = 2
    category = "position information"
    name = "XMP Photoshop Country available"
    description = "Country name localization data is available"

    def check(self, data):
        if data['metadata']['Xmp']['photoshop']['Country']:
            return 'XMP Photoshop Country', data['metadata']['Xmp']['photoshop']['Country']

class XMPPhotoshopStateAvailable(BaseSignature):
    pk = 1037
    severity = 2
    category = "position information"
    name = "XMP Photoshop State available"
    description = "State name localization data is available"

    def check(self, data):
        if data['metadata']['Xmp']['photoshop']['State']:
            return 'XMP Photoshop State', data['metadata']['Xmp']['photoshop']['State']

class XMPPhotoshopCityAvailable(BaseSignature):
    pk = 1038
    severity = 3
    category = "position information"
    name = "XMP Photoshop City available"
    description = "City name localization data is available"

    def check(self, data):
        if data['metadata']['Xmp']['photoshop']['City']:
            return 'XMP Photoshop City', data['metadata']['Xmp']['photoshop']['City']

class XMPCCAttributionNameAvailable(BaseSignature):
    pk = 1039
    severity = 2
    category = "personal information"
    name = "XMP CC AttributionName available"
    description = "Photo author information is available"

    def check(self, data):
        if data['metadata']['Xmp']['cc']['attributionName']:
            return 'XMP CC AttributionName', data['metadata']['Xmp']['cc']['attributionName']

class XMPDCCreatorAvailable(BaseSignature):
    pk = 1040
    severity = 2
    category = "personal information"
    name = "XMP DC Creator available"
    description = "Photo author information is available"

    def check(self, data):
        if data['metadata']['Xmp']['dc']['creator']:
            return 'XMP DC Creator', data['metadata']['Xmp']['dc']['creator']

class XMPIptcCountryCodeAvailable(BaseSignature):
    pk = 1041
    severity = 2
    category = "position information"
    name = "XMP IPTC CountryCode available"
    description = "Country code localization data is available"

    def check(self, data):
        if data['metadata']['Xmp']['iptc']['CountryCode']:
            return 'XMP IPTC CountryCode', data['metadata']['Xmp']['iptc']['CountryCode']

class XMPIptcLocationAvailable(BaseSignature):
    pk = 1042
    severity = 2
    category = "position information"
    name = "XMP IPTC Location available"
    description = "Localization data are available"

    def check(self, data):
        if data['metadata']['Xmp']['iptc']['Location']:
            return 'XMP IPTC Location', data['metadata']['Xmp']['iptc']['Location']

class XMPIptcCreatorContactInfoAvailable(BaseSignature):
    pk = 1043
    severity = 2
    category = "personal information"
    name = "XMP IPTC CreatorContactInfo available"
    description = "Contact data are available"

    def check(self, data):
        for key in data['metadata']['Xmp']['iptc'].keys():
            if str(key).startswith('CreatorContactInfo'):
                return True

class ExifImageImageDescriptionAvailable(BaseSignature):
    pk = 1044
    severity = 2
    category = "personal information"
    name = "Exif Image ImageDescription available"
    description = "A character string giving the title of the image. It may be a comment such as '1988 company picnic' or the like. Two-bytes character codes cannot be used. When a 2-bytes code is necessary, the Exif Private tag <UserComment> is to be used."

    def check(self, data):
        if data['metadata']['Exif']['Image']['ImageDescription']:
            return 'Exif Image ImageDescription', data['metadata']['Exif']['Image']['ImageDescription']

class XMPTiffSoftwareAvailable(BaseSignature):
    pk = 1045
    severity = 1
    category = "editing information"
    name = "XMP Tiff Software detected"
    description = "     TIFF tag 305, 0x131. Software or firmware used to generate image. Note: This property is stored in XMP as xmp:CreatorTool. "

    def check(self, data):
        if data['metadata']['Xmp']['tiff']['software']:
            return 'XMP Tiff Software', data['metadata']['Xmp']['tiff']['software']

class XMPTiffModelAvailable(BaseSignature):
    pk = 1046
    severity = 1
    category = "hardware information"
    name = "XMP Tiff Model available"
    description = "TIFF tag 272, 0x110. Model name or number of equipment."

    def check(self, data):
        if data['metadata']['Xmp']['tiff']['model']:
            return 'XMP Tiff Model', data['metadata']['Xmp']['tiff']['model']

class XMPTiffMakevailable(BaseSignature):
    pk = 1047
    severity = 1
    category = "hardware information"
    name = "XMP Tiff Make available"
    description = "TIFF tag 271, 0x10F. Manufacturer of recording equipment."

    def check(self, data):
        if data['metadata']['Xmp']['tiff']['make']:
            return 'XMP Tiff Make', data['metadata']['Xmp']['tiff']['make']

class ExifPhotoDateTimeOriginalAvailable(BaseSignature):
    pk = 1048
    severity = 2
    category = "time information"
    name = "XMP Exif DateTimeOriginal available"
    description = "Photo date and time is available in metadata"

    def check(self, data):
        if data['metadata']['Xmp']['exif']['DateTimeOriginal']:
            return 'XMP Exif DateTimeOriginal', data['metadata']['Xmp']['exif']['DateTimeOriginal']

class ExifImageProcessingSoftwareAvailable(BaseSignature):
    pk = 1049
    severity = 1
    category = "editing information"
    name = "Exif Image ProcessingSoftware detected"
    description = "The name and version of the software used to post-process the picture."

    def check(self, data):
        if data['metadata']['Exif']['Image']['ProcessingSoftware']:
            return 'EXIF Image ProcessingSoftware', data['metadata']['Exif']['Image']['ProcessingSoftware']

class ExifImageDocumentNameAvailable(BaseSignature):
    pk = 1050
    severity = 1
    category = "editing information"
    name = "Exif Image DocumentName detected"
    description = "The name of the document from which this image was scanned."

    def check(self, data):
        if data['metadata']['Exif']['Image']['DocumentName']:
            return 'EXIF Image DocumentName', data['metadata']['Exif']['Image']['DocumentName']

class ExifImageHostComputerAvailable(BaseSignature):
    pk = 1051
    severity = 2
    category = "personal information"
    name = "Exif Image HostComputer available"
    description = "This tag records information about the host computer used to generate the image."

    def check(self, data):
        if data['metadata']['Exif']['Image']['HostComputer']:
            return 'Exif Image HostComputer', data['metadata']['Exif']['Image']['HostComputer']

class ExifImageImageIDAvailable(BaseSignature):
    pk = 1052
    severity = 2
    category = "personal information"
    name = "Exif Image ImageID available"
    description = "ImageID is the full pathname of the original, high-resolution image, or any other identifying string that uniquely identifies the original image (Adobe OPI)."

    def check(self, data):
        if data['metadata']['Exif']['Image']['ImageID']:
            return 'Exif Image ImageID', data['metadata']['Exif']['Image']['ImageID']

class ExifImageDateTimeOriginalAvailable(BaseSignature):
    pk = 1053
    severity = 2
    category = "time information"
    name = "Exif Image DateTimeOriginal available"
    description = "The date and time when the original image data was generated."

    def check(self, data):
        if data['metadata']['Exif']['Image']['DateTimeOriginal']:
            return 'EXIF Image DateTimeOriginal', data['metadata']['Exif']['Image']['DateTimeOriginal']

class ExifImageImageNumberAvailable(BaseSignature):
    pk = 1054
    severity = 1
    category = "image information"
    name = "Exif Image ImageNumber available"
    description = "Number assigned to an image, e.g., in a chained image burst."

    def check(self, data):
        if data['metadata']['Exif']['Image']['ImageNumber']:
            return 'EXIF Image ImageNumber', data['metadata']['Exif']['Image']['ImageNumber']

class ExifImageSecurityClassificationAvailable(BaseSignature):
    pk = 1055
    severity = 3
    category = "image information"
    name = "Exif Image SecurityClassification available"
    description = "Security classification assigned to the image."

    def check(self, data):
        if data['metadata']['Exif']['Image']['SecurityClassification']:
            return 'EXIF Image SecurityClassification', data['metadata']['Exif']['Image']['SecurityClassification']

class ExifImageImageHistoryAvailable(BaseSignature):
    pk = 1056
    severity = 3
    category = "image information"
    name = "Exif Image ImageHistory available"
    description = "Record of what has been done to the image."

    def check(self, data):
        if data['metadata']['Exif']['Image']['ImageHistory']:
            return 'EXIF Image ImageHistory', data['metadata']['Exif']['Image']['ImageHistory']

class ExifImageXPCommentAvailable(BaseSignature):
    pk = 1057
    severity = 2
    category = "editing information"
    name = "Exif Image XPComment available"
    description = "Comment tag used by Windows, encoded in UCS2."

    def check(self, data):
        if data['metadata']['Exif']['Image']['XPComment']:
            return 'EXIF Image XPComment', data['metadata']['Exif']['Image']['XPComment']

class ExifImageXPTitleAvailable(BaseSignature):
    pk = 1058
    severity = 1
    category = "editing information"
    name = "Exif Image XPTitle available"
    description = "Title tag used by Windows, encoded in UCS2."

    def check(self, data):
        if data['metadata']['Exif']['Image']['XPTitle']:
            return 'EXIF Image XPTitle', data['metadata']['Exif']['Image']['XPTitle']

class ExifImageXPAuthorAvailable(BaseSignature):
    pk = 1059
    severity = 2
    category = "personal information"
    name = "Exif Image XPAuthor available"
    description = "Author tag used by Windows, encoded in UCS2."

    def check(self, data):
        if data['metadata']['Exif']['Image']['XPAuthor']:
            return 'EXIF Image XPAuthor', data['metadata']['Exif']['Image']['XPAuthor']

class ExifImageXPKeywordsAvailable(BaseSignature):
    pk = 1060
    severity = 1
    category = "editing information"
    name = "Exif Image XPTitle available"
    description = "Keywords tag used by Windows, encoded in UCS2."

    def check(self, data):
        if data['metadata']['Exif']['Image']['XPKeywords']:
            return 'EXIF Image XPKeywords', data['metadata']['Exif']['Image']['XPKeywords']

class ExifImageUniqueCameraModelAvailable(BaseSignature):
    pk = 1061
    severity = 3
    category = "hardware information"
    name = "Exif Image UniqueCameraModel available"
    description = "Defines a unique, non-localized name for the camera model that created the image in the raw file. This name should include the manufacturer's name to avoid conflicts, and should not be localized, even if the camera name itself is localized for different markets (see LocalizedCameraModel). This string may be used by reader software to index into per-model preferences and replacement profiles."

    def check(self, data):
        if data['metadata']['Exif']['Image']['UniqueCameraModel']:
            return 'EXIF Image UniqueCameraModel', data['metadata']['Exif']['Image']['UniqueCameraModel']

class ExifImageLocalizedCameraModelAvailable(BaseSignature):
    pk = 1062
    severity = 3
    category = "hardware information"
    name = "Exif Image LocalizedCameraModel available"
    description = "Similar to the UniqueCameraModel field, except the name can be localized for different markets to match the localization of the camera name."

    def check(self, data):
        if data['metadata']['Exif']['Image']['LocalizedCameraModel']:
            return 'EXIF Image LocalizedCameraModel', data['metadata']['Exif']['Image']['LocalizedCameraModel']

class ExifImageCameraSerialNumberAvailable(BaseSignature):
    pk = 1063
    severity = 3
    category = "hardware information"
    name = "Exif Image CameraSerialNumber available"
    description = "CameraSerialNumber contains the serial number of the camera or camera body that captured the image."

    def check(self, data):
        if data['metadata']['Exif']['Image']['CameraSerialNumber']:
            return 'EXIF Image CameraSerialNumber', data['metadata']['Exif']['Image']['CameraSerialNumber']

class ExifImageRawDataUniqueIDAvailable(BaseSignature):
    pk = 1064
    severity = 3
    category = "image information"
    name = "Exif Image RawDataUniqueID available"
    description = "This tag contains a 16-byte unique identifier for the raw image data in the DNG file. DNG readers can use this tag to recognize a particular raw image, even if the file's name or the metadata contained in the file has been changed. If a DNG writer creates such an identifier, it should do so using an algorithm that will ensure that it is very unlikely two different images will end up having the same identifier."

    def check(self, data):
        if data['metadata']['Exif']['Image']['RawDataUniqueID']:
            return 'EXIF Image RawDataUniqueID', data['metadata']['Exif']['Image']['RawDataUniqueID']

class ExifImageOriginalRawFileNameAvailable(BaseSignature):
    pk = 1065
    severity = 3
    category = "image information"
    name = "Exif Image OriginalRawFileName available"
    description = "If the DNG file was converted from a non-DNG raw file, then this tag contains the file name of that original raw file."

    def check(self, data):
        if data['metadata']['Exif']['Image']['OriginalRawFileName']:
            return 'EXIF Image OriginalRawFileName', data['metadata']['Exif']['Image']['OriginalRawFileName']

class ExifImageProfileCopyrightAvailable(BaseSignature):
    pk = 1066
    severity = 2
    category = "personal information"
    name = "Exif Image ProfileCopyright available"
    description = "A UTF-8 encoded string containing the copyright information for the camera profile. This string always should be preserved along with the other camera profile tags."

    def check(self, data):
        if data['metadata']['Exif']['Image']['ProfileCopyright']:
            return 'Exif Image ProfileCopyright', data['metadata']['Exif']['Image']['ProfileCopyright']

class ExifPhotoImageUniqueIDAvailable(BaseSignature):
    pk = 1067
    severity = 3
    category = "image information"
    name = "Exif Photo ImageUniqueID available"
    description = "This tag indicates an identifier assigned uniquely to each image. It is recorded as an ASCII string equivalent to hexadecimal notation and 128-bit fixed length."

    def check(self, data):
        if data['metadata']['Exif']['Photo']['ImageUniqueID']:
            return 'EXIF Photo ImageUniqueID', data['metadata']['Exif']['Photo']['ImageUniqueID']

class ExifPhotoCameraOwnerNameAvailable(BaseSignature):
    pk = 1068
    severity = 2
    category = "personal information"
    name = "Exif Photo CameraOwnerName available"
    description = "This tag records the owner of a camera used in photography as an ASCII string."

    def check(self, data):
        if data['metadata']['Exif']['Photo']['CameraOwnerName']:
            return 'EXIF Photo CameraOwnerName', data['metadata']['Exif']['Photo']['CameraOwnerName']

class ExifPhotoBodySerialNumberAvailable(BaseSignature):
    pk = 1069
    severity = 3
    category = "hardware information"
    name = "Exif Photo BodySerialNumber available"
    description = "This tag records the serial number of the body of the camera that was used in photography as an ASCII string."

    def check(self, data):
        if data['metadata']['Exif']['Photo']['BodySerialNumber']:
            return 'EXIF Photo BodySerialNumber', data['metadata']['Exif']['Photo']['BodySerialNumber']

class ExifPhotoLensSerialNumberAvailable(BaseSignature):
    pk = 1070
    severity = 3
    category = "hardware information"
    name = "Exif Photo LensSerialNumber available"
    description = "This tag records the serial number of the interchangeable lens that was used in photography as an ASCII string."

    def check(self, data):
        if data['metadata']['Exif']['Photo']['LensSerialNumber']:
            return 'EXIF Photo LensSerialNumber', data['metadata']['Exif']['Photo']['LensSerialNumber']

class ExifPhotoLensMakeAvailable(BaseSignature):
    pk = 1071
    severity = 1
    category = "hardware information"
    name = "Exif Photo LensMake available"
    description = "This tag records the lens manufactor as an ASCII string."

    def check(self, data):
        if data['metadata']['Photo']['Image']['LensMake']:
            return 'EXIF Photo LensMake', data['metadata']['Exif']['Photo']['LensMake']

class XMPMPRegPersonDisplayNameAvailable(BaseSignature):
    pk = 1072
    severity = 2
    category = "personal information"
    name = "XMP MPReg PersonDisplayName available"
    description = "Name of the person."

    def check(self, data):
        if data['metadata']['Xmp']['MPReg']['PersonDisplayName']:
            return 'XMP MPReg PersonDisplayName', data['metadata']['Xmp']['MPReg']['PersonDisplayName']

class XMPMPRegPersonEmailDigestAvailable(BaseSignature):
    pk = 1073
    severity = 3
    category = "personal information"
    name = "XMP MPReg PersonEmailDigest available"
    description = "SHA-1 encrypted message hash of the person's Windows Live e-mail address."

    def check(self, data):
        if data['metadata']['Xmp']['MPReg']['PersonEmailDigest']:
            return 'XMP MPReg PersonEmailDigest', data['metadata']['Xmp']['MPReg']['PersonEmailDigest']

class XMPMPRegPersonLiveCIDAvailable(BaseSignature):
    pk = 1074
    severity = 3
    category = "personal information"
    name = "XMP MPReg PersonLiveCID available"
    description = "Signed decimal representation of the person's Windows Live CID."

    def check(self, data):
        if data['metadata']['Xmp']['MPReg']['PersonLiveCID']:
            return 'XMP MPReg PersonLiveCID', data['metadata']['Xmp']['MPReg']['PersonLiveCID']

class XMPexpressionmediaPeopleAvailable(BaseSignature):
    pk = 1075
    severity = 2
    category = "personal information"
    name = "XMP expressionmedia People available"
    description = "Contact."

    def check(self, data):
        if data['metadata']['Xmp']['expressionmedia']['People']:
            return 'XMP expressionmedia People', data['metadata']['Xmp']['expressionmedia']['People']

class XMPmediaproPeopleAvailable(BaseSignature):
    pk = 1076
    severity = 2
    category = "personal information"
    name = "XMP mediapro People available"
    description = "Contact."

    def check(self, data):
        if data['metadata']['Xmp']['mediapro']['People']:
            return 'XMP mediapro People', data['metadata']['Xmp']['mediapro']['People']

class XMPMicrosoftPhotoCameraSerialNumberAvailable(BaseSignature):
    pk = 1077
    severity = 3
    category = "hardware information"
    name = "XMP MicrosoftPhoto CameraSerialNumber available"
    description = "Camera Serial Number."

    def check(self, data):
        if data['metadata']['Xmp']['MicrosoftPhoto']['CameraSerialNumber']:
            return 'XMP MicrosoftPhoto CameraSerialNumber', data['metadata']['Xmp']['MicrosoftPhoto']['CameraSerialNumber']

class XMPMicrosoftPhotoDateAcquiredAvailable(BaseSignature):
    pk = 1078
    severity = 2
    category = "time information"
    name = "XMP MicrosoftPhoto DateAcquired available"
    description = "Date Acquired."

    def check(self, data):
        if data['metadata']['Xmp']['MicrosoftPhoto']['DateAcquired']:
            return 'XMP MicrosoftPhoto DateAcquired', data['metadata']['Xmp']['MicrosoftPhoto']['DateAcquired']

class XMPkipipicasawebGPhotoIdAvailable(BaseSignature):
    pk = 1079
    severity = 3
    category = "personal information"
    name = "XMP kipi picasawebGPhotoId available"
    description = "Item ID from PicasaWeb web service."

    def check(self, data):
        if data['metadata']['Xmp']['kipi']['picasawebGPhotoId']:
            return 'XMP kipi picasawebGPhotoId', data['metadata']['Xmp']['kipi']['picasawebGPhotoId']

class XMPkipiyandexGPhotoIdAvailable(BaseSignature):
    pk = 1080
    severity = 3
    category = "personal information"
    name = "XMP kipi yandexGPhotoId available"
    description = "Item ID from Yandex Fotki web service."

    def check(self, data):
        if data['metadata']['Xmp']['kipi']['yandexGPhotoId']:
            return 'XMP kipi yandexGPhotoId', data['metadata']['Xmp']['kipi']['yandexGPhotoId']

class XMPdigiKamImageHistoryAvailable(BaseSignature):
    pk = 1081
    severity = 3
    category = "editing information"
    name = "XMP digiKam ImageHistory available"
    description = "An XML based content to list all action processed on this image with image editor (as crop, rotate, color corrections, adjustements, etc.)."

    def check(self, data):
        if data['metadata']['Xmp']['digiKam']['ImageHistory']:
            return 'XMP digiKam ImageHistory', data['metadata']['Xmp']['digiKam']['ImageHistory']

class XMPdigiKamCaptionsDateTimeStampsAvailable(BaseSignature):
    pk = 1082
    severity = 2
    category = "time information"
    name = "XMP digiKam CaptionsDateTimeStamps available"
    description = "The list of all captions date time stamps for each language alternative captions set in standard XMP tags."

    def check(self, data):
        if data['metadata']['Xmp']['digiKam']['CaptionsDateTimeStamps']:
            return 'XMP digiKam CaptionsDateTimeStamps', data['metadata']['Xmp']['digiKam']['CaptionsDateTimeStamps']

class XMPdigiKamCaptionsAuthorNamesAvailable(BaseSignature):
    pk = 1083
    severity = 2
    category = "personal information"
    name = "XMP digiKam CaptionsAuthorNames available"
    description = "The list of all captions author names for each language alternative captions set in standard XMP tags."

    def check(self, data):
        if data['metadata']['Xmp']['digiKam']['CaptionsAuthorNames']:
            return 'XMP digiKam CaptionsAuthorNames', data['metadata']['Xmp']['digiKam']['CaptionsAuthorNames']

class XMPdigiKamTagsListAvailable(BaseSignature):
    pk = 1084
    severity = 2
    category = "position information"
    name = "XMP digiKam TagsList available"
    description = "The list of complete tags path as string. The path hierarchy is separated by '/' character (ex.: \"City/Paris/Monument/Eiffel Tower\"."

    def check(self, data):
        if data['metadata']['Xmp']['digiKam']['TagsList']:
            return 'XMP digiKam TagsList', data['metadata']['Xmp']['digiKam']['TagsList']

class XMPauxSerialNumberAvailable(BaseSignature):
    pk = 1085
    severity = 3
    category = "hardware information"
    name = "XMP aux SerialNumber available"
    description = "The serial number of the camera or camera body used to take the photograph."

    def check(self, data):
        if data['metadata']['Xmp']['aux']['SerialNumber']:
            return 'XMP aux SerialNumber', data['metadata']['Xmp']['aux']['SerialNumber']

class XMPplusLicenseeAvailable(BaseSignature):
    pk = 1086
    severity = 1
    category = "photo information"
    name = "XMP plus Licensee available"
    description = "Party or parties to whom the license is granted by the Licensor/s under the license transaction."

    def check(self, data):
        if data['metadata']['Xmp']['plus']['Licensee']:
            return 'XMP plus Licensee', data['metadata']['Xmp']['plus']['Licensee']

class XMPplusLicenseeNameAvailable(BaseSignature):
    pk = 1087
    severity = 1
    category = "photo information"
    name = "XMP plus LicenseeName available"
    description = "Name of each Licensee."

    def check(self, data):
        if data['metadata']['Xmp']['plus']['LicenseeName']:
            return 'XMP plus LicenseeName', data['metadata']['Xmp']['plus']['LicenseeName']

class XMPplusEndUserAvailable(BaseSignature):
    pk = 1088
    severity = 2
    category = "personal information"
    name = "XMP plus EndUser available"
    description = "Party or parties ultimately making use of the image under the license."

    def check(self, data):
        if data['metadata']['Xmp']['plus']['EndUser']:
            return 'XMP plus EndUser', data['metadata']['Xmp']['plus']['EndUser']

class XMPplusEndUserNameAvailable(BaseSignature):
    pk = 1089
    severity = 2
    category = "personal information"
    name = "XMP plus EndUserName available"
    description = "Name of each End User."

    def check(self, data):
        if data['metadata']['Xmp']['plus']['EndUserName']:
            return 'XMP plus EndUserName', data['metadata']['Xmp']['plus']['EndUserName']

class XMPplusLicensorAvailable(BaseSignature):
    pk = 1090
    severity = 1
    category = "personal information"
    name = "XMP plus Licensor available"
    description = "Party or parties granting the license to the Licensee."

    def check(self, data):
        for tag in data['metadata']['Xmp']['plus']:
            if tag.startswith('Licensor'):
                return True

class XMPiptcExtAddlModelInfoAvailable(BaseSignature):
    pk = 1091
    severity = 2
    category = "personal information"
    name = "XMP iptcExt AddlModelInfo available"
    description = "Information about the ethnicity and other facts of the model(s) in a model-released image."

    def check(self, data):
        if data['metadata']['Xmp']['iptcExt']['AddlModelInfo']:
            return 'XMP iptcExt AddlModelInfo', data['metadata']['Xmp']['iptcExt']['AddlModelInfo']

class XMPiptcExtModelAgeAvailable(BaseSignature):
    pk = 1092
    severity = 3
    category = "personal information"
    name = "XMP iptcExt ModelAge available"
    description = "Age of the human model(s) at the time this image was taken in a model released image."

    def check(self, data):
        if data['metadata']['Xmp']['iptcExt']['ModelAge']:
            return 'XMP iptcExt ModelAge', data['metadata']['Xmp']['iptcExt']['ModelAge']

class XMPiptcExtOrganisationInImageNameAvailable(BaseSignature):
    pk = 1093
    severity = 2
    category = "personal information"
    name = "XMP iptcExt OrganisationInImageName available"
    description = "Name of the organisation or company which is featured in the image."

    def check(self, data):
        if data['metadata']['Xmp']['iptcExt']['OrganisationInImageName']:
            return 'XMP iptcExt OrganisationInImageName', data['metadata']['Xmp']['iptcExt']['OrganisationInImageName']

class XMPiptcExtPersonInImageAvailable(BaseSignature):
    pk = 1094
    severity = 2
    category = "personal information"
    name = "XMP iptcExt PersonInImage available"
    description = "Name of a person shown in the image."

    def check(self, data):
        if data['metadata']['Xmp']['iptcExt']['PersonInImage']:
            return 'XMP iptcExt PersonInImage', data['metadata']['Xmp']['iptcExt']['PersonInImage']

class XMPiptcExtEventAvailable(BaseSignature):
    pk = 1095
    severity = 1
    category = "personal information"
    name = "XMP iptcExt Event available"
    description = "Names or describes the specific event at which the photo was taken."

    def check(self, data):
        if data['metadata']['Xmp']['iptcExt']['Event']:
            return 'XMP iptcExt Event', data['metadata']['Xmp']['iptcExt']['Event']

class XMPiptcExtCityAvailable(BaseSignature):
    pk = 1096
    severity = 2
    category = "location information"
    name = "XMP iptcExt City available"
    description = "Name of the city of a location."

    def check(self, data):
        if data['metadata']['Xmp']['iptcExt']['City']:
            return 'XMP iptcExt City', data['metadata']['Xmp']['iptcExt']['City']

class XMPiptcExtCountryNameAvailable(BaseSignature):
    pk = 1097
    severity = 1
    category = "location information"
    name = "XMP iptcExt CountryName available"
    description = "The name of a country of a location."

    def check(self, data):
        if data['metadata']['Xmp']['iptcExt']['CountryName']:
            return 'XMP iptcExt CountryName', data['metadata']['Xmp']['iptcExt']['CountryName']

class XMPtiffDateTimeAvailable(BaseSignature):
    pk = 1098
    severity = 1
    category = "time information"
    name = "XMP tiff DateTime available"
    description = "TIFF tag 306, 0x132 (primary) and EXIF tag 37520, 0x9290 (subseconds). Date and time of image creation (no time zone in EXIF), stored in ISO 8601 format, not the original EXIF format. This property includes the value for the EXIF SubSecTime attribute. NOTE: This property is stored in XMP as xmp:ModifyDate."

    def check(self, data):
        if data['metadata']['Xmp']['tiff']['DateTime']:
            return 'XMP tiff DateTime', data['metadata']['Xmp']['tiff']['DateTime']

class XMPiptcExtProvinceStateAvailable(BaseSignature):
    pk = 1099
    severity = 1
    category = "location information"
    name = "XMP iptcExt ProvinceState available"
    description = "The name of a country of a location."

    def check(self, data):
        if data['metadata']['Xmp']['iptcExt']['ProvinceState']:
            return 'XMP iptcExt ProvinceState', data['metadata']['Xmp']['iptcExt']['ProvinceState']

class XMPiptcExtAOCreatorAvailable(BaseSignature):
    pk = 1100
    severity = 2
    category = "personal information"
    name = "XMP iptcExt AOCreator available"
    description = "Contains the name of the artist who has created artwork or an object in the image. In cases where the artist could or should not be identified the name of a company or organisation may be appropriate."

    def check(self, data):
        if data['metadata']['Xmp']['iptcExt']['AOCreator']:
            return 'XMP iptcExt AOCreator', data['metadata']['Xmp']['iptcExt']['AOCreator']

class XMPiptcCiAdrCityAvailable(BaseSignature):
    pk = 1101
    severity = 1
    category = "location information"
    name = "XMP iptc CiAdrCity available"
    description = "The contact information city part."

    def check(self, data):
        if data['metadata']['Xmp']['iptc']['CiAdrCity']:
            return 'XMP iptc CiAdrCity', data['metadata']['Xmp']['iptc']['CiAdrCity']

class XMPiptcCiAdrExtadrAvailable(BaseSignature):
    pk = 1102
    severity = 2
    category = "location information"
    name = "XMP iptc CiAdrExtadr available"
    description = "The contact information address part. Comprises an optional company name and all required information to locate the building or postbox to which mail should be sent."

    def check(self, data):
        if data['metadata']['Xmp']['iptc']['CiAdrExtadr']:
            return 'XMP iptc CiAdrExtadr', data['metadata']['Xmp']['iptc']['CiAdrExtadr']

class XMPiptcCiAdrPcodeAvailable(BaseSignature):
    pk = 1103
    severity = 1
    category = "location information"
    name = "XMP iptc CiAdrPcode available"
    description = "The contact information part denoting the local postal code."

    def check(self, data):
        if data['metadata']['Xmp']['iptc']['CiAdrPcode']:
            return 'XMP iptc CiAdrPcode', data['metadata']['Xmp']['iptc']['CiAdrPcode']

class XMPiptcCiEmailWorkAvailable(BaseSignature):
    pk = 1104
    severity = 3
    category = "personal information"
    name = "XMP iptc CiEmailWork available"
    description = "The contact information email address part."

    def check(self, data):
        if data['metadata']['Xmp']['iptc']['CiEmailWork']:
            return 'XMP iptc CiEmailWork', data['metadata']['Xmp']['iptc']['CiEmailWork']

class XMPiptcCiTelWorkAvailable(BaseSignature):
    pk = 1105
    severity = 3
    category = "personal information"
    name = "XMP iptc CiTelWork available"
    description = "The contact information phone number part."

    def check(self, data):
        if data['metadata']['Xmp']['iptc']['CiTelWork']:
            return 'XMP iptc CiTelWork', data['metadata']['Xmp']['iptc']['CiTelWork']

class XMPiptcCiUrlWorkAvailable(BaseSignature):
    pk = 1106
    severity = 2
    category = "personal information"
    name = "XMP iptc CiUrlWork available"
    description = "The contact information web address part."

    def check(self, data):
        if data['metadata']['Xmp']['iptc']['CiUrlWork']:
            return 'XMP iptc CiUrlWork', data['metadata']['Xmp']['iptc']['CiUrlWork']

class XMPtiffArtistAvailable(BaseSignature):
    pk = 1107
    severity = 2
    category = "personal information"
    name = "XMP tiff Artist available"
    description = "The contact information web address part."

    def check(self, data):
        if data['metadata']['Xmp']['tiff']['Artist']:
            return 'XMP tiff Artist', data['metadata']['Xmp']['tiff']['Artist']

class XMPPDFPDFVersionAvailable(BaseSignature):
    pk = 1108
    severity = 1
    category = "editing information"
    name = "XMP PDF PDFVersion available"
    description = "The PDF file version (for example: 1.0, 1.3, and so on)."

    def check(self, data):
        if data['metadata']['Xmp']['pdf']['PDFVersion']:
            return 'XMP PDF PDFVersion', data['metadata']['Xmp']['pdf']['PDFVersion']

class XMPPDFKeywordsAvailable(BaseSignature):
    pk = 1109
    severity = 1
    category = "photo information"
    name = "XMP PDF Keywords available"
    description = "Keywords."

    def check(self, data):
        if data['metadata']['Xmp']['pdf']['Keywords']:
            return 'XMP PDF Keywords', data['metadata']['Xmp']['pdf']['Keywords']

class XMPxmpDMlogCommentAvailable(BaseSignature):
    pk = 1110
    severity = 1
    category = "photo information"
    name = "XMP xmpDM logComment available"
    description = "User's log comments."

    def check(self, data):
        if data['metadata']['Xmp']['xmpDM']['logComment']:
            return 'XMP xmpDM logComment', data['metadata']['Xmp']['xmpDM']['logComment']

class XMPxmpDMartistAvailable(BaseSignature):
    pk = 1111
    severity = 2
    category = "personal information"
    name = "XMP xmpDM artist available"
    description = "The name of the artist or artists."

    def check(self, data):
        if data['metadata']['Xmp']['xmpDM']['artist']:
            return 'XMP xmpDM artist', data['metadata']['Xmp']['xmpDM']['artist']

class XMPxmpDMcomposerAvailable(BaseSignature):
    pk = 1112
    severity = 2
    category = "personal information"
    name = "XMP xmpDM composer available"
    description = "The composer's name."

    def check(self, data):
        if data['metadata']['Xmp']['xmpDM']['composer']:
            return 'XMP xmpDM composer', data['metadata']['Xmp']['xmpDM']['composer']

class XMPxmpDMengineerAvailable(BaseSignature):
    pk = 1113
    severity = 2
    category = "personal information"
    name = "XMP xmpDM engineer available"
    description = "The engineer's name."

    def check(self, data):
        if data['metadata']['Xmp']['xmpDM']['engineer']:
            return 'XMP xmpDM engineer', data['metadata']['Xmp']['xmpDM']['engineer']

class XMPxmpRightsOwnerAvailable(BaseSignature):
    pk = 1114
    severity = 2
    category = "personal information"
    name = "XMP xmpRights Owner available"
    description = "An unordered array specifying the legal owner(s) of a resource."

    def check(self, data):
        if data['metadata']['Xmp']['xmpRights']['Owner']:
            return 'XMP xmpRights Owner', data['metadata']['Xmp']['xmpRights']['Owner']

class ExifCanonFirmwareVersionAvailable(BaseSignature):
    pk = 1115
    severity = 1
    category = "hardware information"
    name = "Exif Canon FirmwareVersion available"
    description = "Firmware version."

    def check(self, data):
        if data['metadata']['Exif']['Canon']['FirmwareVersion']:
            return 'Exif Canon FirmwareVersion', data['metadata']['Exif']['Canon']['FirmwareVersion']

class ExifCanonSerialNumberAvailable(BaseSignature):
    pk = 1116
    severity = 1
    category = "hardware information"
    name = "Exif Canon SerialNumber available"
    description = "Camera serial number."

    def check(self, data):
        if data['metadata']['Exif']['Canon']['SerialNumber']:
            return 'Exif Canon SerialNumber', data['metadata']['Exif']['Canon']['SerialNumber']

class XMPexifUserCommentAvailable(BaseSignature):
    pk = 1117
    severity = 2
    category = "personal information"
    name = "XMP exif UserComment available"
    description = "EXIF tag 37510, 0x9286. Comments from user."

    def check(self, data):
        if data['metadata']['Xmp']['exif']['UserComment']:
            return 'XMP exif UserComment', data['metadata']['Xmp']['exif']['UserComment']

class XMPexifDateTimeDigitizedAvailable(BaseSignature):
    pk = 1118
    severity = 2
    category = "time information"
    name = "XMP exif DateTimeDigitized available"
    description = "EXIF tag 36868, 0x9004 (primary) and 37522, 0x9292 (subseconds). Date and time when image was stored as digital data, can be the same as DateTimeOriginal if originally stored in digital form. Stored in ISO 8601 format. Includes the EXIF SubSecTimeDigitized data."

    def check(self, data):
        if data['metadata']['Xmp']['exif']['DateTimeDigitized']:
            return 'XMP exif DateTimeDigitized', data['metadata']['Xmp']['exif']['DateTimeDigitized']

class XMPExifGPSAvailable(BaseSignature):
    pk = 1119
    severity = 3
    category = "position information"
    name = "XMP exif GPS information available"
    description = "XMP exif GPS localization data are available"

    def check(self, data):
        if data['metadata']['Xmp']['exif']['GPSLatitude'] and data['metadata']['Xmp']['exif']['GPSLongitude']: 
            return True

class XMPDCcontributorAvailable(BaseSignature):
    pk = 1120
    severity = 2
    category = "personal information"
    name = "XMP DC contributor available"
    description = "Contributors to the resource (other than the authors)."

    def check(self, data):
        if data['metadata']['Xmp']['dc']['contributor']:
            return 'XMP DC contributor', data['metadata']['Xmp']['dc']['contributor']

class XMPDCpublisherAvailable(BaseSignature):
    pk = 1121
    severity = 2
    category = "personal information"
    name = "XMP DC publisher available"
    description = "An entity responsible for making the resource available. Examples of a Publisher include a person, an organization, or a service. Typically, the name of a Publisher should be used to indicate the entity."

    def check(self, data):
        if data['metadata']['Xmp']['dc']['publisher']:
            return 'XMP DC publisher', data['metadata']['Xmp']['dc']['publisher']

class XMPDCdateAvailable(BaseSignature):
    pk = 1122
    severity = 2
    category = "time information"
    name = "XMP DC date available"
    description = "Date(s) that something interesting happened to the resource."

    def check(self, data):
        if data['metadata']['Xmp']['dc']['date']:
            return 'XMP DC date', data['metadata']['Xmp']['dc']['date']

class IPTCEnvelopeDateSentAvailable(BaseSignature):
    pk = 1123
    severity = 2
    category = "time information"
    name = "IPTC Envelope DateSent available"
    description = "Uses the format CCYYMMDD."

    def check(self, data):
        if data['metadata']['Iptc']['Envelope']['DateSent']:
            return 'IPTC Envelope DateSent', data['metadata']['Iptc']['Envelope']['DateSent']

class IPTCEnvelopeTimeSentAvailable(BaseSignature):
    pk = 1124
    severity = 2
    category = "time information"
    name = "IPTC Envelope TimeSent available"
    description = "Uses the format HHMMSS:HHMM where HHMMSS refers to local hour."

    def check(self, data):
        if data['metadata']['Iptc']['Envelope']['TimeSent']:
            return 'IPTC Envelope TimeSent', data['metadata']['Iptc']['Envelope']['TimeSent']

class IPTCApplication2ReleaseDateAvailable(BaseSignature):
    pk = 1125
    severity = 2
    category = "time information"
    name = "IPTC Application2 ReleaseDate available"
    description = "Designates in the form CCYYMMDD the earliest date the provider intends the object to be used. Follows ISO 8601 standard."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['ReleaseDate']:
            return 'IPTC Application2 ReleaseDate', data['metadata']['Iptc']['Application2']['ReleaseDate']

class IPTCApplication2ReleaseTimeAvailable(BaseSignature):
    pk = 1126
    severity = 2
    category = "time information"
    name = "IPTC Application2 ReleaseTime available"
    description = "Designates in the form HHMMSS:HHMM the earliest time the provider intends the object to be used. Follows ISO 8601 standard."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['ReleaseTime']:
            return 'IPTC Application2 ReleaseTime', data['metadata']['Iptc']['Application2']['ReleaseTime']

class IPTCApplication2ExpirationDateAvailable(BaseSignature):
    pk = 1127
    severity = 2
    category = "time information"
    name = "IPTC Application2 ExpirationDate available"
    description = "Designates in the form CCYYMMDD the latest date the provider or owner intends the object data to be used. Follows ISO 8601 standard."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['ExpirationDate']:
            return 'IPTC Application2 ExpirationDate', data['metadata']['Iptc']['Application2']['ExpirationDate']

class IPTCApplication2ExpirationTimeAvailable(BaseSignature):
    pk = 1128
    severity = 2
    category = "time information"
    name = "IPTC Application2 ExpirationTime available"
    description = "Designates in the form HHMMSS:HHMM the latest time the provider or owner intends the object data to be used. Follows ISO 8601 standard."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['ExpirationTime']:
            return 'IPTC Application2 ExpirationTime', data['metadata']['Iptc']['Application2']['ExpirationTime']

class IPTCApplication2ReferenceDateAvailable(BaseSignature):
    pk = 1129
    severity = 2
    category = "time information"
    name = "IPTC Application2 ReferenceDate available"
    description = "Designates in the form HHMMSS:HHMM the latest time the provider or owner intends the object data to be used. Follows ISO 8601 standard."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['ReferenceDate']:
            return 'IPTC Application2 ReferenceDate', data['metadata']['Iptc']['Application2']['ReferenceDate']

class IPTCApplication2ProgramAvailable(BaseSignature):
    pk = 1130
    severity = 1
    category = "editing information"
    name = "IPTC Application2 Program available"
    description = "Identifies the type of program used to originate the object data."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['Program']:
            return 'IPTC Application2 Program', data['metadata']['Iptc']['Application2']['Program']

class IPTCApplication2ContactAvailable(BaseSignature):
    pk = 1131
    severity = 2
    category = "personal information"
    name = "IPTC Application2 Contact available"
    description = "Identifies the person or organisation which can provide further background information on the object data."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['Contact']:
            return 'IPTC Application2 Contact', data['metadata']['Iptc']['Application2']['Contact']

class ExifMinoltaCsNewMinoltaDateAvailable(BaseSignature):
    pk = 1132
    severity = 2
    category = "time information"
    name = "Exif MinoltaCsNew MinoltaDate available"
    description = "Minolta date."

    def check(self, data):
        if data['metadata']['Exif']['MinoltaCsNew']['MinoltaDate']:
            return 'Exif MinoltaCsNew MinoltaDate', data['metadata']['Exif']['MinoltaCsNew']['MinoltaDate']

class ExifMinoltaCsNewMinoltaTimeAvailable(BaseSignature):
    pk = 1133
    severity = 2
    category = "time information"
    name = "Exif MinoltaCsNew MinoltaTime available"
    description = "Minolta date."

    def check(self, data):
        if data['metadata']['Exif']['MinoltaCsNew']['MinoltaTime']:
            return 'Exif MinoltaCsNew MinoltaTime', data['metadata']['Exif']['MinoltaCsNew']['MinoltaTime']

class ExifMinoltaCsNewMinoltaModelAvailable(BaseSignature):
    pk = 1134
    severity = 1
    category = "hardware information"
    name = "Exif MinoltaCsNew MinoltaTime available"
    description = "Minolta model."

    def check(self, data):
        if data['metadata']['Exif']['MinoltaCsNew']['MinoltaModel']:
            return 'Exif MinoltaCsNew MinoltaModel', data['metadata']['Exif']['MinoltaCsNew']['MinoltaModel']

class ExifSigmaSerialNumberAvailable(BaseSignature):
    pk = 1135
    severity = 2
    category = "hardware information"
    name = "Exif Sigma SerialNumber available"
    description = "Camera serial number."

    def check(self, data):
        if data['metadata']['Exif']['Sigma']['SerialNumber']:
            return 'Exif Sigma SerialNumber', data['metadata']['Exif']['Sigma']['SerialNumber']

class ExifSigmaFirmwareAvailable(BaseSignature):
    pk = 1136
    severity = 2
    category = "hardware information"
    name = "Exif Sigma Firmware available"
    description = "Firmware release."

    def check(self, data):
        if data['metadata']['Exif']['Sigma']['Firmware']:
            return 'Exif Sigma Firmware', data['metadata']['Exif']['Sigma']['Firmware']

class ExifSigmaSoftwareAvailable(BaseSignature):
    pk = 1137
    severity = 2
    category = "hardware information"
    name = "Exif Sigma Software available"
    description = "Software release."

    def check(self, data):
        if data['metadata']['Exif']['Sigma']['Software']:
            return 'Exif Sigma Software', data['metadata']['Exif']['Sigma']['Software']

class ExifSamsung2LensFirmwareAvailable(BaseSignature):
    pk = 1138
    severity = 2
    category = "hardware information"
    name = "Exif Samsung2 LensFirmware available"
    description = "Lens firmware release."

    def check(self, data):
        if data['metadata']['Exif']['Samsung2']['LensFirmware']:
            return 'Exif Samsung2 LensFirmware', data['metadata']['Exif']['Samsung2']['LensFirmware']

class ExifSamsung2FirmwareNameAvailable(BaseSignature):
    pk = 1139
    severity = 2
    category = "hardware information"
    name = "Exif Samsung2 FirmwareName available"
    description = "Firmware name release."

    def check(self, data):
        if data['metadata']['Exif']['Samsung2']['FirmwareName']:
            return 'Exif Samsung2 FirmwareName', data['metadata']['Exif']['Samsung2']['FirmwareName']

class ExifSamsung2FirmwareNameAvailable(BaseSignature):
    pk = 1140
    severity = 2
    category = "photo information"
    name = "Exif Samsung2 EncryptionKey available"
    description = "Encryption key."

    def check(self, data):
        if data['metadata']['Exif']['Samsung2']['EncryptionKey']:
            return 'Exif Samsung2 EncryptionKey', data['metadata']['Exif']['Samsung2']['EncryptionKey']

class ExifSamsung2LocationNameAvailable(BaseSignature):
    pk = 1141
    severity = 2
    category = "location information"
    name = "Exif Samsung2 LocationName available"
    description = "Location name."

    def check(self, data):
        if data['metadata']['Exif']['Samsung2']['LocationName']:
            return 'Exif Samsung2 LocationName', data['metadata']['Exif']['Samsung2']['LocationName']

class ExifSamsung2LocalLocationNameAvailable(BaseSignature):
    pk = 1142
    severity = 2
    category = "location information"
    name = "Exif Samsung2 LocalLocationName available"
    description = "Local location name."

    def check(self, data):
        if data['metadata']['Exif']['Samsung2']['LocalLocationName']:
            return 'Exif Samsung2 LocalLocationName', data['metadata']['Exif']['Samsung2']['LocalLocationName']

class ExifFujifilmSerialNumberAvailable(BaseSignature):
    pk = 1143
    severity = 2
    category = "hardware information"
    name = "Exif Fujifilm SerialNumber available"
    description = "This number is unique, and contains the date of manufacture, but is not the same as the number printed on the camera body."

    def check(self, data):
        if data['metadata']['Exif']['Fujifilm']['SerialNumber']:
            return 'Exif Fujifilm SerialNumber', data['metadata']['Exif']['Fujifilm']['SerialNumber']

class ExifMinoltaCsNewDataImprintAvailable(BaseSignature):
    pk = 1144
    severity = 2
    category = "time information"
    name = "Exif MinoltaCsNew DataImprint available"
    description = "Data Imprint."

    def check(self, data):
        if data['metadata']['Exif']['MinoltaCsNew']['DataImprint']:
            return 'Exif MinoltaCsNew DataImprint', data['metadata']['Exif']['MinoltaCsNew']['DataImprint']

class ExifNikon3SerialNumberAvailable(BaseSignature):
    pk = 1145
    severity = 2
    category = "hardware information"
    name = "Exif Nikon3 SerialNumber available"
    description = "Serial Number."

    def check(self, data):
        if data['metadata']['Exif']['Nikon3']['SerialNumber']:
            return 'Exif Nikon3 SerialNumber', data['metadata']['Exif']['Nikon3']['SerialNumber']

class ExifNikon3CaptureDataAvailable(BaseSignature):
    pk = 1146
    severity = 2
    category = "time information"
    name = "Exif Nikon3 CaptureData available"
    description = "Capture data."

    def check(self, data):
        if data['metadata']['Exif']['Nikon3']['CaptureData']:
            return 'Exif Nikon3 CaptureData', data['metadata']['Exif']['Nikon3']['CaptureData']

class ExifOlympusBodyFirmwareVersionAvailable(BaseSignature):
    pk = 1147
    severity = 2
    category = "hardware information"
    name = "Exif Olympus BodyFirmwareVersion available"
    description = "Body firmware version."

    def check(self, data):
        if data['metadata']['Exif']['Olympus']['BodyFirmwareVersion']:
            return 'Exif Olympus BodyFirmwareVersion', data['metadata']['Exif']['Olympus']['BodyFirmwareVersion']

class ExifOlympusBodySoftwareAvailable(BaseSignature):
    pk = 1148
    severity = 2
    category = "editing information"
    name = "Exif Olympus Software available"
    description = "Software version."

    def check(self, data):
        if data['metadata']['Exif']['Olympus']['Software']:
            return 'Exif Olympus Software', data['metadata']['Exif']['Olympus']['Software']

class ExifOlympusFirmwareAvailable(BaseSignature):
    pk = 1149
    severity = 2
    category = "hardware information"
    name = "Exif Olympus Firmware available"
    description = "Firmware version."

    def check(self, data):
        if data['metadata']['Exif']['Olympus']['Firmware']:
            return 'Exif Olympus Firmware', data['metadata']['Exif']['Olympus']['Firmware']

class ExifOlympusEqSerialNumberAvailable(BaseSignature):
    pk = 1150
    severity = 2
    category = "hardware information"
    name = "Exif OlympusEq SerialNumber available"
    description = "Serial number."

    def check(self, data):
        if data['metadata']['Exif']['OlympusEq']['SerialNumber']:
            return 'Exif OlympusEq SerialNumber', data['metadata']['Exif']['OlympusEq']['SerialNumber']

class ExifPentaxModelIDAvailable(BaseSignature):
    pk = 1151
    severity = 2
    category = "hardware information"
    name = "Exif Pentax ModelID available"
    description = "Pentax model idenfication."

    def check(self, data):
        if data['metadata']['Exif']['Pentax']['ModelID']:
            return 'Exif Pentax ModelID', data['metadata']['Exif']['Pentax']['ModelID']

class ExifPentaxSerialNumberAvailable(BaseSignature):
    pk = 1152
    severity = 2
    category = "hardware information"
    name = "Exif Pentax SerialNumber available."
    description = "Serial Number."

    def check(self, data):
        if data['metadata']['Exif']['Pentax']['SerialNumber']:
            return 'Exif Pentax SerialNumber', data['metadata']['Exif']['Pentax']['SerialNumber']

class PreviewDifference(BaseSignature):
    pk = 1153
    severity = 3
    category = "photo information"
    name = "Preview difference detected"
    description = "There is a mismatch between original image and image stored in preview."

    def check(self, data):
        for preview in data['metadata']['preview']:
            if preview['diff']:
                return True

class ExifGPSInfoAvailable(BaseSignature):
    pk = 1154
    severity = 2
    category = "position information"
    name = "Exif GPSInfo available"
    description = "EXIF GPSInfo data are available."

    def check(self, data):
        if data['metadata']['Exif']['GPSInfo']:
            return True

class IptcApplication2CreditAvailable(BaseSignature):
    pk = 1156
    severity = 2
    category = "personal information"
    name = "IPTC Application2 Credit available"
    description = "A textual description of the object data."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['Credit']:
            return 'IPTC Application2 Credit', data['metadata']['Iptc']['Application2']['Credit']

class IptcApplication2CaptionAvailable(BaseSignature):
    pk = 1157
    severity = 1
    category = "photo information"
    name = "IPTC Application2 Caption available"
    description = "A textual description of the object data."

    def check(self, data):
        if data['metadata']['Iptc']['Application2']['Caption']:
            return 'IPTC Application2 Caption', data['metadata']['Iptc']['Application2']['Caption']
