from typing import IO

from .cpio_entry import CpioEntry


class CpioArchive:
    def __init__(self, path_or_file: str | IO) -> None:
        if isinstance(path_or_file, str):
            file = open(path_or_file, "rb")
        else:
            file = path_or_file

        self._entries: list[CpioEntry] = []

        self._read(file)

        # close file it was opened here
        if isinstance(path_or_file, str):
            file.close()

    def _read(self, file: IO):
        magic = file.read(6)

        if magic != b"070701":
            raise NotImplementedError(
                "This type of cpio archives is not supported")

        file.seek(0)

        def read_number() -> int:
            return int(file.read(8).decode(), 16)

        name = None
        while name != "TRAILER!!!":
            magic = file.read(6).decode()  # Magic number 070701
            assert magic == "070701"
            ino = read_number()         # I-number of file
            mode = read_number()        # File mode
            uid = read_number()         # Owner user ID
            gid = read_number()         # Owner group ID
            nlink = read_number()       # Number of links to file
            mtime = read_number()        # Modify time of file
            filesize = read_number()    # Length of file
            devmajor = read_number()
            devminor = read_number()
            rdevmajor = read_number()
            rdevminor = read_number()
            namesize = read_number()    # Length of path
            check = read_number()

            name = file.read(namesize).decode().removesuffix('\x00')

            # header + name is padded to a multiple of 4 bytes
            n = 110 + namesize
            if n % 4 != 0:
                file.read(4 - n % 4)

            data = file.read(filesize)

            # data is padded to a multiple of 4 bytes
            if filesize % 4 != 0:
                file.read(4 - filesize % 4)

            self._entries.append(CpioEntry(
                ino, mode, uid, gid, nlink, mtime, devmajor, devminor,
                rdevmajor, rdevminor, check, name, data
            ))
        self._extra = file.read()

    def write(self, path_or_file: str | IO):
        if isinstance(path_or_file, str):
            file = open(path_or_file, "wb")
        else:
            file = path_or_file

        def write_number(x: int):
            file.write(hex(x)[2:].zfill(8).encode())
        for entry in self._entries:
            file.write(b"070701")
            write_number(entry.ino)
            write_number(entry.mode)
            write_number(entry.uid)
            write_number(entry.gid)
            write_number(entry.nlink)
            write_number(entry.mtime)
            write_number(len(entry.data))
            write_number(entry.devmajor)
            write_number(entry.devminor)
            write_number(entry.rdevmajor)
            write_number(entry.rdevminor)
            write_number(len(entry.path) + 1)
            write_number(entry.check)

            # header + name is padded to a multiple of 4 bytes
            file.write((entry.path + "\x00").encode())
            n = 110 + len(entry.path) + 1
            if n % 4 != 0:
                file.write(b"\x00" * (4 - n % 4))

            # data is padded to a multiple of 4 bytes
            file.write(entry.data)
            n = len(entry.data)
            if n % 4 != 0:
                file.write(b"\x00" * (4 - n % 4))

        file.write(self._extra)

        # close file it was opened here
        if isinstance(path_or_file, str):
            file.close()

    @property
    def entries(self) -> tuple[CpioEntry, ...]:
        return tuple(self._entries)

    def __iter__(self):
        yield from self._entries

    def __getitem__(self, path: str) -> CpioEntry | None:
        for entry in self._entries:
            if entry.path == path:
                return entry
        raise FileNotFoundError()

    def add(self, entry: CpioEntry):
        if any([e.path == entry.path for e in self._entries]):
            raise FileExistsError()

        self._entries.append(entry)

    def remove(self, entry: CpioEntry):
        self._entries.remove(entry)
