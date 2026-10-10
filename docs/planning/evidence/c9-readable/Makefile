# Merge with consumer targets; generic Go, not a Wails/application mandate.
.PHONY: lint fmt format-check vet test test-coverage build ifaceguard bloat

lint:
	golangci-lint run ./...

fmt:
	golangci-lint fmt

format-check:
	golangci-lint fmt --diff

vet:
	go vet ./...

test:
	go test -race ./...

COVERAGE_THRESHOLD ?= 80
# Separate commands fail closed on test/tool errors; do not hide a pipeline error.
test-coverage:
	go test -race -coverprofile=coverage.out ./...
	go tool cover -func=coverage.out > coverage-summary.txt
	@awk -v min="$(COVERAGE_THRESHOLD)" '\
	/^total:/ { count++; if ($$NF !~ /^[0-9]+([.][0-9]+)?%$$/) bad=1; value=$$NF+0 } \
	END { if (count != 1 || bad || min !~ /^[0-9]+([.][0-9]+)?$$/ || min+0 > 100 || value > 100) { print "coverage: invalid summary or threshold"; exit 1 } \
	if (value < min+0) { printf "coverage %.1f%% < threshold %.1f%%\n", value, min; exit 1 } \
	printf "coverage %.1f%% >= threshold %.1f%%\n", value, min }' coverage-summary.txt

build:
	go build ./...

# Optional selected exported-signature policy, not a default purity/type ban.
# Rebuild each invocation so source, module/sum changes and Go version cannot leave a stale tool.
ifaceguard:
	@tmp=$$(mktemp -d /tmp/ifaceguard.XXXXXXXX) || exit $$?; 	trap 'rm -rf -- "$$tmp"' EXIT; 	(cd tools/ifaceguard && go build -mod=readonly -o "$$tmp/ifaceguard" ./cmd/ifaceguard) || exit $$?; 	go vet -vettool="$$tmp/ifaceguard" ./...

# Optional physical source inventory, no ratchet/size or comment-share quota.
bloat:
	bash scripts/bloat.sh
