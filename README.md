![CVXlab Logo](https://raw.githubusercontent.com/cvxlab/cvxlab/main/docs/source/_static/CVXlab_logo_dark.png)

[![PyPI version](https://img.shields.io/pypi/v/cvxlab?label=PyPI&logo=pypi)](https://pypi.org/project/cvxlab/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cvxlab)](https://pypi.org/project/cvxlab/)
[![Documentation Status](https://readthedocs.org/projects/cvxlab/badge/?version=latest)](https://cvxlab.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20644006.svg)](https://doi.org/10.5281/zenodo.20644006)

CVXlab is an open-source Python laboratory for modeling and solving convex optimization problems. 
It extends [cvxpy](https://www.cvxpy.org/) with user-friendly interfaces, integrated data 
management and support for multiple, interconnected optimization models.

## Table of Contents
- [Installation](#installation)
- [Package Overview](#package-overview)
- [Quick Start](#quick-start)
- [Guided Interface](#guided-interface)
- [Documentation](#documentation)
- [Changelog](#changelog)
- [Contributing](#contributing)
- [Community & Support](#community--support)
- [License](#license)
- [Citing](#citing)

## Installation
**From PyPI**
```bash
pip install cvxlab
```
**From source (for development):**
```bash
git clone https://github.com/cvxlab/cvxlab.git
cd cvxlab
pip install -e .[dev]
```
See the [Installation Guide](https://cvxlab.readthedocs.io/en/latest/installation.html) 
for detailed instructions.

## Package Overview
CVXlab allows you to define optimization problems using:
- **General-purpose model generator**: Model problems as you would mathematically, without restrictive solver forms.
- **Almost no-code required**: Build models using Excel or YAML—no coding required.
- **Centralized data management**: Centralized data input/output via SQLite database.
- **Multi-Model Support**: Generate and solve multiple parallel, sequential, or integrated optimization problems.
- **Powerful engine embedded**: Built on cvxpy package, leveraging its extensive solver support.

**Typical workflow:**

The figure below provides a synthetic and simplified overview of the CVXlab modeling 
process.

![CVXlab workflow](https://raw.githubusercontent.com/cvxlab/cvxlab/main/docs/source/_static/CVXlab_nutshell.png)

In generating and handling a CVXlab model, the user must follow the five fundamental
activities summarized below:

- The user **defines the model settings** and the related structure: model scope, 
  structure of variables, and list of mathematical expressions, including equalities,
  inequalities and (eventually) objective function. This activity requires almost no
  coding, as model definition can be performed via Excel files or YAML configuration 
  files.
- The user proceeds by **generating a CVXlab Model object**, consisting in a *Python* 
  class instance embedding all the model settings and the methods useful to manage 
  the model. At the same time, other items are generated, including the **SQLite 
  database file** (to store all model data), and the Excel files serving as blank 
  templates for collecting exogenous data from the user. 
- The user **feeds input data** to SQLite database through blank Excel template 
  files. Specifically, user defines the data input required to characterize exogenous 
  model variables.
- The **numerical problem is generated**, exogenous data fetched from the database, 
  and the problem is solved through CVXPY engine.
- If problem is successfuly solved, **results are finally exported** to the database.
  Due to the structure of the relational database, it can be easily linked and 
  inspected via Excel or SQL queries, or imported into Business Intelligence tools 
  (such as *PowerBI* or *Tableau*) for more elaborated data visualization and analysis.

## Quick Start

This small model is deliberately abstract, but it uses the same workflow that
scales to larger applications: model structure is separate from numerical data,
one problem is generated for each scenario, and results are stored in SQLite.

For each scenario $s$, solve the following independent problem in vector form:

$$
\begin{aligned}
\text{maximize}\quad & c x^{\mathsf{T}} \\
\text{subject to}\quad & e x^{\mathsf{T}} \leq E_{\text{max}}, \\
& m x^{\mathsf{T}} \leq M_{\text{max}}, \\
& x \geq 0.
\end{aligned}
$$

Here $x$, $c$, $e$, and $m$ are row vectors over products: production,
unit profit, energy requirements, and material requirements, respectively.
The scalars $E_{\text{max}}$ and $M_{\text{max}}$ are energy
and material availability. Non-negativity applies to every component of $x$.
In the YAML below, `@` denotes matrix multiplication and `tran(x)` denotes
the transpose. CVXlab handles the scenario index automatically.

The model has two products, two resources, and two scenarios. Its size is small;
its structure--separate data, indexed variables, scenarios, and persistent
results--is the same used by a larger CVXlab model.

Product 1 uses less energy, while product 2 uses less material. Energy availability
changes across scenarios; material availability stays fixed. Filtered variables
`e` and `m` select energy and material coefficients from the same data table.
Energy availability is `E_max`; material availability is `M_max`.

### 1. Create the model directory

```python
import cvxlab

cvxlab.create_model_dir(
    model_dir_name="quick_start",
    main_dir_path=".",
    settings_file_type="yml",
)
```

This creates `quick_start/` with three YAML files. Replace their template
content with the definitions below.

`structure_sets.yml`

```yml
Products:
    description: products whose optimal production volumes are to be determined | dimension set

Resources:
    description: resources consumed in production | dimension set
    filters:
        type: [energy, material]

Scenarios:
    description: alternative resource-availability conditions | inter-problem set
    split_problem: True
```

`structure_variables.yml`

```yml
production:
    description: production volumes to be determined
    type: endogenous
    coordinates: [Products, Scenarios]
    variables_info:
        x:
            Products:
                dim: cols

unit_profit:
    description: profit earned per unit of each product
    type: exogenous
    coordinates: [Products]
    variables_info:
        c:
            Products:
                dim: cols

resource_requirements:
    description: resource consumption required to produce one unit of each product
    type: exogenous
    coordinates: [Resources, Products]
    variables_info:
        e:
            Resources:
                dim: rows
                filters: {type: energy}
            Products:
                dim: cols
        m:
            Resources:
                dim: rows
                filters: {type: material}
            Products:
                dim: cols

energy_availability:
    description: available energy in each scenario
    type: exogenous
    coordinates: [Resources, Scenarios]
    variables_info:
        E_max:
            Resources:
                dim: rows
                filters: {type: energy}

material_availability:
    description: available material shared by all scenarios
    type: exogenous
    coordinates: [Resources]
    variables_info:
        M_max:
            Resources:
                dim: rows
                filters: {type: material}

```

`problem.yml`

```yml
objective:
    - Maximize(c @ tran(x))

expressions:
    - e @ tran(x) <= E_max
    - m @ tran(x) <= M_max
    - x >= 0

description:
    - maximize total profit
    - respect energy availability in each scenario
    - respect material availability shared by all scenarios
    - define non-negative production volumes
```

### 2. Create the model and fill its sets

```python
model = cvxlab.Model(
    model_dir_name="quick_start",
    main_dir_path=".",
    model_settings_from="yml",
)
```

The constructor creates `quick_start/sets.xlsx`. In that workbook, fill the
`*_Name` column in each sheet with one coordinate per row:

| Sheet | Coordinates |
| --- | --- |
| `_set_PRODUCTS` | `product_1`, `product_2` |
| `_set_RESOURCES` | `resource_1`, `resource_2` |
| `_set_SCENARIOS` | `low`, `high` |

In `_set_RESOURCES`, also fill the generated `Resources_type` column: enter
`energy` for `resource_1` and `material` for `resource_2`. These labels select
the rows used by `e`, `m`, `E_max`, and `M_max`. Save and close the workbook before continuing.

### 3. Generate and fill the numerical input data

```python
model.initialize_model_environment()
```

This creates `quick_start/input_data/input_data.xlsx`. In that workbook, leave
all coordinate and `id` columns unchanged and fill only the `values` column. Use
these values, matching the generated rows by their coordinate columns:

| Sheet | Coordinates | `values` |
| --- | --- | ---: |
| `unit_profit` | `product_1`; `product_2` | 3; 5 |
| `resource_requirements` | `(resource_1, product_1)`; `(resource_1, product_2)`; `(resource_2, product_1)`; `(resource_2, product_2)` | 1; 2; 3; 1 |
| `energy_availability` | `(resource_1, low)`; `(resource_1, high)` | 2; 8 |
| `material_availability` | `resource_2` | 6 |

`E_max` selects only the energy rows of `energy_availability`; `M_max` selects
only the material row of `material_availability`. Fill unused rows with 0;
they do not enter the constraints. Material availability has no scenario dimension.
Save and close the workbook before solving.

### 4. Solve and inspect the results

```python
model.refresh_database_and_initialize_problem()
model.run_model(solver="CLARABEL")
model.load_results_to_database()

for scenario_key, scenario in model.scenarios.iterrows():
    print(f"\nScenario: {scenario.iloc[0]}")
    print(model.variable(name="x", scenario_key=scenario_key).round(2))
```

`model.variable()` returns the optimal production volumes as a DataFrame
for each scenario. The results are also exported to the `production` table
in `quick_start/database.db`.

Expected production volumes (up to solver tolerances):

| Scenario | `product_1` | `product_2` |
| --- | ---: | ---: |
| low | 2 | 0 |
| high | 0.8 | 3.6 |

With scarce energy, production concentrates on product 1, which earns more
profit per unit of energy. With more energy available, the optimal mix shifts
towards product 2, which uses less material. Both scenarios fully use the
available resources.

This example is intentionally compact. Continue with the
[production planning tutorial](https://cvxlab.readthedocs.io/en/latest/resources.html)
for an applied model and the complete workflow.

## Guided Interface
CVXlab provides an interactive guided interface that walks you through the full 
modeling workflow, from directory setup to model solution via a terminal menu. 
Launch it with the `cvxlab.gui()` function:

```python
import cvxlab

frontend_config = {
    'model_dir_name': 'my_model',
    'main_dir_path': '/path/to/models',
    'action_settings': {
        'run_model': {
            'solution_mode': 'parallel',
            'solver': 'CLARABEL',
        },
    },
}

cvxlab.gui(**frontend_config)
```

Model settings are supplied at the top level, while API-specific values belong
under `action_settings`. All values are optional: after an action is selected,
the interface asks only for the settings that were not preconfigured. The
`use_existing_data` model option is selected through **Model session**: choose
**Create new Model instance** for `False` or **Open existing Model environment**
for `True`.

## Documentation
Full documentation is available at [cvxlab.readthedocs.io](https://cvxlab.readthedocs.io/en/latest/).
You can also browse the source documentation in the [docs/source](docs/source) directory.

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## Contributing
We welcome contributions from the community! Please see [CONTRIBUTING.md](CONTRIBUTING.md) 
for guidelines.

## Community & Support
Submit issues and ideas for improvements in GitHub [GitHub Issues](https://github.com/cvxlab/cvxlab/issues)

## License
Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## Citing
If you use CVXlab in academic work, please cite the software as follows.

**APA**
> Rocco, M. V. (2026). *CVXlab* (Version 1.1.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.20644006

**BibTeX**
```bibtex
@software{rocco_cvxlab_2026,
  author    = {Rocco, Matteo V.},
  title     = {{CVXlab}},
  version   = {1.1.0},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20644006},
  url       = {https://doi.org/10.5281/zenodo.20644006}
}
```

For industry or non-academic use, we'd love to hear your feedback: reach out via
email at matteovincenzo.rocco@polimi.it.
