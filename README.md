# gamess-lsp

Language Server Protocol implementation for GAMESS (US) input files.

## Features

- **Syntax Validation**: Real-time validation of GAMESS input files
- **Auto-completion**: Intelligent completion for $ groups and keywords
- **Hover Documentation**: Inline documentation for GAMESS keywords
- **Diagnostics**: Warnings for unknown groups and unclosed sections

## Installation

```bash
pip install gamess-lsp
```

## Usage

### Command Line

```bash
gamess-lsp
```

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

#### Neovim (nvim-lspconfig)

```lua
local lspconfig = require('lspconfig')
lspconfig.gamess.setup {
  cmd = {"gamess-lsp"},
  filetypes = {"gamess"},
}
```

## Supported $ Groups

- `$CONTRL` - Main control options
- `$SYSTEM` - System settings
- `$BASIS` - Basis set specification
- `$SCF` - SCF options
- `$DFT` - DFT options
- `$STATPT` - Geometry optimization
- `$FORCE` - Force calculations
- `$DATA` - Molecular structure
- And many more...

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

## License

MIT License
