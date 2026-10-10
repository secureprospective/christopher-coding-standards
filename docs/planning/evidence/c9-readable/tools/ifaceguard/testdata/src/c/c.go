package c

// Shadowed spelling is a concrete type, not the builtin empty interface.
type any int

func GoodShadow(v any) any { return v }
