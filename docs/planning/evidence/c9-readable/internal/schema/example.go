// Package schema demonstrates external shape checks before domain/effect work.
// This example tolerates unknown provider fields; owned request schemas may choose
// stricter policy. Neither hand-written validation nor parsing grants permission.
package schema

import (
	"encoding/json"
	"fmt"
	"io"
	"math"
	"strconv"
	"strings"
)

// RawPlayerRecord is the shape of one player record as it arrives from the
// MFL `players` endpoint. Every field is a string — MFL's JSON encodes
// numbers as strings (companion plan Section 5: "salary and cap fields
// arrive as strings — parse them, don't assume float").
type RawPlayerRecord struct {
	ID       string `json:"id"`
	Name     string `json:"name"`
	Position string `json:"position"`
	Salary   string `json:"salary"`
}

// DecodePlayerRecord reads one non-null JSON object and rejects trailing values
// or invalid suffixes. Unknown fields are intentionally tolerated in this example.
// Callers set reader/resource limits and validate/normalize before effects.
func DecodePlayerRecord(r io.Reader) (RawPlayerRecord, error) {
	dec := json.NewDecoder(r)
	var rec *RawPlayerRecord
	if err := dec.Decode(&rec); err != nil {
		return RawPlayerRecord{}, fmt.Errorf("schema: decode player record: %w", err)
	}
	if rec == nil {
		return RawPlayerRecord{}, fmt.Errorf("schema: null player record")
	}
	var extra json.RawMessage
	if err := dec.Decode(&extra); err != io.EOF {
		if err != nil {
			return RawPlayerRecord{}, fmt.Errorf("schema: trailing JSON: %w", err)
		}
		return RawPlayerRecord{}, fmt.Errorf("schema: multiple JSON values")
	}
	return *rec, nil
}

// Validate checks the raw record's shape before any normalization runs.
// It does NOT convert types (that's normalize's job, companion plan WF 1C)
// — it only rejects records that cannot possibly be valid.
func (r RawPlayerRecord) Validate() error {
	if strings.TrimSpace(r.ID) == "" {
		return fmt.Errorf("schema: player record missing id")
	}
	id := strings.TrimSpace(r.ID)
	if id[0] < '0' || id[0] > '9' {
		return fmt.Errorf("schema: player id must be an unsigned ASCII decimal")
	}
	if _, err := strconv.Atoi(id); err != nil {
		return fmt.Errorf("schema: player id %q is not numeric: %w", r.ID, err)
	}
	if strings.TrimSpace(r.Name) == "" {
		return fmt.Errorf("schema: player record %q missing name", r.ID)
	}
	if strings.TrimSpace(r.Position) == "" {
		return fmt.Errorf("schema: player record %q missing position", r.ID)
	}
	// Salary is validated as a parseable number here, but kept as a string —
	// normalize.Roster (WF 1C) does the float conversion. Validation and
	// transformation are different jobs (Section 2, item 1: fetchers
	// transform nothing).
	if strings.TrimSpace(r.Salary) != "" {
		salary, err := strconv.ParseFloat(strings.TrimSpace(r.Salary), 64)
		if err != nil {
			return fmt.Errorf("schema: player record %q has non-numeric salary %q: %w", r.ID, r.Salary, err)
		}
		if math.IsNaN(salary) || math.IsInf(salary, 0) {
			return fmt.Errorf("schema: salary must be finite")
		}
	}
	return nil
}
