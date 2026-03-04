"""Tests for GAMESS LSP document symbols feature."""

from unittest.mock import MagicMock, patch

from lsprotocol.types import (
    DocumentSymbolParams,
    Position,
    Range,
    TextDocumentIdentifier,
)
from lsprotocol.types import SymbolKind

from gamess_lsp.server import document_symbol


class TestDocumentSymbol:
    """Test document symbol feature."""

    @patch("gamess_lsp.server.server")
    def test_document_symbol_groups(self, mock_server):
        """Test document symbols for groups."""
        mock_doc = MagicMock()
        mock_doc.source = """$CONTRL SCFTYP=RHF $END
$SYSTEM MWORDS=10 $END
$BASIS GBASIS=CC-PVDZ $END"""
        mock_doc.lines = mock_doc.source.split("\n")
        mock_server.workspace.get_text_document.return_value = mock_doc

        params = DocumentSymbolParams(
            text_document=TextDocumentIdentifier(uri="file:///test.inp"),
        )

        result = document_symbol(params)
        assert len(result) >= 3  # At least 3 groups

        # Check that groups are present
        group_names = [s.name for s in result]
        assert "$CONTRL" in group_names
        assert "$SYSTEM" in group_names
        assert "$BASIS" in group_names

    @patch("gamess_lsp.server.server")
    def test_document_symbol_keywords(self, mock_server):
        """Test document symbols include keywords."""
        mock_doc = MagicMock()
        mock_doc.source = "$CONTRL SCFTYP=RHF RUNTYP=ENERGY $END"
        mock_doc.lines = [mock_doc.source]
        mock_server.workspace.get_text_document.return_value = mock_doc

        params = DocumentSymbolParams(
            text_document=TextDocumentIdentifier(uri="file:///test.inp"),
        )

        result = document_symbol(params)
        # Should have group + keywords
        assert len(result) >= 3  # $CONTRL, SCFTYP, RUNTYP

    @patch("gamess_lsp.server.server")
    def test_document_symbol_empty_document(self, mock_server):
        """Test document symbols for empty document."""
        mock_doc = MagicMock()
        mock_doc.source = ""
        mock_doc.lines = []
        mock_server.workspace.get_text_document.return_value = mock_doc

        params = DocumentSymbolParams(
            text_document=TextDocumentIdentifier(uri="file:///test.inp"),
        )

        result = document_symbol(params)
        assert len(result) == 0

    @patch("gamess_lsp.server.server")
    def test_document_symbol_symbol_kinds(self, mock_server):
        """Test that symbols have correct kinds."""
        mock_doc = MagicMock()
        mock_doc.source = "$CONTRL SCFTYP=RHF $END"
        mock_doc.lines = [mock_doc.source]
        mock_server.workspace.get_text_document.return_value = mock_doc

        params = DocumentSymbolParams(
            text_document=TextDocumentIdentifier(uri="file:///test.inp"),
        )

        result = document_symbol(params)

        # Find group symbol
        group_symbols = [s for s in result if s.name == "$CONTRL"]
        assert len(group_symbols) == 1
        assert group_symbols[0].kind == SymbolKind.Class

        # Find keyword symbol
        keyword_symbols = [s for s in result if s.name == "SCFTYP"]
        assert len(keyword_symbols) == 1
        assert keyword_symbols[0].kind == SymbolKind.Property

    @patch("gamess_lsp.server.server")
    def test_document_symbol_locations(self, mock_server):
        """Test that symbols have valid locations."""
        mock_doc = MagicMock()
        mock_doc.source = """$CONTRL
SCFTYP=RHF
$END"""
        mock_doc.lines = mock_doc.source.split("\n")
        mock_server.workspace.get_text_document.return_value = mock_doc

        params = DocumentSymbolParams(
            text_document=TextDocumentIdentifier(uri="file:///test.inp"),
        )

        result = document_symbol(params)

        for symbol in result:
            assert symbol.location is not None
            assert symbol.location.range.start.line >= 0
            assert symbol.location.range.end.line >= 0
