import requests
from bs4 import BeautifulSoup
from collections import defaultdict

# Function to decode secret Unicode message from a Google Doc
def decode_secret_message(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Error: Failed to fetch document. HTTP Status Code:", response.status_code)
        return
    
    # Parse HTML and extract text
    soup = BeautifulSoup(response.text, "html.parser")
    lines = soup.get_text("\n").strip().splitlines()

    # Remove headers and empty lines
    skip_headers = {"x-coordinate", "y-coordinate", "Character"}
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line in skip_headers or not line:
            continue
        clean_lines.append(line)
        
    # Filter out non-data lines
    filtered = []
    for line in clean_lines:
        line = line.strip()
        if not line:
            continue
        if line.isdigit() or len(line) == 1:
            filtered.append(line)

    # Group into (char, x, y)
    parsed = []
    i = 0
    for i in range(0, len(filtered), 3):
        try:
            x = int(filtered[i])
            char = filtered[i + 1]
            y = int(filtered[i + 2])
            parsed.append((char, x, y))
        except (ValueError, IndexError):
            continue
    
    # Failure to parse any valid data
    if not parsed:
        print("No valid data found.")
        return

    # Create grid with maximum dimensions
    max_x = max(p[1] for p in parsed)
    max_y = max(p[2] for p in parsed)
    grid = defaultdict(lambda: ' ')
    for char, x, y in parsed:
        grid[(x, y)] = char

    # Print the grid
    for y in range(max_y + 1):
        row = ''.join(grid[(x, y)] for x in range(max_x + 1))
        print(row)

    


# Decode message
decode_secret_message("https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub")