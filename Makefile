SHELL := /bin/bash

# Paths (override at runtime: make clab-up LABDIR=arista-avd-lab)
LABDIR ?= arista-avd-lab
TOPO   ?= $(LABDIR)/clab-topo.yml
INV    ?= $(LABDIR)/inventory.yml

BUILD_PLAY    ?= $(LABDIR)/playbooks/build.yml
DEPLOY_PLAY   ?= $(LABDIR)/playbooks/deploy.yml
VALIDATE_PLAY ?= $(LABDIR)/playbooks/validate.yml

VENV ?= arista-avd-lab/cenv
ACT  := . $(VENV)/bin/activate

.PHONY: venv deps clab-up clab-down build deploy validate endpoints reset all

venv:
	python3 -m venv $(VENV)
	$(ACT) && pip install -U pip

deps:
	$(ACT) && pip install -r requirements.txt
	# ensure collections (adjust versions if you pin)
	$(ACT) && ansible-galaxy collection install arista.avd arista.eos

clab-up:
	sudo containerlab deploy -t $(TOPO)

clab-down:
	sudo containerlab destroy -t $(TOPO) --cleanup

build:
	$(ACT) && ansible-playbook -i $(INV) $(BUILD_PLAY)

deploy:
	$(ACT) && ansible-playbook -i $(INV) $(DEPLOY_PLAY)

validate:
	$(ACT) && ansible-playbook -i $(INV) $(VALIDATE_PLAY)

endpoints:
	# If scripts live under LABDIR/scripts, keep these paths. Otherwise adjust.
	sudo docker exec -it clab-lab-client1 sh -lc "$$(cat $(LABDIR)/scripts/endpoints_client1.sh)"
	sudo docker exec -it clab-lab-client2 sh -lc "$$(cat $(LABDIR)/scripts/endpoints_client2.sh)"

reset: clab-down clab-up
	@echo "Lab reset complete."

all: build deploy validate
