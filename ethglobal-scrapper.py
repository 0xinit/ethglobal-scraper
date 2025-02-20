import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures

def fetch_projects(page, identifier):
    url = f"https://ethglobal.com/showcase?events=bangkok&page={page}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching page {page}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #  CSS selector to match the project cards
    project_cards = soup.select("a.block.border-2.border-black.rounded.overflow-hidden.relative")
    if not project_cards:
        print(f"Page {page}: no project cards found.")
    
    filtered_projects = []
    for card in project_cards:
        logos = card.find_all('img')
        if any(f"/organizations/{identifier}/" in img.get("src", "") for img in logos):		#identifier is the user-input that they find for an org logo thru inspect element
            title_elem = card.find('h2', class_="text-2xl")
            title = title_elem.text.strip() if title_elem else "N/A"
            desc_elem = card.find('p')
            description = desc_elem.text.strip() if desc_elem else "N/A"
            filtered_projects.append({
                'title': title,
                'description': description
            })
    
    print(f"Page {page}: found {len(filtered_projects)} matching project(s) out of {len(project_cards)} project card(s).")
    return filtered_projects

# Prompt user for a custom organization identifier which is a logo (for example, 'dkzkp' is for LayerZero)
identifier = input("Enter organization identifier (e.g., dkzkp): ").strip()
all_projects = []
pages = list(range(1, 101))  # put any custom number

# Use ThreadPoolExecutor to run up to 10 pages concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Use a lambda to pass the page and the identifier to the fetch_projects function
    results = executor.map(lambda p: fetch_projects(p, identifier), pages)
    for page_projects in results:
        all_projects.extend(page_projects)

if all_projects:
    with open('filtered_projects.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for project in all_projects:
            writer.writerow(project)
    print(f"Scraping complete. Results saved to filtered_projects.csv. Total matching projects: {len(all_projects)}")
else:
    print("No matching projects found.")
