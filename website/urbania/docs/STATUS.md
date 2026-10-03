# Urbania — status & handoff

**Last updated:** 2026-10-03
**Live:** Force Urbania group-transport site, Hyderabad (working name "Urbania Hyderabad")
**Production:** VPS `ubuntu@129.225.68.128`, app on `:8100` behind a Cloudflare tunnel

---

## The one-paragraph state

The site is live, stable, and the quote funnel works end to end. The single most
valuable thing done recently was fixing a defect that silently cost every enquiry:
the submission confirmation was rendered **inside the form that the code hides on
success**, so customers saw the form vanish with no acknowledgement. That is fixed
and verified against production. The remaining work is almost entirely **owner
inputs** — real rates, specs, photographs and a confirmation about the fleet —
because the site currently publishes honest placeholders rather than invented
figures.

---

## Working on this repo from two places

> **IMPORTANT — read this first.** There is currently **no shared git remote**.
> Verified 2026-10-03:
>
> | | commits | remotes |
> |---|---|---|
> | Local Mac `~/revenue-lab` | 10 | **none** |
> | VPS `~/revenue-lab` | 1 ("Initial commit") | **none** |
>
> The two are independent histories and have already diverged. **The only thing
> syncing them today is `deploy.sh`, and it pushes `app/` only** — so `docs/`,
> `tests/`, `tools/`, `site_data.py` and `build_*.py` do **not** travel to the
> VPS. Editing from both sides without a shared remote will overwrite work.
>
> The documented `git pull` / `git push` loop below **will not work until a
> private GitHub repo is created and both clones are pointed at it.** That is the
> single highest-value next step for safe two-sided work.

Once a remote exists, the intended layout is:

```
local Mac            ~/revenue-lab
VPS dev clone        ~/projects/urbania         (to be created)
VPS production       /home/ubuntu/revenue-lab/website/urbania/app
```

Production stays a build target, not a working copy.

**Rules**

1. `main` is always deployable. Work on a branch, then merge.
2. Never develop directly in the production directory.
3. Never commit: `app/data/`, `app/.admin_token`, `.env`, customer files, `.sshots/`.
4. Production data survives deploys — `deploy.sh` excludes `data/` and `.admin_token`.

**Typical loop (once the remote exists)**

```bash
cd ~/revenue-lab
git pull --rebase origin main
git switch -c feature/<thing>
# ...edit...
cd website/urbania && python3 build_pages.py && python3 -m unittest tests.test_urbania
cd ~/revenue-lab && git commit -am "..." && git switch main && git merge --ff-only feature/<thing>
git push origin main
```

**Until then**, treat one machine as the writer at a time, and pass anything under
`docs/`, `tests/`, `tools/` or `site_data.py` across by hand or through the repo
archive.

**Deploy**

```bash
cd ~/revenue-lab
./deploy.sh status              # what is running on the VPS
./deploy.sh diff                # local vs production drift
./deploy.sh urbania --dry-run   # what would be sent
./deploy.sh urbania             # push + restart + health check
```

`deploy.sh` fails the deploy if the post-restart health check fails, and it stops
the listener **by port**, never by command pattern — a `pkill -f 'python3 server.py'`
matches the remote shell running it and kills its own connection mid-restart,
leaving the site down.

---

## Build & verify

```bash
cd website/urbania
python3 build_pages.py                 # regenerate app/site (35 sitemap URLs)
python3 -m unittest tests.test_urbania # 43 tests
```

Visual QA needs Playwright (kept in an isolated venv so it never touches the
user's Chrome):

```bash
PW=~/.hermes/cache/scratch/pw-venv/bin/python
$PW tools/shoot.py --pages home,quote --viewports desktop,tablet,mobile
$PW tools/audit.py                                   # overflow, bleed, tap targets
$PW tools/flow_test.py                               # browser E2E, local
$PW tools/flow_test.py --base https://<live-host>    # same E2E against production
```

The flow test asserts the confirmation is **visible**, not merely present —
`inner_text()` returns text from hidden elements, which is how the confirmation
bug previously passed every test.

---

## Content: one file to edit

Everything an owner may change lives in **`site_data.py`**: configurations, rates,
routes, services, trust figures, gallery slots, pricing FAQs, and the group-size
recommendation rules.

**The honesty rule:** an unconfirmed value is `None` and renders through `tbc()` /
`money()` as a visible *"To be confirmed"*. Never put a guess in this file — tests
fail the build if a fabricated rupee figure or an unsupported superlative reaches a
page.

### `FLEET_CONFIRMED` — needs an owner decision

```python
FLEET_CONFIRMED = False   # site_data.py
```

The brief describes four configurations (17 / 16 / 12-13 premium / 9-10 Maharaja).
`docs/FACTS_LEDGER.md` and the live site describe **one** 17-seat vehicle. Both
cannot be published. While the flag is `False`, the configuration and rates
sections publish their architecture but show placeholders instead of asserting a
fleet. Flip it to `True` only once the owner confirms which vehicles actually
exist.

---

## Outstanding owner inputs

| # | Needed | Blocks |
|---|---|---|
| 1 | Which Urbania configurations actually exist | `FLEET_CONFIRMED`, fleet + rates pages |
| 2 | Real rates (per km, per day, driver allowance, min km/day, GST) | rates table |
| 3 | Vehicle specs (seat type, AC, charging, luggage, amenities) | config cards |
| 4 | Verified distances / drive times from Hyderabad | destination pages |
| 5 | Trust figures (Google rating, review count, trips, years, vehicles) | trust strip |
| 6 | Real vehicle photographs (12 named slots ready) | hero panel, gallery |
| 7 | Genuine Google reviews | reviews section (empty by design) |
| 8 | Public business name + permanent domain | branding, canonical URLs |

Photography is the biggest quality gap. Until it arrives the hero uses a labelled
illustration and the gallery uses named slots — never stock imagery passed off as
the actual vehicle.

The current live URL is an ephemeral `*.trycloudflare.com` address, not a permanent
domain.

---

## Known remaining work

- **No real 404 for missing assets** beyond pages (pages are covered; the branded
  page is served with a correct 404 status).
- **`og.png` not generated** — Pillow is not installed, so `build_static()` skips it
  and social previews fall back. Install Pillow (or ship a pre-made `og.png`) to fix.
- **`/guides/`** is linked as a breadcrumb parent for destinations; consider a proper
  destinations hub.
- **Duplicate-vehicle content**: the older "one 17-seat vehicle" copy on service
  pages still reads as a single-vehicle business, which will need reconciling if
  `FLEET_CONFIRMED` becomes `True`.

---

## Rollback

Snapshots are taken before each deploy:

```bash
ssh -i ~/.ssh/oci_hermes ubuntu@129.225.68.128
ls -lh /home/ubuntu/urbania-app-backup-*.tar.gz
# restore (excludes live data/ and .admin_token, which are untouched)
```
