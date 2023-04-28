import cx_Freeze as cx
import platform
import os

base = None
include_files = []
target_name = 'Potentiostat'
if platform.system() == "Windows":
    base = "Win32GUI"
    target_name = 'ElectroLAB.exe'
    PYTHON_DIR = os.path.dirname(os.path.dirname(os.__file__))
    os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_DIR, 'tcl', 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(PYTHON_DIR, 'tcl', 'tk8.6')
    include_files += [
        (os.path.join(PYTHON_DIR, 'DLLs', 'tcl86t.dll'), ''),
        (os.path.join(PYTHON_DIR, 'DLLs', 'tk86t.dll'), '')
    ]


shortcut_data = [
    # (Type, Folder, Name, ?, Target exe, arguments, description, hotkey, icon, icon index, show cmd, Working dir)
    ('DesktopShortcut', 'DesktopFolder', 'ElectroLAB', 'TARGETDIR',
     '[TARGETDIR]' + target_name, None,
     'Electrochemical Tecniques', None,
     None, None, None, 'TARGETDIR'),
    ('MenuShortcut', 'ProgramMenuFolder', 'ElectroLAB', 'TARGETDIR',
     '[TARGETDIR]' + target_name, None,
     'Electrochemical Tecniques', None,
     None, None, None, 'TARGETDIR'),
]

cx.setup(
    name='ElectroLAB',
    version='1.0',
    author='Elí A. Flores',
    author_email='eli1998flores@gmail.com',
    description='Potentiostat to electroquemical techniques',
    packages=['app'],
    executables=[
        cx.Executable(
            'app.py',
            base=base,
            targetName=target_name,
            icon='pot.ico'
        )
    ],
    options={
        'build_exe': {
            'packages': ['serial', 'matplotlib'],
            'includes': ['serial.tools'],
            'include_files': include_files
        },

        'bdist_msi': {
            # can be generated in powershell: "{"+[System.Guid]::NewGuid().ToString().ToUpper()+"}"
            'upgrade_code': '{1BB637E8-551D-47C1-93FA-9D04B032F4B3}',
            'data': {'Shortcut': shortcut_data}
        },
        'bdist_mac': {
            # Sets the application name
            'bundle_name': 'Potentiostat'
        }
    }
)