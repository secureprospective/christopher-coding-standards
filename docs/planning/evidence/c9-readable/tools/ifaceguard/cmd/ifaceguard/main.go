// Command ifaceguard is the optional vettool entry point.
// The overlay make target rebuilds to a fresh private space-free /tmp directory:
// selected x/tools version output cannot be parsed by Go when the executable's
// absolute path has spaces. Direct builds must use a compatible executable path.
package main

import (
	"ifaceguard"

	"golang.org/x/tools/go/analysis/unitchecker"
)

func main() {
	unitchecker.Main(ifaceguard.Analyzer)
}
