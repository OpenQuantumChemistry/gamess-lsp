"""Tests for Workspace Symbol feature."""

from gamess_lsp.parser import GAMESSParser
from lsprotocol.types import SymbolKind


class TestWorkspaceSymbolLogic:
    """Tests for workspace/symbol logic."""

    def test_workspace_symbol_empty_query(self):
        """Test workspace symbol with empty query returns all."""
        content = """! Test file
$CONTRL SCFTYP=RHF RUNTYP=ENERGY $END
$SYSTEM MWORDS=100 $END
$BASIS GBASIS=STO $END
"""
        parser = GAMESSParser()
        parsed = parser.parse(content)

        symbols = []
        for group_name, group in parsed.groups.items():
            symbols.append(("$" + group_name, SymbolKind.Class))
            for keyword_name in group.keywords:
                symbols.append((keyword_name, SymbolKind.Property))

        # Should have 3 groups + their keywords
        assert len(symbols) >= 3

    def test_workspace_symbol_filter(self):
        """Test workspace symbol with query filter."""
        content = """! Test file
$CONTRL SCFTYP=RHF RUNTYP=ENERGY $END
$SYSTEM MWORDS=100 $END
"""
        query = "CONTRL"
        parser = GAMESSParser()
        parsed = parser.parse(content)

        matching_symbols = []
        for group_name, group in parsed.groups.items():
            if query in group_name:
                matching_symbols.append("$" + group_name)

        assert len(matching_symbols) == 1
        assert "$CONTRL" in matching_symbols

    def test_workspace_symbol_no_match(self):
        """Test workspace symbol with no matching query."""
        content = """! Test file
$CONTRL SCFTYP=RHF $END
"""
        query = "NONEXISTENT"
        parser = GAMESSParser()
        parsed = parser.parse(content)

        matching_symbols = []
        for group_name in parsed.groups:
            if query in group_name:
                matching_symbols.append(group_name)

        assert len(matching_symbols) == 0
