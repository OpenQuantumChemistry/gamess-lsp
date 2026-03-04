"""Additional tests for GAMESS parser edge cases."""

from gamess_lsp.parser import GAMESSParser, parse_gamess_input


class TestParserEdgeCases:
    """Test edge cases in GAMESS parser."""

    def test_parse_only_whitespace(self):
        """Test parsing content with only whitespace."""
        parser = GAMESSParser()
        result = parser.parse("   \n   \n   ")
        assert result.groups == {}

    def test_parse_multiple_ends(self):
        """Test parsing with multiple $END statements."""
        content = """$CONTRL SCFTYP=RHF $END
$END
$SYSTEM MWORDS=10 $END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        assert "CONTRL" in result.groups
        assert "SYSTEM" in result.groups

    def test_parse_group_on_same_line_as_end(self):
        """Test parsing group start and end on same line."""
        content = "$CONTRL SCFTYP=RHF $END"
        parser = GAMESSParser()
        result = parser.parse(content)
        assert "CONTRL" in result.groups

    def test_parse_empty_group(self):
        """Test parsing empty group."""
        content = """$CONTRL
$END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        assert "CONTRL" in result.groups
        assert len(result.groups["CONTRL"].keywords) == 0

    def test_parse_keyword_without_value(self):
        """Test parsing keyword without value."""
        content = """$CONTRL
NOSYM
$END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        # Keywords without = should be handled gracefully
        assert "CONTRL" in result.groups

    def test_parse_special_characters_in_values(self):
        """Test parsing values with special characters."""
        content = """$CONTRL ICHARG=-1 $END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        assert result.groups["CONTRL"].get_keyword("ICHARG").value == "-1"

    def test_parse_decimal_values(self):
        """Test parsing decimal values."""
        content = """$CONTRL
MAXIT=100
OPTTOL=0.0001
$END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        assert result.groups["CONTRL"].get_keyword("MAXIT").value == "100"
        assert result.groups["CONTRL"].get_keyword("OPTTOL").value == "0.0001"

    def test_parse_exponential_notation(self):
        """Test parsing exponential notation in values."""
        content = """$CONTRL
CONV=1.0E-05
$END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        assert result.groups["CONTRL"].get_keyword("CONV").value == "1.0E-05"

    def test_parse_geometry_with_comments(self):
        """Test parsing geometry with inline comments."""
        content = """$DATA
Water molecule
C1
H 0.0 0.0 0.0 ! Hydrogen atom
O 1.0 0.0 0.0 ! Oxygen atom
$END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        # Comments should be stripped
        assert len(result.geometry) == 2

    def test_parse_case_insensitive_groups(self):
        """Test that group names are case-insensitive."""
        content = """$contrl scftyp=rhf $end"""
        parser = GAMESSParser()
        result = parser.parse(content)
        assert "CONTRL" in result.groups

    def test_parse_mixed_keywords_case(self):
        """Test that keywords are case-insensitive."""
        content = """$CONTRL ScfTyp=RHF $END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        # Should be accessible as uppercase
        assert result.groups["CONTRL"].get_keyword("SCFTYP") is not None
        assert result.groups["CONTRL"].get_keyword("scftyp") is not None

    def test_parser_error_handling(self):
        """Test parser error handling for invalid input."""
        parser = GAMESSParser()
        # Should not crash on invalid input
        result = parser.parse("$$$")
        assert result is not None

    def test_parse_geometry_invalid_coordinates(self):
        """Test parsing geometry with invalid coordinates."""
        content = """$DATA
Test
C1
H abc def ghi
$END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        # Should handle invalid coordinates gracefully
        assert len(result.geometry) == 0

    def test_get_group_at_position_empty_document(self):
        """Test get_group_at_position with empty document."""
        parser = GAMESSParser()
        result = parser.get_group_at_position("", 1)
        assert result is None

    def test_get_group_at_position_before_any_group(self):
        """Test get_group_at_position before any group starts."""
        content = """! Comment
$CONTRL SCFTYP=RHF $END"""
        parser = GAMESSParser()
        result = parser.get_group_at_position(content, 1)
        assert result is None

    def test_get_group_at_position_inside_group(self):
        """Test get_group_at_position inside a group."""
        content = """$CONTRL
SCFTYP=RHF
$END"""
        parser = GAMESSParser()
        result = parser.get_group_at_position(content, 2)
        # Line 2 is inside $CONTRL group
        assert result == "CONTRL"


class TestParserWarnings:
    """Test parser warning generation."""

    def test_warning_unknown_group(self):
        """Test warning for unknown group."""
        parser = GAMESSParser()
        parser.parse("$UNKNOWN $END")
        assert any("Unknown group" in w["message"] for w in parser.warnings)

    def test_warning_unclosed_group(self):
        """Test warning for unclosed group."""
        parser = GAMESSParser()
        parser.parse("$CONTRL SCFTYP=RHF")
        assert any("not properly closed" in w["message"] for w in parser.warnings)

    def test_get_diagnostics_includes_all(self):
        """Test that get_diagnostics returns all issues."""
        parser = GAMESSParser()
        parser.parse("$UNKNOWN")  # Unknown + unclosed
        diagnostics = parser.get_diagnostics()
        assert len(diagnostics) >= 1


class TestConvenienceFunction:
    """Test parse_gamess_input convenience function."""

    def test_convenience_function_simple(self):
        """Test convenience function with simple input."""
        result = parse_gamess_input("$CONTRL SCFTYP=RHF $END")
        assert "CONTRL" in result.groups

    def test_convenience_function_empty(self):
        """Test convenience function with empty input."""
        result = parse_gamess_input("")
        assert result.groups == {}
