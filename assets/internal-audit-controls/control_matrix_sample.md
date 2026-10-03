# Sample Control Matrix (extract) — for prospect demos
Client-agnostic sample across common processes. Illustrative only.

## P2P (Procure-to-Pay)
| C-001 | Three-way match (PO/GRN/invoice) before payment | Preventive | Per transaction | Maker-checker on new vendor bank details (anti-BEC) |
| C-002 | Vendor master change approval | Preventive | Per change | Segregation of duties enforced |

## O2C (Order-to-Cash)
| C-010 | Credit limit check before order release | Preventive | Per order | Override requires manager approval |
| C-011 | Revenue recognition per policy (cut-off testing) | Detective | Monthly | Reconciled to GL |

## Payroll
| C-020 | New joiner / leaver approval before payroll run | Preventive | Per change | HR-Finance reconciliation |

## ITGC
| C-030 | User access review | Detective | Quarterly | Segregation of duties |
| C-031 | Change management approval | Preventive | Per change | Tested in non-prod |

## AML / Financial Crime
| C-040 | Customer due diligence + sanctions screening | Preventive | Per onboarding | Escalation log |
| C-041 | Transaction monitoring alerts disposition | Detective | Daily | SLA on closure |
