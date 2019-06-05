"""
 Copyright © 2019 Bilal Elmoussaoui <bil.elmoussaoui@gmail.com>

 This file is part of pyfavicon.

 pyfavicon is free software: you can redistribute it and/or
 modify it under the terms of the GNU General Public License as published
 by the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 pyfavicon is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with pyfavicon. If not, see <http://www.gnu.org/licenses/>.
"""
__title__ = 'pyfavicon'
__version__ = '0.0.1'
__author__ = 'Bilal Elmoussaoui'
__license__ = 'MIT'

import os
import bs4
import binascii
import aiohttp
import yarl
import pathlib
from enum import Enum
import urllib
from PIL import ImageFile

__all__ = ['Favicon', 'FaviconType']


LINK_RELS = [
    'icon',
    'shortcut icon',
    'apple-touch-icon',
    'apple-touch-icon-precomposed',
    'fluid-icon'
]


async def send_request(url, session: aiohttp.ClientSession, **kwargs):
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    return resp


async def a_max(liste, attr):
    max_elem = liste[0]
    max_val = await getattr(max_elem, attr)
    for elem in liste:
        val = await getattr(elem, attr)
        if val > max_val:
            max_val = val
            max_elem = elem
    return max_elem


def parse_base64_icon(data: str):
    if data:
        _, data = data.split(":")
        mimetype, data = data.split(",")
        data = urllib.parse.unquote_to_bytes(data)
        if mimetype.endswith("base64"):
            return binascii.a2b_base64(data)
    return None


class FaviconType(Enum):
    URL = 0
    DATA = 1


class Icon:

    def __init__(self, **kwargs):
        self.link = kwargs.get("link")
        self._size = None
        self.extension = kwargs.get("extension")
        # If the icon of type FaviconType.DATA
        self.data = parse_base64_icon(kwargs.get("data"))
        self._path = None

        self.type = FaviconType.DATA if self.data else FaviconType.URL

        self.__parse_extension()
        self.__generate_icon_name(kwargs.get('website_url'))

    def __str__(self):
        return "{}  - Size: {}".format(self.link, self._size)

    @property
    async def size(self):
        image = None
        if self._size:
            return self._size
        with ImageFile.Parser() as image_parser:
            if self.type == FaviconType.DATA:
                image_parser.feed(self.data)
                image = image_parser.image
            else:
                buffer = b''
                async with aiohttp.ClientSession() as session:
                    response = await session.get(self.link,
                                                 headers=Favicon.HEADERS)
                    async for chunck in response.content.iter_chunked(1024):
                        if not chunck:
                            break
                        buffer += chunck

                    image_parser.feed(buffer)
                if image_parser.image:
                    image = image_parser.image
        if image:
            self._size = image.size
        return self._size

    @staticmethod
    def new_from_tag(link_tag: bs4.element.Tag, url: yarl.URL):
        parsed_url = urllib.parse.urlparse(link_tag.attrs['href'])
        print(parsed_url)
        if parsed_url.scheme != 'data':
            fav_url = None
            # Missing scheme
            if not parsed_url.netloc and parsed_url.path.startswith(':'):
                fav_url = yarl.URL(url.scheme + parsed_url.path)
            # Absolute path
            elif not parsed_url.netloc:
                fav_url = yarl.URL.build(host=url.host,
                                         scheme=url.scheme,
                                         path=parsed_url.path)
            # Link look fine
            elif parsed_url.netloc:
                fav_url = yarl.URL.build(scheme=parsed_url.scheme,
                                         host=parsed_url.netloc,
                                         path=parsed_url.path)
            # Data scheme:
            print(fav_url)
            return Icon(link=fav_url, website_url=url)
        else:
            return Icon(data=link_tag.attrs['href'], website_url=url)

    @property
    def path(self) -> str:
        return self._path

    async def save(self):
        """

        """
        if os.path.exists(self._path):
            return
        if self.type == FaviconType.DATA:
            with open(self.path, 'wb') as fd:
                fd.write(self.data)
        else:
            async with aiohttp.ClientSession() as session:
                response = await session.get(self.link,
                                             headers=Favicon.HEADERS)
                with open(self.path, 'wb') as fd:
                    async for chunck in response.content.iter_chunked(128):
                        if not chunck:
                            break
                        fd.write(chunck)

    def __parse_extension(self):
        pass

    def __generate_icon_name(self, website_url: yarl.URL) -> str:
        # If we don't have a base64 data image.
        from tempfile import NamedTemporaryFile, gettempdir
        if website_url:
            image_name = website_url.host
        else:
            image_name = os.path.basename(NamedTemporaryFile().name)
        if self._size:
            image_name += '_{}x{}'.format(self._size, self._size)

        if self.type != FaviconType.DATA:
            image_name += os.path.basename(self.link.path)
        if Favicon.DOWNLOAD_DIR:
            self._path = Favicon.DOWNLOAD_DIR.joinpath(image_name)
        else:
            self._path = os.path.join(gettempdir(), image_name)


class IconsList:

    def __init__(self, **kwargs):
        self._data = []
        self._current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current >= len(self._data):
            raise StopIteration
        else:
            current = self._data[self._current]
            self._current += 1
            return current

    def __str__(self):
        return str(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def append(self, icon: Icon):
        self._data.append(icon)

    async def get_largest(self, extension=None) -> Icon:
        icons = self._data
        if extension:
            icons = list(filter(lambda icon: icon.extension == extension,
                                icons))
        if icons:
            largest = await a_max(icons, 'size')
            return largest
        return None


class Favicon:
    DOWNLOAD_DIR = None
    HEADERS = {'DNT': '1'}

    def __init__(self, download_dir: pathlib.Path = None,
                 headers={'DNT': '1'}):
        Favicon.HEADERS = headers
        Favicon.DOWNLOAD_DIR = download_dir

    async def from_url(self, url: str) -> IconsList:
        """

        """
        # Read the html content of the page async
        async with aiohttp.ClientSession() as session:
            resp = await send_request(url, session, headers=Favicon.HEADERS)
            html_content = await resp.text()
            favicons = await self.__find_favicons_links(html_content,
                                                        resp.url)
            return favicons
        return IconsList()

    async def from_html(self, html_content: str, website_url: yarl.URL = None) -> IconsList:
        favicons = await self.__find_favicons_links(html_content,
                                                    website_url)
        return favicons

    async def from_file(self, html_file: pathlib.Path, website_url: yarl.URL = None) -> IconsList:
        with html_file.open() as f:
            html_content = f.read()
        favicons = await self.from_html(html_content, website_url)
        return favicons

    async def __find_favicons_links(self, html_content: str,
                                    url: yarl.URL = None) -> IconsList:
        bsoup = bs4.BeautifulSoup(html_content, features="html.parser")
        icons = IconsList()
        _added = []
        for rel in LINK_RELS:
            link_tags = bsoup.find_all('link', attrs={
                'rel': rel,
                'href': True})
            for link_tag in link_tags:
                icon = Icon.new_from_tag(link_tag, url=url)
                if icon.link not in _added:
                    icons.append(icon)
                    _added.append(icon.link)
        return icons
