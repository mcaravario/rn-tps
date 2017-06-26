# Makefile for LaTeX files

LATEX= pdflatex
BIN=informe.pdf

SRC=informe.tex

all: $(BIN)

$(BIN): $(SRC)
	$(LATEX) $<

clean:
	rm -rf *.aut *.toc informe.pdf *.log

.PHONY:
	clean
