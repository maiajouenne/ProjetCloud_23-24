.PHONY: all prepare run compose 

prepare:
	poetry config virtualenvs.prefer-active-python true
	poetry config virtualenvs.in-project true
	poetry install --no-root

run:
	gnome-terminal -- python3 app.py
	gnome-terminal -- streamlit run dashboard.py
	gnome-terminal -- docker-compose up
