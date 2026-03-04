"""Tests for GAMESS LSP document symbols feature."""

from unittest.mock import MagicMock, patch

from lsprotocol.types import (
    DocumentSymbolParams,
    Range,
    TextDocumentIdentifier,
)
