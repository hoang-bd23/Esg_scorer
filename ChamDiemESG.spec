# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['uvicorn.logging', 'uvicorn.loops', 'uvicorn.loops.auto', 'uvicorn.protocols', 'uvicorn.protocols.http', 'uvicorn.protocols.http.auto', 'uvicorn.protocols.websockets', 'uvicorn.protocols.websockets.auto', 'uvicorn.lifespan', 'uvicorn.lifespan.on', 'uvicorn.lifespan.off', 'esg_scorer', 'esg_scorer.main', 'esg_scorer.api', 'esg_scorer.api.routes', 'esg_scorer.api.batch_routes', 'esg_scorer.core', 'esg_scorer.core.pdf_extractor', 'esg_scorer.core.scoring_engine', 'esg_scorer.core.keywords', 'esg_scorer.core.framework', 'esg_scorer.models', 'esg_scorer.models.schemas', 'esg_scorer.models.database', 'esg_scorer.services', 'esg_scorer.services.export_service', 'esg_scorer.services.batch_service', 'pdfplumber', 'pdfminer', 'pdfminer.high_level', 'openpyxl', 'sqlalchemy', 'sqlalchemy.dialects.sqlite', 'aiosqlite', 'multipart', 'python_multipart']
hiddenimports += collect_submodules('uvicorn')
hiddenimports += collect_submodules('pdfplumber')
hiddenimports += collect_submodules('pdfminer')
hiddenimports += collect_submodules('sqlalchemy')


a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('F:\\A Personal PJ\\Esg_score\\src\\esg_scorer\\web\\templates', 'src/esg_scorer/web/templates'), ('F:\\A Personal PJ\\Esg_score\\scoring principles', 'scoring principles')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ChamDiemESG',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='NONE',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ChamDiemESG',
)
