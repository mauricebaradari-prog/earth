import re

with open('/Users/mauricebaradari/Desktop/MotoTracker/app/src/main/java/com/example/mototracker/TrackerService.kt', 'r') as f:
    content = f.read()

# Replace convertLocationToExifFormat with a simpler robust one
new_func = """            fun convertLocationToExifFormat(coordinate: Double): String {
                val absolute = Math.abs(coordinate)
                val degrees = absolute.toInt()
                val minutes = ((absolute - degrees) * 60).toInt()
                val seconds = (absolute - degrees - minutes / 60.0) * 3600
                return "$degrees/1,$minutes/1,${(seconds * 1000).toInt()}/1000"
            }"""

content = re.sub(r'            fun convertLocationToExifFormat.*?\}', new_func, content, flags=re.DOTALL)

with open('/Users/mauricebaradari/Desktop/MotoTracker/app/src/main/java/com/example/mototracker/TrackerService.kt', 'w') as f:
    f.write(content)
