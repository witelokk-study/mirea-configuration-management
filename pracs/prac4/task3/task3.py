import json

with open("civgraph.json") as f:
    civgraph = json.load(f)

with open("Makefile", "w") as f:
    for target, requirements in civgraph.items():
        f.write(f"{target}: {' '.join(requirements)}\n\t@echo {target}\n\t@touch {target}\n")
    f.write(f".PHONY: clean\nclean:\n\trm -rf {' '.join(civgraph.keys())}")
