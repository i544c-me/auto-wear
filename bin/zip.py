import os
from zipfile import ZipFile
from pathlib import Path


src_path = Path("src").resolve()

with ZipFile("graftbones.zip", "w") as zip:
    for root, dirs, files in os.walk(src_path):
        for file in files:
            file_path = os.path.join(root, file)
            zip.write(file_path, arcname=f'graftbones/{file}')

zip.close()
