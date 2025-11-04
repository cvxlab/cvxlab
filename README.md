![CVXlab Logo](docs/images/logo_10-25/png/CVXlab_logo_260925-02.png)

CVXlab is an open-source Python laboratory for modeling and solving convex optimization problems. 
It extends [cvxpy](https://www.cvxpy.org/) with user-friendly interfaces, integrated data 
management and support for multiple, interconnected optimization models.

## Features
- **General-purpose model generator**: Model problems as you would mathematically, without restrictive solver forms.
- **Almost no-code required**: Build models using Excel or YAML—no coding required.
- **Centralized data management**: Centralized data input/output via SQLite database.
- **Multi-Model Support**: Generate and solve multiple integrated or decomposed optimization problems.
- **Powerful engine embedded**: Built on cvxpy, [CVXPY documentation](https://www.cvxpy.org/tutorial/intro/index.html).

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Community & Support](#community--support)
- [License](#license)
- [Citing](#citing)

## Installation
Install CVXlab from the project root:
```bash
pip install .
```
Or install from source:
```bash
git clone https://github.com/your-repo/cvxlab.git
cd cvxlab
pip install .
```

## Quickstart
Here's a minimal example to get started:
```python
import cvxlab

# Define your optimization problem
# ...existing code...

# Solve the problem
# ...existing code...
```
See the [Usage Guide](usage.rst) for detailed instructions.

## Examples
Explore example scripts and notebooks:
- [Example Script 1](examples/example_script1.py): Basic optimization workflow.
- [Example Script 2](examples/example_script2.py): Advanced modeling features.
- [Example Notebook 1](examples/example_notebook1.ipynb): Interactive problem setup.
- [Example Notebook 2](examples/example_notebook2.ipynb): Data integration with Excel/SQLite.

## Documentation
Full documentation is available in the [docs](docs/) folder and [usage.rst](usage.rst).

## Contributing
We welcome contributions from the community! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Community & Support
- **Chat**: Join us on [Discord](https://discord.gg/4urRQeGBCr)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/cvxlab/discussions)
- **Issues**: [GitHub Issues](https://github.com/your-repo/cvxlab/issues)

Please be respectful and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## License
Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## Citing
If you use CVXlab in academic work, please cite our papers. For industry use, we'd love to hear your feedback—reach out via Discord or email.




