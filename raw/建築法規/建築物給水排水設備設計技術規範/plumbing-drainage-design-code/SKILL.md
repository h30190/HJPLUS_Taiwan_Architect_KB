---
name: plumbing-drainage-design-code
description: "This skill should be used when reviewing or calculating building water supply, hot water, and drainage/ventilation designs according to Taiwan's Technical Code for Building Plumbing and Drainage Equipment Design (建築物給水排水設備設計技術規範). It covers sizing water tanks and booster pumps, cold/hot water piping, Hunter fixture units (WSFU), drainage pipe slopes, trap seals (5-10cm), vent piping (stack/individual/loop/relief/yoke/AAV), grease interceptors, cleanout intervals, and same-floor drainage (同層排水)."
license: CC-BY-SA-4.0
compatibility: claude-code,opencode,agent-skills
metadata:
  audience: architects
  region: taiwan
  class: C
  status: verified
  data-currency: "2026-07-24"
---

# Building Plumbing and Drainage Equipment Design Code

## Overview
This skill provides technical design and compliance evaluation procedures for building cold/hot water supply systems, drainage systems, ventilation piping, trap seal protection, cleanouts, same-floor drainage, and grease interceptors in Taiwan. It is based on Taiwan's official *Technical Code for Building Plumbing and Drainage Equipment Design* (建築物給水排水設備設計技術規範, per Building Technical Regulations Equipment Code Article 26).

Use this skill when:
- Designing or auditing water storage tank capacities (受水槽, 屋頂水塔) and maintenance clearances.
- Sizing water supply pipes using Water Supply Fixture Units (WSFU) and verifying pressure limits (0.3–3.5 kg/cm²).
- Calculating drainage pipe diameters (DFU) and minimum slopes (1/50 for 30~65mm, 1/100 for 75~100mm, 1/200 for ≥150mm).
- Checking trap seal depth (5–10 cm), avoiding double trapping, and reviewing same-floor drainage (同層排水).
- Verifying cleanout intervals (≤15m for ≤100mm, ≤30m for ≥125mm) and operating clearance (30–45 cm).
- Configuring vent systems (stack, individual, loop, yoke, relief, wet vent, AAV) and roof termination heights.
- Selecting and sizing manufactured grease interceptors (油脂截留器) per Appendix formulas.

## Execution Steps

1. **Step 1: Water Supply System Audit (§3.1 – §3.2, Appendix 1)**
   - Determine total daily water consumption based on building occupancy and per-capita demand table (Appendix 1.1).
   - Verify storage tank volumes (§3.2.3):
     - Receiving tank (受水槽): $\ge 2/10$ of daily demand (typically 0.5 day).
     - Elevated roof tank (屋頂水塔): $\ge 1/10$ of daily demand.
     - Combined storage volume: $4/10 \le V_{\text{total}} \le 2.0$ days of daily demand.
   - Inspect tank physical clearances (§3.2.1 – §3.2.2):
     - Double-wall requirement: Tank walls/slab **must not be shared with building structural walls/slabs**.
     - Maintenance clearances: Side clearance $\ge 60\text{ cm}$ (or $\ge 45\text{ cm}$ near structural columns); top manhole and top slab clearance $\ge 60\text{ cm}$ (§3.2.2, §3.2.2(3)); bottom-to-slab clearance $\ge 20\text{ cm}$ (§3.2.2(4)) with a drainage sump.
     - Sloped bottom $\ge 1/50$ toward drainage outlet.
     - Air gap for water inlet $\ge 50\text{ mm}$ or $\ge 1 \times \text{pipe diameter}$ above overflow level (§3.2.6).
   - Check pressure & velocity limits (§3.1.3, §3.4.4):
     - Minimum residual pressure at fixtures: $0.3\text{ kg/cm}^2$ ($30\text{ kPa}$), or $1.0\text{ kg/cm}^2$ for direct flush valves.
     - Maximum fixture pressure: $3.5\text{ kg/cm}^2$ ($350\text{ kPa}$) — install pressure reducing valves (PRVs) if exceeded.
     - Maintain proper flow velocity in pipes to prevent water hammer and noise.

2. **Step 2: Drainage & Vent System Sizing (§4.1 – §4.3, Appendix 3)**
   - Calculate Drainage Fixture Units (DFU) for horizontal branches, stacks, and building drain.
   - Verify minimum pipe slopes (§4.2.3):
     - Pipe diameter $D = 30\text{--}65\text{ mm}$: Slope $\ge 1/50$ (2%).
     - Pipe diameter $D = 75\text{--}100\text{ mm}$: Slope $\ge 1/100$ (1%).
     - Pipe diameter $D \ge 150\text{ mm}$: Slope $\ge 1/200$ (0.5%).
   - Verify horizontal branch length $\le 12\text{ m}$ and maximum 4 bends to ensure solids conveyance (§4.2.16).
   - Verify trap seal depth (§4.4.4): $5.0\text{ cm} \le D_{\text{seal}} \le 10.0\text{ cm}$ ($50\text{–}100\text{ mm}$). Distance from fixture outlet to trap weir $\le 60\text{ cm}$ (§4.4.3). Check for prohibited double traps.
   - Check cleanout placements (§4.5):
     - Maximum interval: $\le 15\text{ m}$ for pipe $D \le 100\text{ mm}$; $\le 30\text{ m}$ for pipe $D \ge 125\text{ mm}$.
     - Required at branch origins, direction changes $> 45^\circ$, stack bases, and building drain connections.
     - Clearance around cleanout: $\ge 45\text{ cm}$ for $D \ge 75\text{ mm}$; $\ge 30\text{ cm}$ for $D < 75\text{ mm}$.

3. **Step 3: Ventilation System Verification (§4.3)**
   - Stack vent (伸頂通氣管): Height above roof $\ge 15\text{ cm}$ ($\ge 1.5\text{ m}$ if roof is accessible/garden/terrace) (§4.3.8).
   - Individual vent (個別通氣管): Diameter $\ge 1/2 \times D_{\text{drain}}$ and $\ge 30\text{ mm}$ (§4.3.2).
   - Loop/Circuit vent (環狀通氣管): Recommended when serving $\ge 8$ fixtures (or $\ge 3$ water closets) per loop (§4.3.12).
   - Yoke vent (結合通氣管): Required every 10 branch intervals/floors for stacks serving $\ge 10$ branches (§4.3.14). Connected below the branch line on the drainage stack, terminating $\ge 90\text{ cm}$ above floor level on the vent stack.
   - Air Admittance Valve (AAV, 吸氣閥): Must be CNS/ISO certified; installed $\ge 15\text{ cm}$ above the flood level rim of the highest served fixture (§4.3.16).

4. **Step 4: Grease Interceptor Sizing (§4.6, Appendix 5)**
   - Required for commercial kitchens, restaurants, food preparation areas (§4.6.2).
   - Determine effective volume $V$ (Liters) based on dining area ($m^2$) or meal count per Appendix formulas. Ensure trap seal depth $5\text{--}20\text{ cm}$ on outlet and provide gas-tight cover (§4.6.3).

---

## Requirements & Constraints
- **Standards Basis**: Taiwan Technical Code for Building Plumbing and Drainage Equipment Design (建築物給水排水設備設計技術規範) & CNS national standards.
- **Unit System**: Metric (mm, cm, m, kg/cm², L/min, m/s).
- **Prohibited Configurations**:
  - No direct connection between potable water and non-potable/drainage systems (cross-connection).
  - No sharing of water tank walls/slabs with building structure (double-wall mandatory).
  - No double trapping (雙重存水彎).
  - No direct pumping from municipal water mains.

---

## Worked Example

### Example 1: Water Tank Volume & Booster Pump Calculations
**Scenario**: An 8-story residential building with 32 units, 4 occupants per unit ($N = 128$ occupants). Daily water consumption benchmark $q = 250\text{ L/person/day}$.

1. **Daily Total Demand ($Q_d$)**:
   $$Q_d = 128 \times 250 = 32,000\text{ Liters/day} = 32\text{ m}^3\text{/day}$$
2. **Receiving Tank Volume ($V_{\text{rcv}}$)** per §3.2.3:
   $$V_{\text{rcv}} = 0.5 \times Q_d = 16\text{ m}^3 \quad (\text{meets }\ge 2/10 = 6.4\text{ m}^3\text{ minimum})$$
3. **Roof Tank Volume ($V_{\text{roof}}$)** per §3.2.3:
   $$V_{\text{roof}} = 0.2 \times Q_d = 6.4\text{ m}^3 \quad (\text{meets }\ge 1/10 = 3.2\text{ m}^3\text{ minimum})$$
4. **Combined Storage Check**:
   $$V_{\text{total}} = 16 + 6.4 = 22.4\text{ m}^3 = 0.70 \times Q_d \quad (\text{within requirement } 0.4 \le V/Q_d \le 2.0)$$
5. **Physical Space Clearance Verification** (§3.2.2):
   - Side maintenance space: $60\text{ cm}$ minimum surrounding all 4 sides.
   - Bottom-to-slab clearance: $30\text{ cm}$ ($> 20\text{ cm}$ min) on concrete pedestals with sump.
   - Top manhole and top-to-ceiling clearance: $60\text{ cm}$ minimum (§3.2.2, §3.2.2(3)).

### Example 2: Horizontal Drainage Branch Sizing & Cleanout Check
**Scenario**: A commercial floor drainage horizontal branch serving 6 water closets (6 DFU each) and 4 lavatories (1 DFU each). Total $\text{DFU} = 6 \times 6 + 4 \times 1 = 40\text{ DFU}$. Total branch length $L = 14\text{ m}$.

1. **Pipe Diameter & Slope Selection** (§4.2.3, Appendix 3.1):
   - For $40\text{ DFU}$ horizontal branch, required nominal pipe size is $100\text{ mm}$ ($4"$).
   - For $D = 100\text{ mm}$, mandatory minimum slope is **1/100 (1.0%)**.
2. **Cleanout Spacing Verification** (§4.5.1):
   - For $D = 100\text{ mm}$, maximum allowed cleanout spacing is $15\text{ m}$.
   - Since branch length $L = 14\text{ m} \le 15\text{ m}$, a cleanout at the branch origin + end of line is compliant.
   - Cleanout operating clearance (§4.5.3): $45\text{ cm}$ clear space around the $100\text{ mm}$ cleanout cover.

---

## Common Pitfalls

### Pitfall: Shared Wall/Slab for Underground Water Storage Tank
- **Severity**: 🔴 Rejection risk (Permit & Health Inspection failure)
- **When it bites**: Architectural schematic design & structural plan review.
- **Wrong**: Utilizing the building basement perimeter RC wall or foundation slab directly as the water tank boundary wall.
- **Right**: Construct independent double walls/slabs with $\ge 60\text{ cm}$ side clearance ($\ge 45\text{ cm}$ near columns) and $\ge 20\text{ cm}$ bottom clearance per §3.2.1 & §3.2.2.

### Pitfall: Insufficient Slope on $75\text{ mm}$ Drainage Piping
- **Severity**: 🔴 Rework risk & clogging during occupancy
- **When it bites**: Mechanical/Plumbing shop drawing review & site installation.
- **Wrong**: Applying 1/100 (1%) slope indiscriminately to all pipe sizes including $50\text{ mm}$ branch lines.
- **Right**: Enforce $\ge 1/50$ (2%) slope for pipe diameters $30\text{--}65\text{ mm}$, 1/100 (1%) for $75\text{--}100\text{ mm}$, and 1/200 (0.5%) only for $D \ge 150\text{ mm}$ per §4.2.3.

### Pitfall: Double Trapping on Sanitary Appliances
- **Severity**: 🟡 Rework risk (Slow drainage & air locking)
- **When it bites**: Interior design & plumbing fixture installation.
- **Wrong**: Installing an external S/P trap underneath a water closet or fixture that already incorporates an integral internal trap.
- **Right**: Omit external trap if the fixture has an integral trap. Maintain trap seal depth between $5\text{ cm}$ and $10\text{ cm}$ per §4.4.2 & §4.4.4.

### Pitfall: Vent Connection Below Fixture Flood Level Rim
- **Severity**: 🔴 Contamination risk
- **When it bites**: Plumbing riser diagram review & piping installation.
- **Wrong**: Tapping horizontal vent pipe below the flood level rim of the highest served fixture.
- **Right**: Elevate all vent connections to $\ge 15\text{ cm}$ above the flood level rim of the highest fixture before turning horizontally per §4.3.4.

---

## AI Design Check Table

| Check | Condition | AI Action |
|---|---|---|
| Water Tank Structure | Tank wall/slab shared with building structure | ERROR: Violation of §3.2.1 & §3.2.2. Water tanks must have independent walls with $\ge 60\text{ cm}$ side clearance and $\ge 20\text{ cm}$ bottom clearance. |
| Water Tank Volume | Receiving tank volume $< 0.2 \times Q_d$ or total storage $< 0.4 \times Q_d$ | ERROR: Violation of §3.2.3. Minimum receiving tank volume is $2/10$ of daily demand; combined storage must be $4/10 \le V/Q_d \le 2.0$. |
| Supply Water Pressure | Residual fixture pressure $< 0.3\text{ kg/cm}^2$ or max pressure $> 3.5\text{ kg/cm}^2$ | ERROR: Violation of §3.4.4 & §3.4.6. Pressure must be $0.3\text{--}3.5\text{ kg/cm}^2$. Install booster pump or PRV. |
| Drainage Pipe Slope | Slope $< 1/50$ for $D \le 65\text{ mm}$, or $< 1/100$ for $D = 75\text{--}100\text{ mm}$ | ERROR: Violation of §4.2.3. Slope must be $\ge 1/50$ for $D \le 65\text{ mm}$ and $\ge 1/100$ for $D = 75\text{--}100\text{ mm}$. |
| Trap Seal Depth | Water seal depth $< 5\text{ cm}$ or $> 10\text{ cm}$ | ERROR: Violation of §4.4.4. Trap seal depth must be between $5.0\text{ cm}$ and $10.0\text{ cm}$. |
| Cleanout Spacing | Cleanout interval $> 15\text{ m}$ for pipe $D \le 100\text{ mm}$ | ERROR: Violation of §4.5.1 & §4.5.3. Cleanout spacing for pipe $\le 100\text{ mm}$ must not exceed $15\text{ m}$. |
| Stack Vent Roof Clearance | Stack vent height above roof $< 15\text{ cm}$ ($< 1.5\text{ m}$ for accessible roof) | ERROR: Violation of §4.3.8. Stack vent termination must be $\ge 15\text{ cm}$ above non-accessible roof or $\ge 1.5\text{ m}$ for accessible roof. |
| Yoke Vent Provision | Drainage stack serves $\ge 10$ branch intervals without yoke vents | ERROR: Violation of §4.3.14. Yoke vents are required every 10 branch intervals for stacks serving 10+ floors. |
| Grease Interceptor | Commercial kitchen/restaurant without grease trap | ERROR: Violation of §4.6.2. Food preparation wastewater must pass through a certified grease interceptor before discharge. |

---

## Data Currency
- Source: *Technical Code for Building Plumbing and Drainage Equipment Design* (建築物給水排水設備設計技術規範, Ministry of the Interior / National Land Management Agency).
- Verified: 2026-07-24 (Current effective technical regulation in Taiwan).
- Volatility: LOW (National technical codes update via official MOI amendments).

---

## To Verify
- [ ] Verify local municipal sewerage connection rules (e.g., Taipei City vs New Taipei City vs Taichung) for direct discharge vs combined septic tank connection.

---

## MCP Tool Examples

```python
# Search Taiwan building code database for plumbing regulations
taiwan-building-code_search_building_code(query="建築物給水排水設備設計技術規範", limit=10)

# Search official interpretations regarding trap seal or water tank clearances
taiwan-building-code_search_building_interpretations(query="受水槽維修空間 雙層牆")
```

---

## Related Skills
- [taiwan-stair-railing-ramp](../../建築技術規則/建築設計施工編/樓梯欄杆坡道/taiwan-stair-railing-ramp/SKILL.md) — Architectural space and clearance compliance in utility and equipment rooms
- [generator-room-fire-safety](../../消防安全/generator-room-fire-safety/SKILL.md) — MEP equipment room clearances and fire safety provisions
