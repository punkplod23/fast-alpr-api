KUBECTL ?= kubectl
K8S_DIR := $(CURDIR)

run:
	.venv\Scripts\activate && python main.py

run-api:
	.venv\Scripts\activate && python -m fastapi dev main.py

apply:
	$(KUBECTL) apply -f alpnr-api.yaml

clean:
	$(KUBECTL) delete -f alpnr-api.yaml --ignore-not-found

setup:
	python -m venv .venv
	.venv\Scripts\activate && pip install fastapi[standard] opencv-python numpy fastmcp fast-alpr