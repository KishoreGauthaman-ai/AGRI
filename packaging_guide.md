# Packaging AgriVision to .exe

You can convert this Python application into a standalone Windows Executable (`.exe`) using PyInstaller.

## 1. Install PyInstaller
```bash
pip install pyinstaller
```

## 2. Create the Spec File
Run this command to generate an initial spec file (do not build yet):
```bash
pyi-makespec --onefile --windowed --name AgriVision --icon=assets/icon.ico main.py
```
*(Note: If you don't have an icon, remove the `--icon` flag)*

## 3. Edit `AgriVision.spec`
KivyMD implies many hidden imports. Open `AgriVision.spec` and modify the `Analysis` block to include KV files and dependencies.

Add this import at the top:
```python
from kivymd import hooks_path as kivymd_hooks_path
```

Modify `Analysis`:
```python
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('agrivision.kv', '.'), ('models/', 'models/'), ('.env', '.'), ('assets/', 'assets/')], 
    hiddenimports=['kivymd.icon_definitions', 'kivymd.uix', 'sklearn.utils._typedefs', 'sklearn.neighbors._partition_nodes'],
    hookspath=[kivymd_hooks_path],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
```
*Make sure `datas` includes all non-python files you need (kv, models, images).*

## 4. Build the Exe
Run PyInstaller with your modified spec file:
```bash
pyinstaller AgriVision.spec
```

## 5. Locating the App
Your `.exe` will be in the `dist/` folder.
