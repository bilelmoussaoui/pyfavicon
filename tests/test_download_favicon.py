import unittest
import asyncio
from pyfavicon import Favicon
from pathlib import Path
import tempfile
import yarl


class HTMLTest(unittest.TestCase):

    def setUp(self):
        self.favicon = Favicon(download_dir=Path(tempfile.gettempdir()))

    def test_url_icon_link_type(self):

        async def run_test():
            icons = await self.favicon.from_url(yarl.URL('https://gitlab.com'))
            icon = icons[0]
            # Ensure that save works correctly
            await icon.save()
            self.assertTrue(icon.path.exists())
            # Remove the test file
            icon.path.unlink()
        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
