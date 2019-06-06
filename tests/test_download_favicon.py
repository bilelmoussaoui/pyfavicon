from pyfavicon import Favicon
from pathlib import Path
import tempfile
import pytest

favicon = Favicon(download_dir=Path(tempfile.gettempdir()))


@pytest.mark.asyncio
async def test_icon_download():
    icons = await favicon.from_url('https://gitlab.com')
    for icon in icons:
        await icon.save()
        assert icon.path.exists()
        
        icon.path.unlink()
