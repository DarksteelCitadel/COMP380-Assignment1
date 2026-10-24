import sys



## List of provinces in Canada with their abbreviations and full names
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

## List of tuples that represent edges between provinces

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


def build_graph(edges, PROVINCES):
    
    graph = {province: [] for province in PROVINCES.keys()}
    for edge in edges:
        province1, province2 = edge
        graph[province1].append(province2)
        graph[province2].append(province1)
    return graph

GRAPH = build_graph(EDGES, PROVINCES)

def select_unassigned_variable(assignment, domain):
    unassigned_vars = [var for var in GRAPH if var not in assignment]
    return min(unassigned_vars, key=lambda var: (len(domain[var]), -len(GRAPH[var])))

def order_domain_values(var, assignment, domain, colors):

    def conflicts(color):
        return sum(1 for neighbor in GRAPH[var] if neighbor not in assignment and color in domain[neighbor])

    legal = [color for color in colors if color in domain[var]]
    return sorted(legal, key=conflicts)

def backtrack(assignment, domains, colors):
    if len(assignment) == len(GRAPH):
        return assignment

    var = select_unassigned_variable(assignment, domains)

    for color in order_domain_values(var, assignment, domains, colors):
        new_domains = {v: set(d) for v, d in domains.items()}
        dead_end = False
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
        del assignment[var]

    return None


def color_map(colors):

    domains = {v: set(colors) for v in GRAPH}
    return backtrack({}, domains, colors)

def is_valid_coloring(assignment):
    return all(assignment[a] != assignment[b] for a, b in EDGES if a in GRAPH and b in GRAPH[a])

def get_colors():
    """Ask the user for a list of colors, or use the default."""
    raw = input("Enter colors separated by commas "
                "(press Enter for Red,Green,Blue): ").strip()
    if not raw:
        return ["Red", "Green", "Blue"]

    colors = [c.strip() for c in raw.split(",") if c.strip()]
    if len(set(colors)) != len(colors):
        raise ValueError("Duplicate colors were entered.")
    return colors


def print_result(assignment):
    """Print the province/territory list with its assigned color."""
    print("\n{:<6} {:<30} {}".format("Code", "Province / Territory", "Color"))
    print("-" * 52)
    for code in sorted(assignment):
        print("{:<6} {:<30} {}".format(code, PROVINCES[code], assignment[code]))


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

    assert is_valid_coloring(result), "Internal error: invalid coloring"
    print_result(result)
    print("\nAll neighboring regions have different colors.")


if __name__ == "__main__":
    main()