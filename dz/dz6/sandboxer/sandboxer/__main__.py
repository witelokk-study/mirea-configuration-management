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


if __name__ == "__main__":
    main()
