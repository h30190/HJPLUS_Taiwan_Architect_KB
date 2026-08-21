#!/usr/bin/env python3
"""
TABC 綠建材檢索與選用建議平台 — 本機開發伺服器
======================================
功能：
  1. 以 http://localhost:8888 提供 ../assets/green-material-toolkit.html
  2. 提供 POST /api/save-sets 端點：接收前端材料 Set JSON 並自動儲存至
     ../assets/exported_material_sets.json
  3. 提供 GET /api/get-sets 端點：供 Agent 確認最新 Set 內容

啟動方式：
  python local_server.py
  然後開啟瀏覽器前往 http://localhost:8888

移植自 REVIT_MCP_study 專案的 local_server.py，行為完全相同，僅將靜態頁面與
Set 儲存路徑改為此技能自己的 assets/ 目錄，不依賴 REVIT_MCP_study 專案或
Revit MCP。
"""

import http.server
import json
import os
import socketserver
import sys
import webbrowser
from urllib.parse import urlparse

PORT = 8888
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "..", "assets")
HTML_FILE = os.path.join(ASSETS_DIR, "green-material-toolkit.html")

# Set 檔是使用者的專案成品，預設寫到使用者家目錄下，不落在知識庫的 raw/ 樹裡；
# 可用 GREEN_MATERIAL_OUTPUT_DIR 指到任何專案路徑（例如某個 BIM 專案資料夾）。
OUTPUT_DIR = os.environ.get(
    "GREEN_MATERIAL_OUTPUT_DIR",
    os.path.join(os.path.expanduser("~"), ".green-material-toolkit"),
)
os.makedirs(OUTPUT_DIR, exist_ok=True)
SETS_FILE = os.path.join(OUTPUT_DIR, "exported_material_sets.json")


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # 只顯示 API 請求，過濾靜態資源雜訊
        if "/api/" in (args[0] if args else ""):
            print(f"  [API] {format % args}")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        # ── API: 取得最新 Sets ──────────────────────────────────────────────
        if path == "/api/get-sets":
            if os.path.exists(SETS_FILE):
                with open(SETS_FILE, "r", encoding="utf-8") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(data.encode("utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "尚未匯出任何 Set"}).encode())
            return

        # ── 主頁面：/ 或 /index.html ────────────────────────────────────────
        if path in ("", "/", "/index.html"):
            try:
                with open(HTML_FILE, "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
                return
            except FileNotFoundError:
                self.send_error(404, f"找不到 {HTML_FILE}")
                return

        # ── 靜態資源 fallback ────────────────────────────────────────────────
        file_path = os.path.join(ASSETS_DIR, path.lstrip("/"))
        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            ct_map = {
                ".html": "text/html; charset=utf-8",
                ".css": "text/css; charset=utf-8",
                ".js": "application/javascript; charset=utf-8",
                ".json": "application/json; charset=utf-8",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".svg": "image/svg+xml",
                ".ico": "image/x-icon",
                ".woff2": "font/woff2",
                ".ttf": "font/ttf",
            }
            content_type = ct_map.get(ext, "application/octet-stream")
            mode = "r" if content_type.startswith("text") or ext == ".json" else "rb"
            with open(file_path, mode, **({"encoding": "utf-8"} if mode == "r" else {})) as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            if isinstance(data, str):
                self.wfile.write(data.encode("utf-8"))
            else:
                self.wfile.write(data)
        else:
            self.send_error(404, f"找不到資源：{path}")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        # ── API: 儲存 Sets ───────────────────────────────────────────────────
        if path == "/api/save-sets":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)
                payload = json.loads(body.decode("utf-8"))

                with open(SETS_FILE, "w", encoding="utf-8") as f:
                    json.dump(payload, f, ensure_ascii=False, indent=2)

                set_names = list(payload.keys())
                print(f"\n  ✅ [自動同步] exported_material_sets.json 已更新")
                print(f"     包含 {len(set_names)} 個材料 Set：{', '.join(set_names)}")
                for name, val in payload.items():
                    items = val.get("items", [])
                    print(f"     【{name}】→ {len(items)} 項：{', '.join(items)}")
                print()

                resp = json.dumps({
                    "success": True,
                    "message": f"已自動儲存 {len(set_names)} 個材料 Set 至 exported_material_sets.json",
                    "sets": set_names
                }, ensure_ascii=False)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(resp.encode("utf-8"))

            except Exception as e:
                err = json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(err.encode("utf-8"))
        else:
            self.send_error(404)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    os.chdir(ASSETS_DIR)

    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        url = f"http://localhost:{PORT}"
        print("=" * 60)
        print("  🌿 TABC 綠建材檢索與選用建議平台 — 本機伺服器已啟動")
        print("=" * 60)
        print(f"  🌐 網址：{url}")
        print(f"  📁 資料目錄：{ASSETS_DIR}")
        print(f"  📤 Sets 自動存檔路徑：{SETS_FILE}")
        print()
        print("  ➜ 點擊網頁「📤 匯出至 Agent」按鈕後，")
        print("    exported_material_sets.json 會立即自動儲存，無需手動操作！")
        print()
        print("  ⌨️  按 Ctrl+C 停止伺服器")
        print("=" * 60)

        # 自動開啟瀏覽器
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  🛑 伺服器已停止。")
            sys.exit(0)


if __name__ == "__main__":
    main()
