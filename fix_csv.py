import re

with open('/Users/mauricebaradari/Desktop/MotoTracker/app/src/main/java/com/example/mototracker/TrackerService.kt', 'r') as f:
    content = f.read()

csv_logic = """            exif.saveAttributes()

            // ---- FALLBACK FOR TEST: WRITE TO CSV ----
            try {
                val publicDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES)
                val sessionDir = File(publicDir, sessionFolder)
                if (!sessionDir.exists()) sessionDir.mkdirs()
                
                val csvFile = File(sessionDir, "route.csv")
                val isNew = !csvFile.exists()
                FileOutputStream(csvFile, true).use { out ->
                    if (isNew) {
                        out.write("timestamp,lat,lng\\n".toByteArray())
                    }
                    val line = "${location.time},${location.latitude},${location.longitude}\\n"
                    out.write(line.toByteArray())
                }
                MediaScannerConnection.scanFile(this@TrackerService, arrayOf(csvFile.absolutePath), null, null)
            } catch (e: Exception) {
                e.printStackTrace()
            }
            // ----------------------------------------

            val fileName = "img_${System.currentTimeMillis()}.jpg\""""

content = content.replace("            exif.saveAttributes()\n\n            val fileName = \"img_${System.currentTimeMillis()}.jpg\"", csv_logic)

with open('/Users/mauricebaradari/Desktop/MotoTracker/app/src/main/java/com/example/mototracker/TrackerService.kt', 'w') as f:
    f.write(content)
