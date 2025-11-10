# Contributing

Thank you for considering contributing to CVXlab! We welcome contributions from 
everyone. 

## How to Contribute

### Reporting Bugs
If you find a bug, please report it by opening an issue on our 
[GitHub Issues](https://github.com/cvxlab/cvxlab/issues) page. 
Include as much detail as possible to help us diagnose and fix the problem quickly.

### Suggesting Features
We welcome new feature suggestions! Please open an issue on our 
[GitHub Issues](https://github.com/cvxlab/cvxlab/issues) page and describe the 
feature you would like to see, why you need it, and how it should work.

### Branching Strategy for Contributions and Maintainers

CVXlab follows the GitFlow branching model:

- **`main`** - Stable releases only (v1.0.0, v1.0.1, etc.)
- **`develop`** - Active development and integration branch
- **`feature/*`** - Individual features (e.g., `feature/new-solver`)
- **`release/*`** - Release preparation (e.g., `release/1.1.0`)
- **`hotfix/*`** - Urgent fixes to main (e.g., `hotfix/critical-bug`)

### Workflow for Contributors

1. **Fork** the repository
2. **Create a feature branch from `develop`:**
   ```sh
   git checkout develop
   git pull origin develop
   git checkout -b feature/my-feature
   ```
3. **Make your changes** and commit
4. **Push** to your fork:
   ```sh
   git push origin feature/my-feature
   ```
5. **Open a pull request** targeting the `develop` branch (not `main`)

### Workflow for Maintainers

1. **Clone the repository:**
   ```sh
   git clone https://github.com/cvxlab/cvxlab.git
   cd cvxlab
   ```
2. **Create and activate the development environment:**
   ```sh
   conda env create -f environment.yml
   conda activate cvxlab_env
   ```
3. **Install the package in editable mode:**
   ```sh
   python -m pip install -e .[docs]
   ```
4. **Create a feature branch from `develop`:**
   ```sh
   git checkout develop
   git pull origin develop
   git checkout -b feature/my-feature
   ```
5. **Make your changes** and commit
6. **Push** to the main repository:
   ```sh
   git push origin feature/my-feature
   ```

---

## Code Style & Testing

- When modify/improve the package, follow existing code style and conventions.
- Add or update docstrings and documentation as needed.
- Add new tests for new features or bug fixes.
- Before submitting, run all tests (make sure the `cvxlab_env` conda environment 
   is activated):
  ```sh
  conda activate cvxlab_env
  python -m pytest
  ```

---

## Documentation

- Update documentation and docstrings to reflect your changes.
- See [docs/index.rst](index.rst) for more details.

---

## License

By contributing to CVXlab, you agree your contributions will be licensed under 
the Apache License 2.0.