# -*- mode: python -*-

block_cipher = None


a = Analysis(['nautilus.py'],
             pathex=['C:\\Users\\ifernand\\Projects\\nautilus'],
             binaries=[],
             datas=[('schema', 'schema'), ('CLICollector', 'CLICollector'), ('ReadMe', 'ReadMe'), ('templates', 'templates'), ('static', 'static')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='nautilus',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
