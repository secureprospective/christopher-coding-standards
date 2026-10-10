package boundary_test

import (
	"strings"
	"testing"

	"example.com/consumer/internal/playerid"
	"example.com/consumer/internal/schema"
)

// Explicit synthetic consumer callback; no persistence/authentication supplied.
func TestSyntheticDecoderConstructorEffect(t *testing.T) {
	var effects []playerid.PlayerID
	receive := func(payload string) {
		raw, err := schema.DecodePlayerRecord(strings.NewReader(payload))
		if err != nil {
			return
		}
		if err := raw.Validate(); err != nil {
			return
		}
		id, err := playerid.New(raw.ID)
		if err != nil {
			return
		}
		effects = append(effects, id)
	}
	valid := `{"id":"99","name":"Chris","position":"QB"}`
	for _, bad := range []string{"null", valid + "{}", `{"id":"-99","name":"Chris","position":"QB"}`, `{"id":"99","name":"Chris","position":"QB","salary":"NaN"}`} {
		receive(bad)
	}
	if len(effects) != 0 {
		t.Fatal("C9 effect on invalid input")
	}
	receive(valid)
	if len(effects) != 1 || effects[0].String() != "0099" {
		t.Fatal("C9 canonical valid effect missing")
	}
}
