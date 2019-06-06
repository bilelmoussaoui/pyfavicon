from pyfavicon import Favicon, FaviconType
from pathlib import Path
import filecmp
import tempfile
import pytest


favicon = Favicon(download_dir=Path(tempfile.gettempdir()))
html_file = Path('./tests/html/base64_favicon_link.html')


@pytest.mark.asyncio
async def test_base64_type():
    favicons = await favicon.from_file(html_file)
    icon = favicons[0]
    assert icon.type is FaviconType.DATA


@pytest.mark.asyncio
async def test_base64_size():
    favicons = await favicon.from_file(html_file)
    icon = favicons[0]

    assert icon.size == (16, 16)


@pytest.mark.asyncio
async def test_base64_extension():
    favicons = await favicon.from_file(html_file)
    icon = favicons[0]

    assert icon.extension == 'ico'


@pytest.mark.asyncio
async def test_base64_save():
    favicons = await favicon.from_file(html_file)
    icon = favicons[0]

    await icon.save()
    assert icon.path.exists()

    # Compare file content
    temp_file = Path(tempfile.NamedTemporaryFile().name)
    with temp_file.open('wb') as fd:
        fd.write(icon.data)
    assert filecmp.cmp(temp_file, icon.path)

    # Remove the test file
    temp_file.unlink()
    icon.path.unlink()
