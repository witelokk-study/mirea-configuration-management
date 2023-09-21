import gzip
from io import BytesIO
from os import path
import subprocess
import pycdlib
import tempfile
from .libcpio.libcpio import CpioArchive, CpioEntry
import os


from .copy_iso import copy_iso_file


class Sandboxer:
    def __init__(self, program_path: str, ui: bool) -> None:
        self._modified_iso_path = None
        self._ui = ui
        print(ui)

        with open(program_path, "rb") as program_file:
            self._program = program_file.read()

        self._prepare_iso()

    def _prepare_iso(self):
        # locate initial iso file
        iso_path = path.join(
            path.dirname(__file__), 
            "TinyCore-current.iso" if self._ui else "Core-current.iso")

        # extract core.gz from archive
        iso_file = pycdlib.PyCdlib()
        iso_file.open(iso_path, "rb")
        core_gz = BytesIO()
        iso_file.get_file_from_iso_fp(core_gz, iso_path="/BOOT/CORE.GZ;1")

        # extract core.cpio from core.gz
        core_gz.seek(0)
        core_cpio_bytes = gzip.open(core_gz).read()

        # modify core.cpio
        core_cpio = CpioArchive(BytesIO(core_cpio_bytes))
        self._modify_core_cpio(core_cpio)

        # recompress
        core_cpio_bytes_io = BytesIO()
        core_cpio.write(core_cpio_bytes_io)
        core_gz = gzip.compress(core_cpio_bytes_io.getvalue(), compresslevel=0)

        # create new iso file an copy data
        # copy core.gz
        new_iso_file = pycdlib.PyCdlib()
        new_iso_file.new(rock_ridge="1.10", interchange_level=3, joliet=3)
        copy_iso_file(iso_file, new_iso_file)

        # modify iso
        self._modify_iso(new_iso_file)

        # add El Torito boot data to new iso
        new_iso_file.add_eltorito(
            "/BOOT/ISOLINUX/ISOLINUX.BIN;1", "/BOOT/ISOLINUX/BOOT.CAT;1",
            boot_info_table=True)

        # replace core.gz with modified core.gz
        new_iso_file.rm_file(iso_path="/BOOT/CORE.GZ;1")
        new_iso_file.add_fp(
            BytesIO(core_gz), len(core_gz), iso_path="/BOOT/CORE.GZ;1",
            rr_name="core.gz")

        # create temporary file for modified iso
        self._modified_iso_path = tempfile.mktemp()

        # write modfied iso
        new_iso_file.force_consistency()
        new_iso_file.write(self._modified_iso_path)
        new_iso_file.close()

    def _modify_core_cpio(self, core_cpio: CpioArchive):
        """Load binaries, change configs etc"""

        core_cpio["etc/os-release"].data = \
            core_cpio["etc/os-release"].data \
            .replace(b"TinyCore", b"Witelokk")

        # copy program to /bin
        core_cpio.add(CpioEntry(
            30234178,       # ino
            0o100755,       # mode; sym?link - 41471
            0,              # uid
            0,              # gid
            1,              # nlink
            1681304330,     # mtime
            8,              # devmajor
            2,              # devminor
            0,              # rdevminor
            0,              # rdevmajor
            0,              # check
            "bin/program",  # path
            self._program   # data
        ))

        # add '/bin/bash' to .profile or .xsession
        if self._ui:
            core_cpio["etc/init.d/tc-config"].data +=\
                b"\necho '\n/bin/program' >> '/home/tc/.xsession'"
        else:
            core_cpio["etc/skel/.profile"].data +=\
                b"\n/bin/program"

    def _modify_iso(self, iso: pycdlib.PyCdlib):
        """Skip boot menu etc"""
        isolinux_cfg_path = "/BOOT/ISOLINUX/ISOLINUX.CFG;1"
        isolinux_cfg = BytesIO()
        iso.get_file_from_iso_fp(isolinux_cfg,
                                 iso_path=isolinux_cfg_path)
        isolinux_cfg.seek(0)

        isolinux_cfg_text = isolinux_cfg.read()\

        if self._ui:
            isolinux_cfg_text = isolinux_cfg_text\
                .replace(b"TIMEOUT 600", b"TIMEOUT 1")
        else:
            isolinux_cfg_text = isolinux_cfg_text\
                .replace(b"prompt 1", b"prompt 0")

        iso.rm_file(iso_path=isolinux_cfg_path)
        iso.add_fp(
            BytesIO(isolinux_cfg_text), len(isolinux_cfg_text),
            iso_path=isolinux_cfg_path, rr_name="isolinux.cfg")

    def run(self):
        """Runs provided program in a Qemu virtual machine"""

        # run qemu with modified iso
        subprocess.run([
            "qemu-system-x86_64",
            "-boot", "d",
            "-cdrom", self._modified_iso_path,
            "-m", "2048",
            "-display", "gtk",
            "-accel", "kvm"
        ])

    def __del__(self):
        if self._modified_iso_path:
            os.remove(self._modified_iso_path)
