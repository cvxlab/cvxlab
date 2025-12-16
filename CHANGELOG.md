# Changelog

All notable changes to CVXlab will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Stable 1.0.0 release
- API stabilization
- Complete documentation coverage

## [1.0.0b1] - 14 November 2025

### Added
- `Model` class for optimization problem management
- SQLite-backed data management via `Database` and `SQLManager`
- CVXPY integration for convex optimization solving
- Support for independent and integrated (coupled) problem solving
- Excel and YAML-based model settings definition
- Symbolic expression parsing and validation
- Initial set of built-in operators and constants
- Basic logging and error handling framework

### Documentation
- Initial user guide with workflow steps
- API reference documentation
- Tutorial: Simple model example
- Installation guide
- Contributing guidelines

### Known Limitations
- Documentation under active development
- API subject to change before 1.0.0 stable
- Limited tutorial coverage
- Limited test converage

[Unreleased]: https://github.com/cvxlab/cvxlab/compare/v1.0.0b1...HEAD
[1.0.0b1]: https://github.com/cvxlab/cvxlab/releases/tag/v1.0.0b1