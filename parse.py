import requests
import json

def fetch_hacker_news_items():
    base_url = "https://hn.algolia.com/api/v1/search?tags=show_hn"
    page = 0
    all_hits = []

    while True:
        url = f"{base_url}&page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            break

        data = response.json()
        hits = data.get("hits", [])
        hits_per_page = data.get("hitsPerPage", 0)
        nb_pages = data.get("nbPages", 0)

        print(f"Page {page + 1} of {nb_pages}, {len(hits)} items per page")
        all_hits.extend(hits)

        # Check if there are more pages to fetch
        if page < nb_pages - 1:
            page += 1
        else:
            break

    return all_hits

def extract_fields(items):
    extracted_data = []
    
    for item in items:
        hn_url = f"https://news.ycombinator.com/item?id={item.get('objectID', '')}"
        
        extracted_item = {
            "created_at": item.get("created_at", ""),
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "num_comments": item.get("num_comments", 0),
            "objectID": item.get("objectID", ""),
            "author": item.get("author", ""),
            "hn_url": hn_url
        }
        extracted_data.append(extracted_item)
    
    return extracted_data

def write_data_to_html(data, output_file):
    with open(output_file, 'w') as file:
        file.write('<html>\n')
        file.write('<head>\n')
        file.write('<title>Hacker News Items</title>\n')
        file.write('</head>\n')
        file.write('<body>\n')
        file.write('<h1>Hacker News Items</h1>\n')
        file.write('<ul>\n')

        for item in data:
            file.write('<li>\n')
            file.write(f'<a href="{item["hn_url"]}">{item["title"]}</a>\n')
            file.write('</li>\n')

        file.write('</ul>\n')
        file.write('</body>\n')
        file.write('</html>\n')

if __name__ == "__main__":
    all_items = fetch_hacker_news_items()
    extracted_data = extract_fields(all_items)
    
    output_file = "hacker_news_items.html"

    write_data_to_html(extracted_data, output_file)
    print(f"Data written to {output_file}")