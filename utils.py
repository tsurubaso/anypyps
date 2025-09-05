import shutil
import os

project_folder = os.path.expanduser('/home/tsurubaso/mysite')

src = os.path.join(project_folder, "googlenewsapiInfo.py")
dst = os.path.join(project_folder, "API", "googlenewsapiInfo.py")

shutil.move(src, dst)
print(f"Déplacé : {src} → {dst}")