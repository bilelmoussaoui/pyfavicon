import unittest
import asyncio
from pyfavicon import Favicon, FaviconType
from pathlib import Path
import filecmp
import tempfile


class HTMLTest(unittest.TestCase):

    def setUp(self):
        self.favicon = Favicon(download_dir=Path(tempfile.gettempdir()))

    def test_url_icon_link_type(self):
        files = [
            Path('./tests/html/base64_favicon_link.html'),
        ]

        async def run_test():
            for html_file in files:
                favicons = await self.favicon.from_file(html_file)
                icon = favicons[0]
                self.assertEqual(icon.type, FaviconType.DATA)
                # Ensure that save works correctly
                await icon.save()
                self.assertTrue(icon.path.exists())
                # Compare file content
                temp_file = Path(tempfile.NamedTemporaryFile().name)
                with temp_file.open('wb') as fd:
                    fd.write(icon.data)
                self.assertTrue(filecmp.cmp(temp_file, icon.path))

                # Remove the test file
                temp_file.unlink()
                icon.path.unlink()

        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
