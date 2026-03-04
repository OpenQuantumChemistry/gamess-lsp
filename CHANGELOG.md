# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-03-04

### Added
- **Go to Definition** (textDocument/definition): Navigate to group and keyword definitions
- **Find References** (textDocument/references): Find all occurrences of groups and keywords
- **Snippet Completions**: Quick-insert templates for common GAMESS calculations
  - Water molecule template
  - DFT geometry optimization template
  - Hartree-Fock single point template
  - MP2 calculation template
  - Frequency calculation template
  - TD-DFT excited states template
- **Workspace Symbols** (workspace/symbol): Search symbols across all open GAMESS files
- New test suites:
  - `test_definition.py` - Go to definition tests
  - `test_references.py` - Find references tests
  - `test_snippets.py` - Snippet completion tests
  - `test_workspace_symbol.py` - Workspace symbols tests

### Changed
- Updated README.md with new features documentation
- Enhanced completion provider to include snippet suggestions
- Updated test count to 129 tests (100% coverage)

### Fixed
- Fixed escape character issues in snippet templates

## [0.1.0] - 2026-03-02

### Added
- Initial LSP server implementation
- GAMESS input file parser
- Syntax validation with diagnostics
- Auto-completion for groups, keywords, and values
- Hover documentation for keywords and groups
- Document formatting with consistent indentation
- Document symbols for navigation
- Code actions for quick fixes:
  - Add missing \$END for unclosed groups
  - Suggest corrections for unknown groups
  - Add required keywords (e.g., RUNTYP for \$CONTRL)
- Rename support for groups and keywords
- Comprehensive test suite (109 tests, 100% coverage)

### Supported Features
- Core GAMESS groups: CONTRL, SYSTEM, BASIS, DATA, SCF, DFT, etc.
- Keyword and value completion with context awareness
- Real-time diagnostics for syntax errors and warnings
- Document formatting with 2-space indentation

## [0.0.1] - 2026-03-01

### Added
- Initial project structure
- Basic GAMESS parser implementation
- Development and testing setup
