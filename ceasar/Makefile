BIN := bin
TARGETS := $(BIN)/caesar-python $(BIN)/caesar-c $(BIN)/caesar-rust \
           $(BIN)/caesar-haskell $(BIN)/caesar-js

.PHONY: all test clean

all: $(TARGETS)

$(BIN):
	mkdir -p $@

$(BIN)/caesar-c: c/caesar.c | $(BIN)
	gcc -Wall -Wextra -O2 -o $@ $<

$(BIN)/caesar-rust: rust/caesar.rs | $(BIN)
	rustc -O -o $@ $<

$(BIN)/caesar-haskell: haskell/Caesar.hs | $(BIN)
	mkdir -p build/haskell
	ghc -dynamic -O2 -outputdir build/haskell -o $@ $<

$(BIN)/caesar-python: python/caesar.py | $(BIN)
	chmod +x $<
	ln -sf ../$< $@

$(BIN)/caesar-js: javascript/caesar.js | $(BIN)
	chmod +x $<
	ln -sf ../$< $@

test:
	-$(MAKE) -k all
	python3 tester.py

clean:
	rm -rf $(BIN) build
