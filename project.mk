#Project specific values
YAML_DIRECTORY?=deploy
SELECTOR_SYNC_SET_TEMPLATE_DIR?=scripts/templates/
GIT_ROOT ?= $(shell git rev-parse --show-toplevel 2>&1)

# WARNING: REPO_NAME will default to the current directory if there are no remotes
REPO_NAME ?= $(shell basename $$((git config --get-regex remote\.*\.url 2>/dev/null | cut -d ' ' -f2 || pwd) | head -n1 | sed 's|.git||g'))

SELECTOR_SYNC_SET_DESTINATION?=${GIT_ROOT}/hack/00-osd-${REPO_NAME}.selectorsyncset.yaml.tmpl

# Munge the output of the following because Linux openssl and MacOS openssl
# somehow have different output formats MacOS merely prints the checksum
# whereas Linux will print (stdin)= checksum.
SOURCE_CODE_HASH ?= $(shell (cat monitor/* 2>/dev/null || echo "no-source-code") | openssl dgst -sha256 | grep -o '[[:xdigit:]][[:xdigit:]]*$$')

