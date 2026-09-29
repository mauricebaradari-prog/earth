import io
from PIL import Image
import piexif

# Create 1x1 image
img = Image.new('RGB', (1, 1), color='black')

# Create empty EXIF dict with GPS IFD
exif_dict = {
    "0th": {},
    "Exif": {},
    "GPS": {
        piexif.GPSIFD.GPSLatitudeRef: b'N',
        piexif.GPSIFD.GPSLatitude: ((0, 1), (0, 1), (0, 1)),
        piexif.GPSIFD.GPSLongitudeRef: b'E',
        piexif.GPSIFD.GPSLongitude: ((0, 1), (0, 1), (0, 1))
    },
    "1st": {},
    "thumbnail": None
}

exif_bytes = piexif.dump(exif_dict)
img.save('/Users/mauricebaradari/Desktop/MotoTracker/app/src/main/assets/template.jpg', 'jpeg', exif=exif_bytes)
