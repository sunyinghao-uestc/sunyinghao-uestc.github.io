from html.parser import HTMLParser
from pathlib import Path
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]
PAGE = REPOSITORY / "projects" / "part" / "index.html"
STYLESHEET = REPOSITORY / "projects" / "part" / "part.css"
PUBLIC_ROUTE = REPOSITORY / "part" / "index.html"


class PartPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.media = []
        self.videos = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if tag in {"img", "source"} and "src" in attributes:
            self.media.append(attributes["src"])
        if tag == "video":
            self.videos.append(attributes)


class PartProjectPageTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(PAGE.is_file(), "PART project page is missing")
        self.assertTrue(STYLESHEET.is_file(), "PART stylesheet is missing")
        self.parser = PartPageParser()
        self.parser.feed(PAGE.read_text(encoding="utf-8"))

    def test_page_exposes_the_complete_research_story(self):
        self.assertTrue(
            {"overview", "method", "results", "demos", "qualitative", "citation"}
            .issubset(self.parser.ids)
        )

    def test_page_links_to_the_public_arxiv_record_and_pdf(self):
        self.assertIn("https://arxiv.org/abs/2609.02289", self.parser.links)
        self.assertIn("https://arxiv.org/pdf/2609.02289", self.parser.links)

    def test_page_references_every_required_local_asset(self):
        required_assets = {
            "assets/architecture.jpg",
            "assets/demo-night.mp4",
            "assets/demo-wheelchair.mp4",
        }
        self.assertTrue(required_assets.issubset(set(self.parser.media)))
        for asset in required_assets:
            self.assertTrue((PAGE.parent / asset).is_file(), f"Missing local asset: {asset}")

    def test_home_page_links_to_part(self):
        home = (REPOSITORY / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="part/"', home)

    def test_home_page_lists_part_first_in_research(self):
        home = (REPOSITORY / "index.html").read_text(encoding="utf-8")
        research = home[home.index("<h2>Research</h2>") : home.index("<h2>Projects</h2>")]
        self.assertLess(
            research.index("PART: Physics-Aware Radar Transformer"),
            research.index("Unsupervised Domain Adaptation for 3D Object Detection"),
        )
        for url in (
            "part/",
            "https://arxiv.org/abs/2609.02289",
            "https://github.com/sunyinghao-uestc/PART",
        ):
            self.assertIn(url, research)

    def test_home_page_does_not_duplicate_part_in_projects(self):
        home = (REPOSITORY / "index.html").read_text(encoding="utf-8")
        projects = home[home.index("<h2>Projects</h2>") :]
        self.assertNotIn("PART: Physics-Aware Radar Transformer", projects)

    def test_home_page_includes_postdoctoral_fellowship_news(self):
        home = (REPOSITORY / "index.html").read_text(encoding="utf-8")
        news = home[home.index("<h2>News</h2>") : home.index("<h2>Research</h2>")]
        self.assertIn(
            "🔥 July 24, 2026: I have been awarded a fellowship from the 79th General Program of the China Postdoctoral Science Foundation.",
            news,
        )
        self.assertIn("<ul>", news)
        self.assertIn("<li>", news)

    def test_video_demos_have_text_descriptions(self):
        self.assertEqual(2, len(self.parser.videos))
        described_by = {video.get("aria-describedby") for video in self.parser.videos}
        self.assertEqual({"night-demo-description", "wheelchair-demo-description"}, described_by)
        self.assertTrue(described_by.issubset(self.parser.ids))

    def test_short_part_route_redirects_to_the_project_page(self):
        self.assertTrue(PUBLIC_ROUTE.is_file(), "Short /part route is missing")
        route = PUBLIC_ROUTE.read_text(encoding="utf-8")
        self.assertIn("../projects/part/", route)


if __name__ == "__main__":
    unittest.main()
