import gzip
from io import BytesIO
from os import path
import subprocess
import pycdlib
from .libcpio.libcpio import CpioArchive

from .copy_iso import copy_iso_file


class Sandboxer:
    def __init__(self, program_path: str) -> None:
        self._modified_iso_path = None
        self._program_path = program_path
        self._prepare_iso()

    def _prepare_iso(self):
        # locate initial iso file
        iso_path = path.join(path.dirname(__file__), "Core-current.iso")

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

        # add El Torito boot data to new iso
        new_iso_file.add_eltorito(
            "/BOOT/ISOLINUX/ISOLINUX.BIN;1", "/BOOT/ISOLINUX/BOOT.CAT;1",
            boot_info_table=True)

        # replace core.gz with modified core.gz
        new_iso_file.rm_file(iso_path="/BOOT/CORE.GZ;1")
        new_iso_file.add_fp(
            BytesIO(core_gz), len(core_gz), iso_path="/BOOT/CORE.GZ;1",
            rr_name="core.gz")

        # write modfied iso
        new_iso_file.force_consistency()
        new_iso_file.write("ModdedTinyCore.iso")
        new_iso_file.close()

    def _modify_core_cpio(self, core_cpio: CpioArchive):
        """Load binaries, change configs etc"""

        core_cpio["etc/os-release"].data = \
            core_cpio["etc/os-release"].data \
            .replace(b"TinyCore", b"Witelokk")

    def run(self):
        """Runs provided program in a Qemu virtual machine"""

        # run qemu with modified iso
        subprocess.run([
            "qemu-system-x86_64",
            "-boot", "d",
            "-cdrom", "ModdedTinyCore.iso",
            "-m", "2048",
            "-display", "gtk",
            "-accel", "kvm"
        ])
