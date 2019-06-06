import unittest
import asyncio
from pyfavicon import Favicon, FaviconType
from pathlib import Path


class HTMLTest(unittest.TestCase):

    def setUp(self):
        self.favicon = Favicon()

    def test_url_icon_link_type(self):
        files = [
            Path('./tests/html/url_icon_link.html'),
            Path('./tests/html/url_shortcut_icon_link.html'),
            Path('./tests/html/url_apple_touch_icon_precomposed_link.html'),
            Path('./tests/html/url_apple_touch_icon_link.html'),
            Path('./tests/html/url_fluid_icon_link.html'),
        ]

        async def run_test():
            for html_file in files:
                favicons = await self.favicon.from_file(html_file,
                                                        'https://github.com')
                icon = favicons[0]

                self.assertEqual(icon.type, FaviconType.URL)
                self.assertEqual(str(icon.link),
                                 'https://github.githubassets.com/favicon.ico')
        asyncio.run(run_test())

    def test_meta_link(self):
        html_file = Path('./tests/html/meta_favicon.html')

        async def run_test():
            icons = await self.favicon.from_file(html_file,
                                                 'https://gitlab.com')
            icon = icons[0]

            self.assertEqual(icon.type, FaviconType.URL)
            self.assertEqual(str(icon.link),
                             'https://assets.gitlab-static.net/assets/msapplication-tile-1196ec67452f618d39cdd85e2e3a542f76574c071051ae7effbfde01710eb17d.png')
        asyncio.run(run_test())

    def test_largest_icon(self):
        html_file = Path('./tests/html/largest_gitlab.html')

        async def run_tests():
            icons = await self.favicon.from_file(html_file)

            largest_icon = icons.get_largest()
            self.assertTupleEqual(largest_icon.size, (188, 188))

        asyncio.run(run_tests())


if __name__ == '__main__':
    unittest.main()
