import requests

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

if __name__ == "__main__":
    all_items = fetch_hacker_news_items()
    print(f"Total {len(all_items)} items fetched.")
    
    # You can now work with the 'all_items' list, which contains all the items from the API.
    # For example, you can iterate through the list and access fields like 'title', 'url', etc.
