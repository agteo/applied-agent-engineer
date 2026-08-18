.PHONY: install test run traces check clean

install:
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest

run:
	python3 run_agent.py --all --quiet

traces:
	python3 run_agent.py --all --quiet
	python3 -m acme_agent.check_traces traces/level-1.jsonl

check: test traces
	@echo "Level 1 checks passed."

clean:
	rm -rf traces/*.jsonl .pytest_cache **/__pycache__
