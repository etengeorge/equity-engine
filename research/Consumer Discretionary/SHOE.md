# SHOE — SHOE STATION GROUP INC
*Consumer Discretionary · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-14 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $12.71 · fair value $12.50 · gap -1.7%
- **Growth:** market implies -19.3%, analyst says -2.0% (delta +17.3%)
- **FCFF base overridden** by the analyst to $25.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 10.3% | 11.3% | 12.3% | 13.3% | 14.3% |
|---|---|---|---|---|---|---|
| bear | -10.0% | $11.47 | $10.80 | $10.27 | $9.83 | $9.46 |
| base | -2.0% | $14.31 | $13.31 | $12.50 | $11.83 | $11.28 |
| bull | +5.0% | $17.60 | $16.20 | $15.07 | $14.14 | $13.36 |

At the point WACC of 12.3%: bear -19.2%, base -1.7%, bull +18.5%
Across the whole grid the gap ranges -25.6% to +38.5% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $12.71 the market is paying ~$216M of enterprise value — a $345M market capitalisation against $131.6M of cash and marketable securities and NO DEBT — for a family footwear retailer that is mid-rebanner, with 21 Shoe Carnival stores converted to the Shoe Station format year to date and management reporting that August comparable sales improved after localised assortments. E-commerce grew 18.8%. The balance sheet means the equity cannot be forced, and if the Shoe Station format works the conversion is a self-funded route to a better box. The market is pricing a business it expects to keep shrinking; it is not pricing bankruptcy.

**What changed.** Q2 2026 (quarter ended 2026-08-01, reported 2026-09-10) was materially worse than the extract knows — the cached fundamentals stop at the 2026-05-02 balance sheet. Net sales fell 7.2% to $284.3M. Gross margin 31.9% against 38.8%, DOWN 690 basis points, of which merchandise margin was -630bp. H1 net income collapsed to $631 THOUSAND from $28,568 thousand. Full-year guidance was LOWERED: net sales $1.100-1.111B (down 2-3%), gross margin ~32.5-32.7% (390-410bp of compression), GAAP EPS $0.32-0.47 and adjusted EPS $0.75-0.90. Management expects 'the promotional environment will persist through the balance of the year'.

**Base case.** The engine's $54.5M FCFF base is the mean of [$26.6M, $69.5M, $66.5M] — two good years and one bad one — for a company that now guides full-year GAAP earnings of $9-13M and adjusted earnings of $20-24M on 27.2M shares. Depreciation of ~$35M roughly offsets capex of ~$40M, so a defensible forward owner-earnings base is $25M, close to the FY2025 actual of $26.6M and nowhere near $54.5M. On that base the market is implying about -1.4% five-year growth, not -19.3%. My -2% is the honest read of a chain guiding sales down 2-3% with 400bp of structural gross margin compression and a promotional environment management expects to persist: roughly flat-to-slightly-down cash flow from an already depressed level.

**Devil's advocate.**
- Strongest counter: That I have marked the base down to the trough and therefore guaranteed a no_edge. The `possible_trough_cycle_base` flag fires at 0.40x, and the flag's own logic says growth applied to a trough understates value. FY2026 contains $13.6M of genuinely non-recurring pre-tax charges (CEO transition and strategic review), the rebanner costs are one-time, and the prior-year gross margin was flattered by a temporary benefit from raising prices ahead of tariff cost increases — so the 690bp decline overstates the underlying deterioration. Normalise all of that and earnings power is well above the $25M I used.
- What would prove it: H2 comparable sales landing at the top of the guided -1% to +1% range with gross margin stabilising, and free cash flow for the full year coming in near the $54.5M the engine assumes.
- Already visible today: It cuts both ways and I am recording both halves honestly. In the bull's favour: the prior-year comparison really was inflated — management says Q2 2025 merchandise margin 'included a temporary benefit from raising prices in advance of increasing tariff-related costs', which is the IEEPA cohort event appearing in a form I had not seen, as a LAPPING problem rather than a refund. Against the bull: the company's own FULL-YEAR guidance already incorporates every one of those normalisations and still lands at $0.75-0.90 of ADJUSTED EPS, i.e. $20-24M — the $13.6M of charges is explicitly excluded from that figure. Management has already done the normalisation the bull is asking me to do, and it does not get anywhere near $54.5M.
- Left unresolved: Whether the August comp inflection is real or a fall-seasonal artifact. One month of directional commentary on an earnings call is not evidence, and I could not find the underlying monthly data.

**Key risks.** $303.4M of operating lease liabilities against a $345M market cap — the fixed cost base does not shrink with sales; 690bp of gross margin compression in a single quarter with management guiding the promotional environment to persist; Rebanner is a bet: 21 stores converted year to date with no completed-format comparable to judge it on
**Watch for.** H2 comparable sales against the guided -1% to +1%; Gross margin stabilising near the guided 32.5-32.7% rather than deteriorating further; Full-year free cash flow against the $26.6M FY2025 level

**Data quality.** The extract is A QUARTER STALE and it is the quarter that matters: fundamentals are cached to the 2026-05-02 balance sheet, while the 10-Q for the quarter ended 2026-08-01 was filed 2026-09-10 and contains a 7.2% sales decline, 690bp of gross margin compression and lowered full-year guidance. I overrode the FCFF base from $54.5M to $25M on the company's own guidance. `possible_trough_cycle_base_newest_fcf_0.40x_oldest` — this is the AMR/LPG problem again: the flag's advisory text says a trough base understates value, and here the trough is the CURRENT state of the business rather than a cyclical low to be normalised away. `operating_leases_141%_of_EV` — I did NOT add the $303.4M lease liability to enterprise value, because the FCFF series is computed after cash rent, and capitalising the liability without also adding rent back to the cash flows would double-count. It remains a real operating-leverage risk and is recorded as such rather than as a valuation adjustment. Note the ticker and name changed from SCVL/Shoe Carnival to SHOE/Shoe Station Group inside the filing window, which is why the filing list mixes scvl- and shoe- prefixed documents.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/895447/000119312526387855/shoe-20260801.htm
- https://www.sec.gov/Archives/edgar/data/895447/000119312526387134/shoe-20260910.htm
