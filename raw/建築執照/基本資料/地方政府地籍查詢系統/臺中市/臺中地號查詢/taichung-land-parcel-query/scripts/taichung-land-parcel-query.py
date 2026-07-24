#!/usr/bin/env python3
# Copyright 2026. Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
臺中市地號查詢工具

⚠️ 僅適用於臺中市，不支援其他縣市。行政區代碼、地段代碼對照表（SECTIONS）
與所有查詢網站都是臺中市政府專屬系統，輸入其他縣市的行政區/地段會查不到資料。

同時查詢：
  1. lohas GIS   — 使用分區、國土功能分區、登記面積
  2. 建築物地籍套繪 — 地號範圍內是否有上色（紅/綠）或空白
來源：
  https://lohas.taichung.gov.tw/webgis/
  https://mcgbm.taichung.gov.tw/geoViewer2/
"""

import io
import sys
import json
import time
import subprocess
import tempfile
import os
import re
import shutil
from PIL import Image
from playwright.sync_api import sync_playwright, Page, BrowserContext

KEYWORDS = ['使用分區', '國土功能分區', '登記面積', '公告地價', '公告現值',
            '登記日期', '地政事務所', '區段徵收', '自然人']

# 套繪圖行政區代碼
DISTRICT_TO_ZON = {
    "中區": "400", "東區": "401", "南區": "402", "西區": "403", "北區": "404",
    "北屯區": "406", "西屯區": "407", "南屯區": "408", "太平區": "411",
    "大里區": "412", "霧峰區": "413", "烏日區": "414", "豐原區": "420",
    "后里區": "421", "石岡區": "422", "東勢區": "423", "和平區": "424",
    "新社區": "426", "潭子區": "427", "大雅區": "428", "神岡區": "429",
    "大肚區": "432", "沙鹿區": "433", "龍井區": "434", "梧棲區": "435",
    "清水區": "436", "大甲區": "437", "外埔區": "438", "大安區": "439",
}

# 套繪圖顏色判讀
# 依據圖例說明 (https://mcgbm.taichung.gov.tw/geoViewer2/images/j.jpg)
COLOR_LEGEND = {
    # 顏色名稱: (判斷條件描述, RGB判斷函式)
    "建築物":           lambda r,g,b: r > 180 and g < 80  and b < 80,    # 紅
    "法定空地":         lambda r,g,b: g > 130 and r < 100 and b < 100,   # 深綠
    "保留地":           lambda r,g,b: r > 200 and 80<g<160 and b < 80,   # 橘
    "退縮地/騎樓地":   lambda r,g,b: r > 220 and g > 200 and b < 80,    # 黃
    "停車空間":         lambda r,g,b: b > 150 and r < 150 and g > 150,   # 青藍
    "天井":             lambda r,g,b: 80<r<180 and g>180 and b<120,      # 亮綠
    "其他(深色)":       lambda r,g,b: r < 100 and g < 100 and b < 100,   # 深色
    "空白(無套繪)":     lambda r,g,b: r > 230 and g > 230 and b > 230,   # 白
}


def analyze_overlay_color(screenshot_bytes: bytes) -> dict:
    """
    分析套繪圖截圖中旗標附近的顏色，依圖例說明回報。
    旗標（紅色定位針）位於地圖中央。
    """
    img = Image.open(io.BytesIO(screenshot_bytes)).convert("RGB")
    w, h = img.size

    # 地圖區域從約 y=150 開始（跳過上方說明文字）
    map_top = 150
    cx, cy = w // 2, (h + map_top) // 2

    sample_size = 30
    color_counts = {k: 0 for k in COLOR_LEGEND}
    color_counts["其他"] = 0
    total = 0

    for dx in range(-sample_size, sample_size):
        for dy in range(-sample_size, sample_size):
            px, py = cx + dx, cy + dy
            if 0 <= px < w and map_top <= py < h:
                r, g, b = img.getpixel((px, py))
                total += 1
                matched = False
                for name, fn in COLOR_LEGEND.items():
                    if fn(r, g, b):
                        color_counts[name] += 1
                        matched = True
                        break
                if not matched:
                    color_counts["其他"] += 1

    dominant = max(color_counts, key=color_counts.get)
    pcts = {k: f"{v/total*100:.0f}%" for k, v in color_counts.items() if v > 0}
    is_blank = dominant == "空白(無套繪)"
    return {"主要顏色": dominant, "各色比例": pcts, "有上色": not is_blank}


def _draw_map_pin(screenshot_bytes: bytes, parcel_ext: dict,
                  map_ext: dict, canvas_bounds: dict) -> bytes:
    """在截圖上用 PIL 畫紅色定位針，自動閃避地圖文字。"""
    from PIL import ImageDraw
    cx_geo = (parcel_ext['xmin'] + parcel_ext['xmax']) / 2
    cy_geo = (parcel_ext['ymin'] + parcel_ext['ymax']) / 2
    cw = canvas_bounds['width']
    ch = canvas_bounds['height']
    ox = canvas_bounds['x']
    oy = canvas_bounds['y']
    ext_w = map_ext['xmax'] - map_ext['xmin']
    ext_h = map_ext['ymax'] - map_ext['ymin']
    if ext_w == 0 or ext_h == 0:
        return screenshot_bytes
    px = int(ox + (cx_geo - map_ext['xmin']) / ext_w * cw)
    py = int(oy + (map_ext['ymax'] - cy_geo) / ext_h * ch)

    img = Image.open(io.BytesIO(screenshot_bytes)).convert('RGBA')
    gray = img.convert('L')
    iw, ih = img.size

    r = 13   # 圓頭半徑
    d = r * 2 + 14  # 錨點到圓頭圓心的桿長

    # 候選圓頭位置（相對錨點偏移），優先往正上方，再往左右上方試
    candidates = [
        (0,           -d),
        (-int(d*0.5), -int(d*0.87)),
        ( int(d*0.5), -int(d*0.87)),
        (-int(d*0.87),-int(d*0.5)),
        ( int(d*0.87),-int(d*0.5)),
    ]

    def dark_score(cx, cy):
        x1, y1 = max(0, cx - r), max(0, cy - r)
        x2, y2 = min(iw, cx + r), min(ih, cy + r)
        if x2 <= x1 or y2 <= y1:
            return 9999
        return sum(1 for p in gray.crop((x1, y1, x2, y2)).getdata() if p < 80)

    best_dx, best_dy = min(candidates, key=lambda c: dark_score(px + c[0], py + c[1]))
    hx, hy = px + best_dx, py + best_dy

    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    RED   = (210, 0, 0, 240)
    WHITE = (255, 255, 255, 210)

    # 桿（白底紅線，形成白邊輪廓讓桿在淺色背景也看得到）
    draw.line([(px, py), (hx, hy)], fill=WHITE, width=6)
    draw.line([(px, py), (hx, hy)], fill=RED,   width=3)

    # 圓頭
    draw.ellipse([(hx - r, hy - r), (hx + r, hy + r)], fill=RED)
    draw.ellipse([(hx - r, hy - r), (hx + r, hy + r)], outline=WHITE, width=2)
    draw.ellipse([(hx - 5,  hy - 5),  (hx + 5,  hy + 5)],  fill=WHITE)

    # 錨點小圓（標示地號實際中心）
    draw.ellipse([(px - 4, py - 4), (px + 4, py + 4)], fill=RED)
    draw.ellipse([(px - 4, py - 4), (px + 4, py + 4)], outline=WHITE, width=1)

    result = Image.alpha_composite(img, layer)
    out = io.BytesIO()
    result.convert('RGB').save(out, format='PNG')
    return out.getvalue()


def _get_map_ext_and_canvas(page) -> tuple:
    """讀取 ArcGIS map 當前 viewport extent 和 canvas 在頁面中的位置。"""
    info = page.evaluate("""() => {
        const e = window.map ? map.extent : null;
        const el = document.getElementById('mapCanvas');
        const r = el ? el.getBoundingClientRect() : null;
        return {
            ext: e ? {xmin:e.xmin, ymin:e.ymin, xmax:e.xmax, ymax:e.ymax} : null,
            canvas: r ? {x:r.x, y:r.y, width:r.width, height:r.height} : null
        };
    }""")
    return info.get('ext'), info.get('canvas')


def _get_parcel_extent(context: BrowserContext, zon: str, section_code: str,
                       lot_main: str, lot_sub: str = "0"):
    """開套繪圖取得地號 EPSG:3857 範圍，供防火間隔縮放用"""
    page = context.new_page()
    try:
        page.goto("https://mcgbm.taichung.gov.tw/geoViewer2/geoViewAction.do?infopage=1&pas=I80")
        page.wait_for_load_state("networkidle", timeout=20000)
        time.sleep(1.5)
        page.select_option("#ZON", value=zon)
        time.sleep(1.5)
        page.select_option("#SECTNO", value=section_code)
        page.fill("#lno1", lot_main)
        page.fill("#lno2", lot_sub)
        with context.expect_page(timeout=10000) as npi:
            page.evaluate("() => { document.querySelector('input[value=送出]').click(); }")
            time.sleep(1)
        rp = npi.value
        rp.wait_for_load_state("networkidle", timeout=20000)
        time.sleep(2)
        ext = rp.evaluate("""() => {
            if (window.map && window.map.extent) {
                const e = window.map.extent;
                return {xmin:e.xmin, ymin:e.ymin, xmax:e.xmax, ymax:e.ymax};
            }
            return null;
        }""")
        rp.close()
        page.close()
        return ext
    except Exception:
        try:
            page.close()
        except Exception:
            pass
        return None


def query_overlay(context: BrowserContext, district: str, section_code: str,
                  lot_main: str, lot_sub: str = "0") -> dict:
    """查詢套繪圖，回傳顏色分析結果"""
    zon = DISTRICT_TO_ZON.get(district, "")
    if not zon:
        return {"error": f"找不到 {district} 的套繪區碼"}

    page = context.new_page()
    try:
        page.goto("https://mcgbm.taichung.gov.tw/geoViewer2/geoViewAction.do?infopage=1&pas=I80")
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)

        page.select_option("#ZON", value=zon)
        time.sleep(1.5)
        page.select_option("#SECTNO", value=section_code)
        page.fill("#lno1", lot_main)
        page.fill("#lno2", lot_sub)
        time.sleep(0.5)

        with context.expect_page(timeout=10000) as new_page_info:
            page.evaluate("() => { document.querySelector('input[value=送出]').click(); }")
            time.sleep(1)

        result_page = new_page_info.value
        result_page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(4)

        # 取得緊縮地號範圍，再縮放至 2.5x 顯示周邊環境
        parcel_ext = result_page.evaluate("""() => {
            if (window.map && window.map.extent) {
                const e = window.map.extent;
                return {xmin:e.xmin, ymin:e.ymin, xmax:e.xmax, ymax:e.ymax};
            }
            return null;
        }""")
        scale = result_page.evaluate("() => window.map ? map.getScale() : null")
        if scale:
            result_page.evaluate(f"() => {{ map.setScale({scale * 2.5}); }}")
            time.sleep(2)

        map_ext, canvas_bounds = _get_map_ext_and_canvas(result_page)
        screenshot = result_page.screenshot()

        # 用 ArcGIS REST identify 取地號中心的建物屬性（含樓層數）
        label_text = ""
        if parcel_ext and map_ext and canvas_bounds:
            try:
                cx = (parcel_ext["xmin"] + parcel_ext["xmax"]) / 2
                cy = (parcel_ext["ymin"] + parcel_ext["ymax"]) / 2
                iw = int(canvas_bounds["width"])
                ih = int(canvas_bounds["height"])
                features = result_page.evaluate("""([cx, cy, ext, iw, ih]) => {
                    const body = new URLSearchParams({
                        f: 'json',
                        geometry: JSON.stringify({x: cx, y: cy, spatialReference: {wkid: 102100}}),
                        geometryType: 'esriGeometryPoint',
                        sr: '102100',
                        layers: 'all',
                        tolerance: '5',
                        mapExtent: JSON.stringify({xmin:ext.xmin,ymin:ext.ymin,xmax:ext.xmax,ymax:ext.ymax,spatialReference:{wkid:102100}}),
                        imageDisplay: iw + ',' + ih + ',96',
                        returnGeometry: 'false'
                    });
                    return fetch('https://mcgbm.taichung.gov.tw/arcgis/rest/services/bcmsMap_I80/MapServer/identify', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                        body: body.toString()
                    }).then(r => r.json())
                      .then(d => (d.results || []).filter(r => r.layerName === '套繪圖_建築物').map(r => r.attributes))
                      .catch(() => []);
                }""", [cx, cy, map_ext, iw, ih]) or []

                all_labels = []
                for attrs in features:
                    lbl = (attrs.get("label") or "").strip()
                    if lbl:
                        all_labels.append(lbl)
                    else:
                        # label 欄位空白時從 floor/dnfloor 重組
                        above = str(attrs.get("floor", "") or "").strip()
                        below = str(attrs.get("dnfloor", "") or "").strip()
                        parts = []
                        if above and above != "0":
                            parts.append(f"{above}F")
                        if below and below != "0":
                            parts.append(f"B{below}F")
                        if parts:
                            all_labels.append(",".join(parts))
                if all_labels:
                    label_text = "；".join(all_labels)
            except Exception:
                pass

        result_page.close()
        page.close()

        if parcel_ext and map_ext and canvas_bounds:
            screenshot = _draw_map_pin(screenshot, parcel_ext, map_ext, canvas_bounds)

        color_result = analyze_overlay_color(screenshot)
        color_result["截圖"] = screenshot
        if label_text:
            color_result["標記文字"] = label_text
        return color_result

    except Exception as e:
        try:
            page.close()
        except Exception:
            pass
        return {"error": str(e)}


def analyze_firebreak_color(screenshot_bytes: bytes) -> dict:
    """
    分析防火間隔截圖，掃描整張地圖區域偵測是否有防火間隔綠色。
    防火間隔網站顯示整個地段，綠色斜線區可能分布於畫面任何位置，
    不能只取中央 60×60，需全圖掃描。
    防火間隔綠色：純亮綠 r<80, g>180, b<80。
    """
    img = Image.open(io.BytesIO(screenshot_bytes)).convert("RGB")
    w, h = img.size
    map_top = 150  # 跳過上方說明文字列

    green_pixels = 0
    total_pixels = 0

    for py in range(map_top, h, 2):       # 每隔1px取樣以加速
        for px in range(0, w, 2):
            r, g, b = img.getpixel((px, py))
            total_pixels += 1
            if r < 80 and g > 180 and b < 80:
                green_pixels += 1

    green_pct = green_pixels / total_pixels * 100 if total_pixels else 0
    has_firebreak = green_pct > 0.5  # 超過 0.5% 判定為有防火間隔

    return {
        "有上色": has_firebreak,
        "主要顏色": "防火間隔" if has_firebreak else "空白(無套繪)",
        "各色比例": {"防火間隔": f"{green_pct:.1f}%"} if has_firebreak else {"空白(無套繪)": "100%"},
    }


def query_firebreak(context: BrowserContext, district: str, section_code: str,
                    lot_main: str, lot_sub: str = "0") -> dict:
    """查詢防火間隔，回傳顏色分析結果；若非公告區域則直接回傳"""
    zon = DISTRICT_TO_ZON.get(district, "")
    if not zon:
        return {"error": f"找不到 {district} 的套繪區碼"}

    # 先從套繪圖取地號的 EPSG:3857 範圍，用於縮放防火間隔地圖到基地位置
    parcel_ext = _get_parcel_extent(context, zon, section_code, lot_main, lot_sub)

    page = context.new_page()
    try:
        page.goto("https://mcgbm.taichung.gov.tw/geoViewer2/geoViewAction.do?infopage=1&pas=I80&for=OFA")
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)

        # ZON 不在清單裡表示該區無防火間隔公告
        zon_exists = page.evaluate(f"() => !!document.querySelector('#ZON option[value=\"{zon}\"]')")
        if not zon_exists:
            page.close()
            return {"結果": "非防火間隔公告區域"}

        page.select_option("#ZON", value=zon)
        time.sleep(1.5)

        # SECTNO 不在清單裡表示該地段無防火間隔公告
        sect_exists = page.evaluate(f"() => !!document.querySelector('#SECTNO option[value=\"{section_code}\"]')")
        if not sect_exists:
            page.close()
            return {"結果": "非防火間隔公告區域"}

        page.select_option("#SECTNO", value=section_code)
        page.fill("#lno1", lot_main)
        page.fill("#lno2", lot_sub)
        time.sleep(0.5)

        with context.expect_page(timeout=10000) as new_page_info:
            page.evaluate("() => { document.querySelector('input[value=送出]').click(); }")
            time.sleep(1)

        result_page = new_page_info.value
        result_page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(4)

        # 縮放到基地位置（加 25 unit 緩衝，與套繪圖縮放比例相近）
        if parcel_ext:
            buf = 25
            xmin = parcel_ext['xmin'] - buf
            ymin = parcel_ext['ymin'] - buf
            xmax = parcel_ext['xmax'] + buf
            ymax = parcel_ext['ymax'] + buf
            result_page.evaluate(f"""() => {{
                var ext = new esri.geometry.Extent(
                    {xmin},{ymin},{xmax},{ymax},
                    new esri.SpatialReference({{wkid:102100}})
                );
                map.setExtent(ext, false);
            }}""")
            time.sleep(2)

        map_ext, canvas_bounds = _get_map_ext_and_canvas(result_page)
        screenshot = result_page.screenshot()
        result_page.close()
        page.close()

        if parcel_ext and map_ext and canvas_bounds:
            screenshot = _draw_map_pin(screenshot, parcel_ext, map_ext, canvas_bounds)

        color_result = analyze_firebreak_color(screenshot)
        color_result["截圖"] = screenshot
        return color_result

    except Exception as e:
        try:
            page.close()
        except Exception:
            pass
        return {"error": str(e)}


def find_section_code(district: str, section_name: str) -> str:
    """根據行政區和地段名稱找代碼，找不到就原值回傳"""
    dist_sections = SECTIONS.get(district, {})
    if section_name in dist_sections:
        return dist_sections[section_name]
    for name, code in dist_sections.items():
        if section_name in name:
            print(f"  (找到近似地段：{name})")
            return code
    print(f"  警告：找不到 {district} {section_name}，請確認地段名稱")
    return section_name


def _open_zone_panel(page: Page):
    """開啟地段地號定位面板"""
    page.evaluate("() => { const el=document.getElementById('locationStart');if(el)el.click(); }")
    time.sleep(1.5)
    page.evaluate("""() => {
        const btns=document.querySelectorAll('button');
        for(let b of btns){if(b.textContent.includes('地段')&&b.textContent.includes('地號')){b.click();return;}}
    }""")
    time.sleep(2)


# ─── 都發局都計土地使用管制 PDF ──────────────────────────────────────────────────

_UD_BASE = "https://www.ud.taichung.gov.tw"

# 都市計畫名稱 → 都發局頁面（直接 PDF 或子頁面）
_UD_PLAN_MAP = {
    "臺中市都市計畫":                        f"{_UD_BASE}/2878076/post",
    "大坑風景特定區計畫":                    f"{_UD_BASE}/media/1316356/2-1大坑風景特定區細部計畫.pdf",
    "中部科學工業園區臺中基地附近特定區計畫": f"{_UD_BASE}/2878372/post",
    "大平霧地區都市計畫":                    f"{_UD_BASE}/2878389/post",
    "烏日大肚地區都市計畫":                  f"{_UD_BASE}/2878395/post",
    "臺中港特定區計畫":                      f"{_UD_BASE}/2878405/post",
    "大甲都市計畫":                          f"{_UD_BASE}/media/1194068/9-1變更大甲都市計畫細部計畫.pdf",
    "大甲(日南地區)都市計畫":                f"{_UD_BASE}/media/1194069/10-1變更臺中市大甲-日南地區-都市計畫細部計畫.pdf",
    "鐵砧山風景特定區計畫":                  f"{_UD_BASE}/media/1194070/11-1鐵砧山風景特定區計畫細部計畫.pdf",
    "大安都市計畫":                          f"{_UD_BASE}/media/1194071/12-1大安都市計畫細部計畫.pdf",
    "外埔都市計畫":                          f"{_UD_BASE}/media/1194072/13-1外埔都市計畫細部計畫.pdf",
    "后里都市計畫":                          f"{_UD_BASE}/2878435/post",
    "豐潭雅神地區都市計畫":                  f"{_UD_BASE}/2878453/post",
    "東勢都市計畫":                          f"{_UD_BASE}/media/1194087/16-1擬定臺中市東勢都市計畫細部計畫.pdf",
    "新社都市計畫":                          f"{_UD_BASE}/media/1194088/17-1擬定新社都市計畫細部計畫.pdf",
    "石岡水壩特定區計畫":                    f"{_UD_BASE}/media/1194089/18-1擬定石岡水壩特定區計畫細部計畫.pdf",
    "谷關風景特定區計畫":                    f"{_UD_BASE}/media/1194090/19-1谷關風景特定區計畫細部計畫土地使用分區管制要點.pdf",
    "梨山風景特定區計畫":                    f"{_UD_BASE}/2878477/post",
}


def _ud_find_plan_url(urban_plan_area: str) -> tuple:
    """在 _UD_PLAN_MAP 中找最符合 urban_plan_area 的條目，回傳 (key, url)"""
    if not urban_plan_area:
        return None, None
    for key, url in _UD_PLAN_MAP.items():
        if urban_plan_area in key or key in urban_plan_area:
            return key, url
    stop = {'都市', '計畫', '臺中市', '地區', '特定區', '風景', ''}
    target_w = set(re.split(r'[\s（）()、，。]', urban_plan_area)) - stop
    best_score, best = 0, (None, None)
    for key, url in _UD_PLAN_MAP.items():
        key_w = set(re.split(r'[\s（）()、，。]', key)) - stop
        score = len(target_w & key_w)
        if score > best_score:
            best_score, best = score, (key, url)
    return best if best_score > 0 else (None, None)


def _ud_fetch_subpage_pdfs(sub_url: str) -> list:
    """抓子頁面，回傳所有 PDF 連結 [(link_text, absolute_url), ...]。
    先用 urllib 靜態抓；若無結果（JS渲染頁面），改用 Playwright 等待渲染後再抓。"""
    import urllib.request as _ur

    def _parse_html(html: str) -> list:
        results, seen = [], set()
        for m in re.finditer(r'<a\s[^>]*href=["\']([^"\']*\.pdf)["\'][^>]*>(.*?)</a>',
                             html, re.DOTALL | re.IGNORECASE):
            href = m.group(1).strip()
            text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
            if not href.startswith('http'):
                href = _UD_BASE + '/' + href.lstrip('/')
            if href not in seen and text:
                seen.add(href)
                results.append((text, href))
        return results

    # 先試靜態 HTTP
    try:
        req = _ur.Request(sub_url, headers={"User-Agent": "Mozilla/5.0"})
        with _ur.urlopen(req, timeout=20) as r:
            html = r.read().decode("utf-8", errors="replace")
        results = _parse_html(html)
        if results:
            return results
    except Exception:
        pass

    # 靜態抓不到 PDF → 改用 Playwright 等 JS 渲染
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            pg = browser.new_page()
            pg.goto(sub_url, wait_until="networkidle", timeout=30000)
            time.sleep(2)
            links = pg.evaluate("""() =>
                Array.from(document.querySelectorAll('a[href]'))
                    .filter(a => a.href.toLowerCase().endsWith('.pdf'))
                    .map(a => ({href: a.href, text: a.innerText.trim()}))
            """)
            browser.close()
        results, seen = [], set()
        for lk in links:
            href, text = lk.get('href', ''), lk.get('text', '')
            if href and href not in seen and text:
                seen.add(href)
                results.append((text, href))
        return results
    except Exception as e:
        print(f"  [ud_fetch_subpage_pdfs] Playwright 失敗：{e}")
        return []


def _ud_best_pdf(plan_case_name: str, pdf_links: list) -> tuple:
    """從 pdf_links=[(text, url)] 找最符合 plan_case_name 的，回傳 (text, url)"""
    if not pdf_links:
        return None, None
    if len(pdf_links) == 1 or not plan_case_name:
        return pdf_links[0]

    stop = {'變更', '都市', '計畫', '臺中市', '細部', '擬定', '使用分區管制', '土地使用分區', ''}

    # 1) 括號內容完整比對
    target_parens = set(re.findall(r'[（(]([^）)]+)[）)]', plan_case_name))
    if target_parens:
        best_score, best = 0, pdf_links[0]
        for text, url in pdf_links:
            cand_parens = set(re.findall(r'[（(]([^）)]+)[）)]', text + url))
            score = len(target_parens & cand_parens)
            if score > best_score:
                best_score, best = score, (text, url)
        if best_score > 0:
            return best

    # 2) 括號內容拆字（「北屯區洲際地區」→「北屯區」+「洲際地區」）再比對
    target_subwords: set = set()
    for paren in target_parens:
        target_subwords.update(re.split(r'[\s、，。\-]+', paren))
    target_subwords -= stop
    if target_subwords:
        best_score, best = 0, pdf_links[0]
        for text, url in pdf_links:
            cand_all = re.split(r'[\s（）()、，。\-]+', text + ' ' + url.split('/')[-1])
            cand_w = set(cand_all) - stop
            score = len(target_subwords & cand_w)
            if score > best_score:
                best_score, best = score, (text, url)
        if best_score > 0:
            return best

    # 3) 整個 plan_case_name 的關鍵字比對
    target_w = set(re.split(r'[\s（）()、，。\-]', plan_case_name)) - stop
    best_score, best = 0, pdf_links[0]
    for text, url in pdf_links:
        cand_w = set(re.split(r'[\s（）()、，。\-]', text + ' ' + url.split('/')[-1])) - stop
        score = len(target_w & cand_w)
        if score > best_score:
            best_score, best = score, (text, url)
    if best_score > 0:
        return best
    return pdf_links[0]


def _query_ud_pdf(urban_plan_area: str, plan_case_name: str, save_dir: str) -> dict:
    """從都發局下載對應的都市計畫土地使用管制 PDF"""
    import urllib.request as _ur
    from urllib.parse import urlparse, quote, urlunparse

    def _safe_url(url: str) -> str:
        """將含中文的 URL 做 percent-encoding，讓 urllib 可以處理。"""
        p = urlparse(url)
        return urlunparse(p._replace(path=quote(p.path, safe='/'), query=quote(p.query, safe='=&')))

    matched_key, matched_url = _ud_find_plan_url(urban_plan_area)
    if not matched_url:
        return {"error": f"找不到對應的都市計畫條目：{urban_plan_area}"}
    save_path = os.path.join(save_dir, "都市計畫土地使用管制.pdf")
    if '/media/' in matched_url and matched_url.lower().endswith('.pdf'):
        req = _ur.Request(_safe_url(matched_url), headers={"User-Agent": "Mozilla/5.0"})
        with _ur.urlopen(req, timeout=30) as r:
            with open(save_path, 'wb') as f:
                f.write(r.read())
        return {"PDF路徑": save_path, "匹配計畫": matched_key}
    pdf_links = _ud_fetch_subpage_pdfs(matched_url)
    if not pdf_links:
        return {"error": "子頁面找不到 PDF", "匹配計畫": matched_key}
    best_text, best_url = _ud_best_pdf(plan_case_name, pdf_links)
    if not best_url:
        return {"error": "無法從子頁面找到匹配 PDF", "匹配計畫": matched_key}
    req = _ur.Request(_safe_url(best_url), headers={"User-Agent": "Mozilla/5.0"})
    with _ur.urlopen(req, timeout=60) as r:
        with open(save_path, 'wb') as f:
            f.write(r.read())
    return {"PDF路徑": save_path, "匹配計畫": matched_key, "匹配PDF": best_text}


def _ud_worker(urban_plan_area: str, plan_case_name: str, save_dir: str, out_file: str):
    """子程序入口：查都市計畫土地使用管制 PDF"""
    os.makedirs(save_dir, exist_ok=True)
    result = _query_ud_pdf(urban_plan_area, plan_case_name, save_dir)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────

def _retry_license_with_old_lot(page: Page, district: str, section_code: str, old_lot: str) -> list:
    """用重測前地號重新定位並查詢執照，回傳 [{num, date}, ...] 或空 list"""
    _open_zone_panel(page)
    page.select_option("#seltown", label=district)
    time.sleep(2)
    page.select_option("#selsect", value=section_code)
    time.sleep(1)
    page.fill("#selnum", old_lot)
    time.sleep(0.5)
    page.evaluate("""() => {
        const btns = document.querySelectorAll('button');
        for (const b of btns) { if (b.textContent.trim() === '定位' && b.offsetParent !== null) { b.click(); return; } }
    }""")
    time.sleep(5)
    page.evaluate("""() => {
        const actions = document.querySelectorAll('.esri-popup__action');
        for (const a of actions) { if (a.textContent.trim() === '分析') { a.click(); return; } }
    }""")
    time.sleep(4)
    page.evaluate("() => { for (const el of document.querySelectorAll('*')) { if (el.textContent.trim() === '建物' && el.offsetParent !== null) { el.click(); return; } } }")
    time.sleep(1.5)
    page.evaluate("""() => {
        for (const b of document.querySelectorAll('button, input[type="button"]')) {
            if (b.offsetParent !== null && (b.innerText || b.value || '').trim().includes('查詢執照')) {
                b.click(); return;
            }
        }
    }""")
    try:
        page.wait_for_function(
            """() => {
                const tbl = document.querySelector('#rptablelayer');
                if (!tbl) return false;
                const txt = tbl.innerText || '';
                return tbl.querySelectorAll('tr').length > 0 || txt.includes('查無') || txt.includes('執照');
            }""",
            timeout=20000
        )
    except Exception:
        time.sleep(10)
    return page.evaluate("""() => {
        const selectors = ['#rptablelayer .layui-table-main tbody', '#rptablelayer tbody', '#rptablelayer table tbody'];
        for (const sel of selectors) {
            const tbody = document.querySelector(sel);
            if (!tbody) continue;
            const result = [];
            tbody.querySelectorAll('tr').forEach(tr => {
                const cells = tr.querySelectorAll('td .layui-table-cell');
                if (cells.length >= 2 && cells[0].innerText.trim()) {
                    result.push({ num: cells[0].innerText.trim(), date: cells[1].innerText.trim() }); return;
                }
                const tds = tr.querySelectorAll('td');
                if (tds.length >= 2 && tds[0].innerText.trim())
                    result.push({ num: tds[0].innerText.trim(), date: tds[1].innerText.trim() });
            });
            if (result.length > 0) return result;
        }
        return [];
    }""")


def _query_one(page: Page, district: str, section_name: str, section_code: str, lot: str,
               current_district: str, current_section: str) -> list:
    """在已開啟的頁面上查詢單筆地號，回傳文字列表"""

    # 攔截 ArcGIS token（用於之後都市計畫分區查詢）
    arcgis_tokens: list = []
    def _token_handler(req):
        if 'lohas.taichung.gov.tw/arcgis' in req.url and 'token=' in req.url:
            m = re.search(r'token=([^&\s]+)', req.url)
            if m and not arcgis_tokens:
                arcgis_tokens.append(m.group(1))
    page.on('request', _token_handler)

    # 若行政區不同才重選
    if district != current_district:
        _open_zone_panel(page)
        page.select_option("#seltown", label=district)
        time.sleep(2.5)
        page.select_option("#selsect", value=section_code)
        time.sleep(1)
    elif section_code != current_section:
        _open_zone_panel(page)
        page.select_option("#seltown", label=district)
        time.sleep(2)
        page.select_option("#selsect", value=section_code)
        time.sleep(1)
    else:
        # 同地段，只需重開面板填地號
        _open_zone_panel(page)
        page.select_option("#seltown", label=district)
        time.sleep(2)
        page.select_option("#selsect", value=section_code)
        time.sleep(1)

    page.fill("#selnum", lot)
    time.sleep(0.5)

    page.evaluate("""() => {
        const btns=document.querySelectorAll('button');
        for(let b of btns){if(b.textContent.trim()==='定位'&&b.offsetParent!==null){b.click();return;}}
    }""")
    time.sleep(5)

    page.evaluate("""() => {
        const actions=document.querySelectorAll('.esri-popup__action');
        for(let a of actions){if(a.textContent.trim()==='分析'){a.click();return;}}
    }""")
    time.sleep(4)

    # 第一步：先收集土地頁籤的全部文字
    land_texts = page.evaluate("""() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let texts = [];
        let node;
        while (node = walker.nextNode()) {
            const txt = node.textContent.trim();
            if (txt.length > 2 && txt.length < 300) {
                const el = node.parentElement;
                if (el && el.offsetParent !== null) texts.push(txt);
            }
        }
        return [...new Set(texts)];
    }""")

    # 第二步：切到建物頁籤查詢建號
    page.evaluate("() => { const all=document.querySelectorAll('*'); for(let el of all){if(el.textContent.trim()==='建物'&&el.offsetParent!==null){el.click();return;}} }")
    time.sleep(1.5)

    # 先嘗試從面板「建號：XXXX」文字直接讀取（頁籤打開即顯示）
    build_result = page.evaluate("""() => {
        // 掃全頁，找含「建號：」的可見元素，用 regex 抽出建號
        const all = document.querySelectorAll('*');
        for (const el of all) {
            if (!el.offsetParent) continue;
            const t = (el.innerText || '').trim();
            const m = t.match(/建號[：:]\s*(\S+)/);
            if (m && m[1] && m[1].length < 30) return m[1];
        }
        return null;
    }""")

    if not build_result:
        page.evaluate("() => { const btns=document.querySelectorAll('button'); for(let b of btns){if(b.textContent.trim()==='查詢建號'&&b.offsetParent!==null){b.click();return;}} }")
        time.sleep(5)
        raw_buildno = page.evaluate("""() => {
            const buildno = document.getElementById('buildno');
            return buildno ? buildno.innerText.trim() : '';
        }""")
        m = re.search(r'建號[：:]\s*(\S+)', raw_buildno or '')
        build_result = m.group(1) if m else '查無建號'

    land_texts.append(f"建號查詢：{build_result}")

    # 第三步：查詢執照
    page.evaluate("""() => {
        const candidates = [...document.querySelectorAll('button, input[type="button"]')];
        for (const b of candidates) {
            if (b.offsetParent !== null && (b.innerText || b.value || '').trim().includes('查詢執照')) {
                b.click(); return;
            }
        }
    }""")
    # 等執照 table 出現（最多等 20 秒），若逾時再用固定等待
    try:
        page.wait_for_function(
            """() => {
                const tbl = document.querySelector('#rptablelayer');
                if (!tbl) return false;
                const txt = tbl.innerText || '';
                return tbl.querySelectorAll('tr').length > 0 || txt.includes('查無') || txt.includes('執照');
            }""",
            timeout=20000
        )
    except Exception:
        time.sleep(10)

    license_rows = page.evaluate("""() => {
        // 嘗試多種可能的 selector
        const selectors = [
            '#rptablelayer .layui-table-main tbody',
            '#rptablelayer tbody',
            '#rptablelayer table tbody',
        ];
        let rows = [];
        for (const sel of selectors) {
            const tbody = document.querySelector(sel);
            if (!tbody) continue;
            const trs = tbody.querySelectorAll('tr');
            if (trs.length === 0) continue;
            trs.forEach(tr => {
                // 先試 layui cell wrapper
                const cells = tr.querySelectorAll('td .layui-table-cell');
                if (cells.length >= 2 && cells[0].innerText.trim()) {
                    rows.push({ num: cells[0].innerText.trim(), date: cells[1].innerText.trim() });
                    return;
                }
                // fallback：直接抓 td
                const tds = tr.querySelectorAll('td');
                if (tds.length >= 2 && tds[0].innerText.trim()) {
                    rows.push({ num: tds[0].innerText.trim(), date: tds[1].innerText.trim() });
                }
            });
            if (rows.length > 0) break;
        }
        return rows;
    }""")

    if license_rows:
        for r in license_rows:
            land_texts.append(f"執照查詢：{r['num']}  發照日期：{r['date']}")
    else:
        land_texts.append("執照查詢：查無執照")

    # 第四步：履歷 - 分割合併與重測異動
    try:
        page.evaluate("() => { const all=document.querySelectorAll('*'); for(let el of all){if(el.offsetParent!==null&&el.textContent.trim()==='履歷'&&el.children.length===0){el.click();return;}} }")
        time.sleep(2)
        page.evaluate("() => { const btns=document.querySelectorAll('button'); for(let b of btns){if(b.textContent.trim()==='分割合併與重測異動'&&b.offsetParent!==null){b.click();return;}} }")
        time.sleep(4)

        def _read_subtab(label):
            page.evaluate(f"""() => {{
                const div = document.getElementById('Alllandtablediv');
                if (!div) return;
                const tabs = div.querySelectorAll('.layui-tab-title li');
                for (let t of tabs) {{ if (t.textContent.trim() === '{label}') {{ t.click(); return; }} }}
            }}""")
            time.sleep(1.5)
            return page.evaluate(f"""() => {{
                const div = document.getElementById('Alllandtablediv');
                if (!div) return null;
                const tabs = div.querySelectorAll('.layui-tab-title li');
                let idx = -1;
                tabs.forEach((t, i) => {{ if (t.textContent.trim() === '{label}') idx = i; }});
                if (idx < 0) return null;
                const content = div.querySelectorAll('.layui-tab-content .layui-tab-item')[idx];
                if (!content) return null;
                const rows = Array.from(content.querySelectorAll('.layui-table tbody tr')).map(tr =>
                    Array.from(tr.querySelectorAll('.layui-table-cell')).map(d => d.innerText.trim())
                ).filter(r => r.some(c => c.length > 0));
                const headers = Array.from(content.querySelectorAll('.layui-table-header th')).map(th => th.innerText.trim());
                return {{ headers, rows }};
            }}""")

        history = {
            "其他登記事項": _read_subtab("其他登記事項"),
            "分割合併紀錄": _read_subtab("分割合併紀錄"),
            "重測前後對照": _read_subtab("重測前後對照"),
        }
        land_texts.append(f"履歷JSON：{json.dumps(history, ensure_ascii=False)}")
    except Exception:
        pass

    # 步驟 4b：若查無執照，嘗試用重測前地號重新查詢
    if "執照查詢：查無執照" in land_texts:
        try:
            hist_str = next((t[len("履歷JSON："):] for t in land_texts if t.startswith("履歷JSON：")), None)
            if hist_str:
                hist = json.loads(hist_str)
                remapping = (hist.get("重測前後對照") or {})
                headers = remapping.get("headers") or []
                rows_data = remapping.get("rows") or []
                tried: set = set()
                for row in rows_data:
                    old_lot_val = ""
                    # 優先找 headers 中含「前」+「地號」的欄位
                    for i, h in enumerate(headers):
                        if i < len(row) and "前" in h and "地號" in h:
                            old_lot_val = row[i].strip()
                            break
                    # fallback：找第一個純數字且不是當前地號的欄位
                    if not old_lot_val:
                        for val in row:
                            if val.strip().isdigit() and 3 <= len(val.strip()) <= 8 and val.strip() != lot:
                                old_lot_val = val.strip()
                                break
                    if not old_lot_val or old_lot_val == lot or old_lot_val in tried:
                        continue
                    tried.add(old_lot_val)
                    retry_rows = _retry_license_with_old_lot(page, district, section_code, old_lot_val)
                    if retry_rows:
                        land_texts = [t for t in land_texts if t != "執照查詢：查無執照"]
                        for r in retry_rows:
                            land_texts.append(
                                f"執照查詢：{r['num']}  發照日期：{r['date']}  （重測前地號 {old_lot_val}）"
                            )
                        break
        except Exception:
            pass

    # 第五步：都市計畫分區（建蔽率、容積率）
    try:
        page.remove_listener('request', _token_handler)
    except Exception:
        pass
    arcgis_token = arcgis_tokens[0] if arcgis_tokens else None

    try:
        if arcgis_token:
            urban_data = page.evaluate(f"""() => new Promise((resolve) => {{
                try {{
                    const twd97x = analgeo1.attributes.TWD97E;
                    const twd97y = analgeo1.attributes.TWD97N;
                    if (!twd97x || !twd97y) {{ resolve(null); return; }}
                    const R = 6378137;
                    const toM = (tx, ty) => {{
                        const w = TWDtoLonLat(tx, ty, 121);
                        return [w[0] * Math.PI * R / 180,
                                Math.log(Math.tan((90 + w[1]) * Math.PI / 360)) * R];
                    }};
                    const [cx, cy] = toM(twd97x, twd97y);
                    const offsets = [[0,0],[15,0],[-15,0],[0,15],[0,-15]];
                    const results = [];
                    let pending = offsets.length;
                    offsets.forEach(([dx, dy]) => {{
                        const [px, py] = toM(twd97x + dx, twd97y + dy);
                        const params = new URLSearchParams({{
                            f: 'json',
                            geometry: JSON.stringify({{x: px, y: py, spatialReference: {{wkid: 3857}}}}),
                            geometryType: 'esriGeometryPoint',
                            layers: 'all:1',
                            tolerance: 3,
                            mapExtent: JSON.stringify({{xmin: cx-500, ymin: cy-500,
                                                        xmax: cx+500, ymax: cy+500,
                                                        spatialReference: {{wkid: 3857}}}}),
                            imageDisplay: '800,600,96',
                            returnGeometry: 'false',
                            token: '{arcgis_token}'
                        }});
                        fetch('https://lohas.taichung.gov.tw/arcgis/rest/services/Tiled3857/URBAN3857/MapServer/identify?' + params)
                            .then(r => r.json())
                            .then(data => {{
                                if (data.results && data.results.length > 0)
                                    results.push(data.results[0].attributes);
                                if (--pending === 0) resolve(results);
                            }})
                            .catch(() => {{ if (--pending === 0) resolve(results); }});
                    }});
                }} catch(e) {{ resolve({{err: e.message}}); }}
            }})""")
            if urban_data and isinstance(urban_data, list):
                seen = set()
                unique = []
                for item in urban_data:
                    zone_key = item.get("使用分區", "") or str(item)
                    if zone_key not in seen:
                        seen.add(zone_key)
                        unique.append(item)
                if unique:
                    land_texts.append(f"都計JSON：{json.dumps(unique, ensure_ascii=False)}")
            elif urban_data and isinstance(urban_data, dict) and not urban_data.get("err"):
                land_texts.append(f"都計JSON：{json.dumps([urban_data], ensure_ascii=False)}")

        # 啟用都市計畫分區圖層
        page.evaluate("""() => {
            const cb = document.getElementById('layer_urban');
            if (cb && !cb.checked) cb.click();
        }""")
        time.sleep(3)

        # 關閉所有浮動視窗：找 × 關閉符號的 leaf 節點並點擊
        page.evaluate("""() => {
            const CLOSE_CHARS = new Set(['×', '✕', '✖', 'X', '×']);
            document.querySelectorAll('*').forEach(el => {
                if (!el.offsetParent) return;
                if (el.children.length > 0) return;
                if (CLOSE_CHARS.has((el.textContent || '').trim())) el.click();
            });
            // 也試 class 含 close 的按鈕
            document.querySelectorAll('[class*="close"],[class*="Close"]').forEach(el => {
                if (el.offsetParent) el.click();
            });
        }""")
        time.sleep(0.3)
        page.keyboard.press("Escape")
        time.sleep(0.3)


        urban_screenshot_bytes = page.screenshot()
        save_dir = os.path.expanduser(f"~/Desktop/查詢結果/臺中市{district}{section_name}{lot}地號")
        os.makedirs(save_dir, exist_ok=True)
        screenshot_path = os.path.join(save_dir, f"臺中市{district}{section_name}{lot}地號_都計截圖.png")
        with open(screenshot_path, "wb") as f:
            f.write(urban_screenshot_bytes)
        land_texts.append(f"都計截圖路徑：{screenshot_path}")
    except Exception:
        pass

    return land_texts


def _parse_license_number(lic_str: str):
    """拆解執照號碼字串，例：114中都建字第00273號 → (year, kind_value, number)"""
    m = re.match(r'(\d{3})[^\d]*?([建雜使拆])[^\d]*(\d+)', lic_str)
    if not m:
        return None
    year = m.group(1)
    kind_char = m.group(2)
    number = m.group(3).zfill(5)
    kind_map = {'建': '1', '雜': '2', '使': '3', '拆': '4'}
    return year, kind_map.get(kind_char, '1'), number


def _license_priority(num_str: str) -> int:
    """執照優先順序：變更使用執照(3) > 使用執照(2) > 建照/其他(1)"""
    if '變使' in num_str:
        return 3
    if re.search(r'使字|使許字', num_str):
        return 2
    return 1


def _best_license(gis_texts: list) -> tuple:
    """從 gis_texts 選出最佳執照：優先變使 > 使 > 建，同優先取最新日期。
    回傳 (num_str, date_str) 或 None（查無執照）。"""
    entries = []
    for t in gis_texts:
        if not t.startswith("執照查詢：") or "查無" in t:
            continue
        m = re.search(r'執照查詢：(\S+)\s+發照日期：(\S*)', t)
        if m:
            entries.append((m.group(1), m.group(2)))

    if not entries:
        return None

    def sort_key(entry):
        num_str, date_str = entry
        mm = re.match(r'(\d+)/(\d+)/(\d+)', date_str or '')
        date_val = int(mm.group(1)) * 10000 + int(mm.group(2)) * 100 + int(mm.group(3)) if mm else 0
        return (_license_priority(num_str), date_val)

    return max(entries, key=sort_key)


def _query_bupic(license_str: str) -> dict:
    """查詢建築執照存根，含詳細頁面資料"""
    parsed = _parse_license_number(license_str)
    if not parsed:
        return {"error": f"無法解析執照號碼：{license_str}"}
    year, kind_value, number = parsed

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=200)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()

        captcha_code = None
        def on_response(resp):
            nonlocal captcha_code
            if 'getCheckCode' in resp.url:
                try:
                    captcha_code = resp.text().strip().strip('"')
                except Exception:
                    pass
        page.on("response", on_response)

        page.goto("https://mcgbm.taichung.gov.tw/bupic/pages/querylic")
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)

        page.evaluate("() => { document.getElementById('QType1').click(); }")
        time.sleep(0.5)
        page.fill("#license_yy", year)
        page.select_option("#licenseKind", value=kind_value)
        page.fill("#license_no1", number)
        time.sleep(1.5)

        if captcha_code:
            page.fill("#inputCode", captcha_code)

        page.evaluate("() => { document.getElementById('btnLogin').click(); }")
        time.sleep(5)

        has_result = page.evaluate("() => !!document.querySelector('button.link-btn')")
        if not has_result:
            browser.close()
            return {"查詢結果": "查無執照存根資料"}

        # 從列表頁抓「建築地址」（結果表格第一行的地址欄）
        list_address = page.evaluate("""() => {
            const rows = document.querySelectorAll('table tbody tr, .table tbody tr');
            for (const tr of rows) {
                const tds = tr.querySelectorAll('td');
                // 建築地址通常在第4欄（index 3）
                if (tds.length >= 4 && tds[3].innerText.trim()) {
                    return tds[3].innerText.trim();
                }
            }
            return '';
        }""")

        # 點執照號碼連結進入詳細頁
        with context.expect_page(timeout=10000) as new_page_info:
            page.evaluate("() => { document.querySelector('button.link-btn').click(); }")
            time.sleep(1)

        detail = new_page_info.value
        detail.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(3)

        # 抓詳細頁：用 div.titl_01 + div.conlist01 結構
        detail_data = detail.evaluate("""() => {
            const result = {};

            // 主要 label/value：titl_01 + 同層 conlist01
            document.querySelectorAll('.titl_01').forEach(label => {
                const key = label.innerText.trim();
                const row = label.closest('.row');
                if (!row) return;
                const val_el = row.querySelector('.conlist01');
                if (!val_el) return;

                // 收集二級 label/value（licdtiltit_02）
                const sub = {};
                val_el.querySelectorAll('.licdtiltit_02').forEach(sl => {
                    const sk = sl.innerText.trim();
                    const sib = sl.nextElementSibling;
                    if (sib) {
                        const sv = sib.innerText.trim().replace(/查看變更[^\\n]*/g, '').trim();
                        if (sv && sv !== '＊＊＊') sub[sk] = sv;
                    }
                });

                if (Object.keys(sub).length > 0) {
                    result[key] = sub;
                } else {
                    const txt = val_el.innerText.trim().replace(/查看變更[^\\n]*/g, '').trim();
                    if (txt && txt !== '＊＊＊') result[key] = txt;
                }
            });

            // 地段地號 (DataTable #datatablelan)
            const landTbl = document.querySelector('#datatablelan');
            if (landTbl) {
                result['_地段地號'] = Array.from(landTbl.querySelectorAll('tbody tr')).map(tr =>
                    Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim())
                );
            }

            // 樓層概要 (#stair div-based)
            const stairDiv = document.querySelector('#stair');
            if (stairDiv) {
                const headers = Array.from(stairDiv.querySelectorAll('.thead > div'))
                    .map(d => d.innerText.trim());
                const rows = Array.from(stairDiv.querySelectorAll('.tbody')).map(row =>
                    Array.from(row.children).map(d => d.innerText.trim())
                );
                result['_樓層概要'] = { headers, rows };
            }

            // 備註 (#memo div-based)
            const memoDiv = document.querySelector('#memo');
            if (memoDiv) {
                result['_備註'] = Array.from(memoDiv.querySelectorAll('.tbody')).map(row => {
                    const children = Array.from(row.children);
                    return children.length >= 2 ? children[1].innerText.trim() : '';
                }).filter(r => r);
            }

            // 停車空間 (#park div-based)
            const parkDiv = document.querySelector('#park');
            if (parkDiv) {
                const headers = Array.from(parkDiv.querySelectorAll('.thead > div'))
                    .map(d => d.innerText.trim());
                const rows = Array.from(parkDiv.querySelectorAll('.tbody')).map(row =>
                    Array.from(row.children).map(d => d.innerText.trim())
                );
                result['_停車空間'] = { headers, rows };
            }

            return result;
        }""")

        browser.close()

    if list_address:
        detail_data["建築地址"] = list_address
    return {"執照存根詳細": detail_data}


def _bupic_address(d: dict) -> str:
    """從 bupic 執照存根詳細 dict 取出門牌地址（不同執照類型欄位名不同）"""
    # 建築地址（從列表頁抓）或使用執照常見欄位：工程地點
    for key in ("建築地址", "工程地點", "工程地址", "地址"):
        val = d.get(key, "")
        if val and "＊＊＊" not in str(val):
            return str(val).strip()
    # 基地概要內的街道欄位（部分版本）
    基地 = d.get("基地概要", {})
    if isinstance(基地, dict):
        for key in ("工程地點", "街道", "門牌", "地址"):
            val = 基地.get(key, "")
            if val and "＊＊＊" not in str(val):
                return str(val).strip()
    return ""


def _bupic_worker(license_str: str, out_file: str):
    """子程序入口：查建築執照存根，結果寫到 out_file"""
    result = _query_bupic(license_str)
    # debug：印出所有欄位名，方便找地址欄
    d = result.get("執照存根詳細", {})
    top_keys = [k for k in d if not k.startswith("_")]
    print(f"[bupic] {license_str} 欄位：{top_keys}", flush=True)
    基地 = d.get("基地概要", {})
    if isinstance(基地, dict):
        print(f"[bupic] 基地概要子欄位：{list(基地.keys())}", flush=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


def _query_slope(district: str, section_name: str, lot: str, save_pdf_to: str = None) -> dict:
    """查詢山坡地 https://wrbeochi.taichung.gov.tw/4LIDEP"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=200)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.on("dialog", lambda d: d.dismiss())

        page.goto("https://wrbeochi.taichung.gov.tw/4LIDEP")
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)

        try:
            page.select_option("#ddlTown", label=district)
        except Exception:
            browser.close()
            return {"error": f"山坡地系統找不到行政區：{district}"}
        time.sleep(2)

        try:
            page.select_option("#ddlSect", label=section_name)
        except Exception:
            browser.close()
            return {"error": f"山坡地系統找不到地段：{section_name}"}
        time.sleep(1)

        page.fill("#txtLand", lot)
        page.click("#btnSearch")
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(3)

        result = page.evaluate("""() => {
            const table = document.querySelector('.main_Table');
            if (!table) return null;
            const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.innerText.trim());
            const rows = Array.from(table.querySelectorAll('tbody tr')).map(tr =>
                Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim())
            );
            return { headers, rows };
        }""")

        if save_pdf_to and page.query_selector(".btn_download"):
            try:
                resp_json = page.evaluate("""async () => {
                    const token = $('input[name="__RequestVerificationToken"]').val().trim();
                    const a = document.querySelector('.btn_download');
                    const opt = {
                        SectId: a.dataset.sect,
                        TownName: a.dataset.town,
                        SectName: a.dataset.sectname,
                        LandNo: a.dataset.land,
                        IsSlope: a.dataset.slope,
                        IsViolate: a.dataset.punish,
                        IsReservoir: a.dataset.reservoir,
                        IsActiveFault: a.dataset.activefault,
                        IsUnderWater: a.dataset.underwater,
                        IsLandSlide: a.dataset.landslide,
                        IsSoilWater: a.dataset.soilwater,
                        IsNationalPark: a.dataset.nationalpark,
                        IsMudslide: a.dataset.mudslide
                    };
                    return new Promise((resolve, reject) => {
                        $.ajax({
                            url: '/4LIDEP/Map/DownloadSlpoeReport',
                            method: 'post',
                            headers: { RequestVerificationToken: token },
                            data: { Dto: opt },
                            dataType: 'json',
                            success: resolve,
                            error: () => resolve(null)
                        });
                    });
                }""")
                if resp_json and resp_json.get("success") and resp_json.get("url"):
                    pdf_url = "https://wrbeochi.taichung.gov.tw" + resp_json["url"]
                    resp = page.context.request.get(pdf_url)
                    if resp.ok:
                        os.makedirs(os.path.dirname(save_pdf_to), exist_ok=True)
                        with open(save_pdf_to, "wb") as f:
                            f.write(resp.body())
            except Exception:
                pass

        browser.close()

    if not result or not result.get("rows"):
        return {"error": "查無山坡地資料"}

    headers = result["headers"]
    row = result["rows"][0]
    data = {}
    skip = {"序號", "行政區", "地段", "地號", "查詢表"}
    for i, h in enumerate(headers):
        if h not in skip and i < len(row):
            data[h] = row[i]
    return {"山坡地查詢": data}


def _slope_worker(district: str, section_name: str, lot: str, out_file: str):
    """子程序入口：查山坡地，結果寫到 out_file"""
    save_dir = os.path.expanduser(f"~/Desktop/查詢結果/臺中市{district}{section_name}{lot}地號")
    os.makedirs(save_dir, exist_ok=True)
    pdf_path = os.path.join(save_dir, f"臺中市{district}{section_name}{lot}地號_山坡地.pdf")
    result = _query_slope(district, section_name, lot, save_pdf_to=pdf_path)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


def _query_gsa(district: str, section_name: str, lot: str, save_pdf_to: str = None) -> dict:
    """查詢地質敏感區 https://gsa.gsmma.gov.tw"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=200)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()
        page.on("dialog", lambda d: d.dismiss())

        page.goto("https://gsa.gsmma.gov.tw/gwh/gsb97-1/sys_2014b_pg/index.cfm")
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)
        page.click('input[value="進入系統"]')
        time.sleep(2)

        locate_frame = next((f for f in page.frames if "locate.cfm" in f.url), None)
        if not locate_frame:
            browser.close()
            return {"error": "找不到查詢框架"}

        locate_frame.evaluate("window.alert = function() {}")
        locate_frame.select_option("[name=parcel_coun]", value="臺中市")
        time.sleep(2)
        locate_frame.select_option("[name=town_name]", label=district)
        time.sleep(2)

        sect_value = locate_frame.evaluate(f"""() => {{
            const opts = Array.from(document.querySelector('[name=sect]').options);
            const target = "{section_name}";
            const opt = opts.find(o => o.text.replace(/^\\(\\d+\\)/, '').trim() === target);
            return opt ? opt.value : null;
        }}""")

        if not sect_value:
            browser.close()
            return {"error": f"地質敏感區系統找不到此地段：{section_name}"}

        locate_frame.select_option("[name=sect]", value=sect_value)
        time.sleep(1)
        locate_frame.fill("[name=landno]", lot)
        locate_frame.evaluate("() => { document.querySelector('[name=gen_type][value=s]').click(); }")
        time.sleep(0.5)
        locate_frame.click("#btn4")

        # 輪詢等待 qry_result frame 出現且有內容（最多等 30 秒）
        text = ""
        qry_frame = None
        for _ in range(30):
            time.sleep(1)
            qry_frame = next((f for f in page.frames if f.name == "qry_result"), None)
            if qry_frame:
                text = qry_frame.evaluate("() => document.body.innerText").strip()
                if text:
                    break

        if not qry_frame or not text:
            browser.close()
            return {"error": "查詢結果框未出現或無內容"}

        if save_pdf_to:
            try:
                security_code = qry_frame.evaluate("""() => {
                    const els = Array.from(document.querySelectorAll('[onclick]'));
                    for (const el of els) {
                        const onclick = el.getAttribute('onclick') || '';
                        const m = onclick.match(/go\\('([^']+)'\\)/);
                        if (m) return m[1];
                    }
                    return null;
                }""")
                if security_code:
                    dl_page_url = (
                        "https://gsa.gsmma.gov.tw/gwh/gsb97-1/sys_2014b_pg/"
                        f"dl_pdf.cfm?security_code={security_code}"
                    )
                    resp = context.request.get(dl_page_url)
                    if resp.ok:
                        import re as _re
                        body_text = resp.text()
                        m = _re.search(r'href="([^"]+\.pdf)"', body_text, _re.IGNORECASE)
                        if m:
                            real_pdf_path = m.group(1)
                            if real_pdf_path.startswith("/"):
                                real_pdf_url = "https://gsa.gsmma.gov.tw" + real_pdf_path
                            else:
                                real_pdf_url = real_pdf_path
                            pdf_resp = context.request.get(real_pdf_url)
                            if pdf_resp.ok:
                                os.makedirs(os.path.dirname(save_pdf_to), exist_ok=True)
                                with open(save_pdf_to, "wb") as f:
                                    f.write(pdf_resp.body())
            except Exception:
                pass

        browser.close()

    return {"地質敏感區查詢": text or "查無資料"}


def _gsa_worker(district: str, section_name: str, lot: str, out_file: str):
    """子程序入口：查地質敏感區，結果寫到 out_file"""
    save_dir = os.path.expanduser(f"~/Desktop/查詢結果/臺中市{district}{section_name}{lot}地號")
    os.makedirs(save_dir, exist_ok=True)
    pdf_path = os.path.join(save_dir, f"臺中市{district}{section_name}{lot}地號_地質敏感區.pdf")
    result = _query_gsa(district, section_name, lot, save_pdf_to=pdf_path)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


def _query_sewer(district: str, section_code: str, lot: str) -> dict:
    """查詢臺中市下水道GIS系統（tcswg）用戶接管狀態。
    回傳：{公告特定區, 工程進度, 工程名稱, 工程聯絡窗口資訊, 公告可使用地區日期}"""
    lot_parts = lot.split("-")
    lot_main = lot_parts[0]
    lot_sub = lot_parts[1] if len(lot_parts) > 1 else "0"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        try:
            page.goto("https://tcswg.taichung.gov.tw/TCPublic/")
            page.wait_for_load_state("networkidle", timeout=30000)
            time.sleep(3)

            page.evaluate("() => document.querySelector('[data-maptool=\"用戶接管查詢\"]').click()")
            time.sleep(2)
            page.evaluate("() => document.querySelector('[data-tab=\"cad\"]').click()")
            time.sleep(1)

            page.select_option("#lt-cad-district", value=district)
            time.sleep(2.5)

            # 確認此地段代碼在 tcswg 系統中存在
            has_sect = page.evaluate(
                f"""() => !!document.querySelector('#lt-cad-section option[value="{section_code}"]')"""
            )
            if not has_sect:
                return {"結果": "非污水下水道系統涵蓋範圍（地段不在系統內）"}

            page.select_option("#lt-cad-section", value=section_code)
            time.sleep(1)

            page.fill("#lt-cad-no-AA49_1", lot_main)
            page.fill("#lt-cad-no-AA49_2", lot_sub)

            # 點開始查詢，等 giscloud LAND API 回應後再等 ArcGIS 圖層交叉比對
            try:
                with page.expect_response(
                    lambda r: 'giscloud.taichung.gov.tw' in r.url and 'webapi' in r.url,
                    timeout=15000
                ) as _:
                    page.evaluate("() => document.querySelector('#lt-pane-cad button').click()")
            except Exception:
                pass
            # 等 ArcGIS 圖層查詢完成（結果出現在 DOM 中）
            try:
                page.wait_for_function(
                    "() => document.querySelector('#lt-pane-cad').innerText.includes('公告特定區')",
                    timeout=20000
                )
            except Exception:
                time.sleep(8)

            result_text = page.evaluate("() => document.querySelector('#lt-pane-cad').innerText")
        finally:
            browser.close()

    result = {}
    for key in ['公告特定區', '工程進度', '工程名稱', '工程聯絡窗口資訊', '公告可使用地區日期']:
        m = re.search(rf'{key}[：:]\s*(.+)', result_text)
        if m:
            result[key] = m.group(1).strip()
    if not result:
        result['結果'] = '查詢失敗或無結果'
    return result


def _sewer_worker(district: str, section_code: str, lot: str, out_file: str):
    result = _query_sewer(district, section_code, lot)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


_FAULT_DISTRICT_CODES = {
    "中區": "B01", "東區": "B02", "南區": "B03", "西區": "B04",
    "北區": "B05", "西屯區": "B06", "南屯區": "B07", "北屯區": "B08",
    "豐原區": "B09", "東勢區": "B10", "大甲區": "B11", "清水區": "B12",
    "沙鹿區": "B13", "梧棲區": "B14", "后里區": "B15", "神岡區": "B16",
    "潭子區": "B17", "大雅區": "B18", "新社區": "B19", "石岡區": "B20",
    "外埔區": "B21", "大安區": "B22", "烏日區": "B23", "大肚區": "B24",
    "龍井區": "B25", "霧峰區": "B26", "太平區": "B27", "大里區": "B28",
    "和平區": "B29",
}


def _query_fault(district: str, section_name: str, lot: str, save_pdf_to: str = None) -> dict:
    """查詢台灣活動斷層 GIS (https://faultgis.gsmma.gov.tw/gis/)，
    計算地號到各活動斷層的最短距離，並繪製量測線截圖"""
    import io as _io
    from PIL import Image as _Image

    district_code = _FAULT_DISTRICT_CODES.get(district)
    if not district_code:
        return {"error": f"不支援的行政區：{district}"}

    section_code = find_section_code(district, section_name)
    lot_main = lot.split("-")[0]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        ctx = browser.new_context(viewport={"width": 1400, "height": 900})
        page = ctx.new_page()

        try:
            page.goto("https://faultgis.gsmma.gov.tw/gis/", timeout=60000, wait_until="domcontentloaded")
            page.wait_for_selector('iframe[src*="index_3.cfm"]', timeout=30000)
            time.sleep(3)
        except Exception as e:
            browser.close()
            return {"error": f"無法連線活動斷層 GIS：{e}"}

        notice = next((f for f in page.frames if "notice.cfm" in f.url), None)
        if notice:
            try:
                notice.evaluate("() => document.querySelector('a[onclick=\"agreeUseAuthority();\"]').click()")
            except Exception:
                pass
            time.sleep(2)
        notice2 = next((f for f in page.frames if "notice_data.cfm" in f.url), None)
        if notice2:
            try:
                notice2.evaluate("() => { const a = document.querySelector('a[onclick=\"close_win();\"]'); if(a) a.click(); }")
            except Exception:
                pass
            time.sleep(1)

        page.evaluate("() => sidebaropen(3, {preventDefault:()=>{}})")
        time.sleep(2)

        sb2 = next((f for f in page.frames if "sidebar2" in f.url), None)
        if not sb2:
            browser.close()
            return {"error": "找不到地號搜尋面板"}

        sb2.select_option("#landPosition_admin_cbx", value="B")
        time.sleep(2)
        sb2.select_option("#landPosition_admit_cbx", value=district_code)
        time.sleep(2)

        try:
            sb2.select_option("#landPosition_sec_cbx", value=section_code)
        except Exception:
            try:
                sb2.select_option("#landPosition_sec_cbx", label=section_name)
            except Exception as e2:
                browser.close()
                return {"error": f"找不到地段 {section_name}：{e2}"}
        time.sleep(1)

        sb2.fill("#landPosition_m_landNo_txt", lot_main)
        sb2.fill("#landPosition_s_landNo_txt", "")
        sb2.evaluate("() => doLandPosition()")
        time.sleep(5)

        mf = next((f for f in page.frames if "index_3.cfm" in f.url), None)
        if not mf:
            browser.close()
            return {"error": "找不到地圖框架"}

        # 取得地號 EPSG:3857 座標
        parcel_coord = mf.evaluate("""() => {
            const layers = window.map.getLayers().getArray();
            for (let i = layers.length - 1; i >= 0; i--) {
                const s = layers[i].getSource && layers[i].getSource();
                if (!s || !s.getFeatures) continue;
                const feats = s.getFeatures();
                if (feats.length > 0) {
                    const g = feats[feats.length - 1].getGeometry();
                    if (g && g.getType() === 'Point') return g.getCoordinates();
                }
            }
            return window.map.getView().getCenter();
        }""")

        # 計算各斷層最近距離（在 browser JS 中執行，避免大量資料傳輸）
        fault_distances = mf.evaluate("""([px, py]) => {
            function distPtToSeg(px, py, ax, ay, bx, by) {
                const dx = bx - ax, dy = by - ay;
                if (dx === 0 && dy === 0) return {d: Math.hypot(px-ax, py-ay), cx:ax, cy:ay};
                const t = Math.max(0, Math.min(1, ((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy)));
                const cx = ax+t*dx, cy = ay+t*dy;
                return {d: Math.hypot(px-cx, py-cy), cx, cy};
            }
            const cos24 = Math.cos(24 * Math.PI / 180);
            const layers = window.map.getLayers().getArray();
            let faultLayer = null;
            for (let i = 0; i < layers.length; i++) {
                const s = layers[i].getSource && layers[i].getSource();
                if (!s || !s.getFeatures) continue;
                const feats = s.getFeatures();
                if (feats.length > 5 && feats[0].get('FAULT_NAME')) { faultLayer = layers[i]; break; }
            }
            if (!faultLayer) return [];
            const byName = {};
            for (const f of faultLayer.getSource().getFeatures()) {
                const name = f.get('FAULT_NAME') || '未知斷層';
                if (!byName[name]) byName[name] = {bestDist: Infinity, bestPt: null};
                for (const ring of f.getGeometry().getCoordinates()) {
                    for (let i = 0; i < ring.length - 1; i++) {
                        const r = distPtToSeg(px, py, ring[i][0], ring[i][1], ring[i+1][0], ring[i+1][1]);
                        if (r.d < byName[name].bestDist) {
                            byName[name].bestDist = r.d;
                            byName[name].bestPt = [r.cx, r.cy];
                        }
                    }
                }
            }
            return Object.entries(byName)
                .map(([n, e]) => ({name: n, distM: Math.round(e.bestDist * cos24), nearestPt: e.bestPt}))
                .sort((a, b) => a.distM - b.distM)
                .slice(0, 5);
        }""", parcel_coord)

        if not fault_distances:
            browser.close()
            return {"error": "無法從地圖計算斷層距離"}

        # 縮放到包含前4個斷層的範圍；同側（方向差 < 60°）只取最近的
        import math as _math
        _px_c, _py_c = parcel_coord
        _draw, _angles = [], []
        for _f in fault_distances:
            _np = _f.get("nearestPt")
            if _np:
                _ang = _math.degrees(_math.atan2(_np[1] - _py_c, _np[0] - _px_c))
                if any(min(abs(_ang - _a), 360 - abs(_ang - _a)) < 60 for _a in _angles):
                    continue
                _angles.append(_ang)
            _draw.append(_f)
            if len(_draw) >= 4:
                break
        top_faults = _draw
        all_pts = [parcel_coord] + [f["nearestPt"] for f in top_faults if f.get("nearestPt")]
        xs = [c[0] for c in all_pts]
        ys = [c[1] for c in all_pts]
        buf = 3000
        xmin, xmax = min(xs) - buf, max(xs) + buf
        ymin, ymax = min(ys) - buf, max(ys) + buf

        mf.evaluate(
            f"() => window.map.getView().fit([{xmin},{ymin},{xmax},{ymax}],"
            f"{{size:window.map.getSize(), padding:[60,60,60,60]}})"
        )
        time.sleep(2)
        try:
            mf.evaluate(
                "() => new Promise((r,j) => { window.map.once('rendercomplete', r); setTimeout(j,5000,'timeout'); })"
            )
        except Exception:
            pass
        time.sleep(1)

        # 取得像素位置
        px_info = mf.evaluate("""([parcel, faults]) => ({
            parcel: window.map.getPixelFromCoordinate(parcel),
            faults: faults.map(f => ({
                name: f.name,
                px: f.nearestPt ? window.map.getPixelFromCoordinate(f.nearestPt) : null
            }))
        })""", [parcel_coord, top_faults])

        # 開啟距離量測工具
        mf.locator(".g4o-toolbar-btn.tool-measureLine").click()
        time.sleep(0.3)
        mf.locator(".g4o-toolbar-subbtn.tool-measureLine").click()
        time.sleep(0.5)

        canvas_el = mf.locator(".ol-viewport canvas").first
        parcel_px = px_info["parcel"]

        for fault in px_info["faults"]:
            fpx = fault.get("px")
            if not fpx:
                continue
            canvas_el.click(position={"x": int(parcel_px[0]), "y": int(parcel_px[1])})
            time.sleep(0.3)
            canvas_el.click(position={"x": int(fpx[0]), "y": int(fpx[1])})
            time.sleep(0.2)
            canvas_el.click(position={"x": int(fpx[0]), "y": int(fpx[1])})
            time.sleep(0.7)

        time.sleep(1)
        screenshot_bytes = page.screenshot(clip={"x": 270, "y": 0, "width": 1130, "height": 900})

        if save_pdf_to:
            try:
                os.makedirs(os.path.dirname(save_pdf_to), exist_ok=True)
                # 監聽 #pdf_link href，等伺服器回傳 PDF URL
                page.evaluate("""() => {
                    window._pdfUrl = null;
                    const obs = new MutationObserver(() => {
                        const link = document.querySelector('#pdf_link');
                        if (link && link.href && link.href.includes('pdf')) {
                            window._pdfUrl = link.href;
                        }
                    });
                    obs.observe(document.body, {childList:true, subtree:true, attributes:true, attributeFilter:['href']});
                }""")
                mf.locator(".g4o-toolbar-btn.tool-print-simple").click()
                pdf_url = None
                for _ in range(30):
                    time.sleep(0.5)
                    u = page.evaluate("() => window._pdfUrl || null")
                    if u and "pdf" in u:
                        pdf_url = u.strip()
                        break
                if pdf_url:
                    resp = page.request.get(pdf_url)
                    with open(save_pdf_to, "wb") as f:
                        f.write(resp.body())
                else:
                    # fallback：PIL 截圖轉 PDF
                    img = _Image.open(_io.BytesIO(screenshot_bytes))
                    img.save(save_pdf_to, "PDF", resolution=150)
            except Exception:
                try:
                    img = _Image.open(_io.BytesIO(screenshot_bytes))
                    img.save(save_pdf_to, "PDF", resolution=150)
                except Exception:
                    pass

        browser.close()

    fault_summary = "\n".join(
        f"  {f['name']}：{f['distM']:,} 公尺" for f in fault_distances
    )
    return {
        "臺灣活動斷層": fault_summary,
        "斷層距離": fault_distances,
        "截圖": screenshot_bytes,
    }


def _fault_worker(district: str, section_name: str, lot: str, out_file: str):
    """子程序入口：查台灣活動斷層，結果寫到 out_file"""
    save_dir = os.path.expanduser(f"~/Desktop/查詢結果/臺中市{district}{section_name}{lot}地號")
    os.makedirs(save_dir, exist_ok=True)
    pdf_path = os.path.join(save_dir, f"臺中市{district}{section_name}{lot}地號_活動斷層.pdf")
    result = _query_fault(district, section_name, lot, save_pdf_to=pdf_path)
    if "截圖" in result:
        img_path = out_file.replace(".json", "_fault.png")
        with open(img_path, "wb") as f:
            f.write(result["截圖"])
        result["截圖路徑"] = img_path
        del result["截圖"]
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


def _overlay_worker(district: str, section_code: str, lot: str, out_file: str):
    """子程序入口：查套繪並把結果寫到 out_file（JSON）"""
    lot_parts = lot.split("-")
    lot_main, lot_sub = lot_parts[0], (lot_parts[1] if len(lot_parts) > 1 else "0")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=200)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        result = query_overlay(context, district, section_code, lot_main, lot_sub)
        browser.close()

    # 截圖另存，result 中用路徑取代 bytes
    if "截圖" in result:
        img_path = out_file.replace(".json", ".png")
        with open(img_path, "wb") as f:
            f.write(result["截圖"])
        result["截圖路徑"] = img_path
        del result["截圖"]

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


def _firebreak_worker(district: str, section_code: str, lot: str, out_file: str):
    """子程序入口：查防火間隔，結果寫到 out_file"""
    lot_parts = lot.split("-")
    lot_main, lot_sub = lot_parts[0], (lot_parts[1] if len(lot_parts) > 1 else "0")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=200)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        result = query_firebreak(context, district, section_code, lot_main, lot_sub)
        browser.close()

    if "截圖" in result:
        img_path = out_file.replace(".json", ".png")
        with open(img_path, "wb") as f:
            f.write(result["截圖"])
        result["截圖路徑"] = img_path
        del result["截圖"]

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


def query_batch(queries: list, headless: bool = False) -> list:
    """
    批次查詢多筆地號，同時查 lohas GIS（主程序）、建築套繪圖和建築執照存根（subprocess 並行）。

    Args:
        queries: [(district, section_name, lot_number), ...]
    Returns:
        [(district, section_name, lot_number, gis_texts, overlay_result, bupic_result), ...]
    """
    results = []
    script_path = os.path.abspath(__file__)

    with sync_playwright() as p:
        gis_browser = p.chromium.launch(headless=headless, slow_mo=300)
        gis_context = gis_browser.new_context(viewport={"width": 1400, "height": 900})
        gis_page = gis_context.new_page()
        gis_page.goto("https://lohas.taichung.gov.tw/webgis/")
        gis_page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(3)
        gis_page.evaluate("() => { const l=document.getElementById('layui-layer1'); if(l){const b=l.querySelectorAll('a');if(b.length>0)b[0].click();}}")
        time.sleep(1.5)

        current_district = ""
        current_section = ""

        for district, section_name, lot in queries:
            code = find_section_code(district, section_name)
            print(f"查詢中：{district} {section_name} {lot}地號...")

            # 啟動地號→地址反查 subprocess（與 GIS 查詢並行，僅在無 address 輸入時啟動）
            lot2addr_file = tempfile.mktemp(suffix=".json")
            proc_lot2addr = subprocess.Popen([
                sys.executable, script_path,
                "--lot2addr-worker", district, section_name, lot, lot2addr_file
            ])

            # 啟動套繪查詢 subprocess（與 GIS 查詢並行）
            overlay_file = tempfile.mktemp(suffix=".json")
            proc_overlay = subprocess.Popen([
                sys.executable, script_path,
                "--overlay-worker", district, code, lot, overlay_file
            ])

            # 啟動防火間隔查詢 subprocess（與 GIS 查詢並行）
            firebreak_file = tempfile.mktemp(suffix=".json")
            proc_firebreak = subprocess.Popen([
                sys.executable, script_path,
                "--firebreak-worker", district, code, lot, firebreak_file
            ])

            # 啟動地質敏感區查詢 subprocess（與 GIS 查詢並行）
            gsa_file = tempfile.mktemp(suffix=".json")
            proc_gsa = subprocess.Popen([
                sys.executable, script_path,
                "--gsa-worker", district, section_name, lot, gsa_file
            ])

            # 啟動山坡地查詢 subprocess（與 GIS 查詢並行）
            slope_file = tempfile.mktemp(suffix=".json")
            proc_slope = subprocess.Popen([
                sys.executable, script_path,
                "--slope-worker", district, section_name, lot, slope_file
            ])

            # 啟動污水下水道接管查詢 subprocess（與 GIS 查詢並行）
            sewer_file = tempfile.mktemp(suffix=".json")
            proc_sewer = subprocess.Popen([
                sys.executable, script_path,
                "--sewer-worker", district, code, lot, sewer_file
            ])

            # 啟動台灣活動斷層查詢 subprocess（與 GIS 查詢並行）
            fault_file = tempfile.mktemp(suffix=".json")
            proc_fault = subprocess.Popen([
                sys.executable, script_path,
                "--fault-worker", district, section_name, lot, fault_file
            ])

            # 主程序同步查 GIS（含建號和執照號碼）
            gis_texts = _query_one(gis_page, district, section_name, code, lot,
                                   current_district, current_section)

            # 從 GIS 結果選最佳執照（變使 > 使 > 建，同優先取最新日期）
            # 建物查詢區塊保留所有執照號碼；存根只查最佳那筆
            best_lic = _best_license(gis_texts)
            license_nums = [best_lic[0]] if best_lic else []

            bupic_procs = []
            for lic in license_nums:
                bupic_file = tempfile.mktemp(suffix=".json")
                proc_b = subprocess.Popen([
                    sys.executable, script_path,
                    "--bupic-worker", lic, bupic_file
                ])
                bupic_procs.append((lic, proc_b, bupic_file))

            # 啟動都市計畫土地使用管制 PDF 查詢 subprocess（GIS 完成後，需要 都計JSON）
            ud_file = tempfile.mktemp(suffix=".json")
            proc_ud = None
            _ud_skip_reason = None
            ud_save_dir = os.path.expanduser(f"~/Desktop/查詢結果/臺中市{district}{section_name}{lot}地號")
            urban_json_str_ud = next((t[len("都計JSON："):] for t in gis_texts if t.startswith("都計JSON：")), None)
            if not urban_json_str_ud:
                _ud_skip_reason = "非都市計畫區域或 GIS 未取得分區資料"
            else:
                try:
                    ud_urban = json.loads(urban_json_str_ud)
                    if isinstance(ud_urban, list) and ud_urban:
                        u0 = ud_urban[0]
                        plan_area = u0.get("都市計畫區", "") or u0.get("都計名稱", "")
                        plan_case = u0.get("計畫案名", "") or u0.get("細部計畫區", "")
                        if plan_area or plan_case:
                            proc_ud = subprocess.Popen([
                                sys.executable, script_path,
                                "--ud-worker", plan_area, plan_case, ud_save_dir, ud_file
                            ])
                        else:
                            _ud_skip_reason = f"都計分區資料缺少必要欄位（keys: {list(u0.keys())}）"
                    else:
                        _ud_skip_reason = "都計JSON 為空"
                except Exception as e:
                    _ud_skip_reason = f"都計JSON 解析失敗：{e}"

            # 等套繪完成
            proc_overlay.wait(timeout=120)
            if os.path.exists(overlay_file):
                with open(overlay_file, encoding="utf-8") as f:
                    overlay_res = json.load(f)
                os.unlink(overlay_file)
            else:
                overlay_res = {"error": "套繪查詢未回傳結果"}

            # 等防火間隔完成
            proc_firebreak.wait(timeout=120)
            if os.path.exists(firebreak_file):
                with open(firebreak_file, encoding="utf-8") as f:
                    firebreak_res = json.load(f)
                os.unlink(firebreak_file)
            else:
                firebreak_res = {"error": "防火間隔查詢未回傳結果"}

            # 等 bupic 完成
            bupic_results = []
            for lic, proc_b, bupic_file in bupic_procs:
                proc_b.wait(timeout=60)
                if os.path.exists(bupic_file):
                    with open(bupic_file, encoding="utf-8") as f:
                        bupic_results.append(json.load(f))
                    os.unlink(bupic_file)
                else:
                    bupic_results.append({"error": f"bupic 查詢失敗：{lic}"})

            # 等地質敏感區完成
            proc_gsa.wait(timeout=120)
            if os.path.exists(gsa_file):
                with open(gsa_file, encoding="utf-8") as f:
                    gsa_res = json.load(f)
                os.unlink(gsa_file)
            else:
                gsa_res = {"error": "地質敏感區查詢未回傳結果"}

            # 等山坡地完成
            proc_slope.wait(timeout=120)
            if os.path.exists(slope_file):
                with open(slope_file, encoding="utf-8") as f:
                    slope_res = json.load(f)
                os.unlink(slope_file)
            else:
                slope_res = {"error": "山坡地查詢未回傳結果"}

            # 等污水下水道接管查詢完成
            proc_sewer.wait(timeout=120)
            if os.path.exists(sewer_file):
                with open(sewer_file, encoding="utf-8") as f:
                    sewer_res = json.load(f)
                os.unlink(sewer_file)
            else:
                sewer_res = {"error": "污水接管查詢未回傳結果"}

            # 等台灣活動斷層查詢完成
            proc_fault.wait(timeout=180)
            if os.path.exists(fault_file):
                with open(fault_file, encoding="utf-8") as f:
                    fault_res = json.load(f)
                os.unlink(fault_file)
            else:
                fault_res = {"error": "活動斷層查詢未回傳結果"}

            # 套繪有上色但執照仍查無（含重測前地號重試後）→ 加異常備注
            if (isinstance(overlay_res, dict) and overlay_res.get("有上色")
                    and "執照查詢：查無執照" in gis_texts):
                gis_texts = [
                    "執照查詢：查無執照（資料不正常，請手動確認）" if t == "執照查詢：查無執照" else t
                    for t in gis_texts
                ]

            # 等都計管制 PDF 完成
            ud_res = {}
            if proc_ud:
                proc_ud.wait(timeout=90)
                if os.path.exists(ud_file):
                    with open(ud_file, encoding="utf-8") as f:
                        ud_res = json.load(f)
                    os.unlink(ud_file)
                else:
                    ud_res = {"error": "都計管制 PDF 查詢未回傳結果"}
            elif _ud_skip_reason:
                ud_res = {"error": _ud_skip_reason}

            # 等地號→地址反查完成（最多 60 秒）
            lot2addr_result = ""
            try:
                proc_lot2addr.wait(timeout=60)
                if os.path.exists(lot2addr_file):
                    with open(lot2addr_file, encoding="utf-8") as f:
                        lot2addr_result = json.load(f).get("address", "")
                    os.unlink(lot2addr_file)
            except Exception:
                try:
                    proc_lot2addr.kill()
                except Exception:
                    pass

            results.append((district, section_name, lot, gis_texts, overlay_res, bupic_results, gsa_res, slope_res, firebreak_res, sewer_res, fault_res, ud_res, lot2addr_result))
            current_district = district
            current_section = code

        gis_browser.close()

    return results


def print_result(district: str, section_name: str, lot: str,
                 texts: list, overlay: dict, bupic_list: list = None, gsa: dict = None, slope: dict = None, firebreak: dict = None, sewer: dict = None, fault: dict = None, ud: dict = None, address: str = ""):
    print()
    print("=" * 60)
    print(f"  {district} {section_name} {lot}地號")
    print(f"  地址：{address if address else '尚無'}")
    print("=" * 60)

    # 分離建物查詢結果與履歷與都計
    build_lines = [t for t in texts if t.startswith("建號查詢：") or t.startswith("執照查詢：")]
    history_json = next((t[len("履歷JSON："):] for t in texts if t.startswith("履歷JSON：")), None)
    urban_json = next((t[len("都計JSON："):] for t in texts if t.startswith("都計JSON：")), None)
    gis_texts = [t for t in texts if not t.startswith("建號查詢：") and not t.startswith("執照查詢：")
                 and not t.startswith("履歷JSON：") and not t.startswith("都計JSON：")
                 and not t.startswith("都計截圖路徑：")]

    # GIS：提取關鍵段落（標籤行後面緊跟的值）
    print("【GIS 分區資訊】")
    key_labels = ['登記面積', '公告地價', '公告現值', '使用資訊', '國土功能分區',
                  '地政事務所', '區段徵收', '登記日期', '自然人']
    value_keywords = ['平方公尺', '住宅區', '商業區', '工業區', '農業區', '保護區',
                      '特定', '城鄉', '元/平方公尺', '地政事務所', '年', '%']
    printed = set()
    for i, t in enumerate(gis_texts):
        if len(t) > 200:
            continue
        # 直接含有意義的行
        if any(kw in t for kw in key_labels) and t not in printed:
            print(f"  {t}")
            printed.add(t)
            # 緊接著的值也印出來
            if i + 1 < len(gis_texts):
                nxt = gis_texts[i + 1]
                if len(nxt) < 150 and nxt not in printed:
                    print(f"    → {nxt}")
                    printed.add(nxt)
        elif any(kw in t for kw in value_keywords) and t not in printed:
            print(f"  {t}")
            printed.add(t)

    if urban_json:
        try:
            zones = json.loads(urban_json)
            if isinstance(zones, dict):
                zones = [zones]
            print()
            print("【都市計畫分區】")
            for i, u in enumerate(zones):
                if len(zones) > 1:
                    print(f"  ── 分區 {i+1} ──")
                for key in ["使用分區", "建蔽率", "容積率", "都市計畫區", "細部計畫區", "計畫案名"]:
                    val = u.get(key, "")
                    if val:
                        print(f"  {key}：{val}")
        except Exception:
            pass

    if history_json:
        try:
            h = json.loads(history_json)
            print()
            print("【履歷 - 分割合併與重測異動】")
            for section_name_h in ["其他登記事項", "分割合併紀錄", "重測前後對照"]:
                tbl = h.get(section_name_h)
                if not tbl or not tbl.get("rows"):
                    continue
                print(f"  ▸ {section_name_h}")
                hdrs = tbl.get("headers", [])
                for row in tbl["rows"]:
                    if hdrs:
                        parts = [f"{hdrs[i]}：{row[i]}" for i in range(min(len(hdrs), len(row))) if row[i]]
                        print(f"    {' | '.join(parts)}")
                    else:
                        print(f"    {' | '.join(c for c in row if c)}")
        except Exception:
            pass

    print()
    print("【建物查詢】")
    for line in build_lines:
        print(f"  {line}")

    if bupic_list:
        print()
        print("【建築執照存根】")
        for bupic in bupic_list:
            if "error" in bupic:
                print(f"  查詢失敗：{bupic['error']}")
            elif "查詢結果" in bupic:
                print(f"  {bupic['查詢結果']}")
            else:
                d = bupic.get("執照存根詳細", {})
                lic_no = (d.get('建造執照號碼') or d.get('使用執照號碼') or
                          d.get('雜項工程執照號碼') or d.get('拆除執照號碼') or '')
                print(f"  執照號碼：{lic_no}")
                def _p(label, val, pad=4):
                    if val and '＊＊＊' not in str(val) and '\n' not in str(val):
                        print(f"  {label}：{val}")
                起造 = d.get('起造人', {})
                if isinstance(起造, dict): _p('起造人', 起造.get('姓名', ''))
                設計 = d.get('設計人', {})
                if isinstance(設計, dict): _p('設計人', f"{設計.get('姓名','')}（{設計.get('事務所','')}）")
                監造 = d.get('監造人', {})
                if isinstance(監造, dict): _p('監造人', f"{監造.get('姓名','')}（{監造.get('事務所','')}）")
                承造 = d.get('承造人', {})
                if isinstance(承造, dict):
                    _p('承造人', 承造.get('姓名', ''))
                    _p('營造廠', 承造.get('營造廠', ''))
                    _p('專任工程人員', 承造.get('專任工程人員', ''))
                基地 = d.get('基地概要', {})
                if isinstance(基地, dict):
                    _p('使用分區', 基地.get('使用分區', ''))
                    _p('基地面積', 基地.get('合計', ''))
                建物 = d.get('建物概要', {})
                if isinstance(建物, dict):
                    for k in ['層棟戶數', '法定空地面積', '設計建蔽率', '設計容積率',
                              '建物高度', '總樓地板面積', '建造類別', '構造種類',
                              '雜項工程', '工程造價', '發照日期']:
                        _p(k, 建物.get(k, ''))
                    ba = 建物.get('建築面積', {})
                    if isinstance(ba, dict): _p('建築面積', ba.get('其他', ''))
                    elif isinstance(ba, str) and '其他' in ba:
                        idx = ba.find('其他\n')
                        if idx >= 0: _p('建築面積', ba[idx+3:].split('\n')[0].strip())
                非供 = d.get('非供公眾使用建築物', '')
                if 非供 and '＊＊＊' not in str(非供): _p('非供公眾使用', 非供)
                執照 = d.get('建築執照', {})
                if isinstance(執照, dict): _p('開工日期', 執照.get('開工日期', ''))
                lands = d.get('_地段地號', [])
                if lands:
                    lots_str = '、'.join(f"{r[2]}{r[3]}地號" for r in lands if len(r) >= 4)
                    print(f"  建築地號：{lots_str}")
                floors = d.get('_樓層概要', {})
                if isinstance(floors, dict) and floors.get('rows'):
                    hdrs = floors.get('headers', [])
                    print("  樓層概要：")
                    for row in floors['rows']:
                        if len(row) >= len(hdrs):
                            layer = row[2] if len(row) > 2 else ''
                            area  = row[4] if len(row) > 4 else ''
                            use   = row[7] if len(row) > 7 else ''
                            if layer and use and '＊＊＊' not in use:
                                print(f"    {layer}  {area}m²  {use}")
                remarks = d.get('_備註', [])
                if remarks:
                    print("  備註：")
                    for i, r in enumerate(remarks, 1):
                        print(f"    {i}. {r}")
                parking = d.get('_停車空間', {})
                if isinstance(parking, dict) and parking.get('rows'):
                    print("  停車空間：")
                    for row in parking['rows']:
                        if len(row) >= 8:
                            print(f"    {row[1]} {row[2]} {row[3]} {row[4]}{row[5]} {row[6]}輛 {row[7]}")

    print()
    print("【建築套繪圖】（依圖例說明判讀）")
    if "error" in overlay:
        print(f"  查詢失敗：{overlay['error']}")
    else:
        dominant = overlay.get("主要顏色", "未知")
        pcts = overlay.get("各色比例", {})
        has_color = overlay.get("有上色", True)
        if has_color:
            print(f"  結果：有上色")
            print(f"  主要類型：{dominant}")
            if overlay.get("標記文字"):
                print(f"  套繪標記：{overlay['標記文字']}")
        else:
            print(f"  結果：空白（無套繪記錄）")
        # 只列出有比例的顏色
        detail = "、".join(f"{k} {v}" for k, v in pcts.items() if k != "其他")
        if detail:
            print(f"  色彩分布：{detail}")
        if "截圖路徑" in overlay:
            print(f"  截圖：{overlay['截圖路徑']}")

    if firebreak:
        print()
        print("【防火間隔】")
        if "error" in firebreak:
            print(f"  查詢失敗：{firebreak['error']}")
        elif "結果" in firebreak:
            print(f"  {firebreak['結果']}")
        else:
            has_color = firebreak.get("有上色", True)
            dominant = firebreak.get("主要顏色", "未知")
            pcts = firebreak.get("各色比例", {})
            if has_color:
                print(f"  結果：有防火間隔")
                print(f"  主要類型：{dominant}")
            else:
                print(f"  結果：空白（無防火間隔記錄）")
            detail = "、".join(f"{k} {v}" for k, v in pcts.items() if k != "其他")
            if detail:
                print(f"  色彩分布：{detail}")
            if "截圖路徑" in firebreak:
                print(f"  截圖：{firebreak['截圖路徑']}")

    if gsa:
        print()
        print("【地質敏感區】")
        if "error" in gsa:
            print(f"  查詢失敗：{gsa['error']}")
        else:
            gsa_txt = gsa.get('地質敏感區查詢', '查無資料')
            if '不在' not in gsa_txt and '查無' not in gsa_txt and '失敗' not in gsa_txt:
                print(f"\033[31m  {gsa_txt}\033[0m")
            else:
                print(f"  {gsa_txt}")

    if slope:
        print()
        print("【山坡地查詢】")
        if "error" in slope:
            print(f"  查詢失敗：{slope['error']}")
        else:
            data = slope.get("山坡地查詢", {})
            for k, v in data.items():
                if v == "是":
                    print(f"\033[31m  {k}：{v}\033[0m")
                else:
                    print(f"  {k}：{v}")

    if sewer:
        print()
        print("【污水下水道接管查詢】")
        if "error" in sewer:
            print(f"  查詢失敗：{sewer['error']}")
        elif "結果" in sewer:
            print(f"  {sewer['結果']}")
        else:
            for key in ['公告特定區', '工程進度', '工程名稱', '工程聯絡窗口資訊', '公告可使用地區日期']:
                if key in sewer:
                    val = sewer[key]
                    suffix = ""
                    if key == '公告特定區' and val and val != "查無資料":
                        suffix = "\033[31m  ※需套繪\033[0m"
                    print(f"  {key}：{val}{suffix}")

    if fault:
        print()
        print("【台灣活動斷層】")
        if "error" in fault:
            print(f"  查詢失敗：{fault['error']}")
        else:
            distances = fault.get("斷層距離", [])
            if distances:
                for item in distances:
                    print(f"  {item['name']}：{item['distM']:,} 公尺")
            if "截圖路徑" in fault:
                print(f"  截圖：{fault['截圖路徑']}")

    print("=" * 60)


def save_pdf(district: str, section_name: str, lot: str,
             texts: list, overlay: dict, bupic_list: list = None, gsa: dict = None, slope: dict = None, firebreak: dict = None, sewer: dict = None, fault: dict = None, ud: dict = None, address: str = ""):
    import base64
    from datetime import date

    build_lines = [t for t in texts if t.startswith("建號查詢：") or t.startswith("執照查詢：")]
    history_json = next((t[len("履歷JSON："):] for t in texts if t.startswith("履歷JSON：")), None)
    urban_json = next((t[len("都計JSON："):] for t in texts if t.startswith("都計JSON：")), None)
    urban_screenshot_path = next((t[len("都計截圖路徑："):] for t in texts if t.startswith("都計截圖路徑：")), None)
    gis_texts = [t for t in texts if not t.startswith("建號查詢：") and not t.startswith("執照查詢：")
                 and not t.startswith("履歷JSON：") and not t.startswith("都計JSON：")
                 and not t.startswith("都計截圖路徑：")]

    key_labels = ['登記面積', '公告地價', '公告現值', '使用資訊', '國土功能分區',
                  '地政事務所', '區段徵收', '登記日期', '自然人']
    value_keywords = ['平方公尺', '住宅區', '商業區', '工業區', '農業區', '保護區',
                      '特定', '城鄉', '元/平方公尺', '地政事務所', '年', '%']

    gis_rows = []
    printed = set()
    for i, t in enumerate(gis_texts):
        if len(t) > 200:
            continue
        if any(kw in t for kw in key_labels) and t not in printed:
            gis_rows.append(f"<tr><td class='lbl'>{t}</td>")
            printed.add(t)
            if i + 1 < len(gis_texts):
                nxt = gis_texts[i + 1]
                if len(nxt) < 150 and nxt not in printed:
                    gis_rows[-1] = gis_rows[-1] + f"<td>{nxt}</td></tr>"
                    printed.add(nxt)
                else:
                    gis_rows[-1] = gis_rows[-1] + "<td></td></tr>"
            else:
                gis_rows[-1] = gis_rows[-1] + "<td></td></tr>"
        elif any(kw in t for kw in value_keywords) and t not in printed:
            gis_rows.append(f"<tr><td class='lbl'></td><td>{t}</td></tr>")
            printed.add(t)

    bupic_rows = []
    if bupic_list:
        for bupic in bupic_list:
            if "error" in bupic:
                bupic_rows.append(f"<tr><td colspan='2'>查詢失敗：{bupic['error']}</td></tr>")
            elif "查詢結果" in bupic:
                bupic_rows.append(f"<tr><td colspan='2'>{bupic['查詢結果']}</td></tr>")
            else:
                d = bupic.get("執照存根詳細", {})
                def r(label, val):
                    if val and '＊＊＊' not in str(val) and '\n' not in str(val):
                        bupic_rows.append(f"<tr><td class='lbl'>{label}</td><td>{val}</td></tr>")
                lic_no = (d.get("建造執照號碼") or d.get("使用執照號碼") or
                          d.get("雜項工程執照號碼") or d.get("拆除執照號碼") or "")
                r("執照號碼", lic_no)
                起造 = d.get("起造人", {})
                if isinstance(起造, dict): r("起造人", 起造.get("姓名", ""))
                設計 = d.get("設計人", {})
                if isinstance(設計, dict): r("設計人", f"{設計.get('姓名','')}（{設計.get('事務所','')}）")
                監造 = d.get("監造人", {})
                if isinstance(監造, dict): r("監造人", f"{監造.get('姓名','')}（{監造.get('事務所','')}）")
                承造 = d.get("承造人", {})
                if isinstance(承造, dict):
                    r("承造人", 承造.get("姓名", ""))
                    r("營造廠", 承造.get("營造廠", ""))
                    r("專任工程人員", 承造.get("專任工程人員", ""))
                基地 = d.get("基地概要", {})
                if isinstance(基地, dict):
                    r("使用分區", 基地.get("使用分區", ""))
                    r("基地面積", 基地.get("合計", ""))
                建物 = d.get("建物概要", {})
                if isinstance(建物, dict):
                    for k in ['層棟戶數','法定空地面積','設計建蔽率','設計容積率',
                              '建物高度','總樓地板面積','建造類別','構造種類',
                              '雜項工程','工程造價','發照日期']:
                        r(k, 建物.get(k, ""))
                    ba = 建物.get("建築面積", {})
                    if isinstance(ba, dict): r("建築面積(其他)", ba.get("其他", ""))
                    elif isinstance(ba, str) and '其他' in ba:
                        idx = ba.find('其他\n')
                        if idx >= 0: r("建築面積(其他)", ba[idx+3:].split('\n')[0].strip())
                非供 = d.get("非供公眾使用建築物", "")
                if 非供 and '＊＊＊' not in str(非供): r("非供公眾使用", 非供)
                執照 = d.get("建築執照", {})
                if isinstance(執照, dict): r("開工日期", 執照.get("開工日期", ""))
                lands = d.get("_地段地號", [])
                if lands:
                    lots_str = "、".join(f"{rr[2]}{rr[3]}地號" for rr in lands if len(rr) >= 4)
                    r("建築地號", lots_str)
                floors = d.get("_樓層概要", {})
                if isinstance(floors, dict) and floors.get("rows"):
                    floor_html = "<table class='inner'><tr><th>層別</th><th>申請面積</th><th>陽台</th><th>使用類組</th></tr>"
                    for row in floors["rows"]:
                        if len(row) >= 8:
                            layer, area, balc, use = row[2], row[4], row[5], row[7]
                            if layer and use and '＊＊＊' not in use:
                                b = "" if balc == "＊＊＊" else balc
                                floor_html += f"<tr><td>{layer}</td><td>{area}m²</td><td>{b}</td><td>{use}</td></tr>"
                    floor_html += "</table>"
                    bupic_rows.append(f"<tr><td class='lbl'>樓層概要</td><td>{floor_html}</td></tr>")
                remarks = d.get("_備註", [])
                if remarks:
                    rem_html = "<ol>" + "".join(f"<li>{rr}</li>" for rr in remarks) + "</ol>"
                    bupic_rows.append(f"<tr><td class='lbl'>備註</td><td>{rem_html}</td></tr>")
                parking = d.get("_停車空間", {})
                if isinstance(parking, dict) and parking.get("rows"):
                    park_html = "<table class='inner'><tr><th>法定/自設</th><th>類別</th><th>車位</th><th>室內外</th><th>地上下</th><th>輛數</th><th>面積</th></tr>"
                    for row in parking["rows"]:
                        if len(row) >= 8:
                            park_html += f"<tr><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td></tr>"
                    park_html += "</table>"
                    bupic_rows.append(f"<tr><td class='lbl'>停車空間</td><td>{park_html}</td></tr>")

    history_html = ""
    if history_json:
        try:
            h = json.loads(history_json)
            rows_html = ""
            for sec in ["其他登記事項", "分割合併紀錄", "重測前後對照"]:
                tbl = h.get(sec)
                if not tbl or not tbl.get("rows"):
                    continue
                hdrs = tbl.get("headers", [])
                rows_html += f"<tr><td colspan='2' class='lbl'>▸ {sec}</td></tr>"
                for row in tbl["rows"]:
                    if hdrs:
                        for i in range(min(len(hdrs), len(row))):
                            if row[i]:
                                rows_html += f"<tr><td class='lbl'>{hdrs[i]}</td><td>{row[i]}</td></tr>"
                    else:
                        rows_html += f"<tr><td colspan='2'>{'　'.join(c for c in row if c)}</td></tr>"
            if rows_html:
                history_html = f"<h2>履歷 - 分割合併與重測異動</h2><table>{rows_html}</table>"
        except Exception:
            pass

    urban_html = ""
    if urban_json:
        try:
            zones = json.loads(urban_json)
            if isinstance(zones, dict):
                zones = [zones]
            urban_rows = ""
            for i, u in enumerate(zones):
                if len(zones) > 1:
                    urban_rows += (f"<tr><td colspan='2' style='background:#f0f0f0;font-weight:bold;"
                                   f"padding:4px 8px;'>分區 {i+1}</td></tr>")
                for key in ["使用分區", "建蔽率", "容積率", "都市計畫區", "細部計畫區", "計畫案名", "發布日期"]:
                    val = u.get(key, "")
                    if val:
                        urban_rows += f"<tr><td class='lbl'>{key}</td><td>{val}</td></tr>"
            if urban_screenshot_path:
                try:
                    with open(urban_screenshot_path, "rb") as f_img:
                        img_b64 = base64.b64encode(f_img.read()).decode()
                    urban_rows += (f"<tr><td colspan='2'><img src='data:image/png;base64,{img_b64}'"
                                   f" style='max-width:100%;margin-top:8px;border:1px solid #ccc;'></td></tr>")
                except Exception:
                    pass
            if urban_rows:
                urban_html = f"<h2>都市計畫分區</h2><table>{urban_rows}</table>"
        except Exception:
            pass

    overlay_html = ""
    if "error" in overlay:
        overlay_html = f"<p>查詢失敗：{overlay['error']}</p>"
    else:
        has_color = overlay.get("有上色", True)
        dominant = overlay.get("主要顏色", "未知")
        pcts = overlay.get("各色比例", {})
        detail = "、".join(f"{k} {v}" for k, v in pcts.items() if k != "其他")
        overlay_html = f"<p>{'有上色' if has_color else '空白（無套繪記錄）'}</p>"
        if has_color:
            overlay_html += f"<p>主要類型：{dominant}</p>"
            if overlay.get("標記文字"):
                overlay_html += f"<p>套繪標記：{overlay['標記文字']}</p>"
        if detail:
            overlay_html += f"<p>色彩分布：{detail}</p>"
        if "截圖路徑" in overlay:
            try:
                img_path = overlay["截圖路徑"]
                with open(img_path, "rb") as f_img:
                    img_b64 = base64.b64encode(f_img.read()).decode()
                overlay_html += f'<img src="data:image/png;base64,{img_b64}" style="max-width:100%;margin-top:8px;border:1px solid #ccc;">'
            except Exception:
                pass

    firebreak_html = ""
    if firebreak:
        if "error" in firebreak:
            firebreak_html = f"<p>查詢失敗：{firebreak['error']}</p>"
        elif "結果" in firebreak:
            firebreak_html = f"<p>{firebreak['結果']}</p>"
        else:
            has_color = firebreak.get("有上色", True)
            dominant = firebreak.get("主要顏色", "未知")
            pcts = firebreak.get("各色比例", {})
            detail = "、".join(f"{k} {v}" for k, v in pcts.items() if k != "其他")
            firebreak_html = f"<p>{'有上色' if has_color else '空白（無防火間隔記錄）'}</p>"
            if has_color:
                firebreak_html += f"<p>主要類型：{dominant}</p>"
            if detail:
                firebreak_html += f"<p>色彩分布：{detail}</p>"
            if "截圖路徑" in firebreak:
                try:
                    img_path = firebreak["截圖路徑"]
                    with open(img_path, "rb") as f_img:
                        img_b64 = base64.b64encode(f_img.read()).decode()
                    firebreak_html += f'<img src="data:image/png;base64,{img_b64}" style="max-width:100%;margin-top:8px;border:1px solid #ccc;">'
                except Exception:
                    pass

    # 地質敏感區 HTML
    if gsa:
        if "error" in gsa:
            gsa_html = f"<h2>地質敏感區</h2><p>{gsa['error']}</p>"
        else:
            gsa_txt = gsa.get('地質敏感區查詢', '查無資料')
            is_sensitive = '不在' not in gsa_txt and '查無' not in gsa_txt and '失敗' not in gsa_txt
            style = " style='color:red;font-weight:bold;'" if is_sensitive else ""
            gsa_html = f"<h2>地質敏感區</h2><p{style}>{gsa_txt}</p>"
    else:
        gsa_html = ""

    # 山坡地 HTML
    if slope and "山坡地查詢" in slope:
        slope_rows = "".join(
            f"<tr style='color:red;font-weight:bold;'><td class='lbl'>{k}</td><td>{v}</td></tr>"
            if v == "是"
            else f"<tr><td class='lbl'>{k}</td><td>{v}</td></tr>"
            for k, v in slope["山坡地查詢"].items()
        )
        slope_html = f"<h2>山坡地查詢</h2><table>{slope_rows}</table>"
    elif slope and "error" in slope:
        slope_html = f"<h2>山坡地查詢</h2><p>{slope['error']}</p>"
    else:
        slope_html = ""

    # 污水下水道接管 HTML
    if sewer:
        if "error" in sewer:
            sewer_html = f"<h2>污水下水道接管查詢</h2><p class='err'>{sewer['error']}</p>"
        elif "結果" in sewer:
            sewer_html = f"<h2>污水下水道接管查詢</h2><p>{sewer['結果']}</p>"
        else:
            sewer_rows = ""
            for k in ['公告特定區', '工程進度', '工程名稱', '工程聯絡窗口資訊', '公告可使用地區日期']:
                if k not in sewer:
                    continue
                v = sewer[k]
                if k == '公告特定區' and v and v != "查無資料":
                    cell = f"{v} <span style='color:red;font-weight:bold;'>※需套繪</span>"
                else:
                    cell = v
                sewer_rows += f"<tr><td class='lbl'>{k}</td><td>{cell}</td></tr>"
            sewer_html = f"<h2>污水下水道接管查詢</h2><table>{sewer_rows}</table>"
    else:
        sewer_html = ""

    # 台灣活動斷層 HTML
    if fault:
        if "error" in fault:
            fault_html = f"<h2>台灣活動斷層</h2><p class='err'>{fault['error']}</p>"
        else:
            import base64 as _b64
            distances = fault.get("斷層距離", [])
            fault_rows = "".join(
                f"<tr><td class='lbl'>{item['name']}</td><td>{item['distM']:,} 公尺</td></tr>"
                for item in distances
            )
            fault_img_html = ""
            if "截圖路徑" in fault:
                try:
                    with open(fault["截圖路徑"], "rb") as _f:
                        img_b64 = _b64.b64encode(_f.read()).decode()
                    fault_img_html = f'<img src="data:image/png;base64,{img_b64}" style="max-width:100%;margin-top:8px;">'
                except Exception:
                    pass
            fault_html = f"<h2>台灣活動斷層</h2><table>{fault_rows}</table>{fault_img_html}"
    else:
        fault_html = ""

    today = date.today().strftime("%Y年%m月%d日")
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
  body {{ font-family: "PingFang TC","Microsoft JhengHei",sans-serif; font-size:13px; color:#222; margin:20px 30px; }}
  h1 {{ font-size:18px; margin-bottom:4px; }}
  .meta {{ color:#666; font-size:11px; margin-bottom:16px; }}
  h2 {{ font-size:13px; background:#2c3e50; color:#fff; padding:4px 8px; margin:16px 0 4px; }}
  table {{ width:100%; border-collapse:collapse; }}
  td {{ padding:3px 6px; vertical-align:top; border-bottom:1px solid #eee; }}
  td.lbl {{ width:40%; color:#555; font-weight:bold; }}
  table.inner td {{ border:none; padding:2px 6px; }}
</style>
</head><body>
<h1>臺中市{district}{section_name}{lot}地號 查詢結果</h1>
<div class="meta">地址：{address if address else "尚無"} &nbsp;|&nbsp; 查詢日期：{today}</div>

<h2>GIS 分區資訊</h2>
<table>{"".join(gis_rows) or "<tr><td>無資料</td></tr>"}</table>

{urban_html}

{history_html}

<h2>建物查詢</h2>
<table>{"".join(f"<tr><td>{line}</td></tr>" for line in build_lines) or "<tr><td>無資料</td></tr>"}</table>

{"<h2>建築執照存根</h2><table>" + "".join(bupic_rows) + "</table>" if bupic_rows else ""}

<h2>建築套繪圖</h2>
{overlay_html}

{"<h2>防火間隔</h2>" + firebreak_html if firebreak_html else ""}

{gsa_html}

{slope_html}

{sewer_html}

{fault_html}
</body></html>"""

    parcel_dir = os.path.expanduser(f"~/Desktop/查詢結果/臺中市{district}{section_name}{lot}地號")
    os.makedirs(parcel_dir, exist_ok=True)

    # 套繪截圖另存至資料夾
    if isinstance(overlay, dict) and overlay.get("截圖路徑"):
        overlay_dest = os.path.join(parcel_dir, f"臺中市{district}{section_name}{lot}地號_套繪圖.png")
        try:
            shutil.copy2(overlay["截圖路徑"], overlay_dest)
        except Exception:
            pass

    pdf_path = os.path.join(parcel_dir, f"臺中市{district}{section_name}{lot}地號.pdf")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        pg.set_content(html, wait_until="domcontentloaded")
        pg.pdf(path=pdf_path, format="A4", print_background=True,
               margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"})
        browser.close()
    print(f"  PDF 已儲存：{pdf_path}")


def lot_to_address(district: str, section_name: str, lot: str) -> str:
    """
    地號 → 門牌地址（第一筆），透過 easymap 地籍查詢。
    查無或失敗回傳空字串。
    """
    section_code = find_section_code(district, section_name)
    lot_main, lot_sub = (lot.split("-") + ["0"])[:2] if "-" in lot else (lot, "0")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            ctx = browser.new_context(
                viewport={"width": 1280, "height": 900},
                has_touch=True,
                user_agent="Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            )
            page = ctx.new_page()
            page.goto("https://easymap.land.moi.gov.tw/P02/Index")
            page.wait_for_load_state("networkidle", timeout=30000)
            time.sleep(2)

            # 找並點擊「地籍查詢」tab
            tab_id = page.evaluate("""() => {
                for (const el of document.querySelectorAll('a[id], button[id]')) {
                    if (el.textContent.includes('地籍')) return el.id;
                }
                return null;
            }""")
            if tab_id:
                page.click(f"#{tab_id}")
            else:
                for btn in ("#button_land", "#button_cad", "#button_lot"):
                    try:
                        page.click(btn, timeout=2000)
                        break
                    except Exception:
                        continue
            time.sleep(1.5)

            # 找目前可見的 select（地籍模式下新出現的）
            def _try_select(candidates: list, label_or_value: str, by: str = "label"):
                for sel_id in candidates:
                    try:
                        if by == "label":
                            page.select_option(f"#{sel_id}", label=label_or_value, timeout=2000)
                        else:
                            page.select_option(f"#{sel_id}", value=label_or_value, timeout=2000)
                        return True
                    except Exception:
                        continue
                return False

            # 選縣市
            _try_select(["select_city_id2", "select_city_land", "select_city_cad", "select_city_id3"], "臺中市")
            time.sleep(1.5)

            # 選行政區
            _try_select(["select_town_id2", "select_town_land", "select_town_cad", "select_town_id3"], district)
            time.sleep(1.5)

            # 等地段選單載入，選地段（4碼 section_code）
            for sect_id in ["select_sect_land", "select_lsect_id", "select_sect_cad", "select_sect_id"]:
                try:
                    page.wait_for_function(
                        f"() => {{ const s = document.getElementById('{sect_id}'); return s && s.options.length > 1; }}",
                        timeout=6000
                    )
                    page.select_option(f"#{sect_id}", value=section_code, timeout=2000)
                    break
                except Exception:
                    continue
            time.sleep(0.5)

            # 填母號
            for no1 in ["cadLandNoMainId", "landNoMainId", "land_no1", "landno1", "cadLandNo1"]:
                try:
                    page.fill(f"#{no1}", lot_main, timeout=2000)
                    break
                except Exception:
                    continue

            # 填子號
            if lot_sub and lot_sub != "0":
                for no2 in ["cadLandNoSubId", "landNoSubId", "land_no2", "landno2", "cadLandNo2"]:
                    try:
                        page.fill(f"#{no2}", lot_sub, timeout=2000)
                        break
                    except Exception:
                        continue

            # 送出搜尋（攔截 API 回應）
            addr = ""
            try:
                with page.expect_response(
                    lambda r: "getDoorByLand" in r.url or "getLandDoor" in r.url or "Land_json" in r.url,
                    timeout=12000
                ) as resp_info:
                    for btn in ["cad_botton", "land_botton", "lot_botton"]:
                        try:
                            page.evaluate(f"() => {{ $('#{btn}').trigger('click'); }}")
                            break
                        except Exception:
                            continue
                data = resp_info.value.json()
                results = data.get("results", []) if isinstance(data, dict) else data
                for item in (results if isinstance(results, list) else []):
                    road = item.get("Road", "") or item.get("door", "") or item.get("address", "")
                    if road and "樓" not in road and "公共" not in road:
                        addr = road
                        break
            except Exception:
                # API 攔截失敗，從 DOM 文字取第一個看起來像地址的字串
                time.sleep(3)
                texts = page.evaluate("""() =>
                    Array.from(document.querySelectorAll('a.ui-link-inherit, li'))
                        .map(el => el.textContent.trim())
                        .filter(t => (t.includes('路') || t.includes('街') || t.includes('道')) && t.includes('號'))
                """)
                for t in texts:
                    if t and "樓" not in t and len(t) < 50:
                        addr = t
                        break

            ctx.close()
            browser.close()
            # 補上行政區前綴（若回傳值沒有）
            if addr and district not in addr and "區" not in addr[:4]:
                addr = f"臺中市{district}{addr}"
            return addr
    except Exception as e:
        print(f"  [lot_to_address] 查詢失敗：{e}")
        return ""


def address_to_lot(address: str) -> tuple:
    """
    透過 easymap.land.moi.gov.tw/P02 將臺中市門牌地址轉為 (district, section_name, lot_number)。
    address 範例: "<行政區><路名><門牌號>號" 或 "臺中市<行政區><路名><門牌號>號"
    """
    district_m = re.search(r'([^\s市]+區)', address)
    district = district_m.group(1) if district_m else ""

    road_m = re.search(r'([^\s號巷弄\d０-９]+(?:街|路|大道|道)(?:[一二三四五六七八九十東西南北]+段)?)', address)
    road = road_m.group(1) if road_m else ""
    # 若路名意外包含行政區前綴（如「<行政區><路名>」或「臺中市<行政區><路名>」），去掉前綴
    if district and district in road:
        road = road[road.find(district) + len(district):]

    lane_m = re.search(r'(\d+)巷', address)
    lane = lane_m.group(1) if lane_m else ""

    alley_m = re.search(r'(\d+)弄', address)
    alley = alley_m.group(1) if alley_m else ""

    no_m = re.search(r'(\d+)號', address)
    no = no_m.group(1) if no_m else ""

    if not (district and road and no):
        print(f"  無法解析地址：{address}（需包含 XX區、道路名、XX號）")
        return "", "", ""

    print(f"  解析地址：{district} {road} {lane+'巷' if lane else ''}{alley+'弄' if alley else ''}{no}號")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 模擬行動裝置 touch 讓 jQuery Mobile vclick 正常觸發
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 900},
            has_touch=True,
            user_agent="Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        )
        page = ctx.new_page()
        page.goto("https://easymap.land.moi.gov.tw/P02/Index")
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)

        page.click("#button_addr")
        time.sleep(1.5)
        page.select_option("#select_city_id1", label="臺中市")
        time.sleep(2)
        page.select_option("#select_town_id1", label=district)

        # 等路名下拉選單實際載入（至少有 2 個選項）
        try:
            page.wait_for_function(
                "() => { const s = document.getElementById('select_road_id'); return s && s.options.length > 1; }",
                timeout=10000
            )
        except Exception:
            time.sleep(3)

        # 路名可能含段號（如「龍富路五段」），也可能下拉只有「龍富路五段」或「龍富路」
        road_bare = re.sub(r'[一二三四五六七八九十東西南北]+段$', '', road)
        road_info = page.evaluate("""([road, road_bare]) => {
            const sel = document.getElementById('select_road_id');
            if (!sel) return {val: null, count: 0, sample: []};
            const opts = Array.from(sel.options);
            const sample = opts.slice(0, 15).map(o => o.text);
            const exact = opts.find(o => o.text === road || o.value === road);
            if (exact) return {val: exact.value, count: opts.length, sample};
            const partial = opts.find(o => o.text === road_bare || o.value === road_bare);
            if (partial) return {val: partial.value, count: opts.length, sample};
            return {val: null, count: opts.length, sample};
        }""", [road, road_bare])
        road_val = road_info.get('val') if isinstance(road_info, dict) else None

        if road_val is not None:
            page.select_option("#select_road_id", value=road_val)
        else:
            try:
                page.click("#radio-choice-B")
                time.sleep(0.5)
            except Exception:
                pass
            page.fill("#roadFreeKeyInId", road)
        time.sleep(1)

        if lane:
            page.fill("#doorLaneId", lane)
        if alley:
            page.fill("#doorAlleyId", alley)
        page.fill("#doorNoId", no)
        time.sleep(0.5)

        # step1: 先設好攔截，再觸發搜尋，取得門牌清單
        def _search_door(mode_label: str):
            """觸發搜尋並返回 getDoorList 回應 dict，失敗回傳 None。"""
            try:
                with page.expect_response(
                    lambda r: 'Door_json_getDoorList' in r.url, timeout=15000
                ) as r1:
                    page.evaluate("() => { $('#door_botton').trigger('click'); }")
                data = r1.value.json()
                results = data.get('results', [])
                return data if results else None
            except Exception as e:
                print(f"  {mode_label}門牌查詢失敗：{e}")
                return None

        # 先試地政門牌（預設已選）
        door_list_data = _search_door("地政")

        # 若無結果，切換到戶政門牌再試一次
        if door_list_data is None:
            try:
                # 找戶政門牌的 radio 並點選，取得戶政模式的 city/town select ID
                hh_selects = page.evaluate("""() => {
                    const radios = document.querySelectorAll('input[type=radio]');
                    const hh = Array.from(radios).find(r => {
                        const label = document.querySelector('label[for="' + r.id + '"]');
                        return label && label.textContent.includes('戶政');
                    });
                    if (!hh) return null;
                    hh.click();
                    $(hh).trigger('change');
                    // 等 DOM 更新後尋找市/區 select
                    const selects = Array.from(document.querySelectorAll('select'));
                    return selects.map(s => s.id);
                }""")
                _ = hh_selects
                time.sleep(2)

                # 重新填市/區（試 select_city_id2/select_town_id2 或同 id1）
                def _try_select_city_town():
                    for city_id, town_id in [("select_city_id2", "select_town_id2"),
                                             ("select_city_id1", "select_town_id1")]:
                        try:
                            page.select_option(f"#{city_id}", label="臺中市")
                            time.sleep(1.5)
                            page.select_option(f"#{town_id}", label=district)
                            return True
                        except Exception:
                            continue
                    return False

                if not _try_select_city_town():
                    print("  [debug] 戶政城市/區選取失敗")
                else:
                    # 等路名下拉
                    try:
                        page.wait_for_function(
                            "() => { const s = document.getElementById('select_road_id'); return s && s.options.length > 1; }",
                            timeout=8000
                        )
                    except Exception:
                        time.sleep(2)
                    road_val2 = page.evaluate("""([road, road_bare]) => {
                        const sel = document.getElementById('select_road_id');
                        if (!sel) return null;
                        const opts = Array.from(sel.options);
                        const exact = opts.find(o => o.text === road || o.value === road);
                        if (exact) return exact.value;
                        const partial = opts.find(o => o.text === road_bare || o.value === road_bare);
                        if (partial) return partial.value;
                        return null;
                    }""", [road, road_bare])
                    if road_val2:
                        page.select_option("#select_road_id", value=road_val2)
                    else:
                        page.fill("#roadFreeKeyInId", road)
                    time.sleep(0.5)
                    page.fill("#doorNoId", no)
                    time.sleep(0.5)
                    door_list_data = _search_door("戶政")
            except Exception as e:
                print(f"  [debug] 戶政門牌切換失敗：{e}")

        # step2: 點擊清單中第一個非樓層/公共設施的結果，取得地號
        detail_api_data = None
        try:
            with page.expect_response(
                lambda r: 'Door_json_getFullDoorListByA' in r.url, timeout=15000
            ) as resp2:
                page.evaluate("""() => {
                    const a = Array.from(document.querySelectorAll('a.ui-link-inherit')).find(a => {
                        const t = a.textContent.trim();
                        return t.endsWith('號') && !t.includes('樓') && !t.includes('公共設施');
                    });
                    if (a) a.click();
                }""")
            detail_api_data = resp2.value.json()
        except Exception:
            pass  # getFullDoorListByA 失敗時改從 DOM 文字解析

        texts = page.evaluate("""() => {
            const root = document.querySelector('.ui-page-active') || document.body;
            const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
            let texts = [];
            let node;
            while (node = walker.nextNode()) {
                const txt = node.textContent.trim();
                if (txt.length > 1 && txt.length < 300) {
                    const el = node.parentElement;
                    if (el && el.offsetParent !== null) texts.push(txt);
                }
            }
            return [...new Set(texts)];
        }""")
        ctx.close()
        browser.close()

    # 優先從 API JSON 取地段名與地號
    if detail_api_data and isinstance(detail_api_data, dict):
        for result in detail_api_data.get('results', []):
            road = result.get('Road', '')
            if '樓' in road or '公共設施' in road:
                continue
            section_name = result.get('sectName', '')
            lot_number = result.get('landno', '')  # 格式：母號-子號（如 252-12）
            if section_name and lot_number:
                print(f"  對應地號：{district} {section_name} {lot_number}地號")
                return district, section_name, lot_number

    # 備用：從 DOM 文字解析
    section_name = ""
    lot_number = ""
    result_district = district  # 可能與輸入行政區不同（如南屯/西屯交界）

    # 從 texts 嘗試取正確行政區（戶政結果會出現「臺中市 南屯區」等字樣）
    for t in texts:
        dm = re.search(r'臺中市\s*([^\s]+區)', t)
        if dm:
            result_district = dm.group(1)
            break

    for t in texts:
        # 格式1: 純數字段號  (段號:0180 ,地號:0050-0001)
        m = re.search(r'段號[：:]\s*(\d+)\s*[,，]\s*地號[：:]\s*([\d\-]+)', t)
        if m:
            sect_code = m.group(1).zfill(4)
            lot_number = m.group(2)
            for sec_name, code in SECTIONS.get(result_district, {}).items():
                if code == sect_code:
                    section_name = sec_name
                    break
            if not section_name:
                section_name = sect_code
            break
        # 格式2: 戶政格式  (段號:三富段2045 ,地號:51-2)
        m2 = re.search(r'段號[：:]\s*([一-鿿]+)(\d+)\s*[,，]\s*地號[：:]\s*([\d\-]+)', t)
        if m2:
            cand_name = m2.group(1)  # 三富段
            sect_code = m2.group(2).zfill(4)  # 2045
            lot_number = m2.group(3)  # 51-2
            # 嘗試在結果行政區找對應段名
            for sec_name, code in SECTIONS.get(result_district, {}).items():
                if sec_name == cand_name or code == sect_code:
                    section_name = sec_name
                    break
            if not section_name:
                section_name = cand_name
            break
        # 格式3: ^(四碼) 段名
        m3 = re.search(r'^(\d{4})\s+(.+段\S*)$', t)
        if m3 and not section_name:
            section_name = m3.group(2)

    if not (section_name and lot_number):
        print(f"  easymap 未能找到對應地號（原始文字：{texts[:10]}）")
        return district, "", ""

    district = result_district

    print(f"  對應地號：{district} {section_name} {lot_number}地號")
    return district, section_name, lot_number


def lookup(district: str, section_name: str, lot_number: str, address: str = ""):
    """單筆查詢"""
    results = query_batch([(district, section_name, lot_number)])
    for d, s, n, texts, overlay, bupic_list, gsa, slope, firebreak, sewer, fault, ud, lot2addr in results:
        bupic_addr = ""
        for bp in (bupic_list or []):
            bupic_addr = _bupic_address(bp.get("執照存根詳細", {}))
            if bupic_addr:
                break
        final_address = address or lot2addr or bupic_addr
        print_result(d, s, n, texts, overlay, bupic_list, gsa, slope, firebreak, sewer, fault=fault, ud=ud, address=final_address)
        save_pdf(d, s, n, texts, overlay, bupic_list, gsa, slope, firebreak, sewer, fault=fault, ud=ud, address=final_address)


# 地段代碼對照（全臺中市，共 29 行政區、1625 地段）
SECTIONS = {
    "中區": {
        "繼光段一小段": "0001",
        "繼光段二小段": "0002",
        "繼光段三小段": "0003",
        "繼光段四小段": "0004",
        "繼光段五小段": "0005",
        "繼光段六小段": "0006",
        "自由段一小段": "0007",
        "自由段二小段": "0008",
        "自由段三小段": "0009",
        "自由段四小段": "0010",
        "自由段五小段": "0011",
        "自由段六小段": "0012",
        "自由段七小段": "0013",
        "綠川段一小段": "0014",
        "綠川段二小段": "0015",
        "綠川段三小段": "0016",
        "綠川段四小段": "0017",
        "綠川段五小段": "0018",
        "綠川段六小段": "0019",
        "重慶段一小段": "0020",
        "重慶段二小段": "0021",
        "重慶段三小段": "0022",
        "重慶段四小段": "0023",
        "重慶段五小段": "0024",
        "重慶段六小段": "0025",
        "建國段一小段": "0026",
        "建國段二小段": "0027",
        "建國段三小段": "0028",
        "建國段四小段": "0029",
        "建國段五小段": "0030",
        "仁愛段一小段": "0031",
        "仁愛段二小段": "0032",
        "仁愛段三小段": "0033",
        "仁愛段四小段": "0034",
        "仁愛段五小段": "0035",
        "仁愛段六小段": "0036",
        "仁愛段七小段": "0037",
        "平等段一小段": "0038",
        "平等段二小段": "0039",
        "平等段三小段": "0040",
        "平等段四小段": "0041",
        "平等段五小段": "0042",
        "平等段六小段": "0043",
        "中墩段一小段": "0044",
        "中墩段二小段": "0045",
        "中墩段三小段": "0046",
        "中墩段四小段": "0047",
        "中墩段五小段": "0048",
        "中墩段六小段": "0049",
        "中墩段七小段": "0050",
        "柳川段一小段": "0051",
        "柳川段二小段": "0052",
        "柳川段三小段": "0053",
        "柳川段四小段": "0054",
        "柳川段五小段": "0055",
        "柳川段六小段": "0056",
        "柳川段七小段": "0057",
        "中華段一小段": "0058",
        "中華段二小段": "0059",
        "中華段三小段": "0060",
        "中華段四小段": "0061",
        "中華段五小段": "0062",
        "中華段六小段": "0063",
        "中華段七小段": "0064",
    },
    "東區": {
        "尚武段": "0300",
        "練武段": "0301",
        "復興段一小段": "0302",
        "復興段二小段": "0303",
        "復興段三小段": "0304",
        "復興段四小段": "0305",
        "復興段五小段": "0306",
        "復興段六小段": "0307",
        "東勢子段": "0308",
        "忠孝段一小段": "0309",
        "忠孝段二小段": "0310",
        "忠孝段三小段": "0311",
        "忠孝段四小段": "0312",
        "忠孝段五小段": "0313",
        "忠孝段六小段": "0314",
        "樂業段": "0315",
        "立德段一小段": "0316",
        "立德段二小段": "0317",
        "立德段三小段": "0318",
        "立德段四小段": "0319",
        "立德段五小段": "0320",
        "立德段六小段": "0321",
        "旱溪段": "0322",
        "花園段一小段": "0323",
        "花園段二小段": "0324",
        "花園段三小段": "0325",
        "花園段四小段": "0326",
        "花園段五小段": "0327",
        "花園段六小段": "0328",
        "頂橋子頭段": "0329",
        "旱清段": "0330",
        "旱平段": "0331",
        "旱新段": "0332",
        "振興段": "0333",
        "泉源段": "0334",
        "新庄段": "0335",
        "大智段": "0336",
        "大公段": "0337",
        "福成段": "0338",
        "東橋段": "0339",
        "東興段": "0340",
    },
    "西區": {
        "麻園頭段": "0700",
        "東昇段一小段": "0701",
        "東昇段二小段": "0702",
        "東昇段三小段": "0703",
        "東昇段四小段": "0704",
        "東昇段五小段": "0705",
        "東昇段六小段": "0706",
        "東昇段七小段": "0707",
        "東昇段八小段": "0708",
        "東昇段九小段": "0709",
        "平和段": "0710",
        "光明段一小段": "0711",
        "光明段二小段": "0712",
        "光明段三小段": "0713",
        "光明段四小段": "0714",
        "光明段五小段": "0715",
        "光明段六小段": "0716",
        "光明段七小段": "0717",
        "民生段一小段": "0718",
        "民生段二小段": "0719",
        "民生段三小段": "0720",
        "民生段四小段": "0721",
        "民生段五小段": "0722",
        "平民段一小段": "0723",
        "平民段二小段": "0724",
        "平民段三小段": "0725",
        "平民段四小段": "0726",
        "平民段五小段": "0727",
        "平民段六小段": "0728",
        "平民段七小段": "0729",
        "平民段八小段": "0730",
        "平民段九小段": "0731",
        "利民段一小段": "0732",
        "利民段二小段": "0733",
        "利民段三小段": "0734",
        "利民段四小段": "0735",
        "利民段五小段": "0736",
        "利民段六小段": "0737",
        "利民段七小段": "0738",
        "中民段一小段": "0739",
        "中民段二小段": "0740",
        "中民段三小段": "0741",
        "中民段四小段": "0742",
        "中民段五小段": "0743",
        "中民段六小段": "0744",
        "中民段七小段": "0745",
        "中民段八小段": "0746",
        "中民段九小段": "0747",
        "三民段一小段": "0748",
        "三民段二小段": "0749",
        "三民段三小段": "0750",
        "三民段四小段": "0751",
        "三民段五小段": "0752",
        "三民段六小段": "0753",
        "三民段七小段": "0754",
        "後壠子段": "0755",
        "福壽段一小段": "0756",
        "福壽段二小段": "0757",
        "福壽段三小段": "0758",
        "公館段": "0759",
        "土庫段": "0760",
        "大益段": "0761",
        "科博段": "0762",
        "藍興段": "0763",
        "五權段": "0764",
        "美舘段": "0765",
        "吉龍段": "0766",
        "公民段": "0767",
        "博館段": "0768",
        "大勇段": "0769",
        "大忠段": "0770",
    },
    "南區": {
        "半平厝段": "0500",
        "萬安段一小段": "0501",
        "萬安段二小段": "0502",
        "萬安段三小段": "0503",
        "萬安段四小段": "0504",
        "萬安段五小段": "0505",
        "萬安段六小段": "0506",
        "萬安段七小段": "0507",
        "萬安段八小段": "0508",
        "萬安段九小段": "0509",
        "正義段一小段": "0510",
        "正義段二小段": "0511",
        "正義段三小段": "0512",
        "正義段四小段": "0513",
        "正義段五小段": "0514",
        "正義段六小段": "0515",
        "正義段七小段": "0516",
        "正義段八小段": "0517",
        "正義段九小段": "0518",
        "城隍段一小段": "0519",
        "城隍段二小段": "0520",
        "城隍段三小段": "0521",
        "城隍段四小段": "0522",
        "城隍段五小段": "0523",
        "城隍段六小段": "0524",
        "城隍段七小段": "0525",
        "城隍段八小段": "0526",
        "城隍段九小段": "0527",
        "樹子腳段": "0528",
        "番婆段": "0529",
        "下橋子頭段": "0530",
        "頂橋子頭段": "0531",
        "信義段一小段": "0532",
        "信義段二小段": "0533",
        "信義段三小段": "0534",
        "信義段四小段": "0535",
        "信義段五小段": "0536",
        "信義段六小段": "0537",
        "信義段七小段": "0538",
        "信義段八小段": "0539",
        "信義段九小段": "0540",
        "大慶段": "0541",
        "合作段": "0542",
        "國光段": "0543",
        "南門段": "0544",
    },
    "北區": {
        "文正段": "1000",
        "水源段": "1001",
        "錦村段": "1002",
        "乾溝子段": "1003",
        "賴厝廍段": "1004",
        "邱厝子段": "1005",
        "中清段": "1006",
        "中德段": "1007",
        "中興段": "1008",
        "東義段": "1009",
        "天祥段": "1010",
        "新賴厝廍一段": "1011",
        "新賴厝廍二段": "1012",
        "新賴厝廍三段": "1013",
        "新賴厝廍五段": "1014",
        "新賴厝廍六段": "1015",
        "新賴厝廍七段": "1016",
        "新賴厝廍八段": "1017",
        "新賴厝廍九段": "1018",
        "邱厝一段": "1019",
        "邱厝二段": "1020",
        "邱厝三段": "1021",
        "邱厝五段": "1022",
    },
    "西屯區": {
        "西屯段": "1600",
        "潮洋段": "1601",
        "水堀頭段": "1602",
        "上牛埔子段": "1603",
        "林厝段": "1604",
        "下石碑段": "1605",
        "上石碑段": "1606",
        "馬龍潭段": "1607",
        "八張犁段": "1608",
        "港尾子段": "1609",
        "下七張犁段": "1610",
        "惠來厝段": "1611",
        "何厝段": "1612",
        "福安段": "1613",
        "中和段": "1614",
        "中義段": "1615",
        "中正段": "1616",
        "中仁段": "1617",
        "協和段": "1618",
        "大明段": "1619",
        "大墩段": "1620",
        "何安段": "1621",
        "永安段": "1622",
        "順安段": "1623",
        "信安段": "1624",
        "民安段": "1625",
        "國安段": "1626",
        "安和段": "1627",
        "順和段": "1628",
        "惠國段": "1629",
        "惠民段": "1630",
        "惠安段": "1631",
        "惠泰段": "1632",
        "惠順段": "1633",
        "廣順段": "1634",
        "廣昌段": "1635",
        "廣福段": "1636",
        "廣明段": "1637",
        "廣安段": "1638",
        "協成段": "1639",
        "協仁段": "1640",
        "協安段": "1641",
        "東林段": "1642",
        "安林段": "1643",
        "永林段": "1644",
        "福林段": "1645",
        "龍門段": "1646",
        "福星段": "1647",
        "福德段": "1648",
        "上石碑段湳子小段": "1649",
        "福順段": "1650",
        "福和段": "1651",
        "龍富段": "1652",
        "鑫港尾段": "1653",
        "鑫大鵬段": "1654",
        "生態段": "1655",
        "經貿段": "1656",
        "逢大段": "1657",
        "文商段": "1658",
        "環廣段": "1659",
        "順新段": "1660",
    },
    "南屯區": {
        "南屯段": "2000",
        "埔興段": "2001",
        "楓樹段": "2002",
        "文山段": "2003",
        "楓興段": "2004",
        "豐安段": "2005",
        "豐樂段": "2006",
        "知高段": "2007",
        "溝子墘段": "2008",
        "番社腳段": "2009",
        "三塊厝段": "2010",
        "田心段": "2011",
        "山子腳段": "2012",
        "黎明段": "2013",
        "同安厝段": "2014",
        "新生段": "2015",
        "鎮南段": "2016",
        "鎮安段": "2017",
        "永定段": "2018",
        "大進段": "2019",
        "大新段": "2020",
        "寶山段": "2021",
        "保安段": "2022",
        "春社段": "2023",
        "春安段": "2024",
        "豐功段": "2025",
        "豐富段": "2026",
        "豐業段": "2027",
        "惠仁段": "2028",
        "惠義段": "2029",
        "惠禮段": "2030",
        "惠智段": "2031",
        "惠信段": "2032",
        "寶文段": "2033",
        "台安段": "2034",
        "麻糍埔段": "2035",
        "下楓樹腳段": "2036",
        "下牛埔子段": "2037",
        "鎮平段": "2038",
        "水碓段": "2039",
        "新庄子段": "2040",
        "劉厝段": "2041",
        "永定厝段": "2042",
        "永春段": "2043",
        "永新段": "2044",
        "三富段": "2045",
        "永富段": "2046",
        "新富段": "2047",
        "建功段": "2048",
        "鎮福段": "2049",
        "楓溪段": "2050",
        "樂田段": "2051",
        "昌明段": "2052",
        "永益段": "2053",
        "永豐段": "2054",
        "寶上段": "2055",
    },
    "北屯區": {
        "北屯段": "1100",
        "水湳段": "1101",
        "陳平段": "1102",
        "水景頭段": "1103",
        "舊社段": "1104",
        "軍功寮段": "1105",
        "大坑段": "1106",
        "廍子段": "1107",
        "同榮段": "1108",
        "仁和段": "1109",
        "仁美段": "1110",
        "仁德段": "1111",
        "松觀段": "1112",
        "松茂段": "1113",
        "松竹段": "1114",
        "松昌段": "1115",
        "東峰段": "1116",
        "東光段": "1117",
        "平田段": "1118",
        "東正段": "1119",
        "東山段": "1120",
        "東新段": "1121",
        "東信段": "1122",
        "建安段": "1123",
        "建功段": "1124",
        "建和段": "1125",
        "建業段": "1126",
        "青萍段": "1127",
        "青雲段": "1128",
        "青田段": "1129",
        "長生段": "1130",
        "長安段": "1131",
        "長春段": "1132",
        "大觀段": "1133",
        "大興段": "1134",
        "大仁段": "1135",
        "崇德段": "1136",
        "昌平段": "1137",
        "軍和段": "1138",
        "軍福段": "1139",
        "倡和段": "1140",
        "景美段": "1141",
        "景東段": "1142",
        "大學段": "1143",
        "大滿段": "1144",
        "大湖段": "1145",
        "大榮段": "1146",
        "大昌段": "1147",
        "大盛段": "1148",
        "大華段": "1149",
        "大富段": "1150",
        "大貴段": "1151",
        "大豐段": "1152",
        "太祥段": "1153",
        "太原段": "1154",
        "太和段": "1155",
        "太順段": "1156",
        "四張犁段": "1157",
        "后庄子段": "1158",
        "水汴頭段": "1159",
        "上七張犁段": "1160",
        "二分埔段": "1161",
        "三分埔段": "1162",
        "大政段": "1163",
        "和平段": "1164",
        "景福段": "1165",
        "鑫新平段": "1166",
        "南興段": "1167",
        "竹興段": "1168",
        "創研段": "1169",
        "文北段": "1170",
        "溝背段": "1171",
        "碧柳段": "1172",
        "榮德段": "1173",
        "洲際段": "1174",
        "環中段": "1175",
        "敦和段": "1176",
        "仁平段": "1177",
        "美和段": "1178",
        "江興段": "1179",
        "景中段": "1180",
        "景順段": "1181",
        "景南段": "1182",
    },
    "大甲區": {
        "大甲段": "3600",
        "庄尾段": "3601",
        "山脚段頂山脚小段": "3602",
        "山脚段下山脚小段": "3603",
        "營盤口段": "3604",
        "社尾段社尾小段": "3605",
        "社尾段溪埔小段": "3606",
        "橫圳段": "3607",
        "番子寮段": "3608",
        "外水尾段": "3609",
        "後厝子段": "3610",
        "六塊厝段": "3611",
        "頂店段": "3612",
        "九張犁段九張犁小段": "3613",
        "九張犁段六股小段": "3614",
        "日南段": "3615",
        "五里牌段": "3616",
        "日南社段": "3617",
        "頂後厝子段": "3618",
        "銅安厝段": "3619",
        "新庄子段": "3620",
        "雙寮段": "3621",
        "西勢段": "3622",
        "船頭埔段": "3623",
        "甲嘉段": "3624",
        "甲惠段": "3625",
        "甲農段": "3626",
        "甲民段": "3627",
        "甲全段": "3628",
        "幼獅段": "3629",
        "朝陽段": "3630",
        "孔門段": "3631",
        "順天段": "3632",
        "平安段": "3633",
        "薰風段": "3634",
        "光明段": "3635",
        "新美段": "3636",
        "岷山段": "3637",
        "文武段": "3638",
        "雁門段": "3639",
        "和平段": "3640",
        "武曲段": "3641",
        "中山段": "3642",
        "幸福段": "3643",
        "南社段": "3644",
        "太白段": "3645",
        "日新段": "3646",
        "黎明段": "3647",
        "孟春段": "3648",
        "臨江段": "3649",
        "九張段": "3650",
        "新興段": "3651",
        "義水段": "3652",
        "義和段": "3653",
        "武陵段": "3654",
        "文曲段": "3655",
        "文安段": "3656",
        "福順段": "3657",
        "福德段": "3658",
        "福安段": "3659",
        "劍井段": "3660",
        "永信段": "3661",
        "金華段": "3662",
        "致用段": "3663",
        "文化段": "3664",
        "德化段": "3665",
        "賢仁段": "3666",
        "奉化段": "3667",
        "奉仁段": "3668",
        "新銅安厝段": "3669",
        "順帆段": "3670",
        "渭水段": "3671",
        "西岐段": "3672",
        "建興段": "3673",
        "如意段": "3674",
        "海尾段": "3675",
    },
    "大安區": {
        "頂大安段": "4300",
        "下大安段": "4301",
        "三十甲段": "4302",
        "北汕段": "4303",
        "海墘厝段海墘厝小段": "4304",
        "海墘厝段大安港小段": "4305",
        "海墘厝段溫寮小段": "4306",
        "田心子段": "4307",
        "龜売段": "4308",
        "溪洲段": "4309",
        "牛埔段": "4310",
        "三塊厝段": "4311",
        "中庄段": "4312",
        "南庄段": "4313",
        "南埔段": "4314",
        "東勢尾段": "4315",
        "福興段": "4316",
        "松子脚段": "4317",
        "頂腳踏": "4318",
        "下腳踏": "4319",
        "安實段": "4320",
        "安行段": "4321",
        "安農段": "4322",
        "安地段": "4323",
        "安重段": "4324",
        "安劃段": "4325",
        "松雅段": "4326",
        "福東段": "4327",
        "南勢厝段": "4328",
        "東安段": "4329",
        "安中段": "4330",
        "頂庄段": "4331",
        "中海段": "4332",
        "南安段": "4333",
        "新南埔段": "4334",
        "新龜売段": "4335",
        "新三塊厝段": "4336",
        "欣洲段": "4337",
        "興安段": "4338",
        "安田段": "4339",
        "安港段": "4340",
        "頂安段": "4341",
    },
    "大肚區": {
        "大肚段": "9100",
        "追分段": "9101",
        "井子頭段井子頭小段": "9102",
        "井子頭段蔗廍小段": "9103",
        "溪洲段": "9104",
        "王田段": "9105",
        "社腳段社腳小段": "9106",
        "社腳段山子頂小段": "9107",
        "汴子頭段山子腳小段": "9108",
        "文昌段": "9109",
        "台紙段": "9110",
        "山陽段": "9111",
        "榮華段": "9112",
        "頂街段": "9113",
        "福利段": "9114",
        "自治段": "9115",
        "大東段": "9116",
        "仁德段": "9117",
        "萬陵段": "9118",
        "中蔗段": "9119",
        "自強段": "9120",
        "慶順段": "9121",
        "遊園段": "9122",
        "瑞井段": "9123",
        "福安段": "9124",
        "福山段": "9125",
        "福吉段": "9126",
        "福和段": "9127",
        "福和北段": "9128",
        "福德段": "9129",
        "南王田段": "9130",
        "王福段": "9131",
        "興和段": "9132",
        "北王田段": "9133",
        "福陽段": "9134",
        "福新段": "9135",
    },
    "大里區": {
        "大里段": "8000",
        "內新段": "8001",
        "涼傘樹段": "8002",
        "大突寮段": "8003",
        "詹厝園段": "8004",
        "草湖段": "8005",
        "塗城段": "8006",
        "中興段": "8007",
        "番子寮段": "8008",
        "番子寮段健仁小段": "8009",
        "新仁段": "8010",
        "新義段": "8011",
        "長春段": "8012",
        "東湖段": "8013",
        "南湖段": "8014",
        "成功段": "8015",
        "金城段": "8016",
        "仁化段": "8017",
        "武德段": "8018",
        "東城段": "8019",
        "向學段": "8020",
        "瑞城段": "8021",
        "北新段": "8022",
        "東榮段": "8023",
        "東興段": "8024",
        "鳳凰段": "8025",
        "立仁段": "8026",
        "公教段": "8027",
        "日新段": "8028",
        "大忠段": "8029",
        "大孝段": "8030",
        "大仁段": "8031",
        "大義段": "8032",
        "喬城段": "8033",
        "吉隆段": "8034",
        "崇光段": "8035",
        "西榮段": "8036",
        "合信段": "8037",
        "華城段": "8038",
        "立新段": "8039",
        "福大段": "8040",
        "新光段": "8041",
        "益民段": "8042",
        "大元段": "8043",
        "國中段": "8044",
        "健民段": "8045",
        "光正段": "8046",
        "練武段": "8047",
        "美群段": "8048",
        "仁城段": "8049",
        "仁美段": "8050",
        "振坤段": "8051",
        "新甲段": "8052",
        "德芳段": "8053",
        "福興段": "8054",
        "大衛段": "8055",
        "樹王段": "8056",
        "萬安段": "8057",
        "大峰段": "8058",
        "西湖北段": "8059",
        "西湖南段": "8060",
        "舊街段": "8061",
        "福德段": "8062",
        "夏田東段": "8063",
        "夏田西段": "8064",
        "東勢尾段": "8065",
        "市政段": "8066",
    },
    "大雅區": {
        "上楓樹腳": "6001",
        "馬岡厝": "6002",
        "大田心": "6003",
        "大雅段": "7000",
        "埔子墘段": "7001",
        "上橫山段": "7002",
        "下橫山段": "7003",
        "上員林段": "7004",
        "下員林段": "7005",
        "四塊厝段": "7006",
        "六張犂段": "7007",
        "十三寮段": "7008",
        "花眉段": "7009",
        "西員寶段": "7010",
        "橫山段": "7011",
        "馬岡段": "7012",
        "上楓段": "7013",
        "三和段": "7014",
        "四德段": "7015",
        "自立段": "7016",
        "自強段": "7017",
        "民生段": "7018",
        "大榮段": "7019",
        "學雅段": "7020",
        "大明段": "7021",
        "永興段": "7022",
        "中山段": "7023",
        "雅潭段": "7024",
        "四維段": "7025",
        "科雅段": "7026",
        "花眉庄段": "7027",
        "西員寶北段": "7028",
        "六寶段": "7029",
        "六雅段": "7030",
        "員寶段": "7031",
        "清雅段": "7032",
        "忠雅段": "7033",
        "寶雅段": "7034",
        "秀雅段": "7035",
        "秀山段": "7036",
        "清泉段": "7037",
        "田心段": "7038",
        "中和段": "7039",
        "信和西段": "7040",
        "信和東段": "7041",
        "馬厝段": "7042",
        "山德段": "7043",
        "陽明段": "7044",
        "永和段": "7045",
        "振興段": "7046",
        "朝順段": "7047",
    },
    "太平區": {
        "太平段": "8500",
        "三汴段": "8501",
        "番子路段": "8502",
        "頭汴坑段": "8503",
        "車籠埔段車籠埔小段": "8504",
        "車籠埔段黃竹坑小段": "8505",
        "宜欣段": "8506",
        "欣欣段": "8507",
        "瑞欣段": "8508",
        "平欣段": "8509",
        "忠平段": "8510",
        "孝平段": "8511",
        "仁平段": "8512",
        "愛平段": "8513",
        "信平段": "8514",
        "義平段": "8515",
        "和平段": "8516",
        "福平段": "8517",
        "壽平段": "8518",
        "中邑段": "8519",
        "光隆段": "8520",
        "永成段": "8521",
        "福星段": "8522",
        "長億段": "8523",
        "福德段": "8524",
        "永新段": "8525",
        "合利段": "8526",
        "永豐段": "8527",
        "福利段": "8528",
        "光華段": "8529",
        "麗園段": "8530",
        "長安段": "8531",
        "萬福段": "8532",
        "光明段": "8533",
        "坪林段": "8534",
        "洪厝段": "8535",
        "吉祥段": "8536",
        "中華段": "8537",
        "勤益段": "8538",
        "大源段": "8539",
        "中山段": "8540",
        "內湖段": "8541",
        "茶寮段": "8542",
        "福隆段": "8543",
        "頂坪段": "8544",
        "興隆段": "8545",
        "光興段": "8546",
        "廣隆段": "8547",
        "七星段": "8548",
        "永隆段": "8549",
        "新德隆段": "8550",
        "溪洲段": "8551",
        "東興段": "8552",
        "東平段": "8553",
        "東和段": "8554",
        "新坪段": "8555",
        "樹孝段": "8556",
        "新高段": "8557",
        "石苓湖段": "8558",
        "德興段": "8559",
        "豐中段": "8560",
        "育賢段": "8561",
        "新興段": "8562",
        "塔湖段": "8563",
        "皇帝筍坑段": "8564",
        "振興段": "8565",
        "新福段": "8566",
        "新光段": "8567",
        "振福段": "8568",
        "樹德段": "8569",
        "永億段": "8570",
        "振文段": "8571",
        "大興段": "8572",
        "聖和段": "8573",
        "中天段": "8574",
        "新頭汴段": "8575",
        "學億段": "8576",
        "長福段": "8577",
        "中南段": "8578",
        "福億段": "8579",
        "內城段": "8580",
        "黃竹段": "8581",
        "竹村段": "8582",
        "淨德段": "8583",
        "東汴段": "8584",
    },
    "外埔區": {
        "六分段": "4000",
        "鐵砧山脚段": "4001",
        "磁磘段": "4002",
        "大甲東段": "4003",
        "內水尾段": "4004",
        "馬鳴埔段": "4005",
        "土城段": "4006",
        "廍子段": "4007",
        "永豐段": "4008",
        "新六分段": "4009",
        "永吉段": "4010",
        "新磁磘段": "4011",
        "大同段": "4012",
        "二崁段": "4013",
        "三崁段": "4014",
        "上土城段": "4015",
        "下土城段": "4016",
        "水美段": "4017",
        "甲東段": "4018",
        "東泰段": "4019",
        "新城段": "4020",
        "大東段": "4021",
        "上鐵山段": "4022",
        "下鐵山段": "4023",
        "蕃社段": "4024",
        "頂竹圍段": "4025",
        "馬鳴段": "4026",
        "風坑段": "4027",
        "上廍子段": "4028",
        "下廍子段": "4029",
        "虎尾寮段": "4030",
        "水美南段": "4031",
        "水美西段": "4032",
        "水美北段": "4033",
        "水美東段": "4034",
    },
    "石岡區": {
        "石岡段石岡小段": "5900",
        "石岡段金星面小段": "5901",
        "石岡段九房厝小段": "5902",
        "仙塘坪段": "5903",
        "社寮角段社寮角小段": "5904",
        "社寮角段梅子樹腳小段": "5905",
        "土牛段土牛小段": "5906",
        "土牛段南眉小段": "5907",
        "土牛段崁子下小段": "5908",
        "岡尾段": "5909",
        "萬安段": "5910",
        "長庚段": "5911",
        "金星段": "5912",
        "廣興段": "5913",
        "萬興段": "5914",
        "梅子段": "5915",
        "國校段": "5916",
        "德興段": "5917",
        "新岡尾段": "5918",
        "新萬安段": "5919",
        "新長庚段": "5920",
        "新金星段": "5921",
        "新廣興段": "5922",
        "新萬興段": "5923",
        "新梅子段": "5924",
        "新國校段": "5925",
        "新德興段": "5926",
        "崁子下段": "5927",
        "南眉段": "5928",
        "八寶圳段": "5929",
        "新金星面段": "5930",
        "龍興段": "5931",
        "石忠段": "5932",
        "電火圳段": "5933",
        "運動段": "5934",
    },
    "后里區": {
        "后里段": "3000",
        "后里段后里小段": "3001",
        "牛稠坑段七星小段": "3002",
        "屯子腳段": "3003",
        "中和段": "3004",
        "舊社段": "3005",
        "圳寮段": "3006",
        "四塊厝段": "3007",
        "月眉段": "3008",
        "月眉段月眉小段": "3009",
        "牛稠坑段": "3010",
        "七塊厝段": "3011",
        "中社段": "3012",
        "公館段": "3013",
        "新店段": "3014",
        "里城段": "3015",
        "金城段": "3016",
        "義里段": "3017",
        "后義段": "3018",
        "泉州段": "3019",
        "后豐段": "3020",
        "后興段": "3021",
        "廣興段": "3022",
        "文明段": "3023",
        "文德段": "3024",
        "公安段": "3025",
        "墩北段": "3026",
        "民富段": "3027",
        "文化段": "3028",
        "平安段": "3029",
        "墩南段": "3030",
        "新公館段": "3031",
        "舊圳段": "3032",
        "中和東段": "3033",
        "中和西段": "3034",
        "舊社新段": "3035",
        "十三張段": "3036",
        "四德段": "3037",
        "四塊庄段": "3038",
        "四月段": "3039",
        "口庄段": "3040",
        "后寶段": "3041",
        "后樟段": "3042",
        "后安段": "3043",
        "后科段": "3044",
        "眉山東段": "3045",
        "眉山西段": "3046",
        "中科北段": "3047",
        "中科南段": "3048",
        "新中社段": "3049",
        "泰安段": "3050",
        "金社庄段": "3051",
        "枋寮段": "3052",
        "后森段": "3053",
        "牛稠新段": "3054",
        "七星段": "3055",
        "新店東段": "3056",
        "新店西段": "3057",
    },
    "沙鹿區": {
        "沙鹿段沙鹿小段": "4900",
        "沙鹿段斗抵小段": "4901",
        "沙鹿段潭子墘小段": "4902",
        "鹿寮段": "4903",
        "北勢坑段北勢坑小段": "4904",
        "北勢坑段六路厝小段": "4905",
        "北勢坑段六埔小段": "4906",
        "竹林段竹林小段": "4907",
        "竹林段犁份小段": "4908",
        "公館段": "4909",
        "南勢坑段南勢坑小段": "4910",
        "南勢坑段埔子小段": "4911",
        "西勢寮段": "4912",
        "西勢段": "4913",
        "中清段": "4914",
        "明德段": "4915",
        "公館北段": "4916",
        "公館南段": "4917",
        "洛泉段": "4918",
        "晉江北段": "4919",
        "英才段": "4920",
        "東英段": "4921",
        "居仁段": "4922",
        "美仁段": "4923",
        "大同段": "4924",
        "福至段": "4925",
        "福興段": "4926",
        "東晉段": "4927",
        "福成段": "4928",
        "護安段": "4929",
        "成衣段": "4930",
        "南勢東段": "4931",
        "慶安段": "4932",
        "南勢段": "4933",
        "鹿峰東段": "4934",
        "鹿峰西段": "4935",
        "鹿寮東段": "4936",
        "沙工段": "4937",
        "沙工北段": "4938",
        "文光段": "4939",
        "太平段": "4940",
        "保寧段": "4941",
        "平等段": "4942",
        "六路段": "4943",
        "新竹林段": "4944",
        "紅竹段": "4945",
        "竹林東段": "4946",
        "福壽段": "4947",
        "興安段": "4948",
        "福田段": "4949",
        "新犁份段": "4950",
        "犁份東段": "4951",
        "大學段": "4952",
        "晉江東段": "4953",
        "六福段": "4954",
        "興安西段": "4955",
        "保成段": "4956",
        "自強段": "4957",
        "三鹿段": "4958",
        "國昌段": "4959",
        "正英段": "4960",
        "正義段": "4961",
        "明秀段": "4962",
        "榜文段": "4963",
        "興仁段": "4964",
        "新站段": "4965",
    },
    "和平區": {
        "南勢段": "6100",
        "博愛段": "6101",
        "谷關段": "6102",
        "達見段": "6103",
        "青山段": "6104",
        "佳陽段": "6105",
        "梨山段": "6106",
        "松茂段": "6107",
        "環山段": "6108",
        "志良段": "6109",
        "勝光段": "6110",
        "七家灣段": "6111",
        "思源段": "6112",
        "武陵段": "6113",
        "福壽山段": "6114",
        "雙崎段": "6115",
        "白毛段": "6116",
        "達觀段": "6117",
        "雪山段": "6118",
        "埋伏坪社段": "6119",
        "黑田段": "6120",
        "七卡段": "6121",
        "桃山段": "6122",
        "松嶺段": "6123",
        "松盧段": "6124",
        "龍谷段": "6125",
        "小雪山段": "6126",
        "鞍馬山段": "6127",
        "新山段": "6128",
        "佳保段": "6129",
        "自由段": "6130",
        "後山寮段": "6131",
        "苗圃段": "6132",
        "阿冷段": "6133",
        "光明段": "6134",
        "劍山段": "6135",
        "釜碗段": "6136",
        "壩新段": "6137",
        "三錐段": "6138",
        "大雪山段": "6139",
        "裡冷段": "6140",
        "沙蓮溪段": "6141",
        "天輪段": "6142",
        "東卯段": "6143",
        "鞍馬溪段": "6144",
        "火石段": "6145",
        "唐呂段": "6146",
        "十文溪段": "6147",
        "西川段": "6148",
        "天池段": "6149",
        "七棟寮段": "6150",
        "百川段": "6151",
        "出雲山段": "6152",
        "達盤段": "6153",
        "大木段": "6154",
        "仁壽段": "6155",
        "興隆段": "6156",
        "四季段": "6157",
        "池有段": "6158",
        "羅葉尾段": "6159",
        "有勝段": "6160",
        "南湖段": "6161",
        "中央段": "6162",
        "羅閑段": "6163",
        "無明段": "6164",
        "捫山段": "6165",
        "育苗段": "6166",
        "崑崙段": "6167",
        "中坑段": "6168",
        "橫流溪段": "6169",
        "東卯溪段": "6170",
        "稍來段": "6171",
        "白鹿段": "6172",
        "裡冷溪段": "6173",
        "八仙山段": "6174",
        "雪山坑段": "6175",
        "摩天嶺段": "6176",
        "烏石坑段": "6177",
        "觀音溪段": "6178",
        "合歡溪段": "6179",
        "白毛山段": "6180",
        "長興段": "6181",
    },
    "東勢區": {
        "東勢段東勢小段": "5400",
        "東勢段上新小段": "5401",
        "東勢段下新小段": "5402",
        "東勢段石角小段": "5403",
        "東勢段中嵙小段": "5404",
        "校栗埔段上校栗埔小段": "5405",
        "校栗埔段下校栗埔小段": "5406",
        "石圍墻段石圍墻小段": "5407",
        "石圍墻段埤頭山小段": "5408",
        "石壁坑段": "5409",
        "新伯公段新伯公小段": "5410",
        "新伯公段上城小段": "5411",
        "新伯公段下城小段": "5412",
        "新伯公段番社小段": "5413",
        "大茅埔段": "5414",
        "互助段": "5415",
        "合作段": "5416",
        "新盛段": "5417",
        "興林段": "5418",
        "詒福段": "5419",
        "詒新段": "5420",
        "保民段": "5421",
        "慶安段": "5422",
        "羊崎段": "5423",
        "和興段": "5424",
        "新成段": "5425",
        "高簡段": "5426",
        "福興段": "5427",
        "新互助段": "5428",
        "新合作段": "5429",
        "泰昌段": "5430",
        "文昌段": "5431",
        "六合段": "5432",
        "義渡段": "5433",
        "仙師段": "5434",
        "東安段": "5435",
        "復興段": "5436",
        "延平段": "5437",
        "民誠段": "5438",
        "興隆段": "5439",
        "下新段": "5440",
        "東新段": "5441",
        "中山段": "5442",
        "吊神山段": "5443",
        "東崎段": "5444",
        "東豐段": "5445",
        "保豐段": "5446",
        "玉高段": "5447",
        "伯公段": "5448",
        "茅埔西段": "5449",
        "茅埔東段": "5450",
        "慶東段": "5451",
        "慶福段": "5452",
        "坪埔段": "5453",
        "石嵙段": "5454",
        "石城段": "5455",
        "埤頭段": "5456",
        "石圍墻二段": "5457",
        "石圍墻一段": "5458",
        "東崎一段": "5459",
        "中嵙一段": "5460",
    },
    "烏日區": {
        "烏日段": "7300",
        "九張犁段": "7301",
        "頭前厝段": "7302",
        "學田段": "7303",
        "朥月胥段頂朥月胥小段": "7304",
        "朥月胥段下朥月胥小段": "7305",
        "五張犁段": "7306",
        "重建段": "7307",
        "阿密哩段": "7308",
        "蘆竹湳段": "7309",
        "溪心壩段": "7310",
        "喀哩段": "7311",
        "同安厝段": "7312",
        "溪南東段": "7313",
        "溪南西段": "7314",
        "螺潭段": "7315",
        "北里段": "7316",
        "九如段": "7317",
        "九德段": "7318",
        "中華段": "7319",
        "自立段": "7320",
        "仁德段": "7321",
        "信義段": "7322",
        "興祥段": "7323",
        "三民段": "7324",
        "自治段": "7325",
        "光日段": "7326",
        "湖日段": "7327",
        "山頂段": "7328",
        "成功嶺段": "7329",
        "便行段": "7330",
        "中山段": "7331",
        "高鐵段": "7332",
        "站南段": "7333",
        "三和段": "7334",
        "榮和段": "7335",
        "榮泉段": "7336",
        "長壽段": "7337",
        "新高鐵段": "7338",
        "新站南段": "7339",
        "新三和段": "7340",
        "新榮和段": "7341",
        "新榮泉段": "7342",
        "新長壽段": "7343",
        "溪尾北段": "7344",
        "溪尾南段": "7345",
        "五張犁東段": "7346",
        "五張犁西段": "7347",
        "溪壩段": "7348",
        "新喀哩段": "7349",
        "新北里段": "7350",
        "高學田段": "7351",
        "頭前厝北段": "7352",
        "頭前厝南段": "7353",
        "新蘆竹湳段": "7354",
        "新同安厝段": "7355",
        "環河段": "7356",
        "前農段": "7357",
        "前竹段": "7358",
        "前興段": "7359",
        "中紡段": "7360",
    },
    "神岡區": {
        "神岡段": "3300",
        "山皮段": "3301",
        "北庄段": "3302",
        "圳堵段": "3303",
        "新庄子段": "3304",
        "社口段": "3305",
        "大社段": "3306",
        "三角子段": "3307",
        "社南段": "3308",
        "建國段": "3309",
        "下溪洲段后寮小段": "3310",
        "下溪洲段後壁厝小段": "3311",
        "望寮段": "3312",
        "圳前段": "3313",
        "福隆段": "3314",
        "厚生段": "3315",
        "林厝段": "3316",
        "神圳段": "3317",
        "順濟段": "3318",
        "神林段": "3319",
        "神洲段": "3320",
        "大富段": "3321",
        "岸裡段": "3322",
        "大社東段": "3323",
        "大洲段": "3324",
        "前寮段": "3325",
        "神工段": "3326",
        "十五庄段": "3327",
        "豐洲北段": "3328",
        "豐工段": "3329",
        "石橋段": "3330",
        "大明段": "3331",
        "大豐段": "3332",
        "國豐段": "3333",
        "三角東段": "3334",
        "三角西段": "3335",
        "光啟段": "3336",
        "李洲段": "3337",
        "溪洲段": "3338",
        "竹圍段": "3339",
        "朝清段": "3340",
        "福庄段": "3341",
        "仁愛段": "3342",
        "光復段": "3343",
        "新和段": "3344",
        "新興段": "3345",
        "新圳段": "3346",
        "圳北段": "3347",
        "六張段": "3348",
        "溝心段": "3349",
        "宋厝段": "3350",
        "新社口段": "3351",
        "庄前段": "3352",
        "瓦磘腳段": "3353",
    },
    "梧棲區": {
        "梧棲段": "5200",
        "中港段": "5201",
        "民生段": "5202",
        "忠孝段": "5203",
        "南簡段": "5204",
        "大庄段大庄小段": "5205",
        "大庄段火燒橋小段": "5206",
        "仁愛段": "5207",
        "信義段": "5208",
        "和平段": "5209",
        "三民段": "5210",
        "民族段": "5211",
        "民權段": "5212",
        "鴨母寮段鴨母寮小段": "5213",
        "永安段": "5214",
        "港口段": "5215",
        "頂寮段": "5216",
        "下寮段": "5217",
        "西建段": "5218",
        "東建段": "5219",
        "安仁段": "5220",
        "文化段": "5221",
        "港加段": "5222",
        "市鎮南段": "5223",
        "興農段": "5224",
        "三條圳段": "5225",
        "庄北段": "5226",
        "庄南段": "5227",
    },
    "清水區": {
        "清水段清水小段": "4600",
        "清水段西勢小段": "4601",
        "銀聯段": "4602",
        "槺榔段": "4603",
        "大突寮段大突寮小段": "4604",
        "大突寮段十塊寮小段": "4605",
        "秀水段秀水小段": "4606",
        "海濱段": "4607",
        "海濱段臨港小段": "4608",
        "高美段": "4609",
        "武秀段": "4610",
        "三塊厝段三塊厝小段": "4611",
        "三塊厝段菁埔小段": "4612",
        "三塊厝段頂湳子小段": "4613",
        "社口段社口小段": "4614",
        "四塊厝段": "4615",
        "田寮段田寮小段": "4616",
        "田寮段橋頭小段": "4617",
        "田寮段下湳子小段": "4618",
        "楊厝寮段楊厝寮小段": "4619",
        "楊厝寮段海風小段": "4620",
        "三田段": "4621",
        "裕嘉段": "4622",
        "吳厝段吳厝小段": "4623",
        "吳厝段橋頭寮小段": "4624",
        "中興段": "4625",
        "西寧段": "4626",
        "光華段": "4627",
        "紫雲段": "4628",
        "新興段": "4629",
        "鰲峰段": "4630",
        "海風段": "4631",
        "楊厝段": "4632",
        "吳厝北段": "4633",
        "吳厝南段": "4634",
        "市鎮北段": "4635",
        "甲南段": "4636",
        "頂湳段": "4637",
        "菁埔北段": "4638",
        "菁埔南段": "4639",
        "臨海段": "4640",
        "朝天段": "4641",
        "高美東段": "4642",
        "高美南段": "4643",
        "高美中段": "4644",
        "高南段": "4645",
        "高北段": "4646",
        "高西段": "4647",
        "金皇段": "4648",
        "下湳段": "4649",
        "朝興段": "4650",
        "朝后段": "4651",
        "東山段": "4652",
        "公正段": "4653",
        "星海段": "4654",
        "西社段": "4655",
        "鎮新段": "4656",
        "橋頭段": "4657",
        "五權段": "4658",
        "三順段": "4659",
        "清甲段": "4660",
        "牛罵頭段": "4661",
        "福安段": "4662",
        "橋江段": "4663",
    },
    "新社區": {
        "新社段新社小段": "5700",
        "新社段食水嵙小段": "5701",
        "新社段山頂小段": "5702",
        "新社段復盛小段": "5703",
        "七分段七分小段": "5704",
        "七分段十分小段": "5705",
        "七分段水井子小段": "5706",
        "大南段大南小段": "5707",
        "大南段番社嶺小段": "5708",
        "水底寮段上水底寮小段": "5709",
        "水底寮段下水底寮小段": "5710",
        "鳥銃頭段": "5711",
        "馬力埔段": "5712",
        "永居湖段": "5713",
        "二櫃段": "5714",
        "三友部段": "5715",
        "食水嵙段": "5716",
        "中正段": "5717",
        "糖廍段": "5718",
        "新安段": "5719",
        "國校段": "5720",
        "新農段": "5721",
        "新中段": "5722",
        "復盛段": "5723",
        "月湖段": "5724",
        "龍安段": "5725",
        "崑山段": "5726",
        "神木段": "5727",
        "新大南段": "5728",
        "新水井段": "5729",
        "新南段": "5730",
        "永興段": "5731",
        "協中段": "5732",
        "湳嶺段": "5733",
        "新七分段": "5734",
        "新馬力埔段": "5735",
        "種苗圃段": "5736",
        "興中段": "5737",
        "華豐段": "5738",
        "二苗圃段": "5739",
        "頭嵙段": "5740",
        "上水底寮一段": "5741",
        "下水底寮段": "5742",
    },
    "潭子區": {
        "潭子段": "6700",
        "甘蔗崙段": "6701",
        "校栗林段": "6702",
        "東員寶段": "6703",
        "瓦磘子段": "6704",
        "茄荎角段": "6705",
        "頭家厝段": "6706",
        "大埔厝段大埔厝小段": "6707",
        "大埔厝段牛埔子小段": "6708",
        "聚興段": "6709",
        "聚興段新興小段": "6710",
        "潭北段": "6711",
        "潭秀段": "6712",
        "潭陽段": "6713",
        "石牌段": "6714",
        "潭興段": "6715",
        "復興段": "6716",
        "聖宮段": "6717",
        "大新段": "6718",
        "甘潭段": "6719",
        "栗林段": "6720",
        "祥和段": "6721",
        "安和段": "6722",
        "潭富段": "6723",
        "工區段": "6724",
        "興華段": "6725",
        "僑忠段": "6726",
        "華泰段": "6727",
        "嘉仁段": "6728",
        "嘉豐段": "6729",
        "東寶一段": "6730",
        "東寶二段": "6731",
        "東寶三段": "6732",
        "東寶五段": "6733",
        "東寶六段": "6734",
        "東寶七段": "6735",
        "家興段": "6736",
        "頭張段": "6737",
        "中興段": "6738",
        "頭家段": "6739",
        "家福段": "6740",
        "中山段": "6741",
        "摘星段": "6742",
        "大豐段": "6743",
        "大富段": "6744",
        "弘富段": "6745",
        "大德段": "6746",
        "牛埔段": "6747",
        "帝君段": "6748",
        "豐興段": "6749",
        "僑興段": "6750",
        "興龍段": "6751",
        "田興段": "6752",
        "新潭段": "6753",
        "寶興段": "6754",
        "新田段": "6755",
    },
    "龍井區": {
        "龍井段竹坑小段": "9300",
        "龍井段龍井小段": "9301",
        "新庄子段新庄子小段": "9302",
        "新庄子段南寮小段": "9303",
        "山腳段": "9304",
        "福麗段": "9305",
        "龍津段": "9306",
        "龍目井段龍目井小段": "9307",
        "龍目井段水師寮小段": "9308",
        "龍目井段水裡社小段": "9309",
        "三德段": "9310",
        "忠和段": "9311",
        "竹泉段": "9312",
        "茄投段": "9313",
        "龍田段": "9314",
        "中山段": "9315",
        "田水段": "9316",
        "東園段": "9317",
        "遊園南段": "9318",
        "永順段": "9319",
        "新庄段": "9320",
        "新興段": "9321",
        "新東段": "9322",
        "東海段": "9323",
        "遊園北段": "9324",
        "南寮段": "9325",
        "藝術段": "9326",
        "遠東段": "9327",
        "龍山段": "9328",
        "鷺山段": "9329",
        "中社段": "9330",
        "龍新段": "9331",
        "龍社段": "9332",
        "木本段": "9333",
        "龍崗段": "9334",
        "龍泉段": "9335",
        "竹師段": "9336",
    },
    "豐原區": {
        "豐原段": "2400",
        "大湳段": "2401",
        "下南坑段": "2402",
        "上南坑段": "2403",
        "圳寮段(豐原)": "2404",
        "翁子段": "2405",
        "鐮子坑口段": "2406",
        "社皮段": "2407",
        "朴子口段": "2408",
        "烏牛欄段烏牛欄小段": "2409",
        "烏牛欄段田心子小段": "2410",
        "車路墘段車路墘小段": "2411",
        "車路墘段溝子墘小段": "2412",
        "北陽段": "2413",
        "向陽段": "2414",
        "中陽段": "2415",
        "陽明段": "2416",
        "博愛段": "2417",
        "東陽段": "2418",
        "豐東段": "2419",
        "綠山段": "2420",
        "南陽段": "2421",
        "安康段": "2422",
        "南村段": "2423",
        "慈興段": "2424",
        "東湳段": "2425",
        "大順段": "2426",
        "大仁段": "2427",
        "豐中段": "2428",
        "龍宮段": "2429",
        "西湳段": "2430",
        "豐洲段": "2431",
        "豐南段": "2432",
        "柑宅段": "2433",
        "豐田段": "2434",
        "鎮宮段": "2435",
        "福德段": "2436",
        "市政段": "2437",
        "育仁段": "2438",
        "合作段": "2439",
        "成功段": "2440",
        "水源段": "2441",
        "豐村段": "2442",
        "永豐段": "2443",
        "翁明段": "2444",
        "三豐段": "2445",
        "下街段": "2446",
        "豐圳段": "2447",
        "建成段": "2448",
        "一心段": "2449",
        "五汴段": "2450",
        "豐社段": "2451",
        "豐年段": "2452",
        "萬年段": "2453",
        "福興段": "2454",
        "順豐段": "2455",
        "萬順段": "2456",
        "師範段": "2457",
        "聯合段": "2458",
        "葫蘆墩段": "2459",
        "豐陽段": "2460",
        "南田段": "2461",
        "新水源段": "2462",
        "南嵩段": "2463",
        "新東陽段": "2464",
        "新綠山段": "2465",
        "復興段": "2466",
        "朝陽段": "2467",
        "鐮村段": "2468",
        "鳳山段": "2469",
        "豐新段": "2470",
        "三陽段": "2471",
        "三和段": "2472",
        "福陽段": "2473",
        "東湳北段": "2474",
        "西湳北段": "2475",
        "北天段": "2476",
        "中興段": "2477",
        "博安段": "2478",
        "議前段": "2479",
        "三村段": "2480",
        "公老坪段": "2481",
        "豐栗段": "2482",
    },
    "霧峰區": {
        "霧峰段霧峰小段": "7700",
        "霧峰段北溝小段": "7701",
        "霧峰段坑口小段": "7702",
        "柳樹湳段": "7703",
        "丁台段丁台小段": "7704",
        "丁台段南勢小段": "7705",
        "吳厝段": "7706",
        "萬斗六段": "7707",
        "萬斗六段六股小段": "7708",
        "天時段": "7709",
        "地利段": "7710",
        "人和段": "7711",
        "峰東段": "7712",
        "峰西段": "7713",
        "峰南段": "7714",
        "峰北段": "7715",
        "北勢段": "7716",
        "北柳段": "7717",
        "峰谷段": "7718",
        "萬豐段": "7719",
        "豐正段": "7720",
        "文化段": "7721",
        "吉峰段": "7722",
        "錦州段": "7723",
        "中正段": "7724",
        "育德段": "7725",
        "新生段": "7726",
        "舊正西段": "7727",
        "南勢東段": "7728",
        "南勢西段": "7729",
        "丁台一段": "7730",
        "丁台二段": "7731",
        "丁台三段": "7732",
        "新六股段": "7733",
        "農試所段": "7734",
        "舊正東段": "7735",
        "桐林段": "7736",
        "霧工段": "7737",
        "南柳段": "7738",
        "北柳南段": "7739",
        "新厝段": "7740",
        "五福段": "7741",
        "新埔段": "7742",
        "四德段": "7743",
        "五福北段": "7744",
        "五福南段": "7745",
        "大圳頭段": "7746",
        "萊園段": "7747",
        "新坑口段": "7748",
        "復興段": "7749",
        "尖後段": "7750",
        "新北溝段": "7751",
        "新峰東段": "7752",
        "暗坑段": "7753",
        "樟公段": "7754",
        "本堂段": "7755",
        "立德段": "7756",
        "南坑段": "7757",
        "大坑段": "7758",
        "慶堡北段": "7759",
        "慶堡南段": "7760",
    },
}


if __name__ == "__main__":
    args = sys.argv[1:]

    # 內部 worker 模式（被 subprocess 呼叫，不顯示給使用者）
    if args and args[0] == "--overlay-worker":
        _, district, code, lot, out_file = args
        _overlay_worker(district, code, lot, out_file)
        sys.exit(0)

    if args and args[0] == "--bupic-worker":
        _, license_str, out_file = args
        _bupic_worker(license_str, out_file)
        sys.exit(0)

    if args and args[0] == "--gsa-worker":
        _, district, section_name, lot, out_file = args
        _gsa_worker(district, section_name, lot, out_file)
        sys.exit(0)

    if args and args[0] == "--slope-worker":
        _, district, section_name, lot, out_file = args
        _slope_worker(district, section_name, lot, out_file)
        sys.exit(0)

    if args and args[0] == "--firebreak-worker":
        _, district, code, lot, out_file = args
        _firebreak_worker(district, code, lot, out_file)
        sys.exit(0)

    if args and args[0] == "--sewer-worker":
        _, district, code, lot, out_file = args
        _sewer_worker(district, code, lot, out_file)
        sys.exit(0)

    if args and args[0] == "--fault-worker":
        _, district, section_name, lot, out_file = args
        _fault_worker(district, section_name, lot, out_file)
        sys.exit(0)

    if args and args[0] == "--ud-worker":
        _, urban_plan_area, plan_case_name, save_dir, out_file = args
        _ud_worker(urban_plan_area, plan_case_name, save_dir, out_file)
        sys.exit(0)

    if args and args[0] == "--lot2addr-worker":
        _, district, section_name, lot, out_file = args
        addr = lot_to_address(district, section_name, lot)
        import json as _json
        with open(out_file, "w", encoding="utf-8") as _f:
            _json.dump({"address": addr}, _f, ensure_ascii=False)
        sys.exit(0)

    # 列出所有地段
    if args == ["list"]:
        for district, sections in SECTIONS.items():
            print(f"\n{district}（{len(sections)} 段）")
            for name in sections:
                print(f"  {name}")
        sys.exit(0)

    # 門牌地址查詢：python3 gis_query.py <行政區><路名><門牌號>號
    if len(args) == 1 and re.search(r'[街路道].*\d+號', args[0]):
        district, section_name, lot = address_to_lot(args[0])
        if district and section_name and lot:
            lookup(district, section_name, lot, address=args[0])
        else:
            print("門牌轉地號失敗，請直接輸入：行政區 地段名 地號")
        sys.exit(0)

    # 從檔案讀取批次查詢：python3 gis_query.py file.txt
    if len(args) == 1 and args[0].endswith(".txt"):
        queries = []
        with open(args[0], encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) == 3:
                    queries.append((parts[0], parts[1], parts[2]))
                else:
                    print(f"略過格式錯誤的行：{line}")
        if queries:
            results = query_batch(queries)
            for d, s, n, texts, overlay, bupic_list, gsa, slope, firebreak, sewer, fault, ud, lot2addr in results:
                bupic_addr = next((_bupic_address(bp.get("執照存根詳細", {})) for bp in (bupic_list or []) if _bupic_address(bp.get("執照存根詳細", {}))), "")
                final_addr = lot2addr or bupic_addr
                print_result(d, s, n, texts, overlay, bupic_list, gsa, slope, firebreak, sewer, fault=fault, ud=ud, address=final_addr)
                save_pdf(d, s, n, texts, overlay, bupic_list, gsa, slope, firebreak, sewer, fault=fault, ud=ud, address=final_addr)
        sys.exit(0)

    # 同地段多地號：python3 gis_query.py <行政區> <地段> <地號1> <地號2> <地號3>
    if len(args) >= 4:
        district, section = args[0], args[1]
        lots = args[2:]
        queries = [(district, section, lot) for lot in lots]
        results = query_batch(queries)
        for d, s, n, texts, overlay, bupic_list, gsa, slope, firebreak, sewer, fault, ud, lot2addr in results:
            bupic_addr = next((_bupic_address(bp.get("執照存根詳細", {})) for bp in (bupic_list or []) if _bupic_address(bp.get("執照存根詳細", {}))), "")
            final_addr = lot2addr or bupic_addr
            print_result(d, s, n, texts, overlay, bupic_list, gsa, slope, firebreak, sewer, fault=fault, ud=ud, address=final_addr)
            save_pdf(d, s, n, texts, overlay, bupic_list, gsa, slope, firebreak, sewer, fault=fault, ud=ud, address=final_addr)
        sys.exit(0)

    # 單筆：python3 gis_query.py <行政區> <地段> <地號>
    if len(args) == 3:
        lookup(args[0], args[1], args[2])
        sys.exit(0)

    print("用法：")
    print("  門牌：  python3 gis_query.py <行政區><路名><門牌號>號")
    print("  單筆：  python3 gis_query.py <行政區> <地段> <地號>")
    print("  多地號：python3 gis_query.py <行政區> <地段> <地號1> <地號2> <地號3>")
    print("  批次檔：python3 gis_query.py 地號清單.txt")
    print("  列地段：python3 gis_query.py list")
    print()
    print("批次檔格式（每行一筆，用空格分隔）：")
    print("  <行政區> <地段> <地號>")
    print("  <行政區> <地段> <地號>")
    print("  <行政區> <地段> <地號>")
