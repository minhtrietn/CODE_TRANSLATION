import winreg

key_path = r"SYSTEM\CurrentControlSet\Control\FileSystem"

try:
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "LongPathsEnabled", 0, winreg.REG_DWORD, 1)
    winreg.CloseKey(key)

except Exception as e:
    print("Đã xảy ra lỗi:", e)
