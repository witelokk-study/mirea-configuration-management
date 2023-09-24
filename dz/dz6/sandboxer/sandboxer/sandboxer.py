import gzip
from io import BytesIO
from os import path, listdir
import subprocess
from random import randint

import pycdlib
import tempfile
from .libcpio.libcpio import CpioArchive, CpioEntry
import os


from .copy_iso import copy_iso_file


class Sandboxer:
    def __init__(self, program_path: str, ui: bool, from_source: bool,
                 headless_output: str) -> None:
        self._modified_iso_path = None
        self._ui = ui
        self._from_source = from_source
        self._program_path = program_path
        self._headless_output = headless_output

        self._prepare_iso()

    def _prepare_iso(self):
        # locate initial iso file
        iso_path = path.join(
            path.dirname(__file__), 
            "data/iso/TinyCorePure64-current.iso" if self._ui
            else "data/iso/CorePure64-current.iso")

        # extract core.gz from archive
        iso_file = pycdlib.PyCdlib()
        iso_file.open(iso_path, "rb")
        core_gz = BytesIO()
        iso_file.get_file_from_iso_fp(core_gz, iso_path="/BOOT/COREPURE64.GZ;1")

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
        new_iso_file.rm_file(iso_path="/BOOT/COREPURE64.GZ;1")
        new_iso_file.add_fp(
            BytesIO(core_gz), len(core_gz), iso_path="/BOOT/COREPURE64.GZ;1",
            rr_name="corepure64.gz")

        # create temporary file for modified iso
        self._modified_iso_path = tempfile.mktemp()

        # write modfied iso
        new_iso_file.force_consistency()
        new_iso_file.write(self._modified_iso_path)
        new_iso_file.close()

    def _modify_core_cpio(self, core_cpio: CpioArchive):
        """Load binaries, change configs etc"""

        # link /lib64 to /lib
        core_cpio.add(CpioEntry(
            32231531,                # ino
            0o120777,                # mode; sym?link
            0,                       # uid
            0,                       # gid
            1,                       # nlink
            1681304330,              # mtime
            8,                       # devmajor
            2,                       # devminor
            0,                       # rdevminor
            0,                       # rdevmajor
            0,                       # check
            "lib64",                 # path
            b"/lib"                  # data
        ))

        # copy program to /etc/skel
        if self._from_source:
            self._copy_dir_to_cpio(core_cpio, self._program_path, "/etc/skel")
            exec_command = f"cd /home/tc/{self._program_path};make run"
        else:
            with open(self._program_path, "rb") as program_file:
                core_cpio.add(CpioEntry(
                    30234178,               # ino
                    0o100755,               # mode; sym?link - 41471
                    0,                      # uid
                    0,                      # gid
                    1,                      # nlink
                    1681304330,             # mtime
                    8,                      # devmajor
                    2,                      # devminor
                    0,                      # rdevminor
                    0,                      # rdevmajor
                    0,                      # check
                    "etc/skel/program",     # path
                    program_file.read()     # data
                ))
            exec_command = "/home/tc/program"

        if self._ui:
            core_cpio["etc/init.d/tc-config"].data +=\
                f"\necho \"\naterm -e sh -c '{exec_command}; sh'\" >> '/home/tc/.xsession'".encode()
        else:
            skel_profile = core_cpio["etc/skel/.profile"].data.decode()
            if self._headless_output:
                # add text to find start and end of program output
                skel_profile += "\necho '========sandboxer======='"

            skel_profile += f"\n{exec_command}"

            if self._headless_output:
                # login user to ttys0 instead of tty1
                core_cpio["etc/inittab"].data = core_cpio["etc/inittab"].data\
                    .replace(b"tty1", b"ttyS0")
                skel_profile += "\necho '========sandboxer======='"
                # shutdown after program execution
                skel_profile += f"\nsudo poweroff"

            core_cpio["etc/skel/.profile"].data = skel_profile.encode()

    def _copy_dir_to_cpio(self, cpio_archive: CpioArchive, dir_path: str,
                          target_dir: str):
        dir_path = path.abspath(dir_path)

        full_path = path.join(target_dir, path.basename(dir_path))

        # create a directory
        cpio_archive.add(CpioEntry(
            30234143,                   # ino
            0o40755,                    # mode; sym?link - 41471
            0,                          # uid
            0,                          # gid
            2,                          # nlink
            1681304330,                 # mtime
            8,                          # devmajor
            2,                          # devminor
            0,                          # rdevminor
            0,                          # rdevmajor
            0,                          # check
            full_path,                  # path
            b""                         # data
        ))
        # copy children
        for child in listdir(dir_path):
            if path.isdir(path.join(dir_path, child)):
                self._copy_dir_to_cpio(
                    cpio_archive,
                    path.join(dir_path, child),
                    full_path
                )
            else:
                self._copy_file_to_cpio(
                    cpio_archive,
                    path.join(dir_path, child),
                    full_path
                )

    def _copy_file_to_cpio(self, cpio_archive: CpioArchive, file_path: str,
                           target_dir: str):
        file_path = path.abspath(file_path)

        with open(file_path, "rb") as file:
            cpio_archive.add(CpioEntry(
                randint(10000, 99999),  # ino
                0o100755,  # mode; sym?link - 41471
                0,  # uid
                0,  # gid
                1,  # nlink
                1681304330,  # mtime
                8,  # devmajor
                2,  # devminor
                0,  # rdevminor
                0,  # rdevmajor
                0,  # check
                path.join(target_dir, path.basename(file_path)),  # path
                file.read()  # data
            ))

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
            kernel_options = ["cde"]  # loads packages from cde/onboot.lst

            if self._headless_output:
                kernel_options.append(
                    # "console=ttyAMA0,115200 console=tty  highres=off "
                    "console=ttyS0"
                )

            isolinux_cfg_text = isolinux_cfg_text\
                .replace(b"prompt 1", b"prompt 0")\
                .replace(b"append",
                         b"append " + " ".join(kernel_options).encode())

        iso.rm_file(iso_path=isolinux_cfg_path)
        iso.add_fp(
            BytesIO(isolinux_cfg_text), len(isolinux_cfg_text),
            iso_path=isolinux_cfg_path, rr_name="isolinux.cfg")

        # add extensions
        extensions = ("gcc", "make", "isl", "isl_dev", "mpc", "mpc_dev",
                      "mpfr", "mpfr_dev", "gmp", "gmp_dev", "zstd", "zstd_dev",
                      "libzstd", "glibc_base_dev", "linux_headers", "binutils",
                      "glibc_add_lib",)

        try:
            iso.add_directory(iso_path="/CDE", rr_name="cde")
            iso.add_directory(iso_path="/CDE/OPTIONAL", rr_name="optional")
        except pycdlib.pycdlibexception.PyCdlibInvalidInput:
            pass
        for extension in extensions:
            extension_path = path.join(
                path.dirname(__file__), f"data/tcz/{extension}.tcz")
            iso.add_file(
                extension_path,
                iso_path=f"/CDE/OPTIONAL/{extension}.tcz;1".upper(),
                rr_name=extension+".tcz")

        try:
            xbase = BytesIO()
            iso.get_file_from_iso_fp(xbase, iso_path="/CDE/ONBOOT.LST;1")
            new_xbase_data = xbase.getvalue().decode()
            iso.rm_file("/CDE/ONBOOT.LST;1", "onboot.lst")
        except pycdlib.pycdlibexception.PyCdlibInvalidInput:
            new_xbase_data = ""
        new_xbase_data += "\n".join(x+".tcz" for x in extensions)
        new_xbase_data = new_xbase_data.encode()
        iso.add_fp(BytesIO(new_xbase_data), len(new_xbase_data),
                   iso_path="/CDE/ONBOOT.LST;1", rr_name="onboot.lst")


    def run(self):
        """Runs provided program in a Qemu virtual machine"""
        qemu_args = [
            "qemu-system-x86_64",
            "-boot", "d",
            "-cdrom", self._modified_iso_path,
            "-m", "2048",
        ]

        if self._headless_output:
            qemu_args += ["-nographic"]
        else:
            qemu_args += ["-display", "gtk", "-accel", "kvm"]

        p = subprocess.Popen(qemu_args, stdout=subprocess.PIPE, text=True)
        output, _ = p.communicate()

        if self._headless_output:
            output_start = output.find("========sandboxer=======") + 24
            output_end = output.find("========sandboxer=======", output_start)

            with open(self._headless_output, "w") as f:
                f.write(output[output_start:output_end])

    def __del__(self):
        if self._modified_iso_path:
            os.remove(self._modified_iso_path)
