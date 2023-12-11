from setuptools import setup

APP=['VirtualMouse.py']
DATA_FILES = [
    ('.', ['./focus_change_keyboard.caf', './focus_change_small.caf']),
]

OPTIONS = {
    'argv_emulation' : True
}

setup(
    app=APP,
    options={'py2app' : OPTIONS},
    data_files=DATA_FILES,
    setup_requires=['py2app']
)