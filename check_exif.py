import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

dir_path = '/Users/mauricebaradari/Library/CloudStorage/GoogleDrive-maurice.baradari@gmail.com/Meine Ablage/Gps images'
files = [f for f in os.listdir(dir_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
if not files:
    print('No image files found')
else:
    print(f'Found {len(files)} image files.')
    # test one file
    img_path = os.path.join(dir_path, files[0])
    img = Image.open(img_path)
    exif_data = img._getexif()
    has_gps = False
    if exif_data:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                has_gps = True
                print('Found GPSInfo in first image')
                gps_data = {}
                for t in value:
                    sub_tag = GPSTAGS.get(t, t)
                    gps_data[sub_tag] = value[t]
                print(gps_data)
                break
    if not has_gps:
        print('No GPSInfo in first image. (Might need to check more or use another method)')
