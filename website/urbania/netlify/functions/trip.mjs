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

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>\"]/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;",
  })[char]);
}

function callbackSummary(data, ref) {
  const value = (...keys) => {
    for (const key of keys) if (data[key]) return text(data[key], 180);
    return "Not provided";
  };
  return [
    ["Name", value("contact_name")],
    ["Phone", value("contact_phone")],
    ["Trip type", value("trip_type")],
    ["Route", `${value("Pickup point", "pickup", "main_pickup", "address")} → ${value("Destination(s)", "Destination", "destinations", "destination", "venue", "temple")}`],
    ["Date", value("Travel date", "date", "Start date", "date_from")],
    ["Group size", value("Passengers", "passengers", "Guests needing transport", "guests", "Team size", "team_size")],
    ["Reference", ref],
  ];
}

async function sendOwnerAlert(data, ref) {
  const token = process.env.ZEPTOMAIL_SEND_MAIL_TOKEN;
  const fromAddress = process.env.ZEPTOMAIL_FROM_ADDRESS;
  if (!token || !fromAddress) return;
  const fields = callbackSummary(data, ref);
  const rows = fields.map(([label, value]) => `<tr><th align="left">${escapeHtml(label)}</th><td>${escapeHtml(value)}</td></tr>`).join("");
  const textBody = fields.map(([label, value]) => `${label}: ${value}`).join("\n");
  const response = await fetch("https://api.zeptomail.com/v1.1/email", {
    method: "POST",
    headers: {
      "Authorization": `zoho-enczapikey ${token}`,
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    signal: AbortSignal.timeout(8000),
    body: JSON.stringify({
      from: { address: fromAddress, name: "UrbanLoop Enquiries" },
      to: [{ email_address: { address: "fca.abhi007@gmail.com", name: "UrbanLoop" } }],
      subject: `New vehicle request ${ref}`,
      textbody: textBody,
      htmlbody: `<p>A customer requested vehicle options. Follow up using the saved request.</p><table>${rows}</table>`,
    }),
  });
  if (!response.ok) throw new Error(`ZeptoMail returned HTTP ${response.status}`);
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
  if (stage === "availability_check") return json({ ok: false, error: "consent_required" }, 400);

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
  try {
    await sendOwnerAlert(data, ref);
  } catch (error) {
    // The durable request is the source of truth. A mail provider outage must
    // never make a saved customer request appear to have failed.
    console.error("trip owner alert failed", error?.message || "unknown error");
  }
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
