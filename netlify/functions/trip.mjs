import crypto from "node:crypto";
import { getStore } from "@netlify/blobs";

const store = () => getStore({ name: "trip-requests", consistency: "strong" });
const hits = new Map();
const RATE_LIMIT = 12;
const RATE_WINDOW_MS = 10 * 60 * 1000;

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
    },
  });
}

function allowedOrigin(request) {
  const origin = request.headers.get("origin");
  return !origin || origin === "https://urbanloop.co" || origin === "https://www.urbanloop.co";
}

function rateAllowed(ip) {
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((at) => now - at < RATE_WINDOW_MS);
  if (recent.length >= RATE_LIMIT) {
    hits.set(ip, recent);
    return false;
  }
  recent.push(now);
  hits.set(ip, recent);
  return true;
}

function makeRef() {
  return `GT${crypto.randomBytes(3).toString("hex").toUpperCase()}`;
}

function text(value, max = 500) {
  return String(value ?? "").trim().slice(0, max);
}

function summary(data) {
  const bits = [text(data.trip_type || "trip", 80)];
  for (const key of ["Pickup point", "pickup", "Destination", "destination", "destinations"]) {
    if (data[key]) { bits.push(text(data[key], 120)); break; }
  }
  for (const key of ["Travel date", "date", "Start date", "date_from"]) {
    if (data[key]) { bits.push(text(data[key], 40)); break; }
  }
  for (const key of ["Passengers", "passengers", "Guests needing transport", "guests", "Team size", "team_size"]) {
    if (data[key]) { bits.push(`${text(data[key], 20)} pax`); break; }
  }
  return bits.join(" · ").slice(0, 180);
}

async function createTrip(request, context) {
  if (!allowedOrigin(request)) return json({ ok: false, error: "origin_not_allowed" }, 403);
  const ip = context.ip || request.headers.get("x-forwarded-for") || "unknown";
  if (!rateAllowed(ip)) return json({ ok: false, error: "rate_limited" }, 429);

  let data;
  try { data = await request.json(); } catch { return json({ ok: false, error: "invalid_json" }, 400); }
  if (!data || typeof data !== "object") return json({ ok: false, error: "empty" }, 400);
  if (text(data._hp, 100)) return json({ ok: true, ref: "GT000000" });

  const stage = text(data.stage, 40) || "quote_request";
  if (stage === "availability_check") {
    const ref = makeRef();
    const now = new Date().toISOString();
    await store().setJSON(ref, {
      ref,
      created_at: now,
      status: "AVAILABILITY_CHECK_REQUESTED",
      summary: summary(data),
      payload: data,
      source_page: text(data.source_page, 300),
    });
    return json({ ok: true, ref, status: "availability_check_requested" });
  }

  const name = text(data.contact_name, 120);
  const phone = text(data.contact_phone, 40);
  const consent = text(data.consent, 20).toLowerCase();
  if (!name || !phone || !["yes", "true"].includes(consent)) {
    return json({ ok: false, error: "missing_consent_or_contact" }, 400);
  }

  const ref = makeRef();
  const now = new Date().toISOString();
  const record = {
    ref,
    created_at: now,
    status: "NEW",
    summary: summary(data),
    payload: data,
    source_page: text(data.source_page, 300),
  };
  await store().setJSON(ref, record);
  return json({ ok: true, ref });
}

async function getStatus(request) {
  const ref = new URL(request.url).searchParams.get("ref") || "";
  if (!/^GT[0-9A-F]{6}$/.test(ref)) return json({ ok: false, error: "not_found" }, 404);
  const record = await store().get(ref, { type: "json" });
  if (!record) return json({ ok: false, error: "not_found" }, 404);
  return json({ ok: true, ref, status: record.status, created_at: record.created_at });
}

export default async (request, context) => {
  try {
    if (request.method === "POST") return await createTrip(request, context);
    if (request.method === "GET") return await getStatus(request);
    return json({ ok: false, error: "method_not_allowed" }, 405);
  } catch (error) {
    console.error("trip function failed", error);
    return json({ ok: false, error: "backend_unavailable" }, 503);
  }
};
