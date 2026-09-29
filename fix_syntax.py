with open('/Users/mauricebaradari/Desktop/MotoTracker/app/src/main/java/com/example/mototracker/TrackerService.kt', 'r') as f:
    content = f.read()

content = content.replace('exif.setLatLong(location.latitude, location.longitude) "E" else "W")', 'exif.setLatLong(location.latitude, location.longitude)')

with open('/Users/mauricebaradari/Desktop/MotoTracker/app/src/main/java/com/example/mototracker/TrackerService.kt', 'w') as f:
    f.write(content)
