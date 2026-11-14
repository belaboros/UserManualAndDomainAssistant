"""The is-a diagram is packed towards a 16:9 (width:height) shape (plan 0002, implementation notes).

A domain with many separate trees and loose top concepts used to render as one very wide, very low
row. The generator now stacks those trees into columns with invisible Mermaid links (``~~~``).
"""

from __future__ import annotations

from domain_model.model import Concept, Ontology
from domain_model.text.layout import TARGET_RATIO, estimated_ratio, pack_columns, tree_components
from domain_model.text.mermaid import is_a_diagram


def _concept(cid: str, parent: str | None = None) -> Concept:
    return Concept(id=cid, label=f"concept {cid}", level=1, status="confirmed", source=["S1"], parent=parent)


def _wide_ontology() -> Ontology:
    """One tree with 6 children and 40 loose top concepts: one row, far wider than 16:9."""
    concepts = [_concept("Root"), *(_concept(f"Child{i}", "Root") for i in range(6))]
    concepts += [_concept(f"Loose{i}") for i in range(40)]
    return Ontology(namespace="https://example.org/t#", prefix="t", label="T", concepts=concepts)


def test_components_are_the_separate_is_a_trees() -> None:
    components = tree_components(_wide_ontology().concepts)
    assert len(components) == 41
    tree = next(c for c in components if "Root" in c.ids)
    assert (tree.width, tree.height) == (6, 2)


def test_packing_comes_close_to_16_to_9() -> None:
    components = tree_components(_wide_ontology().concepts)
    one_row = [[c] for c in components]
    assert estimated_ratio(one_row) > 4 * TARGET_RATIO
    packed = pack_columns(components)
    assert TARGET_RATIO / 1.5 <= estimated_ratio(packed) <= TARGET_RATIO * 1.5
    assert sorted(i for column in packed for c in column for i in c.ids) == sorted(
        c.id for c in _wide_ontology().concepts
    )


def test_diagram_stacks_trees_with_invisible_links_only() -> None:
    lines = is_a_diagram(_wide_ontology())
    edges = {tuple(line.split(" --> ")) for line in lines if " --> " in line}
    assert edges == {(f"    Child{i}", "Root") for i in range(6)}
    invisible = [line for line in lines if " ~~~ " in line]
    assert invisible, "loose concepts should be stacked into columns"
    assert all(line.count("~~~") == 1 for line in invisible)


def test_small_tree_gets_no_invisible_links() -> None:
    onto = Ontology(
        namespace="https://example.org/t#",
        prefix="t",
        label="T",
        concepts=[_concept("Root"), _concept("A", "Root"), _concept("B", "Root")],
    )
    assert not [line for line in is_a_diagram(onto) if "~~~" in line]


def _mixed_ontology() -> Ontology:
    """Trees of different sizes, declared smallest first, plus loose concepts."""
    concepts = [_concept(f"Loose{i}") for i in range(12)]
    concepts += [_concept("Small"), _concept("SmallA", "Small")]
    concepts += [_concept("Mid"), *(_concept(f"Mid{i}", "Mid") for i in range(3))]
    concepts += [_concept("Big"), *(_concept(f"Big{i}", "Big") for i in range(5)), _concept("BigX", "Big0")]
    return Ontology(namespace="https://example.org/t#", prefix="t", label="T", concepts=concepts)


def test_biggest_tree_first_then_smaller_ones_down_and_right() -> None:
    packed = pack_columns(tree_components(_mixed_ontology().concepts))
    assert len(packed) > 1
    reading_order = [len(c.ids) for column in packed for c in column]  # top to bottom, left to right
    assert packed[0][0].top == "Big"
    assert reading_order == sorted(reading_order, reverse=True)


def test_diagram_declares_biggest_tree_first_and_hangs_the_rest_below() -> None:
    lines = is_a_diagram(_mixed_ontology())
    nodes = [line.split("[", 1)[0].strip() for line in lines if '["' in line]
    assert nodes[0] == "Big"
    # flowchart BT: "lower top ~~~ upper leaf" puts the upper tree above, so Mid hangs below Big.
    assert [line for line in lines if line.startswith("    Mid ~~~ Big")]
