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
- The shipped hero poster is **portrait**, matching its box (see the aspect trap below).
- Shipped media never claims ownership while `ASSETS_ARE_OUR_VEHICLE` is False.

---

## Shipped state

Four files ship, all cropped from the **v2 master** — `brand/source/urbanloop-master-v2.png`
(1672×941), supplied by the owner on 2026-10-03. It is the same scene as v1 but
**without the burned-in play button**, which removes the constraint that shaped
every earlier crop.

| Slot | File | Crop | Ships as | Box ratio |
|---|---|---|---|---|
| hero background | `hero/hero-split.jpg` | `crop=1672:812:0:65` | 1672×812 | hero ~2.06 |
| hero still (fallback) | `hero/hero-poster.jpg` | `crop=672:941:500:0` | 672×941 | 0.714 portrait |
| gallery | `gallery/exterior-front.jpg` | `crop=1000:750:250:60` | 1000×750 | 1.333 (4:3) |
| gallery | `gallery/exterior-side.jpg` | `crop=1000:750:672:60` | 1000×750 | 1.333 (4:3) |

The hero source (1672 wide) is now **wider than the 1440px it fills**, so it
downscales and stays sharp. The earlier hero was a 747px crop upscaled ~1.9× and
visibly soft — that is fixed.

These are **AI-generated concept imagery, not photographs of the actual vehicle**,
and the site captions them accordingly. They must be replaced with real photography
(see `PHOTO_SHOT_LIST.md`).

## One live hazard in the hero

The vehicle in this image carries its **own liveried UrbanLoop wordmark** on the
bodywork. With the headline centred, that wordmark lands directly behind the body
copy and reads as a second, half-obscured brand.

Handled with a radial pool of shade behind the copy (`.hx-in::before`), which
suppresses it without darkening the whole photograph. Two things to know if you
touch that rule:

- It uses `radial-gradient(closest-side, …)` so the ellipse reaches zero alpha
  **exactly at its own box edge**. A percentage-sized gradient instead leaves a
  faint rectangular seam, which shipped once and was visible.
- Do **not** add `overflow:hidden` to `.hx` to contain it. The quote bar hangs
  below the hero on a negative margin and would be clipped.

## The v1 play-button problem — resolved, kept for the record

The **v1** master (`brand/source/urbanloop-hero-original.png`) has a play button
burned in at x 744–912, y 409–577. It could not be removed cleanly with the tools
here, and both attempts were rendered and rejected:

- **Interpolating fill** (`ffmpeg -vf delogo`) — obvious vertical streaking, because
  the circle crosses the window/pillar edge.
- **Clone patch** (mirrored pixels + feathered mask, `brand/patch_play_button.py`) —
  far better, but leaves a white arc from the ring's edge *and* duplicates the door
  handle and UL monogram.

That constraint is now moot: v2 is clean. **If you ever fall back to v1, every crop
must again exclude x 744–912.** Verify a replacement master before trusting it:

```bash
# inspect the zone where the button sits in v1
ffmpeg -y -i MASTER.png -vf "crop=280:280:700:350" /tmp/buttonzone.png
```

## The aspect trap (cost us a shipped defect)

The hero still box measures **471×660 → ratio 0.714 (portrait)** and renders with
`object-fit: cover`. A landscape source therefore gets scaled to fill the height and
then centre-cropped to roughly **40% of its width**. Shipping the first (16:9)
poster cut the wordmark to `anLoop` / `R GROUP MOBILITY` — a truncated brand name on
the homepage.

Match crops to the box they land in, and check it:

```bash
# what the box actually is
node -e "..."   # or: read .hv-still's getBoundingClientRect in tools/shoot.py
```

`ShippedMediaTests.test_shipped_hero_poster_is_portrait_like_its_box` now parses the
JPEG's SOF marker directly (there is no Pillow in this project) and fails on a
landscape poster. It was verified to fail by putting the landscape file back.
