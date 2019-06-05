import unittest
import asyncio
from pyfavicon import Favicon, FaviconType
from pathlib import Path
from yarl import URL


class HTMLTest(unittest.TestCase):

    def setUp(self):
        self.favicon = Favicon()

    def test_url_icon_link_type(self):
        files = [
            Path('./tests/html/base64_favicon_link.html'),
        ]

        async def run_test():
            for html_file in files:
                favicons = await self.favicon.from_file(html_file)
                icon = favicons[0]
                self.assertEqual(icon.type, FaviconType.DATA)
        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
