# Reviewer notes - Denver reported offenses brief (2026-10-17)

## Section 11.3 flags for Alex
- AGENCY-ADJACENT FINDINGS DURING A LIVE DECISION WINDOW: this brief names the Denver Police
  Department (as data publisher) throughout and lands during the 2027 budget deliberation
  (proposal Oct 19, hearing Oct 26, amendments Nov 2, passage Nov 9). It makes no conduct claim
  about DPD; its only DPD-directed ask is a documentation note on the dataset page. The budget
  tie-in is confined to "Who can act." Alex should read Finding 1 and the DPD bullet with the
  budget window in mind before approving.
- BUILDER-SURPRISE FINDING: the topic question assumed the offenses file mixes traffic and
  criminal offenses (IS_TRAFFIC / IS_CRIME). It does not: IS_CRIME is set on all 383,643 records
  and IS_TRAFFIC on none. The brief answers the question at the ledger level and says so.
- NO AGENCY HEADS-UP has been sent or is proposed (standing rule). Nothing in this package has
  been published, posted, or sent.

## Claims most likely to be challenged, and their state after review
1. "Everything not involving a car rose" (title). The year-by-year rhythm of the residual is
   grouping-dependent: criminal-mischief-mtr-veh (a public-disorder type) is in the vehicle
   grouping. The sensitivity is printed in Finding 2 with both decompositions; the core claim
   (vehicle types fell by more than the entire net decline) holds under both groupings, with or
   without DIA, and against the 2026 tail shortfall. Expect a DPD analyst to raise the grouping;
   the brief now raises it first.
2. Sexual-assault coverage. The brief's claim is an inventory fact about this layer (no
   sexual-assault offense type among the 173 types), worded as such after review; DPD's own
   documentation speaks of withheld addresses and publishes sex-offense information through its
   own channels. If DPD responds that sex offenses appear elsewhere in its publications, the
   brief's sentence remains accurate for layer 324, which is all it claims.
3. Unit of count. Counts are offense records (NIBRS), not incidents: 358,980 distinct incidents
   underlie the 383,643 records. Journalists comparing against incident-based DPD figures will
   see different totals; Methods now pre-answers this.
4. The non-vehicle rise. The brief's position is reporting-fact only; the strongest hostile
   reading (the rise is substantially reporting/enforcement practice, concentrated in six
   practice-sensitive types supplying 2,178 of the 2,737 additional 2026 reports) is printed in
   Finding 2 itself rather than left to critics.
5. Neighborhood rates. Single ACS 2020-2024 cross-section; area-weighted allocation; downtown
   rates are reports per housing unit over small residential bases. Caveats are in Finding 4,
   not only in Methods, after review.

## Pre-publication checks for the QA run (not yet done)
- [CLOSED at close-out 2026-10-17] Attach the current layer-324 dataset description text to the package: the adversarial reviewer
  could not extract it from the ArcGIS Hub page, and two Data-notes sentences rest on DPD's
  documented wording (sexual-assault address withholding; child-abuse/juvenile exclusion) as
  carried in the dataset description mirrors. Verify the wording against the live page.
  Close-out: live service description saved to data/dataset_description_layer324.txt (dynamic
  wording confirmed live); withheld-data wording confirmed against the mirrored DPD dataset
  description (sexual-assault addresses not included; child-abuse and juvenile-involved cases
  not reported at all). Both brief sentences match.
- Attach a citable city source for the four 2027 budget dates in "Who can act" (currently traced
  to the goal's tracked budget calendar in sources.md, not to a public city page).
- Repo creation is Alex's step (GitHub App cannot create repos); the social drafts carry a
  [REPO LINK] placeholder until then.

## Anything unverifiable in this package
- Traffic-accident counts rest on the service's own count queries (archived); the service warns
  of a Q4 2026 revision, so those counts are as-of October 16, 2026 by construction.
- ACS denominators are estimates with sampling error; the Five Points cross-check against the
  STR specimen (0.06 percent) validates the allocation method, not the ACS estimates themselves.
- DPD's processing-lag statement and dynamic-data characterization are taken from DPD's
  documentation as read by the adversarial reviewer; see the first pre-publication check.

## Review outcome
- Section 10 pre-flight audit: ALL ASSERTIONS PASSED (output in verification.md).
- Independent verifier: every decisive figure confirmed exactly; 3 minor defects, all fixed.
- Adversarial review: 4 blocking + 11 should-fix/nit findings; all blocking findings fixed,
  dispositions recorded in verification.md, one recorded disagreement (N1, table percent for
  arson, counts adjacent). Fix loop closed by builder re-computation of every reviewer-quoted
  figure and a stats.json diff showing exactly the one intended field change.
