# COMP 380 Assignment 1: Map Coloring as a CSP

Colors the 13 provinces and territories of Canada so that no two neighboring regions share a color. The problem is modeled as a constraint satisfaction problem (CSP) and solved with backtracking search using MRV, LCV, and forward checking.

## Requirements

- Python 3.8 or later (tested with Python 3.14.3)
- No external packages

## Usage

1. Open a terminal in the folder containing `map_coloring.py`.
2. Run the program:

   ```bash
   python map_coloring.py
   ```

   On macOS or Linux, use `python3` if `python` is not found.

3. At the prompt, either press Enter to use the default colors (Red, Green, Blue), or type a comma-separated list such as:

   ```
   Crimson, Teal, Gold
   ```

The program prints a table showing each province or territory and its assigned color.

## Notes

- Duplicate colors are rejected.
- If the colors you entered cannot produce a valid coloring, the program reports that none exists. For example, `Red, Green` fails because Canada's map contains triangles of neighboring regions.
- The map is defined by the `PROVINCES` and `EDGES` lists near the top of `map_coloring.py`. Edit those lists to model a different map.

## Files

| File | Description |
|------|-------------|
| `map_coloring.py` | Solver and console interface |
| `README.md` | This file |

## Video Link

https://youtu.be/i7brH-V08uo