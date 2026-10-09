package b

type Empty interface{}
type Alias = Empty

func BadNamed(v Empty)  {}             // want "parameter uses the empty interface"
func BadAlias() []Alias { return nil } // want "result uses the empty interface"

type Recursive map[string]Recursive

func GoodRecursive(v Recursive)    {}
func GoodGeneric[T any](v T) T     { return v }
func GoodCallback(v func(any) any) {} // function values outside selected container scope

//ifaceguard:allow deliberate generic boundary
func Allowed(v Alias) Alias { return v }

//ifaceguard:allowed typo is not the directive
func BadTypo(v Alias) {} // want "parameter uses the empty interface"
