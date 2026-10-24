"""
COMP 380 - Assignment 1: Map Coloring as a Constraint Satisfaction Problem

Colors the 13 provinces and territories of Canada so that no two neighboring
regions share the same color.

CSP formulation:
    Variables   : the 13 provinces and territories (two-letter postal codes)
    Domains     : the colors supplied by the user
    Constraints : for each pair of neighboring regions X and Y, color(X) != color(Y)

Solver: recursive backtracking search with
    - MRV (Minimum Remaining Values) variable ordering, ties broken by degree
    - LCV (Least Constraining Value) value ordering
    - Forward checking, which prunes neighbors' domains after each assignment
"""


import sys



# Provinces and territories, keyed by postal code.
# The keys are the variables in the CSP.
PROVINCES = {
    "AB": "Alberta",
    "BC": "British Columbia",
    "MB": "Manitoba",
    "NB": "New Brunswick",
    "NL": "Newfoundland and Labrador",
    "NS": "Nova Scotia",
    "NT": "Northwest Territories",
    "NU": "Nunavut",
    "ON": "Ontario",
    "PE": "Prince Edward Island",
    "QC": "Quebec",
    "SK": "Saskatchewan",
    "YT": "Yukon"
}

# Each tuple is one shared border. List each border once; build_graph
# adds it in both directions.
# Note: PE is an island, so it's tied to NB and NS across the Northumberland Strait.

EDGES = [
    ("AB", "BC"), ("AB", "SK"), ("AB", "NT"),
    ("BC", "NT"), ("BC", "YT"),
    ("MB", "SK"), ("MB", "ON"), ("MB", "NU"),
    ("NB", "QC"), ("NB", "NS"), ("NB", "PE"),
    ("NL", "QC"),
    ("NS", "PE"),
    ("NT", "SK"), ("NT", "NU"), ("NT", "YT"),
    ("NU", "QC"), ("NU", "ON"),
    ("ON", "QC"),
]


# Turn the edge list into a neighbor list for each region.
def build_graph(edges, PROVINCES):
    
    # Every region starts with no neighbors
    graph = {province: [] for province in PROVINCES.keys()}
    for edge in edges:
        province1, province2 = edge
        # Borders are two-way, so record each one on both ends
        graph[province1].append(province2)
        graph[province2].append(province1)
    return graph

# Built once when the file loads
GRAPH = build_graph(EDGES, PROVINCES)

# Pick the uncolored region with the fewest colors left.
# On a tie, pick the region with the most neighbors.
def select_unassigned_variable(assignment, domain):
    unassigned_vars = [var for var in GRAPH if var not in assignment]
    return min(unassigned_vars, key=lambda var: (len(domain[var]), -len(GRAPH[var])))

# Order the colors for var so the one that blocks the fewest neighbors comes
# first. sorted() is stable, so ties keep the order the user typed them in.
def order_domain_values(var, assignment, domain, colors):

    # How many uncolored neighbors could still use this color
    def conflicts(color):
        return sum(1 for neighbor in GRAPH[var] if neighbor not in assignment and color in domain[neighbor])

    # Only colors that are still allowed for var
    legal = [color for color in colors if color in domain[var]]
    return sorted(legal, key=conflicts)

# Assign colors one region at a time, undoing a choice if it leads nowhere.
# assignment: region -> color for the regions already colored
# domains: region -> colors still allowed
# colors: the user's color list
# Returns the full coloring, or None if there isn't one.
def backtrack(assignment, domains, colors):
    if len(assignment) == len(GRAPH):
        return assignment

    var = select_unassigned_variable(assignment, domains)

    for color in order_domain_values(var, assignment, domains, colors):
        # Work on a copy, so pruning from this guess doesn't leak into other branches
        new_domains = {v: set(d) for v, d in domains.items()}
        dead_end = False
        # Remove this color from uncolored neighbors. If one is left with
        # nothing, this color can't work.
        for neighbor in GRAPH[var]:
            if neighbor not in assignment:
                new_domains[neighbor].discard(color)
                if not new_domains[neighbor]:
                    dead_end = True
                    break
                
                
        if dead_end:
            continue

        assignment[var] = color
        result = backtrack(assignment, new_domains, colors)
        if result is not None:
            return result
        # That guess failed, so take the color back off
        del assignment[var]

    return None


# Start every region with all the colors available, then search.
def color_map(colors):

    domains = {v: set(colors) for v in GRAPH}
    return backtrack({}, domains, colors)

# Check every border to make sure neighbors have different colors.
def is_valid_coloring(assignment):
    return all(assignment[a] != assignment[b] for a, b in EDGES if a in GRAPH and b in GRAPH[a])

# Ask for a comma-separated list of colors. Pressing Enter uses Red, Green, Blue.
def get_colors():
    """Ask the user for a list of colors, or use the default."""
    raw = input("Enter colors separated by commas "
                "(press Enter for Red,Green,Blue): ").strip()
    if not raw:
        return ["Red", "Green", "Blue"]

    colors = [c.strip() for c in raw.split(",") if c.strip()]
    # Repeated names would quietly shrink the palette, so reject them
    if len(set(colors)) != len(colors):
        raise ValueError("Duplicate colors were entered.")
    return colors


# Print a table of each region's code, name, and color.
def print_result(assignment):
    """Print the province/territory list with its assigned color."""
    print("\n{:<6} {:<30} {}".format("Code", "Province / Territory", "Color"))
    print("-" * 52)
    for code in sorted(assignment):
        print("{:<6} {:<30} {}".format(code, PROVINCES[code], assignment[code]))


# Read the colors, solve the map, and print the result.
def main():
    print("=== Canada Map Coloring (CSP) ===\n")
    try:
        colors = get_colors()
    except ValueError as err:
        print(f"Input error: {err}")
        sys.exit(1)

    result = color_map(colors)

    if result is None:
        print(f"\nNo valid coloring exists with {len(colors)} color(s). "
              "Try adding more colors (3 is enough for Canada).")
        return

    # Double-check the answer before printing it
    assert is_valid_coloring(result), "Internal error: invalid coloring"
    print_result(result)
    print("\nAll neighboring regions have different colors.")


if __name__ == "__main__":
    main()