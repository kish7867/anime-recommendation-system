import httpx

async def search_anime(name=None, genre=None):
    query = """
    query ($search: String, $genre: String) {
      Page(perPage: 20) {
        media(search: $search, genre_in: [$genre], type: ANIME) {
          title {
            romaji
          }
          genres
          popularity
        }
      }
    }
    """

    async def fetch(search_name):
        variables = {"search": search_name, "genre": genre}
        async with httpx.AsyncClient() as client:
            response = await client.post("https://graphql.anilist.co", json={"query": query, "variables": variables})
            return response.json().get("data", {}).get("Page", {}).get("media", [])

    # Try user input as is
    results = await fetch(name)

    # If no results and name provided, retry with title case
    if name and not results:
        title_case_name = name.title()
        results = await fetch(title_case_name)

    # Filter results client-side for case-insensitive match (for 'name')
    if name:
        lower_name = name.lower()
        filtered = []
        for anime in results:
            title = anime.get("title", {}).get("romaji", "").lower()
            if lower_name in title:
                filtered.append(anime)
        results = filtered

    return results
