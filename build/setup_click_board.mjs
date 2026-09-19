/* One-time setup of the Monday "Ad Click Log" board used by api/click.js.
 *
 *   MONDAY_API_TOKEN=... node build/setup_click_board.mjs            (dry run)
 *   MONDAY_API_TOKEN=... node build/setup_click_board.mjs --apply    (create)
 *
 * Idempotent: an existing board with this name in the workspace is reused and
 * only missing columns are added. Prints the board id to put in Vercel as
 * CLICK_BOARD_ID. Column ids are fixed because api/click.js writes to them.
 */
const WORKSPACE = "7227449"; // Nacravo CRM Development
const NAME = "Ad Click Log";
const COLUMNS = [
  ["clk_ref", "Attribution Ref"], ["clk_action", "Action"], ["clk_gclid", "GCLID"],
  ["clk_gbraid", "GBRAID"], ["clk_wbraid", "WBRAID"], ["clk_fbclid", "FBCLID"],
  ["clk_campaign", "Campaign ID"], ["clk_adgroup", "Ad Group ID"], ["clk_keyword", "Keyword"],
  ["clk_match", "Match Type"], ["clk_network", "Network"], ["clk_landing", "Landing Page"],
  ["clk_tap_page", "Tap Page"], ["clk_click_time", "Click Time (UTC)"], ["clk_tap_time", "Tap Time (UTC)"],
  ["clk_device", "Device"], ["clk_utm_source", "UTM Source"], ["clk_utm_medium", "UTM Medium"],
  ["clk_utm_content", "UTM Content"], ["clk_ad_consent", "Ad Consent"],
];
const token = (process.env.MONDAY_API_TOKEN || "").trim();
if (!token) { console.error("Set MONDAY_API_TOKEN"); process.exit(1); }
const apply = process.argv.includes("--apply");
async function gql(query, variables) {
  const r = await fetch("https://api.monday.com/v2", { method: "POST",
    headers: { "Content-Type": "application/json", Authorization: token, "API-Version": "2024-10" },
    body: JSON.stringify({ query, variables }) });
  const j = await r.json(); if (j.errors) throw new Error(JSON.stringify(j.errors)); return j.data;
}
const found = await gql(`query($w:[ID!]){boards(workspace_ids:$w,limit:200){id name columns{id}}}`, { w: [WORKSPACE] });
let board = found.boards.find((b) => b.name === NAME);
if (!board) {
  console.log(apply ? "Creating board" : "[dry run] would create board", NAME);
  if (!apply) process.exit(0);
  const d = await gql(`mutation($n:String!,$w:ID!,$d:String){create_board(board_name:$n,board_kind:public,workspace_id:$w,description:$d,empty:true){id}}`,
    { n: NAME, w: WORKSPACE, d: "System-managed by nacravo.com /api/click. One row per WhatsApp/phone tap from a paid ad visit: joins the Ref code to the ad click. No personal data. Do not edit by hand." });
  board = { id: d.create_board.id, columns: [] };
}
const have = new Set(board.columns.map((c) => c.id));
for (const [id, title] of COLUMNS) {
  if (have.has(id)) continue;
  console.log(apply ? "Adding" : "[dry run] would add", id, title);
  if (apply) await gql(`mutation($b:ID!,$id:String!,$t:String!){create_column(board_id:$b,id:$id,title:$t,column_type:text){id}}`, { b: board.id, id, t: title });
}
console.log("CLICK_BOARD_ID =", board.id);
