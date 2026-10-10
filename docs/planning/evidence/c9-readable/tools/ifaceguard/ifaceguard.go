// Package ifaceguard implements an optional exported-signature policy.
// It resolves selected empty-interface types, not application permission,
// semantic purity or complete boundary safety; deliberate generic APIs exist.
package ifaceguard

import (
	"go/ast"
	"go/types"
	"strings"

	"golang.org/x/tools/go/analysis"
	"golang.org/x/tools/go/analysis/passes/inspect"
	"golang.org/x/tools/go/ast/inspector"
)

// Doc is the analyzer's help text (shown by `go vet -vettool=… help`).
const Doc = `report selected empty-interface types in exported signatures

Resolves bare/named/aliased empty interfaces nested in pointer, slice, array,
map or channel parameters/results. Type parameters, function/struct fields,
receivers and unexported functions are outside this selected policy.
Suppress deliberate generic boundaries with //ifaceguard:allow in the doc comment.`

// allowDirective suppresses the diagnostic for a single function when present
// in that function's doc comment.
const allowDirective = "//ifaceguard:allow"

// Analyzer is the ifaceguard analyzer, wired for use via singlechecker,
// unitchecker (go vet -vettool), or golangci-lint's module plugin system.
var Analyzer = &analysis.Analyzer{
	Name:     "ifaceguard",
	Doc:      Doc,
	Requires: []*analysis.Analyzer{inspect.Analyzer},
	Run:      run,
}

func run(pass *analysis.Pass) (any, error) {
	insp := pass.ResultOf[inspect.Analyzer].(*inspector.Inspector)

	insp.Preorder([]ast.Node{(*ast.FuncDecl)(nil)}, func(n ast.Node) {
		fn := n.(*ast.FuncDecl)
		if !fn.Name.IsExported() {
			return
		}
		if hasAllowDirective(fn.Doc) {
			return
		}
		checkFieldList(pass, fn.Type.Params, "parameter", fn.Name.Name)
		checkFieldList(pass, fn.Type.Results, "result", fn.Name.Name)
	})

	return nil, nil
}

func checkFieldList(pass *analysis.Pass, list *ast.FieldList, role, fnName string) {
	if list == nil {
		return
	}
	for _, field := range list.List {
		if containsEmptyInterface(pass.TypesInfo.TypeOf(field.Type), make(map[types.Type]bool)) {
			pass.Reportf(field.Type.Pos(),
				"exported func %s: %s uses the empty interface (interface{}/any); "+
					"give it a concrete type so the compiler enforces the boundary "+
					"(add //ifaceguard:allow to the doc comment if this generic boundary is deliberate)",
				fnName, role)
		}
	}
}

// Resolve types rather than spelling: named aliases are checked, a locally
// shadowed type named any is not falsely diagnosed, and recursive containers stop.
func containsEmptyInterface(t types.Type, seen map[types.Type]bool) bool {
	if t == nil || seen[t] {
		return false
	}
	seen[t] = true
	t = types.Unalias(t)
	switch value := t.(type) {
	case *types.Named:
		return containsEmptyInterface(value.Underlying(), seen)
	case *types.Interface:
		return value.NumMethods() == 0 && value.IsMethodSet()
	case *types.Pointer:
		return containsEmptyInterface(value.Elem(), seen)
	case *types.Slice:
		return containsEmptyInterface(value.Elem(), seen)
	case *types.Array:
		return containsEmptyInterface(value.Elem(), seen)
	case *types.Map:
		return containsEmptyInterface(value.Key(), seen) || containsEmptyInterface(value.Elem(), seen)
	case *types.Chan:
		return containsEmptyInterface(value.Elem(), seen)
	}
	return false
}

func hasAllowDirective(doc *ast.CommentGroup) bool {
	if doc == nil {
		return false
	}
	for _, c := range doc.List {
		fields := strings.Fields(strings.TrimSpace(c.Text))
		if len(fields) > 0 && fields[0] == allowDirective {
			return true
		}
	}
	return false
}
