"""Tests for Go to Definition feature."""

from gamess_lsp.server import _get_word_at_position
from gamess_lsp.parser import GAMESSParser


class TestGetWordAtPosition:
    """Tests for _get_word_at_position helper."""

    def test_get_word_middle(self):
        """Test getting word from middle of line."""
        line = "SCFTYP=RHF DFTTYP=B3LYP"
        assert _get_word_at_position(line, 3) == "SCFTYP"
        assert _get_word_at_position(line, 12) == "DFTTYP"

    def test_get_word_start(self):
        """Test getting word from start of line."""
        line = "CONTRL test"
        assert _get_word_at_position(line, 0) == "CONTRL"

    def test_get_word_empty_line(self):
        """Test with empty line."""
        assert _get_word_at_position("", 0) == ""

    def test_get_word_out_of_range(self):
        """Test with position out of range."""
        line = "test"
        assert _get_word_at_position(line, 100) == ""


class TestDefinitionLogic:
    """Tests for definition logic using parser."""

    def test_definition_finds_group(self):
        """Test that definition can find group location."""
        content = """! Test file
$CONTRL SCFTYP=RHF RUNTYP=ENERGY $END
$BASIS GBASIS=STO $END
"""
        parser = GAMESSParser()
        parsed = parser.parse(content)

        # Should find CONTRL group
        assert "CONTRL" in parsed.groups
        group = parsed.groups["CONTRL"]
        assert group.line_start == 2
        assert group.line_end == 2

    def test_definition_finds_keyword(self):
        """Test that definition can find keyword location."""
        content = """! Test file
$CONTRL SCFTYP=RHF RUNTYP=ENERGY $END
"""
        parser = GAMESSParser()
        parsed = parser.parse(content)

        group = parsed.groups.get("CONTRL")
        assert group is not None
        assert "SCFTYP" in group.keywords
        keyword = group.keywords["SCFTYP"]
        assert keyword.line_number == 2
