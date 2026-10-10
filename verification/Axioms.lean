import NavierStokes.ComparatorSolution

/-! The axioms behind the two main theorems. Each line must read
`depends on axioms: [propext, Classical.choice, Quot.sound]`: no `sorryAx`, no
`Lean.ofReduceBool` (which `native_decide` would add) and no axiom of the project's own. -/

#print axioms NavierStokes.Comparator.navier_stokes_breakdown_R3
#print axioms NavierStokes.Comparator.navier_stokes_breakdown_periodic
