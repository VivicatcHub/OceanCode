BIN := bin
TARGETS := $(BIN)/modexp-python $(BIN)/modexp-c $(BIN)/modexp-elixir \
           $(BIN)/modexp-rust $(BIN)/modexp-ruby

.PHONY: all test clean

all: $(TARGETS)

$(BIN):
	mkdir -p $@

$(BIN)/modexp-c: c/modexp.c | $(BIN)
	gcc -Wall -Wextra -O2 -o $@ $<

$(BIN)/modexp-rust: rust/modexp.rs | $(BIN)
	rustc -O -o $@ $<

$(BIN)/modexp-elixir: elixir/modexp.exs | $(BIN)
	chmod +x $<
	ln -sf ../$< $@

$(BIN)/modexp-python: python/modexp.py | $(BIN)
	chmod +x $<
	ln -sf ../$< $@

$(BIN)/modexp-ruby: ruby/modexp.rb | $(BIN)
	chmod +x $<
	ln -sf ../$< $@

test:
	-$(MAKE) -k all
	python3 tester.py

clean:
	rm -rf $(BIN) build
