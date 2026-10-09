package playerid

import (
	"encoding/json"
	"strings"
	"testing"
)

func TestNormalization(t *testing.T) {
	for raw, want := range map[string]string{"99": "0099", "099": "0099", " 0099 ": "0099", "0": "0000", "00000": "0000", "12345": "12345"} {
		id, err := New(raw)
		if err != nil || id.String() != want || id.IsZero() {
			t.Fatalf("New(%q) = %v, %v", raw, id, err)
		}
	}
	for _, raw := range []string{"", " ", "+99", "-99", "９９", "1a", "1 2", strings.Repeat("9", 100)} {
		id, err := New(raw)
		if err == nil || !id.IsZero() {
			t.Fatalf("invalid %q accepted: %v, %v", raw, id, err)
		}
	}
}

func TestJSONAndFailurePreservesReceiver(t *testing.T) {
	id, err := New("99")
	if err != nil {
		t.Fatal(err)
	}
	b, err := json.Marshal(id)
	if err != nil || string(b) != `"0099"` {
		t.Fatalf("marshal %s, %v", b, err)
	}
	var decoded PlayerID
	if err := json.Unmarshal(b, &decoded); err != nil || decoded.String() != "0099" {
		t.Fatalf("decode %v, %v", decoded, err)
	}
	for _, raw := range []string{`"-99"`, `42`, `null`, `""`} {
		if err := json.Unmarshal([]byte(raw), &decoded); err == nil {
			t.Fatalf("accepted %s", raw)
		}
		if decoded.String() != "0099" {
			t.Fatalf("failed decode changed receiver: %v", decoded)
		}
	}
	if _, err := json.Marshal(PlayerID{}); err == nil {
		t.Fatal("zero-value JSON accepted")
	}
}
