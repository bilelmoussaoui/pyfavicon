import unittest
import asyncio
from pyfavicon import Favicon


GITLAB_FAVICONS = {
    'https://about.gitlab.com/ico/favicon.ico': (32, 32),
    'https://about.gitlab.com/ico/favicon-192x192.png': (190, 175),
    'https://about.gitlab.com/ico/favicon-160x160.png': (158, 145),
    'https://about.gitlab.com/ico/favicon-96x96.png': (95, 87),
    'https://about.gitlab.com/ico/favicon-16x16.png': (16, 14),
    'https://about.gitlab.com/ico/favicon-32x32.png': (32, 29),
    'https://about.gitlab.com/ico/apple-touch-icon-57x57.png': (57, 57),
    'https://about.gitlab.com/ico/apple-touch-icon-114x114.png': (114, 114),
    'https://about.gitlab.com/ico/apple-touch-icon-72x72.png': (72, 72),
    'https://about.gitlab.com/ico/apple-touch-icon-144x144.png': (144, 144),
    'https://about.gitlab.com/ico/apple-touch-icon-60x60.png': (60, 60),
    'https://about.gitlab.com/ico/apple-touch-icon-120x120.png': (120, 120),
    'https://about.gitlab.com/ico/apple-touch-icon-76x76.png': (76, 76),
    'https://about.gitlab.com/ico/apple-touch-icon-152x152.png': (152, 152),
    'https://about.gitlab.com/ico/apple-touch-icon-180x180.png': (180, 180),
}


class HTMLTest(unittest.TestCase):

    def setUp(self):
        self.favicon = Favicon()

    def test_icon_sizes(self):
        async def run_test():
            favicons = await self.favicon.from_url('https://gitlab.com')
            for icon in favicons:
                icon_size = await icon.size
                self.assertEqual(GITLAB_FAVICONS[str(icon.link)], icon_size)
        asyncio.run(run_test())
