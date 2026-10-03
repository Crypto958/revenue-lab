# Media — photos and video

Drop real files into these folders and the site upgrades **on the next build**.
No code change. Until a file exists, the component shows a clearly labelled
placeholder that names the file it is waiting for.

```
website/urbania/app/site/media/
├── hero/
│   ├── hero.mp4            cinematic hero video (H.264, muted, ~8-15s loop)
│   ├── hero.webm           optional, smaller; served first when present
│   └── hero-poster.jpg     REQUIRED with video: poster frame + the mobile still
├── gallery/                exterior / interior set
└── seating/                seating reference set
```

Rebuild after adding files:

```bash
cd website/urbania && python3 build_pages.py
# prints: MEDIA — hero video: True  hero poster: True  gallery: 12/12  seating: 12/12
```

---

## Hero video

Put `hero.mp4` in `media/hero/`. Behaviour:

- **Desktop** — autoplays muted, looping, inline, with `hero-poster.jpg` as the poster
- **Mobile (≤860px)** — the video is **not** loaded; `hero-poster.jpg` is shown instead.
  Autoplaying video on a phone costs data and battery and does not improve conversion.
- **`prefers-reduced-motion: reduce`** — same as mobile: still image only

Recommended: 1920×1080, H.264 MP4, 8–15 seconds, no audio track (it is muted
anyway, and an audio track only adds weight). Keep it under ~4 MB — trim hard.
Aim for one slow move across the vehicle or a short interior walkthrough, not a
montage.

If there is **no video but there is a poster**, the hero uses the still image.

## Gallery — `media/gallery/`

Exterior and general interior. Any of `.jpg .jpeg .png .webp .avif`; `.jpg` is assumed in the placeholder labels.

| File | Shot |
|---|---|
| `exterior-front.jpg` | front three-quarter |
| `exterior-side.jpg` | side profile |
| `exterior-rear.jpg` | rear three-quarter |
| `entry.jpg` | open door and step-in |
| `interior-rows.jpg` | seat rows from the front |
| `interior-aisle.jpg` | aisle and legroom |
| `interior-seats.jpg` | seat detail and trim |
| `ac.jpg` | air-conditioning vents |
| `charging.jpg` | charging points |
| `luggage.jpg` | luggage bay with cases |
| `night-interior.jpg` | interior at night |
| `driver-area.jpg` | driver area and dashboard |

## Seating references — `media/seating/`

The seating detail group buyers ask about most.

| File | Shot |
|---|---|
| `layout-1x1.jpg` | 1×1 (Maharaja) seat layout |
| `layout-2x1.jpg` | 2×1 seat layout |
| `seat-detail.jpg` | seat type and trim |
| `legroom.jpg` | legroom between rows |
| `aisle.jpg` | aisle width |
| `reclined.jpg` | seat pushed back / reclined |
| `headrest.jpg` | headrest and seat back |
| `charging.jpg` | per-seat charging point |
| `reading-light.jpg` | reading light and air vent |
| `rear-bench.jpg` | rear row / last bench |
| `entry-step.jpg` | entry step and grab handle |
| `luggage-bay.jpg` | luggage bay with cases |

---

## Provenance — read this before adding images

Adding a file does **not** automatically make the site claim it is your vehicle.
That is controlled by one flag in `site_data.py`:

```python
ASSETS_ARE_OUR_VEHICLE = False
```

| Flag | Hero caption | `alt` text |
|---|---|---|
| `False` | "Photograph/Footage of the Force Urbania **model**" | "representative image of the model, not a photograph of this operator's vehicle" |
| `True` | "Photograph/Footage of **our** Force Urbania" | "used for pre-booked trips in Hyderabad" |

Set it to `True` **only** for imagery of your own vehicle. If you supply
manufacturer or library images, leave it `False` — the site will show them as
representative of the model, which is honest and still gives you a premium hero.

The rule this protects: `docs/FACTS_LEDGER.md` forbids presenting an image as
the actual vehicle when it is not. Getting that wrong is a customer-trust and
consumer-law problem, not a design preference.

## Optimisation

- Export at ~1600–2000px on the long edge for gallery/seating (they render at
  ~400–800px, so 2× is plenty).
- Strip EXIF. Phone photos often carry GPS coordinates of your home or yard —
  `exiftool -all= *.jpg` or export "without metadata".
- Target under ~250 KB each. `cwebp -q 80 in.jpg -o out.webp` gives a big win.
- Real file sizes are **not** checked by the build; keep them sane by hand.

## What the tests enforce

- Placeholder state renders honestly: no fabricated claims, no fabricated figures.
- Every page's markup stays balanced (an unclosed `<div>` previously collapsed the
  quote bar).
- No page renders a rupee figure that was never supplied.
