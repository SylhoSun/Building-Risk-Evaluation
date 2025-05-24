# build.spec
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['main.py'],  # 主程序文件
    pathex=['.'], 
    binaries=[],
    datas=[
        ('./config.py', '.'),  # 包含配置文件
        ('./ui_main.py', '.'), #界面初始化
        ('./llm_analyzer.py', '.'),  # 包含分析模块
        ('./report_saver.py', '.'),  # 包含报告模块
    ],
    hiddenimports=[
        'PyQt5', 
        'PyQt5.QtCore', 
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        'requests',
        'json',
        'base64',
        'imghdr',
        'sys',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='建筑安全评估系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口
    icon='icon.ico'  # 你的图标文件（.ico格式）
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='基于大语言模型的建筑安全评估系统'
)