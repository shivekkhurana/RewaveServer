
import sys
import platform
from cx_Freeze import setup, Executable

target_dir = "./build/"
base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

if platform.architecture()[0] == '32bit':
    target_dir = "./buildX86/"

build_options = {
    "include_files" : ['images'],
    "optimize": True,
    "compressed": True,
    "build_exe": target_dir,
    "icon": "images/rewave_app_icon.ico"
}

build_msi_options = {
    "upgrade_code": "{44B162E5-A1B5-47C3-851D-98A1ADCCE4E0}"
}

setup(
    data_files = [('images', ['images/rewave_app_icon.png'])],
    name = "Rewave Server",
    version = "0.0.1",
    description = "Rewave App's Server",
    executables = [
        Executable(
            "rewave_server.pyw", 
            base=base,
            targetDir=target_dir
        )
    ],
    options = dict(
        build_exe = build_options
        build_msi = build_msi_options
    )
)