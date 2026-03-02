"""GAMESS Language Server Protocol implementation."""

import logging
from typing import Any, List, Optional

from lsprotocol.types import (
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionParams,
    Diagnostic,
    DiagnosticSeverity,
    DidChangeTextDocumentParams,
    DidOpenTextDocumentParams,
    Hover,
    HoverParams,
    Position,
    Range,
)
from pygls.server import LanguageServer
from pygls.workspace import Document

from .parser import GAMESSParser
from .keywords import GAMESS_KEYWORDS, GAMESS_GROUPS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = LanguageServer("gamess-lsp", "0.1.0")


# Store document states
document_cache: dict = {}


def _get_diagnostics(content: str) -> List[Diagnostic]:
    """Get diagnostics for GAMESS input content."""
    parser = GAMESSParser()
    parsed = parser.parse(content)
    
    diagnostics = []
    for item in parser.get_diagnostics():
        severity = DiagnosticSeverity.Warning
        if item.get('severity') == 'error':
            severity = DiagnosticSeverity.Error
        
        line = item.get('line', 1) - 1
        diagnostics.append(
            Diagnostic(
                range=Range(
                    start=Position(line=line, character=0),
                    end=Position(line=line, character=100)
                ),
                message=item.get('message', ''),
                severity=severity,
                source="gamess-lsp"
            )
        )
    
    return diagnostics


def _update_document(doc: Document) -> None:
    """Update cached document and publish diagnostics."""
    content = doc.source
    document_cache[doc.uri] = content
    
    diagnostics = _get_diagnostics(content)
    server.publish_diagnostics(doc.uri, diagnostics)


@server.feature("textDocument/didOpen")
def did_open(params: DidOpenTextDocumentParams) -> None:
    """Handle document open."""
    doc = server.workspace.get_text_document(params.text_document.uri)
    _update_document(doc)


@server.feature("textDocument/didChange")
def did_change(params: DidChangeTextDocumentParams) -> None:
    """Handle document change."""
    doc = server.workspace.get_text_document(params.text_document.uri)
    _update_document(doc)


@server.feature("textDocument/completion")
def completion(params: CompletionParams) -> CompletionList:
    """Handle completion requests."""
    doc = server.workspace.get_text_document(params.text_document.uri)
    content = doc.source
    line = doc.lines[params.position.line]
    line_before = line[:params.position.character]
    
    items = []
    
    # Check if completing a group
    if '$' in line_before:
        group_prefix = line_before.split('$')[-1].upper()
        for group_name in GAMESS_GROUPS:
            if group_name.startswith(group_prefix):
                items.append(
                    CompletionItem(
                        label=f"${group_name}",
                        kind=CompletionItemKind.Module,
                        detail="GAMESS group",
                        documentation=GAMESS_GROUPS.get(group_name, "")
                    )
                )
        
        # Check for keywords in current group
        parser = GAMESSParser()
        current_group = parser.get_group_at_position(content, params.position.line + 1)
        
        if current_group and current_group in GAMESS_KEYWORDS:
            for keyword, info in GAMESS_KEYWORDS[current_group].items():
                if keyword.upper().startswith(group_prefix):
                    items.append(
                        CompletionItem(
                            label=keyword,
                            kind=CompletionItemKind.Property,
                            detail=f"{current_group} keyword",
                            documentation=info.get('doc', '')
                        )
                    )
    else:
        # Suggest all groups
        for group_name, doc in GAMESS_GROUPS.items():
            items.append(
                CompletionItem(
                    label=f"${group_name}",
                    kind=CompletionItemKind.Module,
                    detail="GAMESS group",
                    documentation=doc
                )
            )
    
    return CompletionList(is_incomplete=False, items=items)


@server.feature("textDocument/hover")
def hover(params: HoverParams) -> Optional[Hover]:
    """Handle hover requests."""
    doc = server.workspace.get_text_document(params.text_document.uri)
    position = params.position
    
    # Get word at position
    line = doc.lines[position.line]
    word = _get_word_at_position(line, position.character)
    
    if not word:
        return None
    
    word_upper = word.upper()
    
    # Check if it's a group
    if word_upper in GAMESS_GROUPS:
        return Hover(
            contents=GAMESS_GROUPS[word_upper]
        )
    
    # Check if it's a keyword in current group
    parser = GAMESSParser()
    current_group = parser.get_group_at_position(doc.source, position.line + 1)
    
    if current_group and current_group in GAMESS_KEYWORDS:
        if word_upper in GAMESS_KEYWORDS[current_group]:
            info = GAMESS_KEYWORDS[current_group][word_upper]
            return Hover(
                contents=f"**{word}**\n\n{info.get('doc', 'No documentation available')}"
            )
    
    return None


def _get_word_at_position(line: str, character: int) -> str:
    """Get the word at a character position."""
    if not line or character >= len(line):
        return ""
    
    # Find word boundaries
    start = character
    while start > 0 and line[start - 1].isalnum():
        start -= 1
    
    end = character
    while end < len(line) and line[end].isalnum():
        end += 1
    
    return line[start:end]


@server.feature("textDocument/diagnostic")
def diagnostic(params: Any) -> List[Diagnostic]:
    """Handle diagnostic requests."""
    doc = server.workspace.get_text_document(params.text_document.uri)
    return _get_diagnostics(doc.source)


def main() -> None:
    """Main entry point."""
    server.start_io()


if __name__ == "__main__":
    main()
