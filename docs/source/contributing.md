# Contributing

Thank you for considering contributing to CVXlab! We welcome contributions from everyone. 

## How to Contribute

### Reporting Bugs
If you find a bug, please report it by opening an issue on our [GitHub Issues](https://github.com/cvxlab/cvxlab/issues) page. Include as much detail as possible to help us diagnose and fix the problem quickly.

### Suggesting Features
We welcome new feature suggestions! Please open an issue on our [GitHub Issues](https://github.com/cvxlab/cvxlab/issues) page and describe the feature you would like to see, why you need it, and how it should work.

### Submitting Changes
1. **Fork** the repository
2. **Create a branch** for your changes:
   ```sh
   git checkout -b my-feature
   ```
3. **Make your changes** and commit:
   ```sh
   git commit -am "Describe your change"
   ```
5. **Push** to the branch
    ```sh
    git push origin my-feature
    ```
6. **Open a pull request** on GitHub.

---

## Development Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/cvxlab/cvxlab.git
   cd cvxlab
   ```

2. **Create and activate the development environment:**
   ```sh
   conda env create -f environment.yml
   conda activate cvxlab
   ```

3. **Install the package in editable mode:**
   ```sh
   python -m pip install -e .
   ```

---

## Code Style & Testing

- Follow existing code style and conventions.
- Add or update docstrings and documentation as needed.
- Run tests before submitting:
  ```sh
  pytest
  ```
- Add new tests for new features or bug fixes.

---

## Building the Package

To build source and wheel distributions:
```sh
python setup.py sdist bdist_wheel
```

---

## Documentation

- Update documentation and docstrings to reflect your changes.
- See [docs/index.rst](index.rst) for more details.

---

## License

By contributing to CVXlab, you agree your contributions will be licensed under 
the Apache License 2.0.