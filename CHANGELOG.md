# Changelog

## 2026-04-06

### Deployment
- Removed `serve.py` because Vercel was interpreting the project as a Python/Lambda deployment instead of a static site.
- Added `vercel.json` to force static routing to `index.html`.
- Synced `index.html` with the latest `급여구조_세금비교_시뮬레이터_v2.html` so Vercel serves the current simulator UI, including the foreign flat-tax option.

### Added
- Created `급여구조_세금비교_시뮬레이터_v2.html` as a separate v2 simulator file.
- Added `Option 3: 법인 경유 배우자포함`.
- Added spouse salary support for `Option 3`.
- Added official 2026 withholding table data in `withholding_table_2026.js`.
- Added `Option 1` foreign worker flat-tax toggle for the 19% single-rate scenario.

### Changed
- Switched salary withholding logic to the attached 2026 Korean withholding table for regular withholding scenarios.
- Fixed monthly non-taxable salary assumption at `200,000 KRW`.
- Added dependent-count slider and applied it to withholding-table lookups.
- Removed employment insurance from comparison logic across options.
- Simplified retirement treatment to assume IRP transfer and count the full retirement payment as IRP value.
- Separated display of national pension, health insurance, and long-term care insurance in cards instead of grouping them into a single line.
- Separated income tax and local income tax display in salary sections.
- Standardized card money display to `만원`.
- Included employer-side national pension in total attributed value.
- Treated corporate expenses as value retained by the user for this simulator's comparison purpose.
- Renamed project folder to `salary-vs-corp-tax-simulator`.

### Fixed
- Corrected salary withholding to use official withholding-table amounts instead of an annualized estimate.
- Corrected insurance calculations to use monthly salary after the fixed non-taxable amount where applicable.
- Corrected `Option 2` and `Option 3` employer-side industrial accident insurance handling so it applies only to the spouse worker scenario, not to the representative director.

### UI
- Added `Opt1 외국인 단일세율 19%` toggle.
- Updated labels so Option 1 can switch between withholding-table wording and foreign flat-tax wording.
- Updated assumptions note to explain the active salary-tax mode.

### Notes
- `Option 1` foreign flat-tax mode is modeled as `gross salary x 19%`, plus local income tax, with no non-taxable exclusion or personal deductions applied.
- Real eligibility for the foreign flat-tax regime still depends on actual legal requirements such as first Korean work date and related-party restrictions.
- Representative director insurance and tax assumptions are intentionally simplified for comparison purposes.
