# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-02

### Added
- Initial GAMESS input file parser with support for:
  - Multiple $ groups (CONTRL, SYSTEM, BASIS, SCF, DFT, STATPT, FORCE, etc.)
  - Keyword-value pair parsing
  - Case-insensitive group and keyword matching
  - Geometry data extraction
  - Unknown group warnings
  - Unclosed group detection

- LSP server implementation:
  - `textDocument/didOpen` - Document open handling
  - `textDocument/didChange` - Document change handling
  - `textDocument/completion` - Auto-completion for groups and keywords
  - `textDocument/hover` - Hover documentation for groups and keywords
  - `textDocument/diagnostic` - Real-time diagnostics

- Keywords database with documentation:
  - CONTRL keywords (RUNTYP, SCFTYP, DFTTYP, MPLEVL, CCTYP, etc.)
  - SYSTEM keywords (MWORDS, MEMDDI, TIMLIM)
  - BASIS keywords (GBASIS, NGAUSS, NDFUNC, etc.)
  - SCF keywords (DIRSCF, DIIS, SOSCF, CONV)
  - DFT keywords (METHOD, NRAD, NLEB)
  - STATPT keywords (METHOD, OPTTOL, NSTEP)
  - FORCE keywords (VIBANL, TEMP, PRES)

- Comprehensive test suite (60 tests):
  - Parser tests
  - Server tests
  - Keywords database tests

- Development tooling:
  - pytest with coverage
  - black, isort, flake8, mypy
  - pre-commit hooks
  - CI/CD via GitHub Actions

### Changed
- Improved parser to handle $END correctly
- Fixed case-insensitive group matching

### Fixed
- Parser now correctly handles inline $END
- Diagnostics properly report warnings and errors
