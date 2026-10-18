# Step-by-step scientific QC checklist

## Global acceptance gate (every case)
1. Record exact patent/PDB/DOI and source page or identifier.
2. Verify that the cited source actually contains the reported compound or experiment.
3. Record whether structure is source-derived, computationally predicted, or synthetic demo.
4. Compare formula, charges, atom identity, bonds and stereochemistry against the source.
5. Run automated checks; investigate failures without changing the expected answer to force a pass.
6. Distinguish independently verified claims from pending or unresolved claims. Automated PASS never implies expert verified.
7. Store evidence hashes, reviewer notes, reference artifacts and negative-control outcomes.

## ReactionRx
Check step identity, substrate/product atom correspondence, bond changes, conditions, yields, mass balance and unresolved regioisomers. Map numbers must not be treated as experimental evidence.

## StereoRx
Check 2D connectivity first, then specified stereocenters and E/Z; distinguish computed conformer from experimental stereochemistry. Compare multiple conformers where justified; MMFF is not valid for all molecules.

## CoordRx
Check element, formal charge, donor atoms, bond representation, coordination number hypotheses, ligand denticity, counterions and source geometry. Distance cutoffs are only screening tools, not oxidation state or geometry proof.

## BioRx
Check PDB/mmCIF entry and chain, ligand residue and chemical dictionary, occupancy/alternate locations, missing atoms, resolution where relevant, pocket contacts and assay source. Proximity alone is not an H-bond or potency claim.

## MarkushRx
Check claim definitions, attachment points, variable domains, substitutions, exclusions, stereochemistry and concrete example identity. Exact finite enumeration is not generic claim coverage.
