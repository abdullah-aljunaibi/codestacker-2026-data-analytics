install:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	python3 -m pytest tests/ -v

run:
	streamlit run app.py

analysis:
	python3 notebooks/population_projection.py
	python3 notebooks/infrastructure_analysis.py

all: install analysis test
