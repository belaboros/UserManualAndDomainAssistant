"""Python quality gate for the monorepo (ADR-0014).

- ``qg-boundaries``: checks imports against the root and app ``components.json`` files.
- ``qg-metrics``: emits the modularity snapshot schema for one ``components.json``.
- ``qg-arch-render``: merges snapshots of one level and renders history, ``latest.md`` and the
  coupling diagram (shared by every language, used by ``/arch-metrics``).
"""
