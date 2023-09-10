import requests
import json


class NpmDependencyVisualizer:
    def __init__(self, package_name: str) -> None:
        self._package_name = package_name

    def generate_dependencies(self, package_name: str) -> list[str]:
        r = requests.get(f"https://registry.npmjs.org/{package_name}")
        response = json.loads(r.content)

        try:
            latest_version = response["dist-tags"]["latest"]
            return list(response["versions"][latest_version]
                        ["dependencies"].keys())
        except Exception:
            return []

    def get_graph(self) -> str:
        """Returns a Graphviz graph of dependencies"""
        xs = [self._package_name]
        graph = f'"{self._package_name}";'
        while xs:
            x = xs.pop()
            dependencies = self.generate_dependencies(x)
            for dependency in dependencies:
                if '"'+dependency+'"' not in graph:
                    xs.append(dependency)
                graph += f'"{x}" -> "{dependency}";'
        return f"digraph {{ {graph} }}"
