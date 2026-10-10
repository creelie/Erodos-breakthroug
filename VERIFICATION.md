# Verification record

Independent build of OpenAI's Lean proof of alternatives (C) and (D), 10 October 2026.

## Source

- `openai/NavierStokesAndEuler`, branch `main`, commit
  `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` (the upstream head on 10 October 2026), whose
  parent is `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`, the commit Formal Conjectures cites.
- Toolchain `leanprover/lean4:v4.34.0-rc2`; Mathlib `v4.34.0-rc2`
  (`85e3a25e006c35636f0e53b0e9296caca2685bc0` in `lake-manifest.json`), compiled files from
  `lake exe cache get`.
- `NavierStokes/` has 816 Lean files, about 429,000 lines.

## 1. Build

```
lake exe cache get
lake build NavierStokes.ComparatorSolution
```

Result: `Build completed successfully (9371 jobs).` in 66 minutes of wall time on a Linux
container (186 minutes of CPU time). The full log is `verification/build-2026-10-10.log`; it has
no errors and no `declaration uses 'sorry'` warning. Its last lines are the axiom report that
`NavierStokes/ComparatorSolution.lean` prints itself:

```
'NavierStokes.Comparator.navier_stokes_breakdown_R3' depends on axioms: [propext, Classical.choice, Quot.sound]
'NavierStokes.Comparator.navier_stokes_breakdown_periodic' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## 2. Axioms

`lake env lean verification/Axioms.lean` prints the same two lines. These three axioms are the
standard ones of Lean and Mathlib. A `sorry` anywhere in the dependency graph would add
`sorryAx`, and `native_decide` would add `Lean.ofReduceBool`; neither appears. A text search of
`NavierStokes/` and `NavierStokes.lean` finds no `sorry`, no `native_decide`, no `axiom`
declaration and no `implemented_by`.

## 3. The statements are Clay's (C) and (D) as formalized by Formal Conjectures

The theorems are proved in namespace `NavierStokes.Comparator`, over definitions in
`NavierStokes/ComparatorDefinitions.lean`. The reference statement is
`FormalConjectures/Millenium/NavierStokes.lean` of google-deepmind/formal-conjectures at commit
`8bf45ed70d48b2b2a501de9c00b26bfa38c573ee`, which `ComparatorChallenges/NavierStokes.lean`
copies with only imports, attributes, namespace and notation adapted.

`verification/compare_statements.py` strips comments, attributes and whitespace and compares
the files declaration by declaration:

| Check | Result |
|---|---|
| each of the 18 declarations of `ComparatorChallenges/NavierStokes.lean` against Formal Conjectures | identical |
| Formal Conjectures declarations absent from the challenge | only (A) and (B), the existence alternatives |
| each of the 16 declarations of `ComparatorDefinitions.lean` against the challenge | identical; only the two challenge theorems are left out |
| the statements of `navier_stokes_breakdown_R3` and `navier_stokes_breakdown_periodic` in `ComparatorSolution.lean` against the challenge | identical |

The comparison passes against the pinned commit and against Formal Conjectures `main` of
9 October 2026 (commit `1646ca16`, where the file has moved to
`FormalConjectures/Millennium/NavierStokes.lean` and marks (C) and (D) as solved with a link to
OpenAI's proof). A change to a single hypothesis makes the script fail; this was tested by
deleting `ForceConditionDecay f` from a copy of the (C) statement.

Not run here: OpenAI's Comparator replay (`lake exe comparator ComparatorChallenges/NavierStokes.json`),
which needs the `landrun`, `lean4export` and `nanoda_bin` tools and checks the same match at the
level of compiled terms. The text comparison above is weaker than that replay but independent
of it.

## 4. The written paper and arXiv:2610.08144

Bastounis, Circelli and Hansen ([arXiv:2610.08144](https://arxiv.org/abs/2610.08144)) show that
some intermediate estimates in the Lean code differ from the written paper: Lemma 8.6, equation
(8.19), loses one more derivative in Lean (Cᵐ⁺⁵ instead of Cᵐ⁺⁴), and the pressure-flux bound
(10.19) is stated and proved differently. Nothing in sections 1 to 3 depends on the written
paper: the kernel checks the Lean proofs of the two theorems as stated. The dispute concerns
whether the paper's own arguments are what Lean checked, which these checks do not address.
