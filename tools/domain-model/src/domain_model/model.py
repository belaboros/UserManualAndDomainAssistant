"""Typed schema of the three YAML sources of a domain folder (plan 0002, "Data and interfaces").

Every model forbids unknown fields, so a misspelt key is reported instead of silently ignored.
Levels are plain integers here; the 1–3 range is a consistency check, so it names the item.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Id = Annotated[str, StringConstraints(pattern=r"^[A-Za-z][A-Za-z0-9_]*$")]
Status = Literal["confirmed", "draft"]
Datatype = Literal["string", "integer", "decimal", "boolean", "date", "dateTime", "anyURI"]
Characteristic = Literal[
    "functional", "inverse_functional", "transitive", "symmetric", "asymmetric", "reflexive", "irreflexive"
]
Scalar = str | bool | int | float | dt.date | dt.datetime
#: "each <domain> has … <range>": ``"1"``, ``"0..1"``, ``"1..*"``, ``"2..4"``, ``"*"``.
Cardinality = Annotated[str, StringConstraints(pattern=r"^(\*|\d+|\d+\.\.(\d+|\*))$")]

#: The rule pattern keys, in documentation order (FR-6). The README's pattern table lists each one.
PATTERN_KEYS = ("cardinality", "values", "implies", "equal", "derive", "sparql")
#: The predicate name a rule uses for rdf:type (in paths and in ``derive.add.predicate``).
TYPE_PREDICATE = "a"


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)


# ---------------------------------------------------------------------------- statements.yaml
class Statement(Strict):
    id: Id
    date: dt.date
    level: int
    text: str


class StatementsFile(Strict):
    statements: list[Statement] = []


# ---------------------------------------------------------------------------- ontology.yaml items
class Item(Strict):
    id: Id
    label: str
    level: int
    status: Status
    source: list[str] = Field(min_length=1)
    definition: str = ""
    synonyms: list[str] = []


class Concept(Item):
    parent: Id | None = None
    also_parents: list[Id] = []
    disjoint_with: list[Id] = []

    @property
    def parents(self) -> list[str]:
        return ([self.parent] if self.parent else []) + list(self.also_parents)


class Individual(Item):
    types: list[Id] = []
    facts: dict[Id, list[Id]] = {}
    values: dict[Id, Scalar] = {}


class Relation(Item):
    domain: Id | None = None
    range: Id | None = None
    inverse: Id | None = None
    parent: Id | None = None
    cardinality: Cardinality | None = None
    characteristics: list[Characteristic] = []


class Property(Item):
    domain: Id | None = None
    datatype: Datatype = "string"
    cardinality: Cardinality | None = None


def cardinality_bounds(text: str) -> tuple[int, int | None]:
    """``(min, max)`` of a cardinality; ``max`` is None when unbounded."""
    if text == "*":
        return 0, None
    low, _, high = text.partition("..")
    if not high:
        return int(low), int(low)
    return int(low), None if high == "*" else int(high)


# ---------------------------------------------------------------------------- rule patterns
class Condition(Strict):
    """``{path, has_value | in | class | min}``: the focus node has at least one such value (or ``min``)."""

    path: str
    has_value: Scalar | None = None
    in_: list[Id] | None = Field(default=None, alias="in")
    class_: Id | None = Field(default=None, alias="class")
    min: int | None = None

    @model_validator(mode="after")
    def _exactly_one_test(self) -> Condition:
        tests = [self.has_value, self.in_, self.class_, self.min]
        if sum(t is not None for t in tests) != 1:
            raise ValueError("a condition needs exactly one of has_value, in, class, min")
        return self


class CardinalityPattern(Strict):
    focus: Id
    path: str
    min: int | None = None
    max: int | None = None
    class_: Id | None = Field(default=None, alias="class")

    @model_validator(mode="after")
    def _has_bound(self) -> CardinalityPattern:
        if self.min is None and self.max is None:
            raise ValueError("cardinality needs min or max")
        return self


class ValuesPattern(Strict):
    focus: Id
    path: str
    in_: list[Id] | None = Field(default=None, alias="in")
    class_: Id | None = Field(default=None, alias="class")
    datatype: Datatype | None = None

    @model_validator(mode="after")
    def _exactly_one_test(self) -> ValuesPattern:
        if sum(t is not None for t in (self.in_, self.class_, self.datatype)) != 1:
            raise ValueError("values needs exactly one of in, class, datatype")
        return self


class ImpliesPattern(Strict):
    focus: Id
    if_: Condition = Field(alias="if")
    then: Condition


class EqualPattern(Strict):
    focus: Id
    left: str
    right: str


class DeriveAdd(Strict):
    predicate: Id
    object: str


class DerivePattern(Strict):
    focus: Id
    if_: Condition | None = Field(default=None, alias="if")
    add: DeriveAdd


class SparqlPattern(Strict):
    focus: Id
    select: str | None = None
    construct_: str | None = Field(default=None, alias="construct")  # `construct` is a BaseModel method

    @model_validator(mode="after")
    def _exactly_one_query(self) -> SparqlPattern:
        if (self.select is None) == (self.construct_ is None):
            raise ValueError("sparql needs exactly one of select, construct")
        return self

    @property
    def query(self) -> str:
        return self.select if self.select is not None else (self.construct_ or "")


Pattern = CardinalityPattern | ValuesPattern | ImpliesPattern | EqualPattern | DerivePattern | SparqlPattern
RuleKind = Literal["constraint", "derivation"]


class Rule(Strict):
    id: Id
    level: int
    status: Status
    source: list[str] = Field(min_length=1)
    statement: str
    cardinality: CardinalityPattern | None = None
    values: ValuesPattern | None = None
    implies: ImpliesPattern | None = None
    equal: EqualPattern | None = None
    derive: DerivePattern | None = None
    sparql: SparqlPattern | None = None

    @model_validator(mode="after")
    def _exactly_one_pattern(self) -> Rule:
        if len([k for k in PATTERN_KEYS if getattr(self, k) is not None]) != 1:
            raise ValueError(f"a rule needs exactly one pattern key: {', '.join(PATTERN_KEYS)}")
        return self

    @property
    def pattern_key(self) -> str:
        return next(k for k in PATTERN_KEYS if getattr(self, k) is not None)

    @property
    def pattern(self) -> Pattern:
        found: Pattern = getattr(self, self.pattern_key)
        return found

    @property
    def kind(self) -> RuleKind:
        if self.derive is not None or (self.sparql is not None and self.sparql.construct_ is not None):
            return "derivation"
        return "constraint"


# ---------------------------------------------------------------------------- ontology.yaml
class LevelInfo(Strict):
    name: str
    audience: str


DEFAULT_LEVELS = {
    1: LevelInfo(name="core", audience="anyone: understand the domain in 5–10 minutes"),
    2: LevelInfo(name="main", audience="an adopter: use the domain for the simplest use cases"),
    3: LevelInfo(name="detailed", audience="everything that exists in the domain"),
}


STANDARD_PREFIXES = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "owl": "http://www.w3.org/2002/07/owl#",
}


class Ontology(Strict):
    namespace: Annotated[str, StringConstraints(pattern=r"^https?://\S+[#/]$")]
    prefix: Id
    label: str
    language: str = "en"
    working_level: int = 1
    levels: dict[int, LevelInfo] = {}
    concepts: list[Concept] = []
    individuals: list[Individual] = []
    relations: list[Relation] = []
    properties: list[Property] = []
    rules: list[Rule] = []

    def level_info(self, level: int) -> LevelInfo:
        return self.levels.get(level) or DEFAULT_LEVELS[level]

    def sparql_prefixes(self) -> dict[str, str]:
        """The prefixes a SPARQL rule may use without declaring them: the domain's and the standard ones."""
        return {self.prefix: self.namespace, **STANDARD_PREFIXES}

    @property
    def items(self) -> list[Item]:
        """Every concept, individual, relation and property (the terms of the glossary)."""
        return [*self.concepts, *self.individuals, *self.relations, *self.properties]


# ---------------------------------------------------------------------------- taxonomy.yaml
class TreeNode(Strict):
    id: Id
    children: list[TreeNode] = []


class Tree(Strict):
    id: Id
    label: str
    relation: str
    top: list[TreeNode] = []


class TaxonomyFile(Strict):
    trees: list[Tree] = []


# ---------------------------------------------------------------------------- the whole folder
@dataclass(frozen=True)
class Domain:
    """A loaded domain folder: the parsed sources plus the optional hand-written axioms (Turtle text)."""

    folder: Path
    statements: list[Statement]
    ontology: Ontology
    taxonomy: TaxonomyFile
    axioms: str | None


@dataclass(frozen=True, order=True)
class Finding:
    """One problem: ``<file>:<item id>: <message>`` (file relative to the domain folder)."""

    file: str
    item: str
    message: str

    def __str__(self) -> str:
        return f"{self.file}:{self.item}: {self.message}" if self.item else f"{self.file}: {self.message}"
