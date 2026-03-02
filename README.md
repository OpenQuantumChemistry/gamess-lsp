# GAMESS-LSP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Language Server Protocol implementation for GAMESS (US) input files (.inp).

## Features

- **Syntax Validation**: Real-time validation of GAMESS input files with warnings for unknown groups and unclosed sections
- **Auto-completion**: Intelligent completion for $ groups and keywords, including value suggestions after `=`
- **Hover Documentation**: Inline documentation for GAMESS keywords and groups
- **Diagnostics**: Warnings for unknown groups, unclosed sections, and syntax issues
- **Document Formatting**: Automatic formatting with consistent indentation
- **Document Symbols**: Navigation support for $ groups and keywords

## Installation

```bash
pip install gamess-lsp
```

### From Source

```bash
git clone https://github.com/newtontech/gamess-lsp.git
cd gamess-lsp
pip install -e ".[dev]"
```

## Usage

### Command Line

```bash
gamess-lsp
```

The server communicates via stdio using the LSP protocol.

### Editor Integration

#### VS Code

Add to your `settings.json`:

```json
{
  "languageserver": {
    "gamess": {
      "command": "gamess-lsp",
      "filetypes": ["gamess"],
      "rootPatterns": ["*.inp"]
    }
  }
}
```

Or use with a VS Code extension that supports LSP.

#### Neovim (nvim-lspconfig)

```lua
local lspconfig = require('lspconfig')
lspconfig.gamess.setup {
  cmd = {"gamess-lsp"},
  filetypes = {"gamess"},
  root_dir = lspconfig.util.root_pattern("*.inp"),
}
```

#### Emacs (lsp-mode)

```elisp
(lsp-register-client
 (make-lsp-client :new-connection (lsp-stdio-connection "gamess-lsp")
                  :major-modes '(gamess-mode)
                  :server-id 'gamess-lsp))
```

## Example GAMESS Input File

```gamess
! Water molecule DFT calculation
 $CONTRL SCFTYP=RHF DFTTYP=B3LYP RUNTYP=OPTIMIZE $END
 $SYSTEM MWORDS=100 $END
 $BASIS GBASIS=CC-PVDZ $END
 $STATPT OPTTOL=0.0001 NSTEP=50 $END
 $DATA
Water molecule
Cnv 2

O     8.0   0.000000   0.000000   0.117489
H     1.0   0.000000   0.757210  -0.469957
 $END
```

## Supported $ Groups

### Core Groups
- `$CONTRL` - Main control options (RUNTYP, SCFTYP, DFTTYP, etc.)
- `$SYSTEM` - System settings (memory, time limits)
- `$BASIS` - Basis set specification (GBASIS, NGAUSS, etc.)
- `$DATA` - Molecular structure and geometry
- `$GUESS` - Initial guess options

### Electronic Structure
- `$SCF` - SCF options (DIIS, SOSCF, CONV)
- `$DFT` - DFT options (functional, grid)
- `$MP2` - Møller-Plesset perturbation theory
- `$CC` - Coupled Cluster (CCSD, CCSD(T))
- `$CIS` - Configuration Interaction Singles
- `$TDDFT` - Time-Dependent DFT
- `$MCSCF` - Multiconfigurational SCF
- `$CI` - Configuration Interaction

### Geometry and Dynamics
- `$STATPT` - Geometry optimization
- `$FORCE` - Force calculations and frequencies
- `$HESSIAN` - Hessian matrix
- `$VIB` - Vibrational analysis
- `$IRC` - Intrinsic Reaction Coordinate
- `$DRC` - Dynamic Reaction Coordinate

### Solvation and Environment
- `$PCM` - Polarizable Continuum Model
- `$COSM` - COSMO solvation
- `$SMD` - SMD solvation model
- `$EFRAG` - Effective Fragment Potential
- `$FFIELD` - Force Field options

### Advanced Options
- `$ECP` - Effective Core Potentials
- `$RELWFN` - Relativistic corrections
- `$LOCAL` - Localized orbitals
- `$NBO` - Natural Bond Orbital analysis

And many more...

## Features in Detail

### Completion

- Type `$` to see all available groups
- Inside a group, type to see available keywords
- After `=`, see allowed values for the keyword

### Hover

Hover over any keyword or group name to see documentation:

```
SCFTYP
Type of SCF wavefunction.
Values: RHF, UHF, ROHF, MCSCF, NONE.
Default: RHF
```

### Diagnostics

Automatic warnings for:
- Unknown $GROUPS
- Unclosed groups (missing $END)
- Invalid keyword values (coming soon)

### Formatting

Automatic formatting with:
- Consistent 2-space indentation
- Standardized spacing around `=`
- Proper $END placement

## Development

### Setup

```bash
git clone https://github.com/newtontech/gamess-lsp.git
cd gamess-lsp
pip install -e ".[dev]"
```

### Testing

```bash
pytest tests/ -v
```

### Code Quality

```bash
black src tests
isort src tests
flake8 src tests
mypy src
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## License

MIT License - see [LICENSE](LICENSE) for details.

## References

- [GAMESS (US) Documentation](https://www.msg.chem.iastate.edu/gamess/documentation.html)
- [Language Server Protocol Specification](https://microsoft.github.io/language-server-protocol/)
- [pygls - Python LSP Library](https://github.com/openlawlibrary/pygls)

## Acknowledgments

- The GAMESS development team at Iowa State University
- The pygls team for the excellent LSP library
