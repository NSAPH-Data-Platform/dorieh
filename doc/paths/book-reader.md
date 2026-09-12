# Learning Path: Readers of the Book

**This path is for you if** you arrived here from
*Research Data that Can Be Trusted* (Bouzinier et al., Springer, 2026)
and want to see the ideas from the book running as software — or to go
past where the book stops.

**At the end you will have** matched every Dorieh-related chapter to
its living counterpart in this documentation, run the two worked
examples the book describes, and seen where the platform has evolved
since the manuscript was finalized.

## The path

1. **Start at [About the companion book](../about-the-book.md)** — the
   full chapter-to-documentation map in one table.
2. **Chapters 5 and 6** (the language design and its implementation)
   correspond to [The Dorieh approach](../concepts.md), with
   [Data Modeling for Dorieh Data Platform](../Datamodels.md) as the
   maintained equivalent of Appendix A and
   [Data Modeling Extensions](../DataModellingExtensions.md) of
   Appendix B.
3. **Chapter 7** (the ML-ready datasets sample application) is the
   [climate tutorial](../tutorial/climate/index.md) — and unlike the
   chapter, you can run every step here, on open data.
4. **Chapter 8** (the Medicare claims pipeline) maps to the
   [Medicare tutorial](../tutorial/medicare/building-medicare-pipeline.md)
   for the guided path, 
   [Medicare: Building a Data Warehouse from ResDac Files](../Medicare.md)
   for the full reference, and the
   [Medicare example](../medicare-example.md) to run it on the
   synthetic dataset the book could only describe.
5. **See what changed since the book.** The docs track the living code,
   which has moved on in places — most notably the entitlement reason
   codes: OREC is now modeled as a per-beneficiary invariant with a
   `consistent_orec` QC flag. Look for the
   "Design note — evolved after the book" call-outs, starting in
   [Entitlement reason codes: OREC and CUREC](../Medicare.md#entitlement-reason-codes-orec-and-curec).

## Going deeper

* The [data dictionary and lineage](../MedicareLineage.md) pages
  generalize the lineage figures from Chapter 8 to every table and
  column in the warehouse.
* The QC statistics discussed in the book can be recomputed on the
  synthetic dataset through the
  [Superset dashboard](../medicare-example.md) — the numbers differ
  (synthetic data), the method is the same.
