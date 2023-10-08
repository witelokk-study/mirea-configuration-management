import os.path

from graphviz import Digraph

from .blob import Blob
from .git import Git


class Gitviz:
    def __init__(self, repo_dir: str):
        self._git = Git(repo_dir)

    def get_dot(self) -> Digraph:
        """Returns Graphviz graph in .dot format"""
        graph = Digraph()
        graph.attr(rankdir="LR")
        # graph.attr(overlap="scale")

        with graph.subgraph() as commit_rank:
            commit_rank.attr(rank='same')

            for object_name, commit in self._git.commits.items():
                commit_rank.node(
                    object_name, label=f"commit {object_name[:6]}\n{commit.name}",
                    shape="box", fillcolor="#edb800", style="filled")

                graph.edge(object_name, commit.tree.object_name)

                if commit.parent:
                    graph.edge(object_name, commit.parent)

        with graph.subgraph() as tree_rank:
            tree_rank.attr(rank='same')

            for object_name, tree in self._git.trees.items():
                tree_rank.node(
                    object_name,
                    label=f"tree {object_name[:6]}",
                    shape="box", fillcolor="#18a6b1", style="filled"
                )

                for entry in tree.entries:
                    graph.edge(tree.object_name,
                               entry.blob_or_tree_object_name,
                               label=entry.name)

        for object_name, blob in self._git.blobs.items():
            graph.node(
                object_name,
                label=f"blob {object_name[:6]}",
                shape="box"
            )

        return graph
