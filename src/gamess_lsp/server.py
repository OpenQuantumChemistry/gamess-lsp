"""GAMESS Language Server Protocol implementation."""

from pygls.server import LanguageServer

server = LanguageServer("gamess-lsp", "0.1.0")


@server.feature("textDocument/completion")
def completion(params):
    """Handle completion requests."""
    return []


@server.feature("textDocument/hover")
def hover(params):
    """Handle hover requests."""
    return None


@server.feature("textDocument/diagnostic")
def diagnostic(params):
    """Handle diagnostic requests."""
    return []


def main():
    """Main entry point."""
    server.start_io()


if __name__ == "__main__":
    main()
