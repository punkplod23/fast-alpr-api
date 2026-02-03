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

create-ghcr-secret:
	kubectl create secret docker-registry ghcr-secret \
	  --docker-server=ghcr.io \
	  --docker-username="Gareth G" \
	  --docker-password=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 \
	  --docker-email=gareth.gwyther@gmail.com
