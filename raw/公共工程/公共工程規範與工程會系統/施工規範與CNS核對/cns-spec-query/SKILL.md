---
name: cns-spec-query
description: "This skill should be used when verifying CNS (Chinese National Standards) on public engineering drawings or querying PCC (Public Construction Commission) guide specifications."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
---

# CNS and Specification Query

## Overview
This skill outlines the process of querying and verifying Chinese National Standards (CNS) and Public Construction Commission (PCC) guide specifications for public works in Taiwan.

## Execution Steps
1. **Identify Specification Chapters:** Check the project drawings or requirements to find the target PCC specification chapters (e.g., Chapter 09910 for Painting).
2. **Search CNS Standards:** Use the CNS Online Service to verify that the cited CNS standards are active and represent the latest editions.
3. **Download PCC Specifications:** Access the PCC official portal or use integration tools to fetch the required XML/PDF specification templates.
4. **Coordinate Drawings & Specifications:** Ensure the descriptions of materials and testing methods on the design drawings align with the updated CNS and PCC standards.

## Requirements & Constraints
- Region: Taiwan (ROC)
- Reference Database: National Standard Search System (CNS: https://www.cnsonline.com.tw/), PCC Official Portal (https://pcic.pcc.gov.tw/pwc-web/)

## Examples
Example tool call (if tools are available):
```
pcc-downloader_download_specification(chapter="09", keyword="09910", format="pdf")
```

## Additional Resources
- For more information on Taiwan's public engineering rules, see [domain.md](../domain.md)
