"""Tests for GAMESS parser."""

import pytest
from gamess_lsp.parser import (
    GAMESSParser,
    GAMESSGroup,
    GAMESSKeyword,
    GAMESSInputFile,
    parse_gamess_input,
)


class TestGAMESSKeyword:
    """Test GAMESSKeyword dataclass."""

    def test_keyword_creation(self):
        """Test keyword creation."""
        kw = GAMESSKeyword(name="SCFTYP", value="RHF", line_number=5)
        assert kw.name == "SCFTYP"
        assert kw.value == "RHF"
        assert kw.line_number == 5


class TestGAMESSGroup:
    """Test GAMESSGroup dataclass."""

    def test_group_creation(self):
        """Test group creation."""
        group = GAMESSGroup(name="CONTRL", line_start=10)
        assert group.name == "CONTRL"
        assert group.line_start == 10
        assert group.keywords == {}

    def test_add_keyword(self):
        """Test adding keyword to group."""
        group = GAMESSGroup(name="CONTRL")
        kw = GAMESSKeyword(name="SCFTYP", value="RHF", line_number=5)
        group.add_keyword(kw)
        
        assert "SCFTYP" in group.keywords
        assert group.get_keyword("SCFTYP").value == "RHF"

    def test_get_keyword_case_insensitive(self):
        """Test case-insensitive keyword lookup."""
        group = GAMESSGroup(name="CONTRL")
        kw = GAMESSKeyword(name="ScfTyp", value="RHF", line_number=5)
        group.add_keyword(kw)
        
        assert group.get_keyword("SCFTYP") is not None
        assert group.get_keyword("scftyp") is not None
    
    def test_get_keyword_not_found(self):
        """Test getting non-existent keyword."""
        group = GAMESSGroup(name="CONTRL")
        assert group.get_keyword("NONEXISTENT") is None


class TestGAMESSInputFile:
    """Test GAMESSInputFile dataclass."""

    def test_input_file_creation(self):
        """Test input file creation."""
        inp = GAMESSInputFile()
        assert inp.groups == {}
        assert inp.title == ""
        assert inp.geometry == []

    def test_add_and_get_group(self):
        """Test adding and getting groups."""
        inp = GAMESSInputFile()
        group = GAMESSGroup(name="CONTRL")
        inp.add_group(group)
        
        assert inp.get_group("CONTRL") is not None
        assert inp.get_group("contrl") is not None
    
    def test_get_group_not_found(self):
        """Test getting non-existent group."""
        inp = GAMESSInputFile()
        assert inp.get_group("NONEXISTENT") is None


class TestGAMESSParser:
    """Test GAMESS parser."""

    def test_parser_creation(self):
        """Test parser creation."""
        parser = GAMESSParser()
        assert parser.errors == []
        assert parser.warnings == []

    def test_parse_empty_content(self):
        """Test parsing empty content."""
        parser = GAMESSParser()
        result = parser.parse("")
        assert isinstance(result, GAMESSInputFile)
        assert result.groups == {}

    def test_parse_simple_group(self):
        """Test parsing simple group."""
        content = """$CONTRL SCFTYP=RHF RUNTYP=ENERGY $END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        
        assert "CONTRL" in result.groups
        group = result.groups["CONTRL"]
        assert group.get_keyword("SCFTYP").value == "RHF"
        assert group.get_keyword("RUNTYP").value == "ENERGY"

    def test_parse_multiline_group(self):
        """Test parsing multiline group."""
        content = """$CONTRL
  SCFTYP=RHF
  RUNTYP=ENERGY
$END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        
        assert "CONTRL" in result.groups
        group = result.groups["CONTRL"]
        assert group.get_keyword("SCFTYP").value == "RHF"
        assert group.get_keyword("RUNTYP").value == "ENERGY"

    def test_parse_multiple_groups(self):
        """Test parsing multiple groups."""
        content = """$CONTRL SCFTYP=RHF $END
$SYSTEM MWORDS=10 $END
$BASIS GBASIS=CC-PVDZ $END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        
        assert "CONTRL" in result.groups
        assert "SYSTEM" in result.groups
        assert "BASIS" in result.groups

    def test_parse_group_without_end(self):
        """Test parsing group without $END."""
        content = """$CONTRL SCFTYP=RHF"""
        parser = GAMESSParser()
        result = parser.parse(content)
        
        assert "CONTRL" in result.groups
        assert len(parser.warnings) == 1
        assert "not properly closed" in parser.warnings[0]["message"]

    def test_parse_unknown_group(self):
        """Test parsing unknown group generates warning."""
        content = """$UNKNOWN KEYWORD=VALUE $END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        
        assert "UNKNOWN" in result.groups
        # Should have 2 warnings: unknown group + not properly closed (since $END is after)
        assert len(parser.warnings) >= 1
        assert any("Unknown group" in w["message"] for w in parser.warnings)

    def test_parse_comments(self):
        """Test parsing with comments."""
        content = """! This is a comment
$CONTRL SCFTYP=RHF $END
! Another comment"""
        parser = GAMESSParser()
        result = parser.parse(content)
        
        assert "CONTRL" in result.groups

    def test_parse_quoted_values(self):
        """Test parsing quoted values."""
        content = """$CONTRL EXETYP="CHECK" $END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        
        assert result.groups["CONTRL"].get_keyword("EXETYP").value == "CHECK"

    def test_parse_geometry(self):
        """Test parsing geometry data."""
        content = """$DATA
Test molecule
C1
H 0.0 0.0 0.0
O 1.0 0.0 0.0
$END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        
        assert len(result.geometry) == 2
        assert result.geometry[0]["symbol"] == "H"
        assert result.geometry[0]["x"] == 0.0

    def test_get_group_at_position(self):
        """Test getting group at line position."""
        content = """Line 1
$CONTRL
  SCFTYP=RHF
$END
Line 5"""
        parser = GAMESSParser()
        parser.parse(content)
        
        assert parser.get_group_at_position(content, 2) == "CONTRL"
        assert parser.get_group_at_position(content, 3) == "CONTRL"
        assert parser.get_group_at_position(content, 5) is None

    def test_get_diagnostics(self):
        """Test getting diagnostics."""
        content = """$UNKNOWN $END"""
        parser = GAMESSParser()
        parser.parse(content)
        
        diagnostics = parser.get_diagnostics()
        assert len(diagnostics) >= 1
        assert diagnostics[0]["severity"] == "warning"

    def test_parse_empty_lines(self):
        """Test parsing with empty lines."""
        content = """
$CONTRL SCFTYP=RHF $END

"""
        parser = GAMESSParser()
        result = parser.parse(content)
        
        assert "CONTRL" in result.groups

    def test_parse_mixed_case_group(self):
        """Test parsing mixed case group names."""
        content = """$Contrl ScfTyp=RHF $end"""
        parser = GAMESSParser()
        result = parser.parse(content)
        
        assert "CONTRL" in result.groups
        assert result.groups["CONTRL"].get_keyword("SCFTYP").value == "RHF"

    def test_parse_complex_input(self):
        """Test parsing complex GAMESS input."""
        content = """! Water molecule calculation
 $CONTRL SCFTYP=RHF RUNTYP=ENERGY $END
 $SYSTEM MWORDS=10 $END
 $BASIS GBASIS=CC-PVDZ $END
 $DATA
Water
Cnv 2

H  0.0  0.757  0.586
O  0.0  0.0    0.0
 $END"""
        parser = GAMESSParser()
        result = parser.parse(content)
        
        assert "CONTRL" in result.groups
        assert "SYSTEM" in result.groups
        assert "BASIS" in result.groups
        assert len(result.geometry) == 2


class TestParseGamessInput:
    """Test parse_gamess_input convenience function."""

    def test_convenience_function(self):
        """Test convenience function."""
        content = """$CONTRL SCFTYP=RHF $END"""
        result = parse_gamess_input(content)
        
        assert isinstance(result, GAMESSInputFile)
        assert "CONTRL" in result.groups
