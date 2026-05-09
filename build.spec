# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# Build three executables: control panel, daily runner, and setup wizard

control_panel = Analysis(
    ['src/control_panel.py'],
    pathex=['.'],
    binaries=[],
    datas=[('templets', 'templets')],
    hiddenimports=['src', 'src.paths', 'src.config_manager', 'src.auth', 'src.excel_reader', 'src.email_sender', 'src.main'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

runner = Analysis(
    ['run.py'],
    pathex=['.'],
    binaries=[],
    datas=[('templets', 'templets')],
    hiddenimports=['src', 'src.paths', 'src.config_manager', 'src.auth', 'src.excel_reader', 'src.email_sender', 'src.main'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

setup = Analysis(
    ['src/setup_wizard.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=['src', 'src.paths', 'src.config_manager'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

control_pyz = PYZ(control_panel.pure, control_panel.zipped_data, cipher=block_cipher)
runner_pyz = PYZ(runner.pure, runner.zipped_data, cipher=block_cipher)
setup_pyz = PYZ(setup.pure, setup.zipped_data, cipher=block_cipher)

control_exe = EXE(control_pyz, control_panel.scripts, control_panel.binaries, control_panel.datas,
    name='VendorReminder',
    console=False,
    icon=None,
)

runner_exe = EXE(runner_pyz, runner.scripts, runner.binaries, runner.datas,
    name='VendorReminderRunner',
    console=False,
    icon=None,
)

setup_exe = EXE(setup_pyz, setup.scripts, setup.binaries, setup.datas,
    name='VendorReminderSetup',
    console=False,
    icon=None,
)

