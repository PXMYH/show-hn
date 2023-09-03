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
            "hn_url": hn_url,
            "points": item.get("points", ""),
        }
        extracted_data.append(extracted_item)

    return extracted_data


def write_data_to_html(data, output_file):
    with open(output_file, 'w') as file:
        file.write('<html>\n')
        file.write('<head>\n')
        file.write('<meta charset="UTF-8">\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        file.write('<title>Hacker News Items</title>\n')
        file.write('</head>\n')
        file.write('<body>\n')
        file.write('<h1>Hacker News Items</h1>\n')
        file.write('<table border="1" id="hn-table">\n')  # Create a table with borders
        file.write('<thead>\n')
        file.write('<tr>\n')
        file.write('<th>Title</th>\n')
        file.write('<th style="text-align:center; cursor: pointer;" onclick="sortTable(1)">Author</th>\n')
        file.write('<th style="text-align:center; cursor: pointer;" onclick="sortTable(2)">Comments</th>\n')
        file.write('<th style="text-align:center; cursor: pointer;" onclick="sortTable(3)">Created Date</th>\n')
        file.write('<th style="text-align:center; cursor: pointer;" onclick="sortTable(4)">Points</th>\n')
        file.write('</tr>\n')
        file.write('</thead>\n')
        file.write('<tbody>\n')

        # Create table rows with centered text for Author, Comments, and Created Date columns
        for item in data:
            hn_url = f"https://news.ycombinator.com/item?id={item['objectID']}"
            file.write('<tr>\n')
            file.write(f'<td><a href="{hn_url}">{item["title"]}</a></td>\n')
            file.write(f'<td style="text-align:center;">{item["author"]}</td>\n')
            file.write(f'<td style="text-align:center;">{item["num_comments"]}</td>\n')
            file.write(f'<td style="text-align:center;">{item["created_at"]}</td>\n')
            file.write(f'<td style="text-align:center;">{item["points"]}</td>\n')
            file.write('</tr>\n')

        file.write('</tbody>\n')
        file.write('</table>\n')

        # JavaScript code for sorting
        file.write('<script>\n')
        file.write('const sortOrders = [null, "asc", "asc", "asc"];\n')
        file.write('function sortTable(columnIndex) {\n')
        file.write('    const table = document.querySelector("#hn-table");\n')
        file.write('    const tbody = table.querySelector("tbody");\n')
        file.write('    const rows = Array.from(tbody.querySelectorAll("tr"));\n')
        file.write('\n')
        file.write('    let sortOrder = sortOrders[columnIndex];\n')
        file.write('\n')
        file.write('    if (sortOrder === "asc") {\n')
        file.write('        sortOrder = "desc";\n')
        file.write('    } else {\n')
        file.write('        sortOrder = "asc";\n')
        file.write('    }\n')
        file.write('\n')
        file.write('    sortOrders[columnIndex] = sortOrder;\n')
        file.write('\n')
        file.write('    rows.sort((a, b) => {\n')
        file.write('        const aValue = (columnIndex === 2 || columnIndex === 4) ? parseInt(a.children[columnIndex].textContent) : a.children[columnIndex].textContent;\n')
        file.write('        const bValue = (columnIndex === 2 || columnIndex === 4) ? parseInt(b.children[columnIndex].textContent) : b.children[columnIndex].textContent;\n')
        file.write('\n')
        file.write('        if (sortOrder === "asc") {\n')
        file.write('            return (columnIndex === 2 || columnIndex === 4) ? aValue - bValue : aValue.localeCompare(bValue);\n')
        file.write('        } else {\n')
        file.write('            return (columnIndex === 2 || columnIndex === 4) ? bValue - aValue : bValue.localeCompare(aValue);\n')
        file.write('        }\n')
        file.write('    });\n')
        file.write('\n')
        file.write('    tbody.innerHTML = "";\n')
        file.write('    rows.forEach(row => tbody.appendChild(row));\n')
        file.write('}\n')
        file.write('</script>\n')

        file.write('</body>\n')
        file.write('</html>\n')

if __name__ == "__main__":
    all_items = fetch_hacker_news_items()
    extracted_data = extract_fields(all_items)

    output_file = "index.html"

    write_data_to_html(extracted_data, output_file)
    print(f"Data written to {output_file}")
