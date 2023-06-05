import requests

NOTION_TOKEN = "notion secret"
DATABASE_ID = "db id"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

class Birthday:
    def __init__(self, name, days_left, bday, age_this_year, bday_this_year):
        self.name = name
        self.days_left = days_left
        self.bday = bday
        self.age_this_year = age_this_year
        self.bday_this_year = bday_this_year

    def __str__(self):
        return f"{self.name} - {self.bday_this_year}"


def get_pages(num_pages=None):
    # If num_pages is None, get all pages, otherwise just the defined number.

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    # loop through results, and sort by days left
    birthdays = []
    for elt in results:
        element_data = elt["properties"]
        name = element_data["Name"]["title"][0]["text"]["content"]

        # days left property is not returned correctly
        # only returns 1, could instead sort by bday
        days_left = element_data["Days left"]["formula"]["number"]

        bday = element_data["Birthday"]["date"]["start"]
        age_this_year = element_data["Age this year"]["formula"]["number"]
        bday_this_year = element_data["Birthday This Year"]["formula"]["date"]["start"]

        birthdays.append(Birthday(name, days_left, bday, age_this_year, bday_this_year))

    # sort data
    sorted_birthdays = sorted(birthdays, key=lambda x: x.bday_this_year)

    return sorted_birthdays


# result = get_pages()
# for elt in result[:10]:
#     print(elt)