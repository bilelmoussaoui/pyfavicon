from pyfavicon import Favicon, FaviconType
from pathlib import Path
import pytest

favicon = Favicon()


@pytest.mark.asyncio
async def test_link_tag():
    files = [
        Path('./tests/html/url_icon_link.html'),
        Path('./tests/html/url_shortcut_icon_link.html'),
        Path('./tests/html/url_apple_touch_icon_precomposed_link.html'),
        Path('./tests/html/url_apple_touch_icon_link.html'),
        Path('./tests/html/url_fluid_icon_link.html'),
    ]

    for html_file in files:
        icons = await favicon.from_file(html_file,
                                                'https://github.com')
        assert len(icons) != 0
        icon = icons[0]
        
        assert icon.type is FaviconType.URL
        assert str(icon.link) == 'https://github.githubassets.com/favicon.ico'


@pytest.mark.asyncio
async def test_meta_tag():
    html_file = Path('./tests/html/meta_favicon.html')

    icons = await favicon.from_file(html_file, 'https://gitlab.com')
    assert len(icons) != 0

    icon = icons[0]

    assert icon.type is FaviconType.URL
    assert str(icon.link) == 'https://assets.gitlab-static.net/assets/msapplication-tile-1196ec67452f618d39cdd85e2e3a542f76574c071051ae7effbfde01710eb17d.png'


@pytest.mark.asyncio
async def test_largest_icon():
    html_file = Path('./tests/html/largest_gitlab.html')

    icons = await favicon.from_file(html_file)
    assert len(icons) != 0

    largest_icon = icons.get_largest()
    assert largest_icon

    assert largest_icon.size == (188, 188)
