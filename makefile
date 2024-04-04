# Makefile for Python project

# Variables
PYTHON = python3.11

# Default target
all: run

run:
	@printf "#!/bin/bash\n\nARGS=\"\$$1 \$$2 \$$3 \$$4\"\nPYTHON_VER=\"$(PYTHON)\"\n\nsource env/bin/activate\n\$$PYTHON_VER src/main.py \$$ARGS" > run.sh 
	@chmod +x run.sh

# Clean the project
clean:
	rm -rf __pycache__