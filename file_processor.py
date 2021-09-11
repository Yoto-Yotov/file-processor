import os
import exifread
from win32com.propsys import propsys, pscon

directory = r'D:\recovery_files'
mp4_files = {}

for filename in os.listdir(directory):

    filepath = f'{directory}\{filename}'
    # Directory to save the new named file. Same dir in this scenario
    new_filepath = 'D:\\recovery_files\\'

    if filename.startswith('[') and filename.endswith('.jpg'):
        with open(filepath, 'rb') as file:
            tags = exifread.process_file(file, stop_tag="EXIF DateTimeOriginal")
        try:
            date_taken = tags["EXIF DateTimeOriginal"]
            new_name = str(date_taken).replace(':', '').replace('-','').replace(' ', '_') + '.jpg'

            print(filename,  new_filepath + new_name)
            os.rename(filepath, new_filepath + new_name)

        except Exception as ex:
            print('Exception for: ', filename, ex)

    elif filename.startswith('[') and filename.endswith('.mp4'):
        try:
            properties = propsys.SHGetPropertyStoreFromParsingName(filepath)
            date_taken = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
            new_name = str(date_taken)[0:-6].replace(':', '').replace('-','').replace(' ', '_') + '.mp4'
            print(filepath, new_filepath + new_name)
            mp4_files[filepath] = new_filepath + new_name

        except Exception:
            print('Exception for: ', filename, date_taken)

    else:
        print(filename)


for old_name, new_name in mp4_files.items():
    os.rename(old_name, new_name)
