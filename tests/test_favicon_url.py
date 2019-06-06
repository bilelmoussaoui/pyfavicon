from pyfavicon import Favicon
import pytest

CASES = [
    ('<link rel="icon" href="/favicon.ico">', 'https://gitlab.com/favicon.ico'),
    ('<link rel="icon" href="://gitlab.com/favicon.ico">',
     'https://gitlab.com/favicon.ico'),
    ('<link rel="shortcut icon" type="image/png" href="/uploads/-/system/appearance/favicon/1/GnomeLogoVertical.svg.png">',
     'https://gitlab.com/uploads/-/system/appearance/favicon/1/GnomeLogoVertical.svg.png'),
    ('<link rel="shortcut icon" href="images/favicon.png">', 'https://gitlab.com/images/favicon.png'),
    ('<link rel="icon" href="/Areas/FirstTech.Web/Assets/images/apple-touch-icon-144x144.png">',
     'https://gitlab.com/Areas/FirstTech.Web/Assets/images/apple-touch-icon-144x144.png'),
    ('<link rel="shortcut icon" href="favicon.ico" />', 'https://gitlab.com/favicon.ico')
]

favicon = Favicon()


@pytest.mark.asyncio
async def test_favicon_url():
    for html_content, expected_result in CASES:
        icons = await favicon.from_html(html_content,
                                        "https://gitlab.com")

        assert len(icons) != 0
        assert str(icons[0].link) == expected_result

