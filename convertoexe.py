import PyInstaller.__main__

PyInstaller.__main__.run([
    'guimain.py',
    '--collect-data', 'librosa',
])
