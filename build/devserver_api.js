/* Local preview server: static files with Vercel's cleanUrls behaviour, plus
 * the real api/*.js handlers.
 *
 *   node build/devserver_api.js 4599            live CRM (needs MONDAY_API_TOKEN)
 *   NACRAVO_STUB_CRM=1 node build/devserver_api.js 4599   stubbed CRM
 *
 * With NACRAVO_STUB_CRM=1 the Monday API is replaced by an in-memory stub, so
 * the whole lead flow can be exercised end to end without a single test lead
 * reaching the operators. Not for production use.
 */
"use strict";

const http = require("http");
const fs = require("fs");
const path = require("path");
const url = require("url");

const ROOT = path.join(__dirname, "..");
const PORT = Number(process.argv[2] || 4599);

const TYPES = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".json": "application/json",
  ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
  ".svg": "image/svg+xml", ".webp": "image/webp", ".ico": "image/x-icon",
  ".xml": "application/xml", ".txt": "text/plain; charset=utf-8",
  ".webmanifest": "application/manifest+json",
};

/* ------------------------------------------------------------- CRM stub */
// Stub unless a real token is present, so a local run can never write a test
// lead into the operators' board by accident.
const STUB = process.env.NACRAVO_STUB_CRM === "1" || !process.env.MONDAY_API_TOKEN;
const stubItems = [];
if (STUB) {
  process.env.MONDAY_API_TOKEN = process.env.MONDAY_API_TOKEN || "stub-token";
  const realFetch = global.fetch;
  global.fetch = async (target, opts) => {
    if (String(target).indexOf("api.monday.com") === -1) return realFetch(target, opts);
    const body = JSON.parse(opts.body);
    if (/items_page_by_column_values/.test(body.query)) {
      const wanted = body.variables.val || body.variables.name;
      const hit = stubItems.find((it) => it.key === wanted);
      return { json: async () => ({ data: { items_page_by_column_values: {
        items: hit ? [{ id: hit.id, column_values: Object.keys(hit.vals).map((k) => ({ id: k, text: String(hit.vals[k]) })) }] : [],
      } } }) };
    }
    const vals = JSON.parse(body.variables.vals || "{}");
    const id = String(1000 + stubItems.length);
    const key = vals["text_mm6fxhqb"] || body.variables.name;
    stubItems.push({ id, key, name: body.variables.name, vals });
    console.log("\n[STUB CRM] item created:", body.variables.name);
    console.log(JSON.stringify(vals, null, 2));
    return { json: async () => ({ data: { create_item: { id } } }) };
  };
}

/* ------------------------------------------------------------- routing */
function resolveStatic(pathname) {
  if (pathname.endsWith("/")) pathname += "index";
  let p = path.join(ROOT, pathname);
  if (fs.existsSync(p) && fs.statSync(p).isFile()) return p;
  if (fs.existsSync(p + ".html")) return p + ".html";       // cleanUrls
  return null;
}

const server = http.createServer(async (req, res) => {
  const parsed = url.parse(req.url, true);
  const pathname = decodeURIComponent(parsed.pathname);

  if (pathname.startsWith("/api/")) {
    const file = path.join(ROOT, "api", path.basename(pathname) + ".js");
    if (!fs.existsSync(file)) { res.writeHead(404).end("no such function"); return; }
    let raw = "";
    req.on("data", (c) => { raw += c; if (raw.length > 200000) req.destroy(); });
    req.on("end", async () => {
      // Match Vercel's body parsing: JSON and urlencoded both arrive as objects.
      const ctype = String(req.headers["content-type"] || "");
      if (ctype.indexOf("form-urlencoded") > -1) {
        req.body = Object.fromEntries(new URLSearchParams(raw));
      } else {
        try { req.body = raw ? JSON.parse(raw) : {}; } catch (e) { req.body = {}; }
      }
      const shim = {
        _status: 200, _headers: {},
        setHeader(k, v) { this._headers[k] = v; return this; },
        status(c) { this._status = c; return this; },
        json(b) {
          res.writeHead(this._status, Object.assign({ "Content-Type": "application/json" }, this._headers));
          res.end(JSON.stringify(b));
          console.log("  " + req.method + " " + pathname + " -> " + this._status);
          return this;
        },
        send(b) {
          res.writeHead(this._status, Object.assign({ "Content-Type": "text/html; charset=utf-8" }, this._headers));
          res.end(b);
          console.log("  " + req.method + " " + pathname + " -> " + this._status + " (html)");
          return this;
        },
        end() { res.writeHead(this._status, this._headers); res.end(); return this; },
      };
      try {
        delete require.cache[require.resolve(file)];
        await require(file)(req, shim);
      } catch (e) {
        console.error(e);
        res.writeHead(500).end("handler threw");
      }
    });
    return;
  }

  const file = resolveStatic(pathname);
  if (!file) { res.writeHead(404, { "Content-Type": "text/html" }).end("<h1>404</h1>"); return; }
  const body = fs.readFileSync(file);
  res.writeHead(200, {
    "Content-Type": TYPES[path.extname(file)] || "application/octet-stream",
    "Cache-Control": "no-store",
  });
  res.end(body);
});

server.listen(PORT, () => {
  console.log("Nacravo preview on http://localhost:" + PORT + (STUB ? "  [CRM STUBBED]" : ""));
});
