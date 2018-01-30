# -*- mode: python -*-

block_cipher = None


a = Analysis(['virtual_ins.py'],
             pathex=['E:\\project\\python\\codes\\serrial'],
             binaries=[],
             datas=[('SerialComm.ui', '.'),('ha32.ico','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='virtual_ins',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='ha32.ico')
