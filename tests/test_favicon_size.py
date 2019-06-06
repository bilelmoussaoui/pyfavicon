from pyfavicon import Favicon
import pytest

GITLAB_FAVICONS = {
    'https://about.gitlab.com/ico/favicon.ico': (-1, -1),
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
    'https://about.gitlab.com/ico/mstile-144x144.png': (144, 144)
}

favicon = Favicon()


@pytest.mark.asyncio
async def test_icon_size():
    icons = await favicon.from_url('https://gitlab.com')
    assert len(icons) != 0

    for icon in icons:
        assert GITLAB_FAVICONS[str(icon.link)] == icon.size

    largest = icons.get_largest(extension='png')
    assert largest.size == (190, 175)
    assert largest.extension == 'png'
