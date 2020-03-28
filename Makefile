SRC_DIRS = clean_actions
TEST_DIRS = tests
flit = flit


##@ bootup

.PHONY: install setup
install:  ## installs all your dependencies
install: python-install
setup: install

.PHONY: python-install
python-install:  ## Installs your python dependencies
	$(flit) install --pth-file


##@ Code Checks

.PHONY: test
test: ## Runs all the tests
test:
	 python -m pytest $(TEST_DIRS)

.PHONY: fixlint autofix
fixlint: autofix
autofix: ## Attempts to rectify any linting issues
autofix:
	 autoflake --in-place --remove-unused-variables --recursive $(SRC_DIRS) $(TEST_DIRS)
	 isort --recursive $(SRC_DIRS) $(TEST_DIRS)
	 black $(SRC_DIRS) $(TEST_DIRS)

.PHONY: lint
lint: ## Checks the code for any style violations
lint:
	 autoflake --check --remove-unused-variables --recursive $(SRC_DIRS) $(TEST_DIRS)
	 isort --check-only --recursive $(SRC_DIRS) $(TEST_DIRS)
	 black --check $(SRC_DIRS) $(TEST_DIRS)


##@ Helpers

ifndef NO_COLOUR
  cyan = \033[36m
  bold = \033[1m
  reset = \033[0m
  target_style ?= $(cyan)
  header_style ?= $(bold)
endif

.DEFAULT_GOAL:=help
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN { \
		FS = ":.*##"; \
		printf "\n"; \
		printf "$(header_style)Usage:$(reset)"; \
	    printf "\n"; \
		printf "  make $(target_style)<target>$(reset)"; \
		printf "\n"; \
	}; \
	/^[a-zA-Z_-]+:.*?##/ { \
		printf "  $(target_style)%-15s$(reset) %s", $$1, $$2; \
		printf "\n" \
	}; \
	/^##@/ { \
		printf "\n"; \
		printf "$(header_style)%s$(reset)", substr($$0, 5); \
		printf "\n"; \
	};' $(MAKEFILE_LIST)
