# H2 SAMPLE DELIVERABLE — spec + template
Purpose: show buyers exactly what they get. THIS IS A FORMAT TEMPLATE — do not present sample rows as real leads.

## Columns (Standard tier)
first_name | last_name | title | company | company_size | industry | location | linkedin_url | email | email_status | source

## Rules
- `email_status` ∈ {verified, risky, best-effort, unknown}. Never write "verified" unless a verifier confirmed it.
- `source` = where the record came from (public directory / company site / professional network).
- De-dupe on email + company+title.
- Deliver CSV + Google Sheet link.

## Illustrative row (NOT a real person — format only)
Jane | Doe | Head of Growth | ExampleCo | 11-50 | Ecommerce | Austin, US | linkedin.com/in/example | jane@example.com | best-effort | company site
