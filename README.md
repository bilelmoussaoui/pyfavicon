# pyfavicon

[![Build Status](https://travis-ci.org/bilelmoussaoui/pyfavicon.svg)](https://travis-ci.org/bilelmoussaoui/pyfavicon)
[![Coverage Status](https://coveralls.io/repos/github/bilelmoussaoui/pyfavicon/badge.svg)](https://coveralls.io/github/bilelmoussaoui/pyfavicon)
[![https://pypi.org/project/pyfavicon/](https://img.shields.io/pypi/v/pyfavicon.svg)](https://pypi.org/project/pyfavicon/)
[![https://pypi.org/project/pyfavicon/](https://img.shields.io/pypi/pyversions/pyfavicon.svg)](https://pypi.org/project/pyfavicon/)
[![https://bilelmoussaoui.github.io/pyfavicon/](https://img.shields.io/badge/-docs-blue.svg)](https://bilelmoussaoui.github.io/pyfavicon/)


Async favicon fetcher


### Requirements
- `Python 3.7`
- `aiohttp`
- `beautifulsoup4`
- `Pillow`

### How to use 

```python
from pyfavicon import Favicon
import asyncio
from pathlib import Path


async def download_favicon():
    favicon_manager = Favicon(download_dir=Path('.'), 
                             headers={'DNT': '1'})

    icons = await favicon_manager.from_url('https://gitlab.com')
    # icons = await favicon_manager.from_file('my_html_file.html')
    # icons = await avicon_manager.from_html('<link rel="icon" href="favicon.png">')
    for icon in icons:
        # We use PIL to get the exact size of images.
        icon_size = await icon.size
        print("Favicon from : {}".format(icon.link))
        print("Favicon export name : {}".format(icon.path))
        print("Favicon size : {}".format(icon_size))
    # Select the largest icon
    largest_icon = await icons.get_largest()
    await largest_icon.save()

asyncio.run(download_favicon())
```

### Examples
You can find a bunch of usage examples here: 
- [Gtk Application](examples/gtk_app.py)