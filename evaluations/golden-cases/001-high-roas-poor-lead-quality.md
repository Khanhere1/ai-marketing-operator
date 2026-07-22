# Golden Case 001: High Platform ROAS vs Poor CRM Lead Quality

## Business Context
* **Organization**: B2B SaaS company ($5M ARR)
* **Channel**: Google Search Ads
* **Symptom**: Marketing team reports 4.2x ROAS in Google Ads dashboard, but Sales team reports leads are "junk" with low opportunity conversion.

## Input Data Fixtures
1. `google_ads_export.csv`: Campaign "US_Search_Generic" shows 250 conversions, $12,000 spend, 4.2x ROAS. Conversion goal: Form-fill / E-book download.
2. `hubspot_leads.csv`: 250 form-fills synced; 10 accepted by sales (4% acceptance rate vs 22% company benchmark).
3. `margin_assumptions.json`: 78% gross margin, $250 target CPA for sales-qualified lead.

## Expected System Outputs
1. **Data Quality & Reconciliation**:
   * Flag conversion discrepancy between Google Ads form-fills and HubSpot Sales Accepted Leads.
   * Calculate true CRM CPA ($1,200 per sales accepted lead vs target $250).
2. **Diagnosis**:
   * Identify broad match search terms driving unvetted e-book downloads rather than commercial intent demo requests.
3. **Recommendation**:
   * Recommend pausing 5 lowest-performing broad match ad groups.
   * Propose Offline Conversion Tracking (OCT) sync implementation to send qualified opportunity signals back to Google Smart Bidding.

## Critical Failure Modes (Instant Fail)
* System accepts platform 4.2x ROAS as true performance and recommends increasing campaign budget.
* System ignores CRM lead acceptance data.
* System proposes autonomous campaign deletion without approval contract.

## Scoring Rubric (1-5)
* **5 (Optimal)**: Accurately reconciles CRM vs Ad platform, identifies exact broad match terms, proposes OCT long-term fix, outputs valid schema contract.
* **3 (Acceptable)**: Identifies high CPA but fails to specify OCT long-term capability task.
* **1 (Unacceptable)**: Recommends budget increase based on platform ROAS.
