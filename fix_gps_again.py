import re

with open('/Users/mauricebaradari/Desktop/MotoTracker/app/src/main/java/com/example/mototracker/TrackerService.kt', 'r') as f:
    content = f.read()

# Remove the old convertLocationToExifFormat and setAttribute calls for GPS
new_gps_logic = """            // The bulletproof way to write GPS coordinates in Android
            exif.setLatLong(location.latitude, location.longitude)"""

# Match from `fun convertLocationToExifFormat` down to `exif.setAttribute(ExifInterface.TAG_GPS_LONGITUDE_REF...`
pattern = r'            fun convertLocationToExifFormat.*?exif\.setAttribute\(ExifInterface\.TAG_GPS_LONGITUDE_REF.*?\)'

content = re.sub(pattern, new_gps_logic, content, flags=re.DOTALL)

with open('/Users/mauricebaradari/Desktop/MotoTracker/app/src/main/java/com/example/mototracker/TrackerService.kt', 'w') as f:
    f.write(content)
