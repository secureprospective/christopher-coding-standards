package schema

import (
	"strings"
	"testing"
)

func TestExactObjectDecoding(t *testing.T) {
	valid := `{"id":"99","name":"Chris","position":"QB","salary":"1.5","new_provider_field":true}`
	rec, err := DecodePlayerRecord(strings.NewReader(valid + " \n"))
	if err != nil {
		t.Fatal(err)
	}
	if rec.ID != "99" || rec.Salary != "1.5" {
		t.Fatalf("changed raw fields: %+v", rec)
	}
	if err := rec.Validate(); err != nil {
		t.Fatal(err)
	}
	for _, raw := range []string{"", "null", "[]", "42", `"text"`, "{", valid + "{}", valid + "null", valid + "garbage"} {
		if _, err := DecodePlayerRecord(strings.NewReader(raw)); err == nil {
			t.Fatalf("accepted invalid/trailing %q", raw)
		}
	}
}

func TestShapeAndFiniteNumbers(t *testing.T) {
	valid := RawPlayerRecord{ID: "99", Name: "Chris", Position: "QB", Salary: ""}
	for _, salary := range []string{"", " ", "1.5", "-1", "1e3"} {
		r := valid
		r.Salary = salary
		if err := r.Validate(); err != nil {
			t.Fatalf("valid salary %q: %v", salary, err)
		}
	}
	invalid := []RawPlayerRecord{
		{ID: "", Name: "Chris", Position: "QB"}, {ID: "+99", Name: "Chris", Position: "QB"},
		{ID: "-99", Name: "Chris", Position: "QB"}, {ID: "x", Name: "Chris", Position: "QB"},
		{ID: "99", Name: " ", Position: "QB"}, {ID: "99", Name: "Chris", Position: " "},
		{ID: "99", Name: "Chris", Position: "QB", Salary: "bad"}, {ID: "99", Name: "Chris", Position: "QB", Salary: "NaN"},
		{ID: "99", Name: "Chris", Position: "QB", Salary: "Inf"}, {ID: "99", Name: "Chris", Position: "QB", Salary: "1e999"},
	}
	for _, r := range invalid {
		if err := r.Validate(); err == nil {
			t.Fatalf("accepted %+v", r)
		}
	}
}

func TestSyntheticBoundaryCallerRejectsBeforeEffect(t *testing.T) {
	var accepted []RawPlayerRecord
	receive := func(raw string) {
		rec, err := DecodePlayerRecord(strings.NewReader(raw))
		if err != nil {
			return
		}
		if err := rec.Validate(); err != nil {
			return
		}
		accepted = append(accepted, rec)
	}
	valid := `{"id":"99","name":"Chris","position":"QB"}`
	for _, raw := range []string{valid + "{}", "null", `{"id":"-99","name":"Chris","position":"QB"}`} {
		receive(raw)
	}
	if len(accepted) != 0 {
		t.Fatalf("effect after rejection: %+v", accepted)
	}
	receive(valid)
	if len(accepted) != 1 || accepted[0].ID != "99" {
		t.Fatalf("valid effect missing: %+v", accepted)
	}
}
