import aiohttp
from bs4 import BeautifulSoup


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        result = await session.get(url=url)
        result = await result.text()
    return result


class GitHubRepo:
    def __init__(self, url: str, loop):
        self.loop = loop
        self.URL = url
        self.author = f"https://github.com/{url.split('/')[3]}"
        self.soup: BeautifulSoup = None

    def get_page(self):
        data = self.loop.run_until_complete(request(self.URL))
        self.soup = BeautifulSoup(data, features="html.parser")

    def socials(self):
        social_counts = self.soup.find_all("a", ["social-count", "js-social-count"])
        return [tag.get_text().strip() for tag in social_counts]

    def trackers(self):
        track = self.soup.find_all("span", ["Counter"])
        issues, prs = [tag.get_text().strip() for tag in track[1:3]]
        contributors = track[-1].get_text()
        last_commit = self.soup.find("relative-time", ["no-wrap"])
        last_commit = last_commit.get_text() if last_commit.text else None
        return issues, prs, contributors, last_commit

    def stats(self):
        self.get_page()

        stat_dict = dict()

        a, b = self.socials()
        stat_dict['stars'] = a
        stat_dict['forks'] = b

        a, b, c, d = self.trackers()
        stat_dict['issues'] = a
        stat_dict['prs'] = b
        stat_dict['contributors'] = c
        stat_dict['last_commit'] = d
        stat_dict['author'] = self.author
        return stat_dict

