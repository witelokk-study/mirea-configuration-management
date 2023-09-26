from .git import Git


class Gitviz:
    def __init__(self, repo_dir: str):
        self._git = Git(repo_dir)

    def get_dot(self) -> str:
        """Returns Graphviz graph in .dot format"""
        pass
