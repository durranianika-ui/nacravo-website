/* POST /api/click-map — persist the ad-click → attribution mapping.
 *
 * Called fire-and-forget by assets/nacravo-attr.js, only when a visit
 * actually carries a Google click id (gclid/gbraid/wbraid). Writes one item
 * to the Monday.com board "11 - Click Map" (5102697760), item name = the
 * NCR reference token that also travels inside the visitor's WhatsApp
 * message. That makes the mapping WhatsApp Ref -> GCLID recoverable by the
 * CRM, which is what offline conversion uploads to Google Ads require.
 *
 * Requires the MONDAY_API_TOKEN environment variable (Vercel project
 * settings). Until it is set, this endpoint answers 503 and the site
 * behaves exactly as before — the client ignores failures.
 *
 * No PII is handled here: click ids, utm values, a path and a timestamp.
 */

const BOARD_ID = "5102697760";
const COLS = {
  gclid: "text_mm6fx6s7",
  gbraid: "text_mm6f1m9j",
  wbraid: "text_mm6fvy48",
  utm_campaign: "text_mm6frrxv",
  utm_term: "text_mm6f2mh4",
  landing_page: "text_mm6ffcag",
  landed_at: "text_mm6f651r",
  utm_source: "text_mm6f7cm0",
};
const REF_RE = /^NCR-[A-Z0-9]{2}-[A-Z0-9]{1,8}-[A-Z0-9]{2}$/;

function clean(v, max) {
  if (typeof v !== "string") return undefined;
  const s = v.trim();
  if (!s || s.length > max) return undefined;
  // Column values are plain text; strip anything that is not printable ASCII.
  return /^[\x20-\x7E]+$/.test(s) ? s : undefined;
}

async function monday(token, query, variables) {
  const r = await fetch("https://api.monday.com/v2", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: token },
    body: JSON.stringify({ query, variables }),
  });
  const j = await r.json();
  if (j.errors) throw new Error(JSON.stringify(j.errors).slice(0, 500));
  return j.data;
}

module.exports = async (req, res) => {
  if (req.method !== "POST") { res.status(405).json({ error: "POST only" }); return; }

  const token = process.env.MONDAY_API_TOKEN;
  if (!token) { res.status(503).json({ error: "mapping store not configured" }); return; }

  const b = req.body && typeof req.body === "object" ? req.body : {};
  const ref = clean(b.ref, 24);
  if (!ref || !REF_RE.test(ref)) { res.status(400).json({ error: "bad ref" }); return; }

  const vals = {};
  if (clean(b.gclid, 200)) vals[COLS.gclid] = clean(b.gclid, 200);
  if (clean(b.gbraid, 200)) vals[COLS.gbraid] = clean(b.gbraid, 200);
  if (clean(b.wbraid, 200)) vals[COLS.wbraid] = clean(b.wbraid, 200);
  if (!vals[COLS.gclid] && !vals[COLS.gbraid] && !vals[COLS.wbraid]) {
    res.status(400).json({ error: "no click id" }); return;
  }
  if (clean(b.utm_campaign, 60)) vals[COLS.utm_campaign] = clean(b.utm_campaign, 60);
  if (clean(b.utm_term, 120)) vals[COLS.utm_term] = clean(b.utm_term, 120);
  if (clean(b.utm_source, 40)) vals[COLS.utm_source] = clean(b.utm_source, 40);
  if (clean(b.landing_page, 120)) vals[COLS.landing_page] = clean(b.landing_page, 120);
  if (clean(b.landed_at, 40)) vals[COLS.landed_at] = clean(b.landed_at, 40);

  try {
    // Idempotency: one item per ref.
    const existing = await monday(token,
      `query ($board: ID!, $name: CompareValue!) {
         items_page_by_column_values (board_id: $board, limit: 1,
           columns: [{column_id: "name", column_values: [$name]}]) { items { id } } }`,
      { board: BOARD_ID, name: ref });
    if (existing.items_page_by_column_values.items.length > 0) {
      res.status(200).json({ ok: true, dup: true }); return;
    }
    const created = await monday(token,
      `mutation ($board: ID!, $name: String!, $vals: JSON!) {
         create_item (board_id: $board, item_name: $name, column_values: $vals) { id } }`,
      { board: BOARD_ID, name: ref, vals: JSON.stringify(vals) });
    res.status(201).json({ ok: true, id: created.create_item.id });
  } catch (e) {
    res.status(502).json({ error: "store write failed" });
  }
};
