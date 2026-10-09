# ifaceguard — optional exported-signature profile

Separate `go/analysis` module. Select only when the application's boundary policy justifies restricting empty interfaces; this is not a universal ban on legitimate any/generic APIs or proof of semantic purity.

The analyzer inspects exported function/method parameters/results and selected nested pointer/slice/array/variadic/map/channel types for empty interfaces. It resolves named/aliased empty interfaces and does not treat a shadowed type named any as the builtin. Recursive containers terminate. Type parameters, function/struct fields and receivers are outside this selected policy. It is not a whole-program value/effect/authorization checker; read source and regression fixtures for actual supported type shapes. Nonempty typed interfaces and type-set constraints are distinct; unexported helpers are outside its stated boundary scope.

```sh
go mod verify
go test ./...
go build -mod=readonly -o bin/ifaceguard ./cmd/ifaceguard
# Execute from the selected target module:
go vet -vettool=/absolute/path/to/ifaceguard ./...
```

The overlay's optional make ifaceguard rebuilds before each vet invocation to a private mktemp /tmp/ifaceguard.XXXXXXXX directory and cleans it on exit. Selected x/tools v0.50.0 prints the executable absolute path in -V=full; Go1.27.2 cannot parse that output when the path contains spaces. Quoting the flag is insufficient. The temporary space-free binary recipe is actually exercised from a space-path project, not a speculative upgrade of an unfixed library. This Unix reference requires a writable/executable /tmp; other platforms/noexec policies need an owner-selected compatible path, not permission/config changes. Direct commands above require a space-free executable path. Do not let a preexisting binary silently stand in for changed source/module/sum/toolchain. This is not a default lint/hook prerequisite.

A function doc comment containing `//ifaceguard:allow` can suppress a deliberate boundary. Supply a rationale for review; the directive itself is not authenticated permission or anti-bypass. Example: validated generic marshalling or owner-selected sql.Scanner boundary. Exercise the actual bad/good/allow and regression cases before enabling a consumer gate.

Pinned module versions/go.sum constrain resolution/integrity, not universal safety or authenticated approval. Review changes to the complete direct/indirect graph, run regression tests and verify modules with a compatible selected local Go toolchain. Do not silently bootstrap a newer SDK or assume all other linters stay silent on a case because a historical project did. Maintain authority/ownership and reader/resource limits separately.
