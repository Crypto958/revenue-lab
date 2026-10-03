#!/usr/bin/env python3
"""Westbridge explainer video renderer.
Renders 1280x720 @30fps frames with Pillow, then encodes with ffmpeg and muxes
the six narration clips. Scene length = that scene's narration length + tail.
"""
import os, subprocess, math
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(OUT, "frames")
os.makedirs(FR, exist_ok=True)
W, H, FPS = 1280, 720, 30

AUDIO = [
    "/home/ubuntu/.hermes/cache/audio/tts_20261002_221853_540759.ogg",
    "/home/ubuntu/.hermes/cache/audio/tts_20261002_222051_581475.ogg",
    "/home/ubuntu/.hermes/cache/audio/tts_20261002_222054_701328.ogg",
    "/home/ubuntu/.hermes/cache/audio/tts_20261002_222056_504958.ogg",
    "/home/ubuntu/.hermes/cache/audio/tts_20261002_222058_501700.ogg",
    "/home/ubuntu/.hermes/cache/audio/tts_20261002_222100_408669.ogg",
]

def dur(p):
    o = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","default=nw=1:nk=1",p], capture_output=True, text=True)
    return float(o.stdout.strip())

BG      = (5, 7, 14)
INK     = (244, 247, 252)
DIM     = (147, 166, 192)
FAINT   = (99, 118, 143)
ACCENT  = (59, 123, 255)
LINE    = (30, 36, 51)
BUB_IN  = (17, 22, 34)

F = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(F + name, size)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS  = lambda s: font("DejaVuSans.ttf", s)
SANSB = lambda s: font("DejaVuSans-Bold.ttf", s)
MONO  = lambda s: font("DejaVuSansMono.ttf", s)

def ease(t):  # ease-out cubic
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def ap(p, a, b):  # sub-progress
    if b <= a: return 0.0
    return ease((p - a) / (b - a))

def txt(d, xy, s, f, fill, anchor="la", a=1.0):
    if a <= 0: return
    if a >= 1:
        d.text(xy, s, font=f, fill=fill, anchor=anchor); return
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(xy, s, font=f, fill=fill, anchor=anchor)
    layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    d._image.alpha_composite(layer)

def slide(d, xy, s, f, fill, p, dy=14, anchor="la"):
    """text that fades up into place"""
    a = ap(p, 0, 1)
    if a <= 0: return
    x, y = xy[0], xy[1] + (1 - a) * dy
    txt(d, (x, y), s, f, fill, anchor, a)

def bg(d):
    d.rectangle([0, 0, W, H], fill=BG)
    # one hairline rule, echoing the site
    d.line([80, 96, W - 80, 96], fill=LINE, width=1)
    txt(d, (80, 62), "W E S T B R I D G E", MONO(13), FAINT, "la", 0.9)

def phone(d, x, y, w, h, p):
    a = ap(p, 0, .4)
    if a <= 0: return
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([x, y, x + w, y + h], 26, fill=(10, 14, 24, int(255 * a)),
                         outline=(40, 50, 72, int(255 * a)), width=1)
    ld.rounded_rectangle([x + w / 2 - 26, y + 13, x + w / 2 + 26, y + 18], 9,
                         fill=(50, 60, 82, int(255 * a)))
    d._image.alpha_composite(layer)

def bubble(d, x, y, w, s, f, out, a, tail=0):
    if a <= 0: return
    pad_x, pad_y = 16, 12
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    bb = tmp.textbbox((0, 0), s, font=f)
    th = bb[3] - bb[1]
    hgt = th + pad_y * 2
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    col = (ACCENT[0], ACCENT[1], ACCENT[2], int(255 * a)) if out else (17, 22, 34, int(255 * a))
    ld.rounded_rectangle([x, y, x + w, y + hgt], 14, fill=col)
    d._image.alpha_composite(layer)
    txt(d, (x + pad_x, y + pad_y - bb[1]), s, f, INK if out else (222, 232, 246), "la", a)

def accent_bar(d, y, p, w=280):
    a = ap(p, 0, 1)
    d.rectangle([80, y, 80 + w * a, y + 3], fill=ACCENT)

# ----------------------------------------------------------------- scenes

def s_intro(d, p):
    bg(d)
    y = 250 + (1 - ap(p, .0, .5)) * 18
    txt(d, (W / 2, y), "Westbridge", SERIF(96), INK, "mm", ap(p, 0, .5))
    txt(d, (W / 2, y + 92), "W E   B R I N G   C L I E N T S", MONO(17), DIM, "mm", ap(p, .25, .75))
    accent_bar(d, y + 128, ap(p, .45, 1), w=320)
    txt(d, (W / 2, 470), "Enquiry recovery  ·  Hyderabad", MONO(13), FAINT, "mm", ap(p, .5, 1))

def s_problem(d, p):
    bg(d)
    phone(d, 110, 150, 340, 460, p)
    bubble(d, 135, 230, 280, "Hi - do you have a", SANS(17), False, ap(p, .12, .3))
    bubble(d, 135, 268, 260, "slot this Saturday?", SANS(17), False, ap(p, .16, .34))
    # the silence
    txt(d, (300, 400), "Sat  9:04 pm", MONO(15), DIM, "mm", ap(p, .3, .45))
    txt(d, (300, 430), "no reply", MONO(15), FAINT, "mm", ap(p, .4, .5))
    txt(d, (300, 470), "Mon  10:12 am", MONO(15), DIM, "mm", ap(p, .55, .7))
    txt(d, (300, 512), "still no reply", MONO(15), FAINT, "mm", ap(p, .62, .78))
    slide(d, (540, 250), "A customer writes on", SANS(30), INK, ap(p, .3, .7))
    slide(d, (540, 292), "Saturday evening.", SANS(30), INK, ap(p, .36, .76))
    slide(d, (540, 360), "Nobody answers until Monday.", SANS(26), DIM, ap(p, .6, .95))
    slide(d, (540, 410), "By then they have booked elsewhere.", SANS(26), DIM, ap(p, .68, 1))
    accent_bar(d, 500, ap(p, .8, 1), w=200)

def s_cost(d, p):
    bg(d)
    slide(d, (110, 210), "Every unanswered enquiry is a", SANS(28), DIM, ap(p, 0, .5))
    n = int(ap(p, .1, .85) * 12)
    txt(d, (110, 262), str(n), SERIF(150), ACCENT, "la", 1.0)
    txt(d, (110, 430), "enquiries left unanswered this week", MONO(15), FAINT, "la", ap(p, .3, .8))
    slide(d, (110, 490), "Each one is a customer who chose someone faster.", SANS(25), INK, ap(p, .5, 1))
    slide(d, (110, 540), "Most businesses never even see them leave.", SANS(25), DIM, ap(p, .68, 1))

def s_fix(d, p):
    bg(d)
    phone(d, 110, 150, 340, 460, p)
    bubble(d, 135, 205, 280, "Hi - do you have a", SANS(17), False, ap(p, .1, .28))
    bubble(d, 135, 243, 260, "slot this Saturday?", SANS(17), False, ap(p, .14, .32))
    bubble(d, 105, 300, 300, "Yes - Saturday 4:30pm", SANS(17), True, ap(p, .3, .5))
    bubble(d, 105, 338, 250, "is free. Hold it for you?", SANS(17), True, ap(p, .34, .54))
    txt(d, (300, 400), "replied in 8 seconds  ·  9:04 pm", MONO(13), ACCENT, "mm", ap(p, .5, .7))
    bubble(d, 135, 450, 280, "Appointment confirmed", SANS(16), False, ap(p, .62, .78))
    txt(d, (300, 540), "reminder sent 24h before", MONO(12), FAINT, "mm", ap(p, .72, .9))
    slide(d, (540, 240), "Westbridge answers", SANS(31), INK, ap(p, .15, .5))
    slide(d, (540, 284), "in minutes.", SANS(31), ACCENT, ap(p, .2, .55))
    slide(d, (540, 356), "Qualified automatically.", SANS(25), DIM, ap(p, .42, .72))
    slide(d, (540, 402), "Booked, with a reminder.", SANS(25), DIM, ap(p, .52, .82))
    slide(d, (540, 448), "No one has to remember.", SANS(25), DIM, ap(p, .62, .95))
    accent_bar(d, 500, ap(p, .7, 1), w=200)

def s_outcome(d, p):
    bg(d)
    rows = [("Quiet quotes get followed up.", .05),
            ("Happy customers get asked for a review.", .3),
            ("Fewer enquiries lost.", .55)]
    y = 250
    for s, st in rows:
        slide(d, (140, y), s, SANS(30), INK, ap(p, st, st + .3))
        d.rectangle([80, y + 16, 100, y + 19], fill=ACCENT)
        y += 74
    txt(d, (140, 510), "MORE BOOKINGS WON", MONO(15), ACCENT, "la", ap(p, .8, 1))

def s_cta(d, p):
    bg(d)
    txt(d, (W / 2, 250), "Westbridge", SERIF(84), INK, "mm", ap(p, 0, .45))
    txt(d, (W / 2, 336), "W E   B R I N G   C L I E N T S", MONO(16), DIM, "mm", ap(p, .25, .7))
    accent_bar(d, 372, ap(p, .4, .9), w=300)
    txt(d, (W / 2, 450), "Ask for your free enquiry audit", SANS(26), INK, "mm", ap(p, .55, .95))
    txt(d, (W / 2, 505), "fca.abhi007@gmail.com", MONO(16), ACCENT, "mm", ap(p, .68, 1))

SCENES = [s_intro, s_problem, s_cost, s_fix, s_outcome, s_cta]

# ----------------------------------------------------------------- render
durs = [dur(p) for p in AUDIO]
print("narration durations:", [round(x, 2) for x in durs], "total", round(sum(durs), 1), "s")

idx = 0
for sc, dsec in zip(SCENES, durs):
    total = dsec + 0.7
    n = int(total * FPS)
    for i in range(n):
        img = Image.new("RGBA", (W, H), (5, 7, 14, 255))
        d = ImageDraw.Draw(img)
        d._image = img
        sc(d, i / max(1, n - 1))
        frame = img.convert("RGB")
        frame.save(os.path.join(FR, "f%05d.png" % idx))
        idx += 1
print("frames:", idx)

# ----------------------------------------------------------------- encode
silent = os.path.join(OUT, "westbridge_silent.mp4")
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),
                "-i", os.path.join(FR,"f%05d.png"), "-c:v","libx264","-preset","medium",
                "-crf","20","-pix_fmt","yuv420p", silent], check=True)

# concat narration, then mux
voice = os.path.join(OUT, "westbridge_voice.m4a")
inputs = []
for p in AUDIO: inputs += ["-i", p]
fc = "".join("[%d:a]" % i for i in range(len(AUDIO))) + "concat=n=%d:v=0:a=1[a]" % len(AUDIO)
subprocess.run(["ffmpeg","-y","-loglevel","error"] + inputs +
               ["-filter_complex", fc, "-map","[a]","-c:a","aac","-b:a","160k", voice], check=True)

final = os.path.join(OUT, "westbridge_explainer.mp4")
subprocess.run(["ffmpeg","-y","-loglevel","error","-i", silent, "-i", voice,
                "-c:v","copy","-c:a","aac","-shortest", final], check=True)
print("FINAL:", final, os.path.getsize(final), "bytes")
