"""
Graphify — generate an interactive knowledge graph for the Taiwan Architect KB.

Scans raw/, parses SKILL.md frontmatter, and outputs a self-contained HTML
file with a D3.js force-directed graph (loaded from CDN, no local deps).
"""

import json
import os
import re
import sys

RAW = os.path.join(os.path.dirname(__file__), "..", "raw")
OUT = os.path.join(os.path.dirname(__file__), "..", "outputs")


def parse_frontmatter(path):
    """Extract YAML frontmatter fields from a SKILL.md file. Returns dict."""
    with open(path, encoding="utf-8") as f:
        content = f.read()

    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {}

    fields = {}
    for line in m.group(1).splitlines():
        kv = re.match(r"^(\w+)\s*:\s*(.+)$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            # Strip quotes
            val = re.sub(r'^["\']|["\']$', "", val)
            fields[key] = val
    return fields


def scan(raw):
    """Walk raw/ and build node/link data for the knowledge graph."""
    nodes = []
    links = []
    node_ids = set()
    cat_colors = {}

    palette = [
        "#4e79a7", "#f28e2b", "#e15759", "#76b7b2",
        "#59a14f", "#edc948", "#b07aa1", "#ff9da7",
        "#9c755f", "#bab0ac", "#6b6ecf",
    ]

    def add_node(id_, label, group, level):
        if id_ not in node_ids:
            node_ids.add(id_)
            nodes.append({"id": id_, "label": label, "group": group, "level": level})

    def add_link(source, target):
        links.append({"source": source, "target": target})

    # Walk directories
    for cat_name in sorted(os.listdir(raw)):
        cat_path = os.path.join(raw, cat_name)
        if not os.path.isdir(cat_path) or cat_name.startswith("."):
            continue

        cat_id = f"cat:{cat_name}"
        cat_idx = len([k for k in cat_colors])
        cat_colors[cat_name] = palette[cat_idx % len(palette)]
        add_node(cat_id, cat_name, cat_name, 0)

        for entry_name in sorted(os.listdir(cat_path)):
            entry_path = os.path.join(cat_path, entry_name)
            if not os.path.isdir(entry_path) or entry_name.startswith("."):
                continue

            # Check if this entry has skill subdirs
            skill_dirs = []
            for sub in sorted(os.listdir(entry_path)):
                sub_path = os.path.join(entry_path, sub)
                if os.path.isdir(sub_path) and not sub.startswith("."):
                    skill_path = os.path.join(sub_path, "SKILL.md")
                    if os.path.isfile(skill_path):
                        skill_dirs.append((sub, skill_path))
                    else:
                        # Could be old-style: SKILL.md in entry itself
                        pass

            # Old-style: SKILL.md directly in entry dir
            old_style_skill = os.path.join(entry_path, "SKILL.md")
            if os.path.isfile(old_style_skill):
                fm = parse_frontmatter(old_style_skill)
                skill_id = f"skill:{cat_name}/{entry_name}"
                skill_label = fm.get("name", entry_name)
                add_node(skill_id, skill_label, cat_name, 2)
                add_link(cat_id, skill_id)
                continue

            if skill_dirs:
                # This entry is a sub-category with multiple skills
                entry_id = f"entry:{cat_name}/{entry_name}"
                add_node(entry_id, entry_name, cat_name, 1)
                add_link(cat_id, entry_id)

                for skill_name, skill_path in skill_dirs:
                    fm = parse_frontmatter(skill_path)
                    skill_id = f"skill:{cat_name}/{entry_name}/{skill_name}"
                    skill_label = fm.get("name", skill_name)
                    add_node(skill_id, skill_label, cat_name, 2)
                    add_link(entry_id, skill_id)
            else:
                # Empty or planned entry — just show it as leaf
                entry_id = f"entry:{cat_name}/{entry_name}"
                add_node(entry_id, entry_name, cat_name, 1)
                add_link(cat_id, entry_id)

    return {"nodes": nodes, "links": links}, cat_colors


def build_html(graph_data, cat_colors):
    """Wrap the graph data in a self-contained HTML with D3.js."""
    nodes_json = json.dumps(graph_data["nodes"], ensure_ascii=False)
    links_json = json.dumps(graph_data["links"], ensure_ascii=False)
    colors_json = json.dumps(cat_colors, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>Taiwan Architect KB — Knowledge Graph</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: system-ui, sans-serif; background: #f8f9fa; }}
  #header {{ background: #2c3e50; color: #fff; padding: 16px 24px;
             display: flex; align-items: center; justify-content: space-between; }}
  #header h1 {{ font-size: 18px; font-weight: 600; }}
  #header span {{ font-size: 13px; opacity: 0.7; }}
  #graph {{ width: 100vw; height: calc(100vh - 56px); }}
  .node circle {{ stroke: #fff; stroke-width: 1.5px; cursor: pointer; }}
  .node text {{ font-size: 11px; pointer-events: none;
                text-shadow: 0 1px 2px rgba(0,0,0,0.15); }}
  .link {{ stroke: #ccc; stroke-opacity: 0.6; }}
  .legend {{ position: fixed; right: 20px; top: 80px; background: rgba(255,255,255,0.92);
             border-radius: 8px; padding: 12px 16px; font-size: 12px;
             box-shadow: 0 2px 8px rgba(0,0,0,0.1); max-height: 70vh; overflow-y: auto; }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; margin: 3px 0; }}
  .legend-swatch {{ width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }}
  .tooltip {{ position: fixed; display: none; background: rgba(0,0,0,0.8); color: #fff;
              padding: 6px 12px; border-radius: 6px; font-size: 13px; pointer-events: none;
              z-index: 100; white-space: nowrap; }}
</style>
</head>
<body>
<div id="header">
  <h1>Taiwan Architect KB — Knowledge Graph</h1>
  <span>Drag nodes · Scroll to zoom · Hover for details</span>
</div>
<div id="graph"></div>
<div class="legend" id="legend"></div>
<div class="tooltip" id="tooltip"></div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
(function() {{
  const nodes = {nodes_json};
  const links = {links_json};
  const catColors = {colors_json};

  const width = window.innerWidth;
  const height = window.innerHeight - 56;

  const svg = d3.select("#graph").append("svg")
      .attr("width", width).attr("height", height);

  const g = svg.append("g");
  const tooltip = d3.select("#tooltip");

  const zoom = d3.zoom().scaleExtent([0.1, 4]).on("zoom", (e) => {{
    g.attr("transform", e.transform);
  }});
  svg.call(zoom);

  const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(d => 60 + 40 * d.source.level + 40 * d.target.level))
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(d => 5 + d.level * 8));

  const link = g.append("g").selectAll("line")
      .data(links).join("line")
      .attr("class", "link")
      .attr("stroke-width", 1);

  const nodeRadius = d => 6 + d.level * 5;

  const node = g.append("g").selectAll("g")
      .data(nodes).join("g")
      .attr("class", "node")
      .call(d3.drag()
          .on("start", (e, d) => {{
            if (!e.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x; d.fy = d.y;
          }})
          .on("drag", (e, d) => {{ d.fx = e.x; d.fy = e.y; }})
          .on("end", (e, d) => {{
            if (!e.active) simulation.alphaTarget(0);
            d.fx = null; d.fy = null;
          }}));

  node.append("circle")
      .attr("r", nodeRadius)
      .attr("fill", d => catColors[d.group] || "#999")
      .on("mouseover", (e, d) => {{
        tooltip.style("display", "block")
            .html(d.label + (d.level === 2 ? '<br><small>Skill</small>' : ''))
            .style("left", (e.clientX + 12) + "px")
            .style("top", (e.clientY - 10) + "px");
      }})
      .on("mouseout", () => tooltip.style("display", "none"));

  node.append("text")
      .attr("dx", d => nodeRadius(d) + 4)
      .attr("dy", 4)
      .text(d => d.label);

  simulation.on("tick", () => {{
    link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    node.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
  }});

  // Legend
  const legend = d3.select("#legend");
  legend.append("div").style("font-weight", "600").style("margin-bottom", "6px").text("Categories");
  Object.entries(catColors).forEach(([name, color]) => {{
    legend.append("div").attr("class", "legend-item")
        .html(`<span class="legend-swatch" style="background:${{color}}"></span>${{name}}`);
  }});

  // Fit initial view
  svg.call(zoom.transform, d3.zoomIdentity.translate(width/4, height/3).scale(0.7));
}})();
</script>
</body>
</html>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    graph_data, cat_colors = scan(RAW)
    html = build_html(graph_data, cat_colors)

    out_path = os.path.join(OUT, "knowledge-graph.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] Knowledge graph generated: {out_path}")
    print(f"     {len(graph_data['nodes'])} nodes, {len(graph_data['links'])} links")

    # Auto-stage the output when running as pre-commit hook
    try:
        import subprocess
        result = subprocess.run(
            ["git", "add", out_path],
            capture_output=True, text=True, cwd=os.path.dirname(__file__)
        )
        if result.returncode == 0:
            print(f"     Staged in git")
    except Exception:
        pass


if __name__ == "__main__":
    main()
