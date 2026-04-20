#!/usr/bin/env python3
"""
Graphify for HJPLUS Taiwan Architect KB
========================================
Turn a folder of markdown files into a knowledge graph.
Zero external dependencies (Python 3.6+).

Usage:
    python graphify.py ./raw -o ./graphify-out

Output:
    graphify-out/
        graph.json              - Persistent knowledge graph (nodes + edges)
        graph.html              - Interactive visualization (vis.js)
        GRAPH_REPORT.md         - Summary report (god nodes, communities, connections)
"""

import argparse
import hashlib
import json
import math
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


# ============================================================
# YAML Frontmatter Parser (zero dependency)
# ============================================================
def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content."""
    fm_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    match = fm_pattern.match(content)
    if not match:
        return {}

    fm_text = match.group(1)
    result = {}
    for line in fm_text.strip().split('\n'):
        line = line.strip()
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # Handle boolean values
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            result[key] = value
    return result


# ============================================================
# Node and Edge Definitions
# ============================================================
class Node:
    def __init__(self, node_id, label, node_type, category=None, subcategory=None, skill_name=None, file_path=None, frontmatter=None):
        self.id = node_id
        self.label = label
        self.type = node_type  # 'category', 'subcategory', 'domain', 'skill', 'empty_dir'
        self.category = category
        self.subcategory = subcategory
        self.skill_name = skill_name
        self.community = None
        self.description = ''
        self.file_path = file_path or ''
        self.frontmatter = frontmatter or {}

    def to_dict(self):
        d = {
            'id': self.id,
            'label': self.label,
            'type': self.type
        }
        if self.description:
            d['description'] = self.description
        if self.file_path:
            d['file_path'] = self.file_path
        if self.frontmatter:
            d['frontmatter'] = {k: v for k, v in self.frontmatter.items() if v is not None}
        return d


class Edge:
    def __init__(self, source, target, edge_type, source_file=None):
        self.source = source
        self.target = target
        self.type = edge_type  # 'contains', 'derived_from', 'related', 'also_refers_to'
        self.source_file = source_file

    def to_dict(self):
        d = {
            'source': self.source,
            'target': self.target,
            'type': self.type
        }
        if self.source_file:
            d['source_file'] = self.source_file
        return d


# ============================================================
# Graph Builder
# ============================================================
class KnowledgeGraphBuilder:
    def __init__(self, raw_dir, output_dir, exclude_dirs=None, include_empty=False):
        self.raw_dir = Path(raw_dir)
        self.output_dir = Path(output_dir)
        self.nodes = []
        self.edges = []
        self.node_map = {}  # id -> Node
        # Convert exclude_dirs to tuples for proper comparison
        self.exclude_dirs = tuple(tuple(d) for d in (exclude_dirs or []))
        self.include_empty = include_empty

    def build(self):
        """Main build pipeline."""
        print(f"[1/4] Scanning {self.raw_dir}...")
        self.scan_files()

        print(f"[2/4] Building graph ({len(self.nodes)} nodes, {len(self.edges)} edges)...")
        self.add_keyword_edges()

        print(f"[3/4] Detecting communities...")
        self.assign_communities()

        print(f"[4/4] Writing output to {self.output_dir}...")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.write_graph_json()
        self.write_graph_html()
        self.write_report_md()

        print(f"Done! Output saved to {self.output_dir}/")
        print(f"  - {self.output_dir}/graph.json")
        print(f"  - {self.output_dir}/graph.html")
        print(f"  - {self.output_dir}/GRAPH_REPORT.md")
        print()

        # Print stats
        type_counts = defaultdict(int)
        for n in self.nodes:
            type_counts[n.type] += 1
        print("Node types:")
        for t, c in sorted(type_counts.items()):
            print(f"  {t}: {c}")
        print(f"Edges: {len(self.edges)}")

    def scan_files(self):
        """Scan all markdown files in raw_dir."""
        # Collect all directories first if include_empty is True
        all_dirs = set()
        if self.include_empty:
            for dir_path in self.raw_dir.rglob('*'):
                if dir_path.is_dir():
                    rel_path = dir_path.relative_to(self.raw_dir)
                    if not any(rel_path.parts[:i] in self.exclude_dirs for i in range(1, len(rel_path.parts) + 1)):
                        all_dirs.add(str(rel_path))

        for md_file in sorted(self.raw_dir.rglob('*.md')):
            rel_path = md_file.relative_to(self.raw_dir)
            parts = tuple(rel_path.parts)

            # Check if directory is excluded
            if any(parts[:i] in self.exclude_dirs for i in range(1, len(parts) + 1)):
                continue

            # Parse frontmatter
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            fm = parse_frontmatter(content)

            # Extract title from frontmatter or filename
            skill_name = fm.get('name', parts[-1].replace('.md', '').replace('-', ' '))
            description = fm.get('description', '')

            # Extract first paragraph from content as description
            if not description:
                para_match = re.search(r'\n\n(.*?)(?:\n|$)', content)
                if para_match:
                    description = para_match.group(1)[:200]

            # Determine node type
            is_skill = md_file.name == 'skill.md' or md_file.name == 'SKILL.md'
            is_domain = md_file.name == 'domain.md'

            # Build unique node ID using full directory path
            dir_path = parts[-2] if len(parts) >= 2 else parts[-1]
            path_slug = '-'.join(parts[:-1]).replace('/', '-').replace('\\', '-')
            if is_skill:
                node_id = f"skill-{path_slug}"
            elif is_domain:
                node_id = f"domain-{path_slug}"
            else:
                continue  # Skip other markdown files

            # Create node
            node = Node(
                node_id=node_id,
                label=skill_name,
                node_type='skill' if is_skill else 'domain',
                category=parts[0] if len(parts) > 1 else '',
                subcategory=parts[1] if len(parts) > 2 else '',
                skill_name=parts[-2] if len(parts) > 2 else parts[0],
                file_path=str(rel_path),
                frontmatter=fm
            )
            node.description = description
            self.nodes.append(node)
            self.node_map[node_id] = node

            # Create category and subcategory nodes (for visualization)
            if len(parts) > 1:
                category_name = parts[0]
                cat_node_id = f"category-{category_name}"
                if cat_node_id not in self.node_map:
                    cat_node = Node(
                        node_id=cat_node_id,
                        label=category_name,
                        node_type='category'
                    )
                    self.nodes.append(cat_node)
                    self.node_map[cat_node_id] = cat_node

            if len(parts) > 2:
                category_name = parts[0]
                subcategory = parts[1]
                subcat_node_id = f"subcategory-{category_name}-{subcategory}"
                if subcat_node_id not in self.node_map:
                    subcat_node = Node(
                        node_id=subcat_node_id,
                        label=subcategory,
                        node_type='subcategory',
                        category=category_name
                    )
                    self.nodes.append(subcat_node)
                    self.node_map[subcat_node_id] = subcat_node

            # Add skill <-> domain relationship (same directory)
            if len(parts) >= 3:
                parent_dir = parts[-2]
                path_slug = '-'.join(parts[:-1]).replace('/', '-').replace('\\', '-')
                if is_skill:
                    domain_id = f"domain-{path_slug}"
                    if domain_id in self.node_map:
                        self.edges.append(Edge(domain_id, node_id, 'derived_from', str(rel_path)))
                elif is_domain:
                    skill_id = f"skill-{path_slug}"
                    if skill_id in self.node_map:
                        self.edges.append(Edge(node_id, skill_id, 'derived_from', str(rel_path)))

        # Create nodes for empty directories if include_empty is True
        if self.include_empty:
            for dir_path in sorted(all_dirs):
                rel_parts = dir_path.replace('\\', '/').split('/')
                if len(rel_parts) == 0:
                    continue

                # Check if this directory already has skill or domain files
                full_dir_path = self.raw_dir / dir_path
                has_skill_or_domain = any(
                    f.name in ['skill.md', 'SKILL.md', 'domain.md']
                    for f in full_dir_path.iterdir()
                    if f.is_file()
                )

                if not has_skill_or_domain:
                    dir_name = rel_parts[-1]
                    path_slug = '-'.join(rel_parts).replace('/', '-').replace('\\', '-')
                    node_id = f"dir-{path_slug}"

                    if node_id not in self.node_map:
                        node = Node(
                            node_id=node_id,
                            label=dir_name,
                            node_type='empty_dir',
                            category=rel_parts[0] if len(rel_parts) > 1 else '',
                            subcategory=rel_parts[1] if len(rel_parts) > 2 else '',
                            skill_name=rel_parts[-2] if len(rel_parts) > 2 else rel_parts[0],
                            file_path=dir_path
                        )
                        node.description = '(Empty directory)'
                        self.nodes.append(node)
                        self.node_map[node_id] = node

    def add_keyword_edges(self):
        """Add semantic edges between skill and domain in same category."""
        # Group by category
        category_nodes = defaultdict(list)
        for n in self.nodes:
            if n.type in ('skill', 'domain') and n.category:
                category_nodes[n.category].append(n)

        # Track degree to limit edges per node
        degree = defaultdict(int)
        MAX_EDGES_PER_NODE = 4

        for category, nodes in category_nodes.items():
            skills = [n for n in nodes if n.type == 'skill']
            domains = [n for n in nodes if n.type == 'domain']
            
            for skill in skills:
                for domain in domains:
                    # Skip if same subcategory (already connected via derived_from)
                    if skill.subcategory and domain.subcategory and skill.subcategory == domain.subcategory:
                        continue
                    
                    # Connect skill with domains from other subcategories
                    if degree[skill.id] < MAX_EDGES_PER_NODE and degree[domain.id] < MAX_EDGES_PER_NODE:
                        self.edges.append(Edge(skill.id, domain.id, 'semantic_related'))
                        degree[skill.id] += 1
                        degree[domain.id] += 1

        # Add edges from category nodes to representative nodes
        for cat_id, cat_node in self.node_map.items():
            if cat_node.type == 'category':
                cat_nodes = [n for n in self.nodes if n.type in ('domain', 'skill') and n.category == cat_node.label]
                connections = 0
                for n in cat_nodes:
                    if connections >= 3 or degree[n.id] >= 4:
                        break
                    self.edges.append(Edge(cat_id, n.id, 'semantic_related'))
                    degree[cat_id] += 1
                    degree[n.id] += 1
                    connections += 1

    def assign_communities(self):
        """Assign communities based on category."""
        for n in self.nodes:
            n.community = n.category if n.category else 'Other'

    def write_graph_json(self):
        """Write graph.json."""
        graph = {
            'nodes': [n.to_dict() for n in self.nodes],
            'edges': [e.to_dict() for e in self.edges],
            'metadata': {
                'total_nodes': len(self.nodes),
                'total_edges': len(self.edges),
                'communities': list(set(n.community for n in self.nodes if n.community)),
                'generated_at': self._get_timestamp()
            }
        }

        output_path = self.output_dir / 'graph.json'
        output_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding='utf-8')

    def write_graph_html(self):
        """Write interactive graph.html using vis.js."""
        # Prepare data for vis.js
        # Calculate node degrees for sizing
        degree_map = defaultdict(int)
        for e in self.edges:
            degree_map[e.source] += 1
            degree_map[e.target] += 1

        edges_data = []
        for e in self.edges:
            edges_data.append({
                'from': e.source,
                'to': e.target,
                'label': '',  # Hide edge labels
                'arrows': 'to' if e.type == 'derived_from' else '',
                'color': {'color': '#F00' if e.type == 'derived_from' else '#888'},
                'width': 1.5 if e.type == 'derived_from' else 1.0
            })

        nodes_data = []
        for n in self.nodes:
            color_map = {
                'category': '#FF6B6B',
                'subcategory': '#4ECDC4',
                'domain': '#45B7D1',
                'skill': '#96CEB4',
                'empty_dir': '#DDDDDD'
            }
            
            # Size based on type (hierarchy level), not just degree
            base_size = {
                'category': 30,
                'subcategory': 22,
                'domain': 14,
                'skill': 14,
                'empty_dir': 10
            }.get(n.type, 12)
            
            nodes_data.append({
                'id': n.id,
                'label': n.label,
                'color': {'background': color_map.get(n.type, '#999'), 'highlight': color_map.get(n.type, '#999')},
                'font': {'size': 12 if n.type == 'category' else 11 if n.type == 'subcategory' else 10},
                'shape': 'dot',
                'size': base_size,
                'title': n.description[:100] if n.description else f'{n.type} ({n.label})',
                'frontmatter': n.frontmatter
            })

        html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>知識圖譜 - HJPLUS Taiwan Architect KB</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; height: 100vh; overflow: hidden; }}
        #left-panel {{ flex: 1; display: flex; flex-direction: column; }}
        #mynetwork {{ width: 100%; height: 100%; border: none; }}
        #legend {{ padding: 10px; background: #f5f5f5; display: flex; gap: 20px; flex-wrap: wrap; border-bottom: 1px solid #ddd; }}
        .legend-item {{ display: flex; align-items: center; gap: 5px; }}
        .legend-color {{ width: 15px; height: 15px; border-radius: 50%; }}
        #search {{ padding: 10px; background: #fff; border-bottom: 1px solid #ddd; }}
        #search input {{ padding: 8px 12px; width: 300px; border: 1px solid #ddd; border-radius: 4px; }}
        #side-panel {{
            width: 350px;
            background: #fff;
            border-left: 1px solid #ddd;
            overflow-y: auto;
            padding: 20px;
            display: none;
        }}
        #side-panel.active {{ display: block; }}
        #side-panel h2 {{ margin-bottom: 10px; font-size: 18px; color: #333; }}
        #side-panel .label {{ margin-bottom: 5px; }}
        #side-panel .label strong {{ display: inline-block; width: 80px; color: #666; }}
        #side-panel pre {{ background: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; font-size: 12px; }}
        #side-panel .close-btn {{ position: absolute; top: 10px; right: 10px; cursor: pointer; font-size: 20px; color: #999; }}
        #side-panel .close-btn:hover {{ color: #333; }}
        #side-panel .open-link {{ display: inline-block; margin-top: 10px; padding: 5px 10px; background: #4ECDC4; color: white; text-decoration: none; border-radius: 4px; }}
        #side-panel .open-link:hover {{ background: #3db5ab; }}
    </style>
</head>
<body>
    <div id="left-panel">
        <div id="search">
            <input type="text" id="searchInput" placeholder="搜尋知識圖譜..." oninput="searchNodes(this.value)">
        </div>
        <div id="legend">
            <div class="legend-item"><div class="legend-color" style="background:#FF6B6B"></div>類別 (Category)</div>
            <div class="legend-item"><div class="legend-color" style="background:#4ECDC4"></div>子類別 (Subcategory)</div>
            <div class="legend-item"><div class="legend-color" style="background:#45B7D1"></div>領域知識 (Domain)</div>
            <div class="legend-item"><div class="legend-color" style="background:#96CEB4"></div>技能萃取 (Skill)</div>
            <div class="legend-item"><div class="legend-color" style="background:#ddd"></div>空資料夾 (Empty)</div>
        </div>
        <div id="mynetwork"></div>
    </div>
    <div id="side-panel">
        <span class="close-btn" onclick="closeSidePanel()">&times;</span>
        <h2 id="panel-title"></h2>
        <div class="label"><strong>類型：</strong><span id="panel-type"></span></div>
        <div class="label" id="panel-desc-row"><strong>描述：</strong><span id="panel-description"></span></div>
        <div id="panel-frontmatter-row" style="margin-top: 15px;">
            <strong>Frontmatter：</strong>
            <pre id="panel-frontmatter"></pre>
        </div>
        <div class="label" id="panel-file-row" style="margin-top: 15px;"><strong>文件：</strong><span id="panel-file-path"></span></div>
    </div>
    <script>
        var nodes = new vis.DataSet({json.dumps(nodes_data)});
        var edges = new vis.DataSet({json.dumps(edges_data)});
        var container = document.getElementById('mynetwork');
        var data = {{ nodes: nodes, edges: edges }};
        var options = {{
            physics: {{
                enabled: true,
                barnesHut: {{
                    gravitationalConstant: -3000,
                    centralGravity: 0.3,
                    springLength: 95,
                    springConstant: 0.04,
                    damping: 0.09,
                    avoidOverlap: 0.3
                }},
                stabilization: {{
                    enabled: true,
                    iterations: 2000,
                    fit: true
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200,
                zoomView: true,
                dragView: true,
                dragNode: true,
                zoomSpeed: 0.3
            }}
        }};
        var network = new vis.Network(container, data, options);
        function searchNodes(query) {{
            var filteredIds = [];
            if (query) {{
                filteredIds = Array.from(nodes.getIds()).filter(function(id) {{
                    return nodes.get(id).label.toLowerCase().includes(query.toLowerCase());
                }});
            }}
            nodes.forEach(function(n) {{
                n.shade = !filteredIds || filteredIds.includes(n.id);
            }});
            nodes.update(nodes.get());
        }}
        network.on('click', function(params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var nodeData = nodes.get(nodeId);
                showSidePanel(nodeData);
            }} else {{
                closeSidePanel();
            }}
        }});
        function showSidePanel(nodeData) {{
            document.getElementById('panel-title').textContent = nodeData.label;
            document.getElementById('panel-type').textContent = nodeData.type;
            document.getElementById('panel-description').textContent = nodeData.title || '';
            document.getElementById('panel-description').parentElement.parentElement.style.display = (nodeData.title || '').trim() ? 'block' : 'none';
            var frontmatter = nodeData.frontmatter || {{}};
            var fmText = Object.keys(frontmatter).length > 0 ? JSON.stringify(frontmatter, null, 2) : '(無 frontmatter)';
            document.getElementById('panel-frontmatter').textContent = fmText;
            document.getElementById('panel-frontmatter-row').style.display = Object.keys(frontmatter).length > 0 ? 'block' : 'none';
            var filePath = nodeData.file_path || '';
            document.getElementById('panel-file-path').textContent = filePath || '(無文件)';
            document.getElementById('panel-file-row').style.display = filePath ? 'block' : 'none';
            document.getElementById('side-panel').classList.add('active');
        }}
        function closeSidePanel() {{
            document.getElementById('side-panel').classList.remove('active');
        }}
    </script>
</body>
</html>'''

        output_path = self.output_dir / 'graph.html'
        output_path.write_text(html, encoding='utf-8')

    def write_report_md(self):
        """Write GRAPH_REPORT.md."""
        # Calculate stats
        type_counts = defaultdict(int)
        community_members = defaultdict(list)
        node_degrees = defaultdict(int)

        for n in self.nodes:
            type_counts[n.type] += 1
            if n.community:
                community_members[n.community].append(n)

        for e in self.edges:
            node_degrees[e.source] += 1
            node_degrees[e.target] += 1

        # Find god nodes (highest degree)
        god_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)[:10]

        # Build report
        lines = []
        lines.append('# Knowledge Graph Report')
        lines.append('')
        lines.append(f'**Generated:** {self._get_timestamp()}')
        lines.append(f'**Total Nodes:** {len(self.nodes)}')
        lines.append(f'**Total Edges:** {len(self.edges)}')
        lines.append('')
        lines.append('---')
        lines.append('')
        lines.append('## Node Types')
        lines.append('')
        lines.append('| Type | Count |')
        lines.append('|------|-------|')
        for t in ['category', 'subcategory', 'domain', 'skill']:
            lines.append(f'| {t} | {type_counts.get(t, 0)} |')
        lines.append('')

        lines.append('---')
        lines.append('')
        lines.append('## God Nodes (Highest Degree)')
        lines.append('')
        lines.append('| Node | Degree |')
        lines.append('|------|--------|')
        for node_id, degree in god_nodes:
            node = self.node_map.get(node_id)
            if node:
                lines.append(f'| {node.label} | {degree} |')
        lines.append('')

        lines.append('---')
        lines.append('')
        lines.append('## Communities')
        lines.append('')
        for community_name, members in sorted(community_members.items()):
            lines.append(f'### {community_name}')
            lines.append('')
            lines.append('| ID | Label | Type |')
            lines.append('|----|-------|------|')
            for m in sorted(members, key=lambda x: x.label):
                lines.append(f'| `{m.id}` | {m.label} | {m.type} |')
            lines.append('')

        lines.append('---')
        lines.append('')
        lines.append('## Suggested Questions')
        lines.append('')
        lines.append('1. What connects different categories in this knowledge base?')
        lines.append('2. How are domain knowledge and skill extraction related?')
        lines.append('3. What are the most interconnected concepts in each community?')
        lines.append('4. Which skills are derived from which domain knowledge?')
        lines.append('')

        output_path = self.output_dir / 'GRAPH_REPORT.md'
        output_path.write_text('\n'.join(lines), encoding='utf-8')

    def _get_timestamp(self):
        from datetime import datetime, timezone
        utc_now = datetime.now(timezone.utc)
        return utc_now.strftime('%Y-%m-%d %H:%M UTC')


# ============================================================
# Main
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='Turn a folder of markdown files into a knowledge graph.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python graphify.py ./raw -o ./graphify-out
  python graphify.py ./my-docs
  python graphify.py ./raw -o ./graphify-out --exclude Skills-Architects
  python graphify.py ./raw -o ./graphify-out --include-empty
'''
    )
    parser.add_argument('raw_dir', help='Path to folder containing markdown files')
    parser.add_argument('-o', '--output', default='./graphify-out', help='Output directory (default: ./graphify-out)')
    parser.add_argument('--no-visual', action='store_true', help='Skip generating graph.html')
    parser.add_argument('--json-only', action='store_true', help='Only generate graph.json')
    parser.add_argument('--exclude', nargs='+', help='Exclude specific directories')
    parser.add_argument('--include-empty', action='store_true', help='Include empty directories')

    args = parser.parse_args()

    raw_path = Path(args.raw_dir)
    if not raw_path.exists():
        print(f'Error: {raw_path} does not exist')
        sys.exit(1)

    builder = KnowledgeGraphBuilder(
        str(raw_path),
        args.output,
        exclude_dirs=[e.split('/') for e in args.exclude] if args.exclude else [],
        include_empty=args.include_empty
    )
    builder.build()

    if args.json_only:
        print('JSON only mode - skipping HTML and report')


if __name__ == '__main__':
    main()
