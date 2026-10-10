// Package playerid is an example domain identifier, not a universal ID policy.
// It uses nonnegative ASCII decimals fitting the platform int range, normalized
// to at least four digits. Preserve/change those protocol rules deliberately.
// An unexported field prevents direct string conversion but NOT zero values;
// callers still validate at boundaries, and zero-value JSON encoding rejects.
package playerid

import (
	"encoding/json"
	"fmt"
	"strconv"
	"strings"
)

// minWidth is MFL's canonical id width: IDs are left-zero-padded to 4 digits
// ("0099"). Larger IDs (5+ digits) keep their natural width.
const minWidth = 4

// PlayerID is a validated, normalized MFL player identifier. The zero value is
// not a valid id; New never returns it on success (see IsZero).
type PlayerID struct {
	id string
}

// New validates and normalizes a raw MFL id. It rejects empty/non-numeric
// input and collapses every leading-zero variant of the same number to one
// canonical form, so "99", "099", and "0099" all become "0099".
func New(raw string) (PlayerID, error) {
	trimmed := strings.TrimSpace(raw)
	if trimmed == "" {
		return PlayerID{}, fmt.Errorf("playerid: empty id")
	}
	if trimmed[0] < '0' || trimmed[0] > '9' {
		return PlayerID{}, fmt.Errorf("playerid: id must be an unsigned ASCII decimal")
	}
	if _, err := strconv.Atoi(trimmed); err != nil {
		return PlayerID{}, fmt.Errorf("playerid: %q is not numeric: %w", raw, err)
	}

	digits := strings.TrimLeft(trimmed, "0")
	if digits == "" { // input was all zeros, e.g. "0000"
		digits = "0"
	}
	if len(digits) < minWidth {
		digits = strings.Repeat("0", minWidth-len(digits)) + digits
	}
	return PlayerID{id: digits}, nil
}

// String returns the canonical zero-padded id.
func (p PlayerID) String() string { return p.id }

// IsZero reports whether p is the zero value (never produced by a successful New).
func (p PlayerID) IsZero() bool { return p.id == "" }

// MarshalJSON encodes the id as its canonical string form.
func (p PlayerID) MarshalJSON() ([]byte, error) {
	if p.IsZero() {
		return nil, fmt.Errorf("playerid: cannot marshal zero value")
	}
	return json.Marshal(p.id)
}

// UnmarshalJSON decodes a JSON string THROUGH New, so an id arriving over the
// wire cannot smuggle in an unvalidated or unnormalized value.
func (p *PlayerID) UnmarshalJSON(data []byte) error {
	var s string
	if err := json.Unmarshal(data, &s); err != nil {
		return fmt.Errorf("playerid: unmarshal: %w", err)
	}
	id, err := New(s)
	if err != nil {
		return err // already prefixed with "playerid:"
	}
	*p = id
	return nil
}

// Persistence is owner-configured: store canonical String() values and validate
// reads through New. No database driver, I/O or application permission is supplied.
