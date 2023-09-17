from io import BytesIO
from os import path
import gzip
import pycdlib
import subprocess
from tempfile import mkdtemp


def main():
    # extract root.gz from archive
    iso_path = path.join(path.dirname(__file__), "TinyCore-current.iso")

    iso_file = pycdlib.PyCdlib()
    iso_file.open(iso_path)

    root_gz = BytesIO()
    iso_file.get_file_from_iso_fp(root_gz, iso_path="/BOOT/CORE.GZ;1")
    # extract root.cpio from root.gz

    root_gz.seek(0)
    root_cpio_bytes = gzip.open(root_gz).read()
    # print(f"bytes = {root_cpio_bytes}")

    # extract files from root.cpio
    temp_dir = mkdtemp()
    print(temp_dir)
    subprocess.run(["cpio", "-id", "--no-absolute-filenames"], input=root_cpio_bytes, cwd=temp_dir)

    # copy bash to temp_dir/bin/
    subprocess.run(["cp", "/usr/bin/bash", path.join(temp_dir, "bin")])

    # pack it back to root.cpio
    subprocess.run(["find", temp_dir, "|", "cpio", "-o", "-H", "newc", "|", "gzip", "-9", ">", "/rootfs.gz"], input=subprocess.PIPE, cwd=temp_dir)


if __name__ == "__main__":  
    main()
