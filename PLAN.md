# Development Plan for gamess-lsp

## Overview
This is the development plan for gamess-lsp.

## Phase 1: Foundation (Week 1) ✅ COMPLETED
- [x] Setup project structure
- [x] Basic parser implementation
- [x] Initial test suite

## Phase 2: Core Features (Week 2) ✅ COMPLETED
- [x] LSP server implementation
- [x] Diagnostics support
- [x] Completion provider

## Phase 3: Advanced Features (Week 3) ✅ COMPLETED
- [x] Hover documentation
- [x] Code formatting
- [x] Quick fixes (completed)

## Phase 4: Refinement (Week 4) ✅ COMPLETED
- [x] Code Actions (Quick Fixes)
  - [x] Add missing \$END for unclosed groups
  - [x] Suggest corrections for unknown groups
  - [x] Add required keywords (RUNTYP for \$CONTRL)
- [x] Rename Support
  - [x] Rename group names
  - [x] Rename keywords
- [x] Document Symbols
  - [x] Navigation for groups
  - [x] Navigation for keywords
- [x] Enhanced Testing (109 tests, 100% coverage)
  - [x] test_formatting.py - Formatting tests
  - [x] test_document_symbol.py - Symbol navigation tests
  - [x] test_code_actions.py - Code action tests
  - [x] test_parser_edge_cases.py - Edge case tests

## Phase 5: Enhanced Navigation (March 2026) ✅ COMPLETED
- [x] Go to Definition (textDocument/definition)
  - [x] Navigate to group definitions
  - [x] Navigate to keyword definitions
- [x] Find References (textDocument/references)
  - [x] Find all group occurrences
  - [x] Find all keyword occurrences
- [x] Snippet Completions
  - [x] Water molecule template
  - [x] DFT optimization template
  - [x] HF single point template
  - [x] MP2 calculation template
  - [x] Frequency calculation template
  - [x] TD-DFT calculation template
- [x] Workspace Symbols (workspace/symbol)
  - [x] Search symbols across all open documents
  - [x] Filter by query string
- [x] Enhanced Testing (129 tests, 100% coverage)
  - [x] test_definition.py - Go to definition tests
  - [x] test_references.py - Find references tests
  - [x] test_snippets.py - Snippet completion tests
  - [x] test_workspace_symbol.py - Workspace symbols tests

## Testing
- Run tests: `pytest tests/`
- Check coverage: `pytest --cov`
- Current status: **161 tests, 100% coverage** ✅

## Maintenance
- Nightly automated maintenance at random time
- See .maintenance/last-run.md for last check

## Future Enhancements
- [ ] Semantic highlighting
- [ ] Multi-file support
- [ ] Configuration file support
- [x] More snippet templates (TS search, IRC, CCSD(T), PCM)
