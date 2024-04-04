# Makefile for Python project

# Variables
PYTHON = python3
ARGS = 3 10 src/Basic_Green_Cards.txt src/Basic_RED_cards.txt

# Default target
all: run

# Run the main file
run:
	$(PYTHON) src/main.py $(ARGS)

wext:
	$(PYTHON) -m py_compile src/*.py

# Clean the project
clean:
	rm -rf __pycache__