######################
# Setup Commands #
######################

# Install
.PHONY: install
install:
	./scripts/install.sh

########################
# Development Commands #
########################

# Run ruff
.PHONY: ruff
ruff:
	./scripts/run_ruff.sh

.PHONY: start-worker
start-worker:
	poetry run celery -A senior_living_evaluator.celery.tasks worker --concurrency=4 --loglevel=INFO
