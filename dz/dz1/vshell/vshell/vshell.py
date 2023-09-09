from zipfile import ZipFile, ZipInfo
from os import path, system, name as os_name


def split_command(command: str) -> list[str]:
    res = [""]
    quote = None
    for c in command:
        if c == " " and quote is None:
            res.append("")
        elif c in ("'", '"'):
            if quote is None:
                quote = c
            elif quote == c:
                quote = None
        else:
            res[-1] += c
    return res


class VShell:
    def __init__(self, zip_path: str):
        self._zipfile = ZipFile(zip_path)
        self._current_path = "/"
        self._filelist = self._zipfile.filelist
        self._commands = ["pwd", "ls", "cd", "cat", "exit", "clear"]

    def loop(self):
        while True:
            self.execute_command(input("$ "))

    def execute_command(self, command: str):
        command = split_command(command)

        if command[0] in self._commands:
            method = getattr(self, command[0])
        else:
            print("Error: Command does not exist!")
            return

        result = method(*command[1:])

        if result:
            if isinstance(result, list):
                print("\n".join(result))
            else:
                print(result)

    def parse_path(self, path_: str) -> str:
        return path.abspath(path.join(self._current_path, path_))

    def _get_info(self, full_path: str) -> ZipInfo | None:
        for info in self._filelist:
            if path.abspath("/"+info.filename) == path.abspath(full_path):
                return info
        return None

    def pwd(self) -> str:
        """Prints the name of the current directory"""
        return self._current_path

    def ls(self, dir: str = ".") -> list[str]:
        """Prints the list of files in directories in the current directory"""
        full_path = self.parse_path(dir)
        if full_path == "/":
            pass
        elif not (info := self._get_info(full_path)):
            return "Error: Directory does not exist"
        elif not info.is_dir():
            return "Error: Not a directory"

        prefix = full_path.removeprefix("/")

        filenames = [x.filename for x in self._filelist]
        filenames = [x.removeprefix(prefix+"/") for x in filenames 
                     if x.startswith(prefix) and x != prefix+"/"]
        return [filename for filename in filenames if "/" not in filename 
                or (filename.endswith("/") and filename.count("/") == 1)]

    def cd(self, dir: str) -> None | str:
        """Changes current directory"""
        full_path = self.parse_path(dir)
        if full_path == "/":
            pass
        elif not (info := self._get_info(full_path)):
            return "Error: Directory does not exist"
        elif not info.is_dir():
            return "Error: Not a directory"

        self._current_path = self.parse_path(dir)

    def exit(self) -> None:
        """Exits the terminal"""
        exit(0)

    def clear(self) -> None:
        """Clears the terminal screen"""
        system('cls' if os_name == 'nt' else 'clear')

    def cat(self, filename: str) -> str:
        """Prints file content to the terminal screen"""
        full_path = self.parse_path(filename)

        if not (info := self._get_info(full_path)):
            return "Error: File does not exist"
        if full_path == "/" or info.is_dir():
            return "Error: Filename is a directory"

        with self._zipfile.open(full_path.removeprefix("/")) as f:
            return f.read().decode("utf8")
