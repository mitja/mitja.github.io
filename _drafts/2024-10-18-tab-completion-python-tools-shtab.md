
Shtab is a nice tool that generates bash, zsh, and tcsh tab completion scipts for Python tools. It works by processing  `argparse.ArgumentParser` instances. Thus, it also supports `docopt`, but not `click` or `typer` as `click` does not use `argparse`.

The basic usage is just a single command (see [Usage](https://docs.iterative.ai/shtab/use/#__tabbed_2_2)).

Has some library features that can be added to commands.  interesting use cases like...

Also supports Django management commands.

https://github.com/iterative/shtab