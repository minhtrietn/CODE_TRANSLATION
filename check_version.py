import urllib.request
import zipfile
import subprocess
import os
import shutil

version_url = 'https://raw.githubusercontent.com/minhtrietn/CODE_TRANSLATE/main/version.txt'
software_url = 'https://github.com/minhtrietn/CODE_TRANSLATE/archive/refs/heads/main.zip'
current_version = float(str(open("version.txt", "r").readline()))

response = urllib.request.urlopen(version_url)
new_version = float(response.read().decode('utf-8').strip())

if new_version > current_version:
    print('Có phiên bản phần mềm mới. Đang tải về...')
    urllib.request.urlretrieve(software_url, 'CODE_TRANSLATE.zip')

    with zipfile.ZipFile('CODE_TRANSLATE.zip', 'r') as zip_ref:
        zip_ref.extractall()

    for i in os.listdir("CODE_TRANSLATE-main"):
        if i in os.listdir(os.getcwd()):
            try:
                os.remove(i)
            except PermissionError:
                shutil.rmtree(i)

    for i in os.listdir("CODE_TRANSLATE-main"):
        os.replace("CODE_TRANSLATE-main/{}".format(i), i)

    os.remove("CODE_TRANSLATE.zip")
    os.rmdir("CODE_TRANSLATE-main")
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])

    print("Đã hoàn tất việc nâng cấp!")
