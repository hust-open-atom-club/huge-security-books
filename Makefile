# =============================================
# Makefile for building and testing the book and Rust packages
# =============================================

MDBOOK_CHECK_ROOT := mdbook-check

PACKAGES := \
	$(MDBOOK_CHECK_ROOT)/packages/mdbook-trpl \
	$(MDBOOK_CHECK_ROOT)/packages/trpl \
	$(MDBOOK_CHECK_ROOT)/packages/autocorrect

# Declare all targets as .PHONY (they do not produce files with matching names)
.PHONY: build run watch check-ci check-lint clean help

# ---------------------------------------------
# Build the mdBook documentation
# ---------------------------------------------
build:
	mdbook build

# ---------------------------------------------
# Serve the book on 0.0.0.0 (useful for LAN access)
# First builds the book, then serves it
# ---------------------------------------------
run: build
	mdbook serve -n 0.0.0.0

# ---------------------------------------------
# Watch the source files and rebuild on changes
# Note: also builds first (to ensure state is correct)
# ---------------------------------------------
watch: build
	mdbook watch

# ---------------------------------------------
# Run CI checks:
#   - mdbook test: tests all code blocks in the book
#   - custom script: additional CI validations
# ---------------------------------------------
check-ci: check-lint
	mdbook test
	bash $(MDBOOK_CHECK_ROOT)/scripts/check_ci.sh

# ---------------------------------------------
# Run Lint checks
# ---------------------------------------------
check-lint:
	bash $(MDBOOK_CHECK_ROOT)/scripts/check_lint.sh

# ---------------------------------------------
# Clean build artifacts and cargo targets
# Includes:
#   - mdBook build output
#   - Cargo registry cache & target dirs
#   - Specific packages: mdbook-trpl and trpl
# ---------------------------------------------
clean:
	mdbook clean
	cargo clean
	$(foreach pkg,$(PACKAGES),cargo clean --manifest-path $(pkg)/Cargo.toml;)

# ---------------------------------------------
# Show help message for available targets
# ---------------------------------------------
help:
	@echo "Available targets:"
	@echo "  build     - Build the mdBook"
	@echo "  run       - Build and serve the book on 0.0.0.0"
	@echo "  watch     - Watch & rebuild the book on changes"
	@echo "  check-ci  - Run tests and custom CI checks"
	@echo "  clean     - Clean build & cargo artifacts"
	@echo ""
	@echo "Use 'make <target>' to run a specific action."
