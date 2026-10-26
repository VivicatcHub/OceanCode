BIN := bin
TARGETS := $(BIN)/twosum-python $(BIN)/twosum-lisp $(BIN)/twosum-zig \
           $(BIN)/twosum-ocaml $(BIN)/twosum-go

.PHONY: all test clean

all: $(TARGETS)

$(BIN):
	mkdir -p $@

$(BIN)/twosum-python: python/twosum.py | $(BIN)
	chmod +x $<
	ln -sf ../$< $@

$(BIN)/twosum-lisp: commonlisp/twosum.lisp | $(BIN)
	chmod +x $<
	ln -sf ../$< $@

$(BIN)/twosum-zig: zig/twosum.zig | $(BIN)
	mkdir -p build/zig
	zig build-exe -O ReleaseSafe --cache-dir build/zig -femit-bin=$@ $<

$(BIN)/twosum-ocaml: ocaml/twosum.ml | $(BIN)
	mkdir -p build/ocaml
	cp $< build/ocaml/twosum.ml
	ocamlfind ocamlopt -O3 -o $@ build/ocaml/twosum.ml 2>/dev/null \
		|| ocamlopt -o $@ build/ocaml/twosum.ml

$(BIN)/twosum-go: go/twosum.go | $(BIN)
	go build -o $@ $<

test:
	-$(MAKE) -k all
	python3 tester.py

clean:
	rm -rf $(BIN) build
