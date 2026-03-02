"""GAMESS Language Server Protocol implementation."""

import logging
import re
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
    DocumentFormattingParams,
    DocumentSymbolParams,
    Hover,
    HoverParams,
    Position,
    Range,
    SymbolKind,
    SymbolInformation,
    TextEdit,
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
    
    # Check if we're after an equals sign (value completion)
    if '=' in line_before:
        parts = line_before.rsplit('=', 1)
        if len(parts) == 2:
            keyword_part = parts[0].strip().split()[-1].upper() if parts[0].strip() else ""
            value_prefix = parts[1].strip().upper()
            
            # Find the current group
            parser = GAMESSParser()
            current_group = parser.get_group_at_position(content, params.position.line + 1)
            
            if current_group and current_group in GAMESS_KEYWORDS:
                if keyword_part in GAMESS_KEYWORDS[current_group]:
                    keyword_info = GAMESS_KEYWORDS[current_group][keyword_part]
                    allowed_values = keyword_info.get('values', [])
                    
                    for val in allowed_values:
                        if val.upper().startswith(value_prefix):
                            items.append(
                                CompletionItem(
                                    label=val,
                                    kind=CompletionItemKind.Value,
                                    detail=f"Value for {keyword_part}",
                                    documentation=keyword_info.get('doc', '')
                                )
                            )
            
            if items:
                return CompletionList(is_incomplete=False, items=items)
    
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
        for group_name, doc_text in GAMESS_GROUPS.items():
            items.append(
                CompletionItem(
                    label=f"${group_name}",
                    kind=CompletionItemKind.Module,
                    detail="GAMESS group",
                    documentation=doc_text
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


@server.feature("textDocument/formatting")
def formatting(params: DocumentFormattingParams) -> List[TextEdit]:
    """Handle document formatting requests.
    
    Formats GAMESS input files with:
    - Consistent indentation for group contents
    - Standardized spacing around keywords
    - $END on its own line
    """
    doc = server.workspace.get_text_document(params.text_document.uri)
    content = doc.source
    lines = content.split('\n')
    
    formatted_lines = []
    in_group = False
    indent = "  "  # 2-space indentation
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            formatted_lines.append("")
            continue
        
        # Handle comments
        if stripped.startswith('!'):
            formatted_lines.append(stripped)
            continue
        
        # Check for group start
        if stripped.startswith('$') and not re.match(r'^\$END\b', stripped, re.IGNORECASE):
            # Extract group name and any keywords on the same line
            match = re.match(r'^\$([A-Za-z_][A-Za-z0-9_]*)\s*(.*)', stripped)
            if match:
                group_name = match.group(1).upper()
                rest = match.group(2).strip()
                
                if rest and not rest.startswith('$'):
                    # Keywords on same line - format them
                    formatted_lines.append(f"${group_name}")
                    in_group = True
                    # Format the keywords
                    keywords = _format_keywords(rest)
                    formatted_lines.append(f"{indent}{keywords}")
                else:
                    formatted_lines.append(f"${group_name}")
                    in_group = True
                    
                    # Check if $END is on the same line
                    if rest.upper().startswith('$END'):
                        in_group = False
                        formatted_lines.append("$END")
        # Check for $END
        elif re.match(r'^\$END\b', stripped, re.IGNORECASE):
            in_group = False
            formatted_lines.append("$END")
        # Regular content line
        elif in_group:
            # Format keywords if they contain =
            if '=' in stripped and not stripped.startswith('!'):
                formatted_keywords = _format_keywords(stripped)
                formatted_lines.append(f"{indent}{formatted_keywords}")
            else:
                formatted_lines.append(f"{indent}{stripped}")
        else:
            formatted_lines.append(stripped)
    
    # Create TextEdit for the entire document
    return [
        TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=len(lines), character=0)
            ),
            new_text='\n'.join(formatted_lines)
        )
    ]


def _format_keywords(line: str) -> str:
    """Format a line of keyword=value pairs."""
    # Split by spaces but preserve quoted values
    tokens = []
    current = ""
    in_quotes = False
    quote_char = None
    
    for char in line:
        if char in '"\'':
            if not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char:
                in_quotes = False
                quote_char = None
            current += char
        elif char == ' ' and not in_quotes:
            if current:
                tokens.append(current)
                current = ""
        else:
            current += char
    
    if current:
        tokens.append(current)
    
    # Format each token
    formatted_tokens = []
    for token in tokens:
        if '=' in token:
            key, value = token.split('=', 1)
            formatted_tokens.append(f"{key.strip()}={value.strip()}")
        else:
            formatted_tokens.append(token.strip())
    
    return ' '.join(formatted_tokens)


@server.feature("textDocument/documentSymbol")
def document_symbol(params: DocumentSymbolParams) -> List[SymbolInformation]:
    """Handle document symbol requests.
    
    Returns all $GROUP sections as symbols for navigation.
    """
    doc = server.workspace.get_text_document(params.text_document.uri)
    content = doc.source
    lines = content.split('\n')
    
    symbols = []
    
    parser = GAMESSParser()
    parsed = parser.parse(content)
    
    for group_name, group in parsed.groups.items():
        # Create symbol for each group
        symbol = SymbolInformation(
            name=f"${group_name}",
            kind=SymbolKind.Class,
            location={
                'uri': params.text_document.uri,
                'range': Range(
                    start=Position(line=group.line_start - 1, character=0),
                    end=Position(line=group.line_end - 1, character=0)
                )
            }
        )
        symbols.append(symbol)
        
        # Create symbols for each keyword in the group
        for keyword_name, keyword in group.keywords.items():
            kw_symbol = SymbolInformation(
                name=keyword_name,
                kind=SymbolKind.Property,
                location={
                    'uri': params.text_document.uri,
                    'range': Range(
                        start=Position(line=keyword.line_number - 1, character=0),
                        end=Position(line=keyword.line_number - 1, character=100)
                    )
                },
                container_name=f"${group_name}"
            )
            symbols.append(kw_symbol)
    
    return symbols


def main() -> None:
    """Main entry point."""
    server.start_io()


if __name__ == "__main__":
    main()
