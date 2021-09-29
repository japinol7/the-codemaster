# -*- mode: python -*-

block_cipher = None

added_files = [
         ('V:\\repos\\git\\the-codemaster\\data\\*.ttf', 'data'),
         ('V:\\repos\\git\\the-codemaster\\assets\\img\\*.png', 'img'),
         ('V:\\repos\\git\\the-codemaster\\assets\\snd\\*.ogg', 'snd'),
         ('V:\\repos\\git\\the-codemaster\\assets\\snd\\*.wav', 'snd'),
         ('V:\\repos\\git\\the-codemaster\\assets\\music\\*.ogg', 'music'),
         ('V:\\repos\\git\\the-codemaster\\assets\\music\\*.mp3', 'music'),
         ]


a = Analysis(['game_entry_point.py'],
             pathex=['V:\\repos\\git\\the-codemaster'],
             binaries=[],
             datas=added_files,
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
          name='codemaster',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=False )
