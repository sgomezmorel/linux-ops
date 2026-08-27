.PHONY: perms venv install check-env run-health run-inventory

perms:
	chmod 755 scripts/* 2>/dev/null || true
	chmod 644 conf/* 2>/dev/null || true
	chmod 600 .env 2>/dev/null || true

venv:
	python3 -m venv .venv

install:
	.venv/bin/pip install -r requirements.txt 2>/dev/null || true

check-env:
	./scripts/check-env.sh

run-health:
	./scripts/linux-ops health

run-inventory:
	./scripts/linux-ops inventory
