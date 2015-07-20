
PDFVIEWER=xdg-open # evince okular xpdf
MAIN_NAME=paper
PDF_NAME=$(MAIN_NAME).pdf

CSV_FILE='Analysis.csv'
STAT_DIR='stat'

# You want latexmk to *always* run, because make does not have all the info.
.PHONY: $(PDF_NAME)

default: show

all: $(PDF_NAME)

graph: 
	python stat/stat.py $(CSV_FILE) $(STAT_DIR)

$(PDF_NAME): $(MAIN_NAME).tex graph
	latexmk -pdf -pdflatex="pdflatex -shell-escape -enable-write18" \
	  -use-make $(MAIN_NAME).tex

clean:
	latexmk -CA

show: $(PDF_NAME)
	$(PDFVIEWER) $(PDF_NAME) 2> /dev/null &

release: all
	smartcp -v config.yml
