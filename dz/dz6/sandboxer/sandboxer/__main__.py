from io import BytesIO
from os import path
import gzip
import pycdlib
import subprocess
from .libcpio.libcpio import CpioArchive, CpioEntry


def modify_core_cpio(core_cpio: CpioArchive):
    core_cpio["etc/os-release"].data = \
        core_cpio["etc/os-release"].data \
        .replace(b"TinyCore", b"Witelokk")


def copy_iso_file(old_iso: pycdlib.PyCdlib, new_iso: pycdlib.PyCdlib, dir="/"):
    for file in old_iso.list_children(iso_path=dir):
        name = file.file_identifier().decode()
        iso_path = dir+name
        rr_name = file.rock_ridge._full_name.decode()

        # print(name)

        if name in (".", ".."):
            continue

        if file.is_dir():
            new_iso.add_directory(
                iso_path=iso_path,
                rr_name=rr_name)
            copy_iso_file(old_iso, new_iso, iso_path+"/")
        else:
            io = BytesIO()
            old_iso.get_file_from_iso_fp(io, iso_path=iso_path)
            print(len(io.getvalue()))
            new_iso.add_fp(BytesIO(io.getvalue()), len(io.getvalue()), iso_path=iso_path,
                           rr_name=rr_name)

            # test
            # io2 = BytesIO()
            # new_iso.get_file_from_iso_fp(io2, iso_path=iso_path)
            # print(io2.getvalue()[:100])


def main():
    # extract core.gz from archive
    iso_path = path.join(path.dirname(__file__), "Core-current.iso")

    iso_file = pycdlib.PyCdlib()
    iso_file.open(iso_path, "rb")

    core_gz = BytesIO()
    iso_file.get_file_from_iso_fp(core_gz, iso_path="/BOOT/CORE.GZ;1")

    # extract core.cpio from core.gz
    core_gz.seek(0)
    core_cpio_bytes = gzip.open(core_gz).read()

    # modify core.cpio
    core_cpio = CpioArchive(BytesIO(core_cpio_bytes))
    modify_core_cpio(core_cpio)

    # recompress
    core_cpio_bytes_io = BytesIO()
    core_cpio.write(core_cpio_bytes_io)
    core_gz = gzip.compress(core_cpio_bytes_io.getvalue(), compresslevel=0)
    # core_gz = core_gz[:3] + bytes([0b00100000]) + core_gz[4:10] + b"core.gz\x00" + core_gz[11:]  # set file name

    # create new iso file an copy data

    # copy core.gz
    new_iso_file = pycdlib.PyCdlib()
    new_iso_file.new(rock_ridge="1.10",
                     interchange_level=iso_file.interchange_level,
                     joliet=3, )

    copy_iso_file(iso_file, new_iso_file)
    new_iso_file.add_eltorito("/BOOT/ISOLINUX/ISOLINUX.BIN;1", "/BOOT/ISOLINUX/BOOT.CAT;1",boot_info_table=True)

    # new_iso_file.add_directory(iso_path="/BOOT", rr_name="boot")
    new_iso_file.rm_file(iso_path="/BOOT/CORE.GZ;1")
    new_iso_file.add_fp(BytesIO(core_gz), len(core_gz), iso_path="/BOOT/CORE.GZ;1",
                        rr_name="core.gz")

    new_iso_file.force_consistency()

    new_iso_file.write("ModdedTinyCore.iso")
    new_iso_file.close()

    # return
    # run qemu with modified iso
    subprocess.run([
        "qemu-system-x86_64",
        "-boot", "d",
        "-cdrom", "ModdedTinyCore.iso",
        "-m", "2048",
        "-display", "gtk",
        "-accel", "kvm"
    ])


if __name__ == "__main__":
    main()
