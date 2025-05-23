# AniList API + Routes

import httpx

async def search_anime(name=None, genre=None):
    query = """
    query ($search: String, $genre: String) {
      Page(perPage: 10) {
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
    variables = {"search": name, "genre": genre}
    async with httpx.AsyncClient() as client:
        response = await client.post("https://graphql.anilist.co", json={"query": query, "variables": variables})
        return response.json()["data"]["Page"]["media"]
