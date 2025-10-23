KUBECTL ?= kubectl
K8S_DIR := $(CURDIR)

run:
	.venv\Scripts\activate && python main.py

run-api:
	.venv\Scripts\activate && uv run fastapi dev

apply:
	$(KUBECTL) apply -f alpnr-api.yaml

clean:
	$(KUBECTL) delete -f alpnr-api.yaml --ignore-not-found
