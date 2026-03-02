# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-02

### Added
- Initial release of GAMESS-LSP
- **Parser**: Complete GAMESS input file (.inp) parser
  - Support for all standard GAMESS $GROUPS
  - Keyword-value pair parsing with case-insensitive handling
  - Geometry data extraction
  - Inline comment support
  - Diagnostic warnings for unknown groups and unclosed sections
  
- **LSP Features**:
  - `textDocument/completion`: Auto-completion for $ groups and keywords
  - `textDocument/hover`: Hover documentation for groups and keywords
  - `textDocument/diagnostic`: Real-time validation and diagnostics
  - `textDocument/didOpen` and `textDocument/didChange`: Document synchronization
  - `textDocument/formatting`: Document formatting with consistent indentation
  - `textDocument/documentSymbol`: Document symbols for navigation

- **Keywords Database**:
  - Comprehensive GAMESS group documentation
  - Keyword documentation with allowed values
  - Support for CONTRL, SYSTEM, BASIS, SCF, DFT, STATPT, FORCE, and many more groups
  - 40+ documented GAMESS groups
  - 50+ documented keywords with values

- **Testing**:
  - 60 unit tests with 100% pass rate
  - Tests for parser, server, and keywords modules
  - Comprehensive edge case coverage

- **Documentation**:
  - README with installation and usage instructions
  - Editor integration guides (VS Code, Neovim)
  - API documentation in code

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)

## [Unreleased]

### Planned
- Signature help for keywords
- Code actions for quick fixes
- Rename support for keywords
- Workspace symbols support
- Better error recovery in parser
- More comprehensive keyword database
- Support for GAMESS-US specific extensions

[0.1.0]: https://github.com/newtontech/gamess-lsp/releases/tag/v0.1.0
[Unreleased]: https://github.com/newtontech/gamess-lsp/compare/v0.1.0...HEAD
