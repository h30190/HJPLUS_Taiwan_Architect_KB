#!/usr/bin/env python3
"""
綠建材選用說明書產生引擎
========================================================================
根據使用者在檢索平台建立的材料 Set（一組 TABC 核定字號 licno 清單），
比對 assets/tabc_master_database.json 取得每項建材的完整標章資料，
產生一份可放入案件文件的「建材選用說明書」（Markdown），並將摘要回寫至
assets/exported_material_sets.json 供平台頁面顯示。

這是 REVIT_MCP_study 專案 generate_revit_injection_plan.py 的移植版本：
拿掉 Revit 品類/構造層/共享參數等 Revit 專屬對映邏輯，只保留「讀取 Set →
比對主資料庫 → 產出人類可讀的選用建議」這一段，不含任何 Revit 或其他
BIM 軟體的寫入動作。
"""

import json
import os
import re
import datetime

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(WORKSPACE, "..", "assets")
DB_PATH = os.path.join(ASSETS_DIR, "tabc_master_database.json")

# Set 檔與說明書是使用者的專案成品，預設寫到使用者家目錄下，不落在知識庫的
# raw/ 樹裡；可用 GREEN_MATERIAL_OUTPUT_DIR 指到任何專案路徑，需與
# local_server.py 使用同一個值才能讀寫同一份 Set 檔。
OUTPUT_DIR = os.environ.get(
    "GREEN_MATERIAL_OUTPUT_DIR",
    os.path.join(os.path.expanduser("~"), ".green-material-toolkit"),
)
os.makedirs(OUTPUT_DIR, exist_ok=True)
SETS_FILE = os.path.join(OUTPUT_DIR, "exported_material_sets.json")
REPORT_PATH = os.path.join(OUTPUT_DIR, "Material_Advisory_Report.md")


def load_database():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_exported_sets():
    if os.path.exists(SETS_FILE):
        try:
            with open(SETS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _normalize_licno(licno: str) -> str:
    """去除尾端的 (續)/(增)/(變) 等註記後綴，僅供比對使用；輸出一律採用資料庫
    記錄原始（帶後綴）的 licno。"""
    if not licno:
        return licno
    return re.sub(r"[（(].*?[）)]\s*$", "", licno).strip()


def _find_set_entry(set_name: str, sets: dict):
    if set_name in sets:
        return sets[set_name]
    for key, val in sets.items():
        if set_name in key or key in set_name:
            return val
    return None


# ── 建議適用部位：依 subCategory 給出通用建築語彙描述，不對映任何特定軟體的
# 品類/構造層/元件系統。跨用途的材料（如混凝土、玻璃）誠實標示為「建議人工
# 確認」，不做無依據的臆測。──
_SUB_CATEGORY_USAGE = {
    "塗料類": "牆面或天花板塗裝面材",
    "地板類": "地坪面材（依材質可能為地磚、木地板、塑木等，建議依產品規格確認施工基底需求）",
    "牆壁類": "牆體結構或牆面飾材（依成分可能為結構板材或面材，建議依產品規格確認）",
    "天花板類": "天花板飾面板材",
    "隔音緩衝類": "樓地板或牆體隔音緩衝層",
    "透水鋪面類": "戶外透水鋪面或人行步道",
}


def suggest_usage(sub_cat: str, title: str) -> str:
    if sub_cat in _SUB_CATEGORY_USAGE:
        return _SUB_CATEGORY_USAGE[sub_cat]
    return "跨用途通用建材，建議依產品規格與案件實際使用部位人工確認"


def generate_material_advisory(set_name: str, licno_list=None, user_intent: str = "") -> dict:
    """比對 Set 內的 licno 清單與主資料庫，產出建材選用說明書資料結構。"""
    database = load_database()

    extracted = []
    if isinstance(licno_list, list) and licno_list:
        extracted = licno_list
    elif isinstance(licno_list, str):
        extracted = re.findall(r"GBM\d+", licno_list)
    if not extracted and user_intent:
        extracted = re.findall(r"GBM\d+", user_intent)
    if not extracted:
        sets = load_exported_sets()
        entry = _find_set_entry(set_name, sets)
        if entry:
            extracted = entry.get("items", [])

    # 比對 Master DB：先精確比對，找不到的裸編號再用去除 (續)/(增)/(變) 後綴的
    # 正規化比對回補；輸出一律採用資料庫記錄原始（帶後綴）的 licno。
    licno_set = set(extracted)
    matched = [item for item in database if item.get("licno") in licno_set]
    matched_licnos = {item.get("licno") for item in matched}
    unmatched = [l for l in licno_set if l not in matched_licnos]
    if unmatched:
        normalized_targets = {_normalize_licno(l) for l in unmatched}
        covered = set()
        for item in database:
            raw_licno = item.get("licno")
            if raw_licno in matched_licnos:
                continue
            norm = _normalize_licno(raw_licno)
            if norm in normalized_targets and norm not in covered:
                matched.append(item)
                covered.add(norm)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    advisory_id = f"ADVISORY-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    material_entries = []
    for item in matched:
        sub_cat = item.get("subCategory", "")
        material_entries.append({
            "licno": item.get("licno"),
            "title": item.get("title"),
            "company": item.get("company"),
            "category": item.get("category"),
            "subCategory": sub_cat,
            "period": item.get("period"),
            "cnsSpec": item.get("cnsSpec"),
            "qualifiedItems": item.get("qualifiedItems"),
            "testItems": item.get("testItems"),
            "suggestedUsage": suggest_usage(sub_cat, item.get("title", "")),
        })

    unmatched_still = [l for l in licno_set if l not in {m["licno"] for m in material_entries}
                        and _normalize_licno(l) not in {_normalize_licno(m["licno"]) for m in material_entries}]

    advisory = {
        "advisoryId": advisory_id,
        "setName": set_name,
        "generatedAt": timestamp,
        "userIntent": user_intent,
        "totalMaterialsCount": len(material_entries),
        "materials": material_entries,
        "unmatchedLicnos": unmatched_still,
    }

    _write_markdown_report(advisory)
    print(f"Successfully generated advisory {advisory_id} with {len(material_entries)} materials: "
          f"{[m['licno'] for m in material_entries]}.")
    return advisory


def _write_markdown_report(advisory: dict):
    lines = [
        "# 🌿 建材選用說明書",
        "",
        f"- **說明書編號**：`{advisory['advisoryId']}`",
        f"- **材料 Set 名稱**：`{advisory['setName']}`",
        f"- **產生時間**：`{advisory['generatedAt']}`",
    ]
    if advisory.get("userIntent"):
        lines.append(f"- **需求備註**：{advisory['userIntent']}")
    lines += ["", "---", "", "## 材料清單", ""]

    for idx, m in enumerate(advisory["materials"], 1):
        lines += [
            f"### [{idx}] {m['title']} (`{m['licno']}`)",
            f"- **申請廠商**：{m['company']}",
            f"- **標章分類**：{m['category']}綠建材（{m['subCategory']}）",
            f"- **有效期限**：{m['period']}",
            f"- **建議適用部位**：{m['suggestedUsage']}",
            f"- **CNS 試驗依據**：{m['cnsSpec']}",
            f"- **合格項目**：{m['qualifiedItems']}",
            f"- **試驗項目**：{m['testItems']}",
            "",
        ]

    if advisory.get("unmatchedLicnos"):
        lines += ["---", "", "## ⚠️ 未能比對之核定字號", ""]
        for l in advisory["unmatchedLicnos"]:
            lines.append(f"- `{l}`：主資料庫查無此字號，建議確認字號是否輸入正確，或執行更新腳本重新抓取最新資料。")
        lines.append("")

    lines += [
        "---",
        "",
        "> 本說明書依 TABC 綠建材標章公開資料自動彙整，僅供案件文件參考，正式送審請以 TABC 官方核定文件為準。",
    ]

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_back_to_set_manager(set_name: str, advisory: dict, purpose_override: str = ""):
    """將說明書摘要回寫至 exported_material_sets.json，供平台頁面顯示。"""
    sets = load_exported_sets()

    materials_summary = "、".join(
        f"{m['title']} ({m['licno']})" for m in advisory["materials"]
    )
    purpose = purpose_override or f"已為 {len(advisory['materials'])} 項綠建材產生選用說明書：{materials_summary}"

    usage_lines = [f"{m['licno']}：{m['suggestedUsage']}" for m in advisory["materials"]]
    planned_actions = "\n".join(usage_lines) if usage_lines else ""

    matched_key = None
    for key in sets:
        if key == set_name or set_name in key or key in set_name:
            matched_key = key
            break
    if matched_key is None:
        matched_key = set_name
        sets[matched_key] = {
            "name": set_name,
            "createdAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": [m["licno"] for m in advisory["materials"]],
        }

    sets[matched_key]["purpose"] = purpose
    sets[matched_key]["plannedActions"] = planned_actions
    sets[matched_key]["planStatus"] = "已請 Agent 撰寫說明書"
    sets[matched_key]["advisoryId"] = advisory["advisoryId"]
    sets[matched_key]["updatedAt"] = datetime.datetime.now().isoformat()

    with open(SETS_FILE, "w", encoding="utf-8") as f:
        json.dump(sets, f, ensure_ascii=False, indent=2)

    print(f"[OK] Advisory written back to Set Manager: [{matched_key}]")
    print(f"     advisoryId: {advisory['advisoryId']}")
    return sets[matched_key]


if __name__ == "__main__":
    licnos = ["GBM0104204", "GBM0104194"]
    user_intent = "請為材料 Set 【室內牆】(GBM0104204, GBM0104194) 撰寫建材選用說明書"
    advisory = generate_material_advisory("室內牆", licnos, user_intent)
    write_back_to_set_manager("室內牆", advisory)
