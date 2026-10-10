OpenAI's Lean 4 proof of finite-time blowup for the forced Navier–Stokes equations
(openai/NavierStokesAndEuler at f9e8bc5, Apache-2.0), unchanged, with the record of an
independent build made on 10 October 2026.

- `lake build NavierStokes.ComparatorSolution` on Lean v4.34.0-rc2: 9,371 jobs, no errors.
- Alternatives (C) `navier_stokes_breakdown_R3` and (D) `navier_stokes_breakdown_periodic`
  depend only on `propext`, `Classical.choice` and `Quot.sound`.
- No `sorry`, `native_decide` or new `axiom` in the 816 files of `NavierStokes/`.
- The definitions and both statements are identical to Google DeepMind's Formal Conjectures
  at commit 8bf45ed.

The proof, the papers and the Lean code are OpenAI's; this release adds no new proof. The
README summarizes arXiv:2610.08144 on where the Lean proof departs from the written paper.
