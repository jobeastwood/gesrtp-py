# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

**NOTE**: When releasing, this should be version **1.2.0** (MINOR bump) - new packaging feature with minor breaking change (import path).

### Added
- **Proper Python package structure** with `pyproject.toml`
- Package is now installable via `pip install -e .`
- Modern package layout: `src/gesrtp/` with all modules
- Clean imports: `from gesrtp import GE_SRTP_Driver` (no more sys.path hacks!)
- New test environment configuration for Emerson PACSystems EPXCPE210
- Comprehensive test script `03_memory_comprehensive_0_64.py` for testing addresses 0-64
- Complete test suite documentation in `tests/README.md`
- Professional numbered naming for tests (01_, 02_, 03_)
- Professional numbered naming for examples (01_, 02_, 03_)
- Difficulty ratings for examples (⭐ to ⭐⭐⭐)
- `docs/` directory for organized documentation
- Versioning infrastructure (CHANGELOG.md, VERSION file)
- Installation instructions in README.md

### Changed
- **BREAKING**: Package renamed from `src` to `gesrtp` - update imports!
  - Old: `from src.driver import GE_SRTP_Driver`
  - New: `from gesrtp import GE_SRTP_Driver`
- **BREAKING**: Updated test environment to EPXCPE210 (slot 0, IP 172.16.12.124)
- Restructured source: `src/` → `src/gesrtp/` for proper package layout
- Completely rewrote `02_realtime_monitor.py` with in-place updates (no scrolling!)
- Improved `examples/README.md` with better structure and quick start guide
- Renamed test files with numbered prefix for better organization
- Renamed example files with numbered prefix for better organization
- Updated all documentation for new hardware configuration and new import style
- Updated all examples and tests to use clean `from gesrtp` imports
- Reorganized documentation: moved 6 markdown files to `docs/` directory
  - `PROJECT_OVERVIEW.md` → `docs/overview.md`
  - `PROTOCOL_DISCOVERIES.md` → `docs/protocol.md`
  - `HARDWARE_CONFIG.md` → `docs/hardware.md`
  - `WIRESHARK_CAPTURE_GUIDE.md` → `docs/wireshark.md`
  - `SYMBOLIC_ADDRESSING_INVESTIGATION.md` → `docs/symbolic_addressing.md`
  - `TODO.md` → `docs/todo.md`

### Removed
- **sys.path.insert() hacks** from all examples and test files
- 5 obsolete discrete I/O debugging test files
- Old test file naming convention

### Fixed
- Import path issues in all test and example files (now using proper package imports)
- Cursor positioning in real-time monitor for options 2 and 3
- Section header display in analog I/O and discrete I/O monitors

## [1.0.0] - 2025-10-16

### Added
- Initial production-ready release
- Complete GE-SRTP protocol driver implementation
- Support for 9 memory types with 15 access modes
- All memory types verified on Emerson RX3i IC695CPE330
- 5 major protocol discoveries documented
- 3 example scripts (basic_usage, continuous_monitor, memory_dump)
- Comprehensive documentation (8 markdown files)
- Read-only design for safety

### Protocol Features
- TCP/IP connection over port 18245
- Multi-packet response handling
- Slot-specific mailbox addressing
- 0-based protocol addressing
- RX3i-specific minimum length enforcement

### Memory Types Supported
- %R (Registers) - word mode
- %AI (Analog Input) - word mode
- %AQ (Analog Output) - word mode
- %I (Discrete Input) - bit & byte modes
- %Q (Discrete Output) - bit & byte modes
- %M (Internal Memory) - bit & byte modes
- %T (Temporary Memory) - bit & byte modes
- %S (System Memory) - bit & byte modes
- %G (Global Memory) - bit & byte modes

### Diagnostics Functions
- PLC status query
- Controller info
- Program names
- Date/time
- Fault table

### Documentation
- `docs/overview.md` - Complete project summary
- `docs/protocol.md` - 5 major technical discoveries
- `docs/hardware.md` - RX3i hardware configuration
- `DEVELOPMENT.md` - Developer guide
- `README.md` - User guide
- `docs/todo.md` - Project status tracking

---

## Version History

- **1.0.0** (2025-10-16) - Initial production release
- **Unreleased** - New test rig and improved examples/tests

---

## Semantic Versioning

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backwards compatible manner
- **PATCH** version for backwards compatible bug fixes

Given a version number MAJOR.MINOR.PATCH (e.g., 1.2.3):
- Increment MAJOR when you make incompatible API changes
- Increment MINOR when you add functionality in a backwards compatible manner
- Increment PATCH when you make backwards compatible bug fixes
