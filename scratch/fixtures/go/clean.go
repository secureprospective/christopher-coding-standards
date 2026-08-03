package fixtures

import (
	"fmt"
)

// PlayerID wraps a player identifier string with compile-time safety.
type PlayerID struct {
	id string
}

// NewPlayerID validates and constructs a PlayerID.
func NewPlayerID(raw string) (PlayerID, error) {
	if len(raw) != 4 {
		return PlayerID{}, fmt.Errorf("player ID must be 4 characters, got %d", len(raw))
	}
	return PlayerID{id: raw}, nil
}

// String returns the player identifier.
func (p PlayerID) String() string {
	return p.id
}

// Validate checks that the player ID is properly formatted.
func (p PlayerID) Validate() error {
	if len(p.id) != 4 {
		return fmt.Errorf("invalid player ID length")
	}
	return nil
}

// GetName returns a player's name from an ID.
func GetName(id PlayerID) string {
	return "player-" + id.String()
}