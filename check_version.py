import urllib.request
import zipfile
import subprocess
import os
import shutil
import runpy


def versiontuple(v):
    return tuple(map(int, (v.split("."))))


version_url = 'https://raw.githubusercontent.com/minhtrietn/CODE_TRANSLATE/main/version.txt'
software_url = 'https://github.com/minhtrietn/CODE_TRANSLATE/archive/refs/heads/main.zip'
current_version = str(open("version.txt", "r").readline())

response = urllib.request.urlopen(version_url)
new_version = (response.read().decode('utf-8').strip())

if versiontuple(new_version) > versiontuple(current_version):
    print("Có phiên bản phần mềm mới. Đang tải về...")
    print("VUI LÒNG KHÔNG THOÁT TRÁNH GÂY LỖI CHƯƠNG TRÌNH")
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
    
    runpy.run_module("GUI")
