from io import BytesIO
import pycdlib


def copy_iso_file(old_iso: pycdlib.PyCdlib, new_iso: pycdlib.PyCdlib, dir="/"):
    for file in old_iso.list_children(iso_path=dir):
        name = file.file_identifier().decode()
        iso_path = dir+name
        rr_name = file.rock_ridge._full_name.decode()

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
            new_iso.add_fp(BytesIO(io.getvalue()), len(io.getvalue()),
                           iso_path=iso_path, rr_name=rr_name)
