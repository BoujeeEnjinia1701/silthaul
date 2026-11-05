---
doc_id: SLH-MKT-001
title: SiltHaul market and viability
project: SiltHaul
doc_type: Market and viability
version: "0.1"
status: Draft
date: 2026-11-03
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-03
    author: Amish Chadha
    change: First market note, written for the kit 1.9.1 upgrade; prices cited with the date they were checked
---

# SiltHaul market and viability

Relief groups and municipal crews that clear flood mud by shovel and bucket are the users; no portable, hand-powered slusher for flood recovery was found (SLH-PRB-001), so the benchmarks below are partial and only show the price range of hand pulling and hand pumping gear. An open design lets a local fabricator build and mend a kit from stock steel for about USD 1,056 in parts, and spread it through NGOs and workshops without a licence fee. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Relief NGOs and community groups | Flood clean-up in South and Southeast Asia, for example Kerala after the 2018 floods ([Gulf News, 2018](https://gulfnews.com/world/asia/india/kerala-flood-70000-people-participate-in-massive-post-flood-clean-up-drive-in-kuttanad-1.2271770)), and other flood regions | Shovels and buckets (no price checked: to assess); a 2 ton hand cable puller (come-along), USD 83.99, listed as discontinued, on a retailer page checked 2026-11-03 ([Paul B Hardware](https://paulbhardware.com/maasdam-144sb-6-cable-puller-2-ton-lifting-3-16-in-dia-rope-cable-12-ft-l-rope-cable-6-ft-lift-mp144sb6)); its 6 ft cable cannot drag a box 12 m | Option A: 1,055.60 (BOM, indicative prices). Option B: about 454 for lines carried over from the BOM, foot boards and grips not priced. Option C: to assess | A kit that two or three volunteers can set up and a crew of four can use to move mud without lifting it |
| Municipal drain and sanitation crews | Narrow lanes, open drains and culverts where machines cannot enter | Powered mine slushers and scraper winches ([Mining History Association](https://www.mininghistoryassociation.org/Journal/MHJ-v22-2015-Reynolds.pdf)); no price found: to assess | As above | A hand-powered rope scraper with no fuel or power supply |
| Householders and volunteers | Owners of flooded ground-floor rooms | No sale: users borrow a kit from an NGO or council | Not applicable | Less lifting and less time in the mud |
| Local fabricators | Workshops near flood-prone areas | A hand diaphragm pump, for scale only: AMT hand diaphragm pump HP01-99, USD 182.95, USA Blue Book page checked 2026-11-03 ([USA Blue Book](https://www.usabluebook.com/theme/diaphragm-pump/category=pumps/price=200-to-299-99,100-to-199-99/)); the page does not say whether it passes solids, and it is far smaller than option C | Parts only; labour and workshop margin to assess | A paid build and repair service from open drawings |

## Open route

NGOs and relief groups would borrow or buy a kit, local fabricators would build it from `bom/bom.csv` and the drawings, and universities and makerspaces could build a test unit. The hardware is under CERN-OHL-S-2.0 and the calculators under MIT (`REUSE.toml`), so any maker can share improvements back under the same terms. Whether a commercial supplier would ever sell kits is Amish's decision and is not assumed here.

## Viability

On paper the parts cost is USD 944.40 under the USD 2,000 value-engineering target (a hypothetical control target). Demand is episodic: flood seasons, and one kit serves many sites if the NGO stores it. Unknown: willingness to pay, how many kits an NGO would hold, and local labour rates; all are "to assess" with a co-design partner. No price in this note is a quote.

## Sources

- Gulf News, 2018, Kerala clean-up, <https://gulfnews.com/world/asia/india/kerala-flood-70000-people-participate-in-massive-post-flood-clean-up-drive-in-kuttanad-1.2271770>.
- Paul B Hardware, Maasdam Powr-Pull 2 ton cable puller MP144SB6, USD 83.99, discontinued, checked 2026-11-03.
- USA Blue Book, AMT hand diaphragm pump HP01-99, USD 182.95, checked 2026-11-03.
- Mining History Association, journal 2015 on slusher scrapers, <https://www.mininghistoryassociation.org/Journal/MHJ-v22-2015-Reynolds.pdf>.
