"""Tests for Snippet Completion feature."""

from gamess_lsp.server import GAMESS_SNIPPETS


class TestSnippets:
    """Tests for snippet completions."""

    def test_snippet_available(self):
        """Test that snippets are defined."""
        assert len(GAMESS_SNIPPETS) >= 5
        assert "water" in GAMESS_SNIPPETS
        assert "dft-opt" in GAMESS_SNIPPETS
        assert "hf-sp" in GAMESS_SNIPPETS
        assert "mp2" in GAMESS_SNIPPETS
        assert "freq" in GAMESS_SNIPPETS
        assert "tddft" in GAMESS_SNIPPETS

    def test_snippet_structure(self):
        """Test snippet structure."""
        for snippet_id, snippet in GAMESS_SNIPPETS.items():
            assert "label" in snippet
            assert "documentation" in snippet
            assert "insertText" in snippet
            assert snippet["insertText"]  # Non-empty

    def test_water_snippet_content(self):
        """Test water molecule snippet content."""
        snippet = GAMESS_SNIPPETS["water"]
        assert "Water" in snippet["label"]
        assert "B3LYP" in snippet["insertText"]
        assert "$CONTRL" in snippet["insertText"]
        assert "$DATA" in snippet["insertText"]

    def test_dft_opt_snippet_has_placeholders(self):
        """Test DFT optimization snippet has placeholders."""
        snippet = GAMESS_SNIPPETS["dft-opt"]
        # Check for placeholder pattern
        assert "${" in snippet["insertText"]

    def test_mp2_snippet_content(self):
        """Test MP2 snippet content."""
        snippet = GAMESS_SNIPPETS["mp2"]
        assert "MP2" in snippet["documentation"]
        assert "MPLEVL" in snippet["insertText"]

    def test_freq_snippet_content(self):
        """Test frequency calculation snippet content."""
        snippet = GAMESS_SNIPPETS["freq"]
        assert "Frequency" in snippet["label"] or "frequency" in snippet["label"].lower()
        assert "HESSIAN" in snippet["insertText"] or "FORCE" in snippet["insertText"]

    def test_tddft_snippet_content(self):
        """Test TD-DFT snippet content."""
        snippet = GAMESS_SNIPPETS["tddft"]
        assert "TD-DFT" in snippet["label"] or "TD-DFT" in snippet["documentation"]
        assert "$TDDFT" in snippet["insertText"]

    def test_hf_sp_snippet_content(self):
        """Test HF single point snippet content."""
        snippet = GAMESS_SNIPPETS["hf-sp"]
        assert "Hartree" in snippet["label"] or "HF" in snippet["label"]
        assert "RHF" in snippet["insertText"]

    def test_all_snippets_have_valid_labels(self):
        """Test all snippets have non-empty labels."""
        for snippet_id, snippet in GAMESS_SNIPPETS.items():
            assert snippet["label"], f"Snippet {snippet_id} has empty label"

    def test_all_snippets_have_valid_docs(self):
        """Test all snippets have non-empty documentation."""
        for snippet_id, snippet in GAMESS_SNIPPETS.items():
            assert snippet["documentation"], f"Snippet {snippet_id} has empty documentation"
