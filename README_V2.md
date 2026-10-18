# PatentRx Intelligence X — scientific upgrade pack v0.2

This standalone directory is a **copy** of the original MVP plus conservative scientific enhancements; it is not an in-place patch of your existing project.

## Install and test

```bash
python -m pip install -e '.[dev]'
python -m pytest tests -q
python -m patentrx.cli demo
```

## Added modules

- `reactionrx/advanced.py`: atom-map integrity and element identity checks
- `stereorx/advanced.py`: mapped-center CIP comparison with explicit interpretation limits
- `coordrx/advanced.py`: explicit metal bond inventory
- `biorx/advanced.py`: PDB HETATM ligand-presence check
- `markushrx/advanced.py`: finite exact structure enumeration matching
- `core/provenance.py`: source SHA-256 fingerprinting
- `tests/test_advanced.py`: positive, negative, and edge-case unit tests
- `docs/SCIENTIFIC_VALIDATION.md`: claims and limitations

## Boundaries

This is an expanded **research MVP**, not a complete industrial cheminformatics system, not a validated patent-claim interpreter, and not a clinical/biological assay engine. The original patent regioisomer remains unresolved. Never label a record `expert_verified` without authenticated human review.

## Safe migration

Extract into a **new directory** (`D:/PatentRx-Intelligence-X-V2`) and test there first. Do not overwrite the original `D:/PatentRx-Intelligence` or `D:/PatentRx-Intelligence-X-MVP` directories. No merge is performed by this package.
