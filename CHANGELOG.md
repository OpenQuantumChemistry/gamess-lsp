# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Enhanced Testing Suite**:
  - Added 34 new tests for comprehensive coverage (109 total tests)
  - New test files: test_formatting.py, test_document_symbol.py, test_parser_edge_cases.py
  - Tests for document formatting feature
  - Tests for document symbols navigation
  - Tests for parser edge cases and error handling

- **Test Coverage Improvements**:
  - Edge case handling for empty documents
  - Parser error recovery tests
  - Warning generation tests
  - Convenience function tests

### Changed
- Updated pyproject.toml coverage configuration for proper source path
- Improved test organization with dedicated test modules

### Fixed
- Fixed test parameter requirements for DocumentFormattingParams
- Corrected test assertions for parser behavior

## [0.1.1] - 2026-03-03

### Added
- **Code Actions (Quick Fixes)**:
  - `Add missing $END`: Automatically adds $END for unclosed groups
  - `Change to $GROUP`: Suggests similar valid group names for unknown groups
  - `Add RUNTYP=ENERGY`: Adds required RUNTYP keyword to $CONTRL group
  
- **Rename Support**:
  - Rename group names across the document
  - Rename keywords within their groups
  - Smart word detection at cursor position

- **Code Quality Improvements**:
  - Added .flake8 configuration file with 100 character line length
  - Configured to work with black formatter settings

### Fixed
- **Type Safety**: Resolved MyPy type error in codeAction handler
  - Fixed WorkspaceEdit document_changes to use proper LSP types
  - Added proper imports for TextDocumentEdit and OptionalVersionedTextDocumentIdentifier

## [0.1.0] - 2026-03-02

### Added
- Initial release of GAMESS-LSP
- **Parser**: Complete GAMESS input file (.inp) parser
  - Support for all standard GAMESS GROUPS
  - Keyword-value pair parsing with case-insensitive handling
  - Geometry data extraction
  - Inline comment support
  - Diagnostic warnings for unknown groups and unclosed sections
  
- **LSP Features**:
  - textDocument/completion: Auto-completion for groups and keywords
  - textDocument/hover: Hover documentation for groups and keywords
  - textDocument/diagnostic: Real-time validation and diagnostics
  - textDocument/didOpen and textDocument/didChange: Document synchronization
  - textDocument/formatting: Document formatting with consistent indentation
  - textDocument/documentSymbol: Document symbols for navigation

- **Keywords Database**:
  - Comprehensive GAMESS group documentation
  - Keyword documentation with allowed values
  - Support for CONTRL, SYSTEM, BASIS, SCF, DFT, STATPT, FORCE, and many more groups
  - 40+ documented GAMESS groups
  - 50+ documented keywords with values

- **Testing**:
  - 75 unit tests with 100% pass rate
  - Tests for parser, server, and keywords modules
  - Comprehensive edge case coverage

- **Documentation**:
  - README with installation and usage instructions
  - Editor integration guides (VS Code, Neovim)
  - API documentation in code

[0.1.0]: https://github.com/newtontech/gamess-lsp/releases/tag/v0.1.0
[Unreleased]: https://github.com/newtontech/gamess-lsp/compare/v0.1.1...HEAD
