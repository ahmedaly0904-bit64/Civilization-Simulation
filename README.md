# Project Omran — عُمران
### Civilization Simulation

> *"To simulate how shared ideas shape the rise and fall of civilizations —*
> *translating Ibn Khaldun's theory of Asabiyyah into computational physics."*

> [!WARNING]
> **Document status:** verified against actual `src/` on **25 August 2026**.
> Claims that were not present in the code have been removed. Every equation below
> **exists in the code** unless explicitly marked otherwise.

---

## Why Omran?

Named after Ibn Khaldun's concept of *'ilm al-'umran* — the systematic study
of civilization, urbanization, and social organization.

This project asks a simple but profound question:

> **How does a civilization rise — and why does another one collapse?**

The answer, according to Ibn Khaldun, lies not only in resources and armies —
but in **ideas** and **social cohesion (Asabiyyah)**. This simulation translates
that theory into equations and code.

---

## What the Code Does Right Now

Four forces drive every civilization in the simulation:

- **Population** — grows logistically via RK4, collapses under famine
- **Food** — produced each year with weather randomness, consumed by population
- **Territory** — spreads across a 2D NumPy grid, contested by warfare
- **Ideas** — an SIR model inside each nation (S / I / R compartments)

Civilizations expand into empty cells until they meet. Where two nations touch,
both take attrition damage proportional to the shared border length.
Nations may also declare war on a neighbor if they outnumber it.

---

## Project Structure

```
omran/
├── src/
│   ├── functions.py   # RK4 solver + stochastic growth — pure math
│   ├── traits.py      # Traits — SIR fractions (s/i/r summing to 1.0)
│   ├── nation.py      # Nation — population, food, warfare, famine
│   ├── grid.py        # WorldGrid — spatial map, neighbors, spread, borders
│   ├── world.py       # WorldModel — orchestrator, runs the yearly loop
│   ├── main.py        # Entry point — creates nations, runs, renders Plotly
│   └── asabiyyah.py   # EMPTY (0 bytes) — placeholder, not implemented
├── MVP/               # v1 — Jupyter notebook, Mesa + Matplotlib (reference)
└── README.md
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| NumPy | Spatial grid and vectorized operations |
| Plotly | Interactive heatmap and population charts |

> No game engines. No ABM frameworks. Pure Python + Math.

---

## Architectural Decisions

**Dependency Injection**
`WorldModel` does not create nations internally.
Nations are defined in `main.py` and passed in as a parameter.
The engine is decoupled from the scenario.

**Single Source of Truth — Spatial Data**
Nations have no `x` or `y` attributes.
`WorldGrid` owns the `ownership` array and is the only place that knows
where any civilization is.

**Spatial Logic Belongs in the Grid**
`get_neighbors()` lives in `WorldGrid`.
It queries the `ownership` array via `np.where` instead of comparing
coordinate attributes on Nation objects.

**Combat SRP**
`WorldGrid` does not modify population directly.
It calls `nation.border_attrition(border_length)` — passing a *spatial fact*
and letting the Nation translate it into its own demographic response.

**Border Length Scaling**
Attrition is aggregated **once per nation-pair** using `defaultdict` +
`frozenset`, not per-cell. This was the fix for the Phase-3 mass-extinction bug.

**Population Changes Funnel Through One Control Point**
Every path that changes population — growth, famine, war, attrition —
goes through `Nation.change_populations()`. Its body is a single line today;
its value is being the one place where a population rule can be enforced.

**Ideas Are Fractions, Not Head-counts**
`Traits` stores `s`, `i`, `r` as fractions constrained by `s + i + r == 1.0`,
enforced inside the class by `_check()`. `Nation` owns the head-count and never
writes to `Traits`; births and deaths do not touch the composition at all.
This removed an entire class of integer-rounding drift rather than patching it.

**Output is Not the Engine's Problem**
`print_summary()` lives in `main.py`. The engine returns data.

---

## Technical Principles

### Population Growth — implemented

```
dP/dt = r × P × (1 − P/K)
```

Solved via RK4 each step (`functions.solve_rk4`). Integer population is
recovered via a Monte Carlo step (`stochastic_growth`) to avoid float drift.

### Food & Famine — implemented

```
consumption = population × CONSUMPTION_PER_PERSON
production  = food_production × uniform(0.8, 1.2)
```

If food goes negative, deaths scale with the per-person deficit
and `famine_count` increments.

### Warfare — implemented

Two independent mechanisms:

**1. Declared war** (`Nation._attempt_warfare`)
With probability `WARFARE_PROBABILITY`, a nation picks a random living
neighbor. It attacks **only if it has more people**. Both sides take losses
(`ENEMY_DAMAGE` = 0.1, `ATTACKER_DAMAGE` = 0.04).

**2. Border attrition** (`WorldGrid.spread` → `Nation.border_attrition`)
Every pair of touching nations loses population each year:

```
damage = min(0.5, 0.2 × border_length / population)
```

### Idea Spread — implemented

An SIR model over fractions. Each year a nation's force of infection is summed
over its **grid neighbours only**, then applied once:

```
λ  = Σ over neighbours of  β × i_neighbour      β = IDEA_TRANSMISSION_RATE = 0.05
s -= min(1, λ) × s                              (moved into i)
i -= γ × i                                      γ = RECOVERY_RATE = 0.1  (moved into r)
```

`Traits` holds `_S`, `_I`, `_R` privately with read-only properties, and
`_check()` enforces `s + i + r == 1.0` after every transfer.

Because the sum is gathered before it is applied, the result no longer depends
on the order nations are iterated in — a two-phase update, the same pattern
`WorldGrid.spread()` uses with its `ownership.copy()`.

The initial carrier is a **scenario** decision, not an engine one:
`main.py` calls `random.choice(nations).idea.infect(0.01)` before the run.
Without it the model is mathematically correct but completely inert.

### Territorial Expansion — **NOT implemented as documented**

> [!CAUTION]
> **This equation does not run.**
> ```
> spread_rate = population / carrying_capacity      ← dead code
> ```
> `spread_rate` is computed in `grid.py` lines 54–55 and **never used anywhere**.
>
> Actual behavior: every nation expands into every adjacent empty cell each year
> at maximum speed, regardless of its population. Demography has **no effect**
> on territorial expansion.
>
> This is the first item on the fix list.

---

## Development Phases

| Phase | Description | Status |
|---|---|---|
| 1 | Core OOP — Nation, World, Grid, Traits | ✅ |
| 2 | Visualization — Plotly heatmap + population curves | ✅ |
| 3 | Spatial Environment — NumPy grid + spread + borders | ⚠️ partial |
| 4 | Economy — Resources | ⚠️ partial |
| 5 | Interaction — Conflict / Trade | ⚠️ partial |
| 6 | Advanced Logic — AI | ⏳ |

**Why "partial":**

- **3** — grid, expansion and borders work, but `spread_rate` is dead code (see above)
- **4** — food, production and famine exist inside `Nation` since Phase 1. No trade, no market, no shared stock
- **5** — conflict is done (war + border attrition). Trade has not started

---

## What's Coming

**Asabiyyah (العصبية)**

`asabiyyah.py` exists but is empty (0 bytes). The design is **still an open question**.

Decided so far (from Dr. Zeinab Boumehdi's paper, 2020):

- Asabiyyah is **generational, not contagious** — an internal property, strongest at
  founding and weakening over time. It is not transmitted between nations like the SIR model.
- Its combat effect applies in `border_attrition()` only, not in `receive_damage()`,
  to avoid double-counting.
- Affluence = `population / carrying_capacity`.

The earlier equation `dA/dt = -0.01 × (1 - idea_strength)` is **rejected** — it was an
early proposal made before asabiyyah was determined to be generational.

---

## Intellectual Lineage

- **Ibn Khaldun** — *Muqaddimah* (1377) — Asabiyyah and civilizational cycles
- **Peter Turchin** — *Cliodynamics* — Mathematical modeling of historical dynamics
- **Thomas Malthus** — Population and resource limits
- **د. زينب بومهدي (2020)** — *مفهوم العصبية ونشأة الدولة في الفكر الخلدوني*

---

*Developed as a personal project in computational physics and complex systems.*

*Copyright 2026 Ahmed. All rights reserved.*
