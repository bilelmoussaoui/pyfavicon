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
                favicons = await self.favicon.from_file(html_file)
                icon = favicons[0]

                self.assertEqual(icon.type, FaviconType.URL)
                self.assertEqual(str(icon.link),
                                 'https://github.githubassets.com/favicon.ico')
        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
