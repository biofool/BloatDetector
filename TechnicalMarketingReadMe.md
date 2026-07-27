# BloatDetector — Technical Marketing Summary

## One-Line Positioning

A Linux system analysis toolkit that identifies unused files and packages by examining file access timestamps, helping security teams reduce attack surface through data-driven package removal.

## Target Users / Personas

- **Security practitioners and sysadmins** who need to identify rarely-used packages for removal or patching to reduce system attack surface.
- **DevOps engineers** managing Ubuntu/Debian servers who want to optimize package footprints and identify bloat.
- **Compliance auditors** who need evidence-based reports on package usage patterns for security reviews.

## Key Features (Grounded in Code)

- **File access timestamp collection**: Shell script (`CollectFileUsageStats.sh`) uses `find` to scan directory trees and record file paths with creation and access times, supporting configurable thresholds, directory lists, and monitoring loops with sleep intervals.
- **Package-to-file mapping**: Shell script (`packages_exploder.sh`) enumerates all installed `dpkg` packages and their files, producing a `path|package` mapping file.
- **Pandas-based data analysis**: Python scripts merge file usage data with package mappings using pandas outer joins, group by package, and compute the oldest access time per package to identify least-accessed packages (`UnusedFilesAndPackages.py`, `UnusedPackageReport.py`).
- **Unused file identification**: Filters files whose normalized access time exceeds a configurable stale-age threshold (default 45 days) to flag files not accessed within the specified period (`UnusedPackageReport.py`, `stale_age` parameter).
- **Visualization**: Generates area charts showing file access distribution over days since system build using matplotlib (`UnusedFilesAndPackages.py`, `UnusedPackageReport.py`).
- **CSV-to-PSV conversion**: Utility script (`csv2psv.py`) converts comma-separated file access data to pipe-separated format with error logging for unparseable lines.
- **Systemd service installer**: `install_bloatdetector.sh` installs the collection script as a systemd service for continuous monitoring with auto-restart.
- **Clipboard-based buffer unitizer**: `buffer_unitizer.py` reads spreadsheet data from the clipboard, normalizes units (MB, GB, SSD, HDD, CPU, GHz), and writes results back to the clipboard.
- **Jupyter notebooks**: Multiple `.ipynb` notebooks provide interactive analysis workflows (`UnusedFilesAndPackages.ipynb`, `UnusedFilesAndPackages-V2.ipynb`, `UnusedPackageReport.ipynb`, `WhatsUnused.ipynb`).

## Technical Differentiators

- **Filesystem-level evidence**: Uses actual file access timestamps from the filesystem rather than heuristics or package metadata, providing ground-truth usage data.
- **Non-intrusive approach**: Evaluated against SELinux, auditd, eBPF, and AppArmor — chose `find`-based collection to avoid real-time monitoring performance impacts and the engineering overhead of ensuring complete file utilization detection.
- **Package-level aggregation**: Correlates individual file access times back to their owning packages, enabling package-level removal recommendations (generates `sudo dpkg -r` commands).
- **Continuous monitoring mode**: The collection script supports infinite-loop monitoring with configurable sleep intervals and SIGHUP-based restart, deployable as a systemd service.

## Use Cases

- Identifying packages that haven't been used in 30+ days for removal on production servers.
- Generating security-focused reports prioritizing packages by oldest file access time for patch/removal decisions.
- Monitoring file access patterns over time on Ubuntu/Debian systems to detect drift in package usage.
- Converting and normalizing system inventory data for further analysis.

## Benefits / Value Proposition

- Reduces system attack surface by identifying packages safe to remove based on actual usage evidence.
- Enables proactive maintenance: regular analysis of file access patterns catches stale packages before they become security liabilities.
- No real-time monitoring overhead — uses existing filesystem metadata (atime/mtime).
- Produces actionable output: directly generates `dpkg -r` commands for package removal.

## Tech Stack

- **Language**: Python 3, Bash shell
- **Data analysis**: `pandas`, `matplotlib`, `numpy`
- **System tools**: `find`, `dpkg`, `sort`, `tar`, `vmstat`
- **Notebooks**: Jupyter Notebook
- **Platform**: Ubuntu 20+ (ext4 filesystem), Debian-based Linux
- **Deployment**: systemd service

## Known Limitations

- Designed for Ubuntu 20+ and ext4 filesystems; ext4 `relatime` mount option may affect access time granularity (access times are only updated if more than 1 day old since Linux 2.6.30).
- The installer script (`install_bloatdetector.sh`) is noted as still in alpha testing.
- Large CSV data files (9-11 MB) are committed to the repo, which may be specific to a particular system snapshot rather than generally reusable.
- Requires root/sudo privileges for comprehensive filesystem scanning and systemd service installation.
- The `buffer_unitizer.py` utility depends on the `clipboard` Python package and is unrelated to the core bloat detection workflow.
