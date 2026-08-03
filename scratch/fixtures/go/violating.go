package fixtures

import (
	"fmt"
)

// BadSignature returns an empty-interface value — ifaceguard must flag this.
func BadSignature(input string) any {
	return input
}

// ProcessData fails to check error — errcheck must flag this.
func ProcessData(data string) string {
	result, _ := ParseData(data) //nolint:errcheck // deliberate violation for test
	return result
}

// ParseData parses a data string.
func ParseData(data string) (string, error) {
	if data == "" {
		return "", fmt.Errorf("empty data")
	}
	return data, nil
}

// AnotherBadSignature takes an empty-interface parameter — ifaceguard must flag this too.
func AnotherBadSignature(input any) string {
	return fmt.Sprintf("%v", input)
}