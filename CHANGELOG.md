# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Code Actions (Quick Fixes)**:
  - `Add missing \$END`: Automatically adds \$END for unclosed groups
  - `Change to \$GROUP`: Suggests similar valid group names for unknown groups
  - `Add RUNTYP=ENERGY`: Adds required RUNTYP keyword to \$CONTRL group
  
- **Rename Support**:
  - Rename group names across the document
  - Rename keywords within their groups
  - Smart word detection at cursor position

- **Enhanced Testing**:
  - Added 8 new tests for code actions and rename functionality
  - Total test count: 75 tests, all passing
  - 100% test coverage maintained

### Changed
- Updated server.py with code action and rename providers

## [0.1.1] - 2026-03-03

### Added
- **Code Quality Improvements**:
  - Added .flake8 configuration file with 100 character line length
  - Configured to work with black formatter settings
  - Extended ignore rules for E203 and W503 (black compatibility)

- **Enhanced Testing**:
  - Improved test coverage configuration
  - All 67 tests passing with comprehensive coverage

### Changed
- Updated code quality workflow documentation

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

[0.1.0]: https://github.com/newtontech/gamess-lsp/releases/tag/v0.1.0
[Unreleased]: https://github.com/newtontech/gamess-lsp/compare/v0.1.0...HEAD
