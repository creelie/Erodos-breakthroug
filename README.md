# Finite-time blowup for Navier–Stokes: OpenAI's Lean proof, built and checked

This repository holds OpenAI's Lean 4 proof of finite-time blowup for the forced
three-dimensional Navier–Stokes equations, unchanged, together with a record of an independent
build. The mathematics, the paper and the Lean code are OpenAI's. Nothing here is a new proof.

- Source: [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler), commit
  [`f9e8bc5`](https://github.com/openai/NavierStokesAndEuler/commit/f9e8bc5b38b6e212696e8a30e3e91517af887bbd)
  (10 September 2026). Both upstream commits are kept here with their original author.
- Licence: Apache 2.0 (`LICENSE`). OpenAI's own README is kept as `OPENAI_README.md`.

## Paper

**OpenAI, *Finite time blowup for Navier–Stokes*, September 2026:**
<https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf>

Companion paper: OpenAI, *Finite time blowup for the Euler equation*,
<https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf>.
Announcement: <https://openai.com/index/navier-stokes-solution/>.

## What is proved

For every viscosity ν > 0 the Lean library proves

- **(C), breakdown on ℝ³** (`NavierStokes.Comparator.navier_stokes_breakdown_R3`): there are smooth,
  rapidly decaying initial data and forcing for which no smooth solution with bounded energy
  exists for all time;
- **(D), breakdown on ℝ³/ℤ³** (`NavierStokes.Comparator.navier_stokes_breakdown_periodic`): there are
  smooth periodic initial data and forcing for which no smooth periodic solution exists for all
  time.

These are alternatives (C) and (D) of Fefferman's official problem description for the Clay
Mathematics Institute's [Navier–Stokes Millennium Prize Problem](https://www.claymath.org/millennium/navier-stokes-equation/),
in the formalization of Google DeepMind's
[Formal Conjectures](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/Millennium/NavierStokes.lean)
project, which now lists both as solved with a link to OpenAI's Lean proof. Whether the Clay
Mathematics Institute awards the prize is decided by the Institute under its own rules, which ask
for publication and two years of acceptance; a formal check does not replace that process.

## The independent build (10 October 2026)

`VERIFICATION.md` has the details. In short:

| Check | Result |
|---|---|
| `lake build NavierStokes.ComparatorSolution` (Lean v4.34.0-rc2, Mathlib from `lake exe cache get`) | 9,371 jobs, no errors, 66 minutes; log in `verification/build-2026-10-10.log` |
| `#print axioms` for (C) and (D) (`verification/Axioms.lean`) | both use only `propext`, `Classical.choice` and `Quot.sound` |
| `sorry`, `native_decide`, new `axiom` in the 816 files of `NavierStokes/` | none |
| Statements against Formal Conjectures (`verification/compare_statements.py`) | the 16 definitions and both theorem statements are identical, declaration by declaration, to Formal Conjectures at commit `8bf45ed` and at its main branch of 9 October 2026 |

`#print axioms` would show `sorryAx` for a `sorry` and `Lean.ofReduceBool` for `native_decide`,
so the axiom line alone rules both out for the two main theorems.

## The arXiv dispute

A. Bastounis, F. Circelli and A. C. Hansen, *Navier–Stokes lost in translation: Why Lean
verification of AI autoformalisation does not guarantee correct natural language proofs*,
[arXiv:2610.08144](https://arxiv.org/abs/2610.08144) (6 October 2026), compare the written paper
with the Lean code at commit `f9e8bc5`. They find places where the Lean proof is not a
line-by-line translation of the paper:

- Lemma 8.6, equation (8.19): the paper bounds the inverse operator in Cᵐ by the Cᵐ⁺⁴ norm of
  the input; the Lean estimate uses the Cᵐ⁺⁵ norm (Example 3.1 and Remark 3.2 of their paper).
- The pressure-flux bound, equation (10.19): Lean proves a differently shaped bound by a
  different route, through Sobolev embedding and the L² bound for the Riesz transforms instead
  of the L^{3/2} bound (Example 3.3).

Their conclusion is that the Lean proof does not certify the written paper step by step. They
state that they make no claim about the correctness of the written proof, and they do not point
to any error in the Lean theorems. The checks above concern only the Lean theorems: the kernel
accepts the proofs of (C) and (D) as stated, whatever the differences in the intermediate
estimates of the paper.

## Rebuilding

With [elan](https://github.com/leanprover/elan) installed:

```sh
lake exe cache get
lake build NavierStokes.ComparatorSolution
lake env lean verification/Axioms.lean
curl -sSfLo fc.lean https://raw.githubusercontent.com/google-deepmind/formal-conjectures/8bf45ed70d48b2b2a501de9c00b26bfa38c573ee/FormalConjectures/Millenium/NavierStokes.lean
python3 verification/compare_statements.py fc.lean
```

The `build` workflow runs the same steps on GitHub. `lake build` with no target also builds the
Euler library and the Comparator challenges, as in OpenAI's README.

## Changes from upstream

No Lean file, `lakefile.toml`, `lake-manifest.json` or `lean-toolchain` is changed. Added:
this README (OpenAI's README moved to `OPENAI_README.md`), `VERIFICATION.md`, the `verification/`
folder and `.github/workflows/build.yml`.
