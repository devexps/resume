# Resume Makefile
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)
DATE := $(shell date "+%B %Y")

DOCKER_RUN = docker run --rm -v ${PWD}:/work -w /work -it --user=$(CURRENT_UID):$(CURRENT_GID)
BUILD_PY = python3 resume.py

.PHONY: all clean html md markdown txt test text pdf docx json
all: html md txt pdf docx json

html md markdown txt text json:
	$(BUILD_PY) $@

pdf:
	@echo "Creating PDF"
	$(DOCKER_RUN) \
		--entrypoint=/usr/bin/google-chrome \
		browserless/chrome:latest --headless --disable-gpu \
		--no-sandbox --print-to-pdf=docs/thangn.pdf docs/index.html

docx word:
	@echo "Creating docx"
	$(DOCKER_RUN) \
		pandoc/latex --from markdown --to docx README.md \
		-f gfm \
		-V linkcolor:blue \
		-V geometry:a4paper \
		-V geometry:margin=2cm \
		-o docs/thangn.docx

serve:
	docker run --rm -v ${PWD}/docs:/usr/share/nginx/html/resume -w /work -p 8080:80 nginx

test:
	$(DOCKER_RUN) pipelinecomponents/yamllint yamllint resume.yaml

clean:
	rm -f docs/thangn-narrow.txt docs/thangn.txt docs/thangn.json \
		docs/thangn.docx docs/thangn.pdf docs/index.html
	git restore --staged README.md
	git restore README.md
