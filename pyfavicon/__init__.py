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

__all__ = ['Favicon', 'FaviconType', 'Icon', 'Icons']


LINK_RELS = [
    'icon',
    'shortcut icon',
    'apple-touch-icon',
    'apple-touch-icon-precomposed',
    'fluid-icon'
]
META_NAMES = [
    'msapplication-TileImage'
]

TAGS = [
    {'name': 'link', 'attrs': {'rel': LINK_RELS, 'href': True}, 'attr': 'href'},
    {'name': 'meta', 'attrs': {'name': META_NAMES, 'content': True}, 'attr': 'content'}
]


async def a_max(liste, attr):
    max_elem = liste[0]
    max_val = await getattr(max_elem, attr)
    for elem in liste:
        val = await getattr(elem, attr)
        if val > max_val:
            max_val = val
            max_elem = elem
    return max_elem


def parse_base64_icon(data: str) -> bytes:
    if data:
        _, data = data.split(":")
        mimetype, data = data.split(",")
        data = urllib.parse.unquote_to_bytes(data)
        assert mimetype.endswith('base64')
        return binascii.a2b_base64(data)
    return None


class FaviconType(Enum):
    URL = 0
    DATA = 1


class Icon:
    '''
    The Icon object

    Attributes:
        size (int, int) : The dimensions of the favicon

        extension (str) : The icon extension, .png, .ico...

        type (FaviconType) : Whether the icon scheme is of type data or not.

        link (yarl.URL) : The favicon URL

        data (bytes) : The favicon image content
    '''

    def __init__(self, **kwargs):
        self.link = kwargs.get("link")
        self._size = None
        self.extension = kwargs.get("extension")
        # If the icon of type FaviconType.DATA
        self.data = parse_base64_icon(kwargs.get("data"))
        self._path = None

        self.type = FaviconType.DATA if self.data else FaviconType.URL

        # self._parse_extension()
        self._generate_icon_name(kwargs.get('website_url'))

    @staticmethod
    def new(source: str, url: yarl.URL):
        '''
        Create a new Icon from the source tag content.

        Args:
            source (str) : The source tag content;

            url (yarl.URL) : The website URL

        Returns:
            Icon
        '''
        parsed_url = urllib.parse.urlparse(source)
        if parsed_url.scheme != 'data':
            fav_url = None
            # Missing scheme
            if not parsed_url.netloc:
                if parsed_url.path.startswith(':'):
                    fav_url = yarl.URL(url.scheme + parsed_url.path)
                else:
                    p = '/' + \
                        parsed_url.path.lstrip(
                            '../').lstrip('../').lstrip('./').lstrip('/')
                    fav_url = yarl.URL.build(host=url.host,
                                             path=p)
            # Link look fine
            elif parsed_url.netloc:
                fav_url = yarl.URL.build(host=parsed_url.netloc,
                                         path=parsed_url.path)
            if parsed_url.scheme:
                fav_url = fav_url.with_scheme(parsed_url.scheme)
            else:
                fav_url = fav_url.with_scheme(url.scheme)
            return Icon(link=fav_url, website_url=url)
        else:  # Data scheme:
            return Icon(data=source, website_url=url)

    @property
    async def size(self):
        image = None
        if self._size:
            return self._size
        image_content = b''
        if os.path.exists(self.path):
            with open(self.path, 'rb') as fp:
                image_content = fp.read()
        else:
            if self.type is FaviconType.DATA:
                image_content = self.data
            else:
                async with aiohttp.ClientSession() as session:
                    response = await session.get(self.link,
                                                 headers=Favicon.HEADERS)
                    async for chunck in response.content.iter_chunked(1024):
                        if not chunck:
                            break
                        image_content += chunck

        with ImageFile.Parser() as image_parser:
            image_parser.feed(image_content)
            image = image_parser.image
            if image:
                self._size = image.size
        return self._size

    @property
    def path(self) -> str:
        return self._path

    def __str__(self):
        return str(self.link)

    async def save(self):
        '''Save the icon

        You can retrieve the favicon cached path using the path property.
        '''
        if os.path.exists(self._path):
            return

        file_content = b''
        if self.type is FaviconType.DATA:
            file_content = self.data
        else:
            async with aiohttp.ClientSession() as session:
                response = await session.get(self.link,
                                             headers=Favicon.HEADERS)
                async for chunck in response.content.iter_chunked(128):
                    if not chunck:
                        break
                    file_content += chunck

        assert file_content

        with open(self.path, 'wb') as fd:
            fd.write(file_content)

    def _parse_extension(self):
        pass

    def _generate_icon_name(self, website_url: yarl.URL) -> str:
        '''
        Generate an icon name

        Args:
            website_url (yarl.URL): The website url

        Returns:
            str, the icon name
        '''
        # If we don't have a base64 data image.
        from tempfile import NamedTemporaryFile, gettempdir
        if website_url:
            image_name = website_url.host
        else:
            image_name = os.path.basename(NamedTemporaryFile().name)
        if self._size:
            image_name += '_{}x{}'.format(self._size, self._size)

        if self.type is not FaviconType.DATA:
            image_name += os.path.basename(self.link.path)

        if Favicon.DOWNLOAD_DIR:
            self._path = Favicon.DOWNLOAD_DIR.joinpath(image_name)
        else:
            self._path = os.path.join(gettempdir(), image_name)


class Icons:
    '''
    Icons, contains a lot of Icon.
    '''

    def __init__(self, **kwargs):
        self._data = []
        self._current = 0

    async def get_largest(self, extension: str = None) -> Icon:
        '''Get the largest icon

        Args:
            extension (str) : The required extension

        Returns:
            Icon
        '''
        icons = self._data
        if extension:
            icons = list(filter(lambda icon: icon.extension == extension,
                                icons))
        if icons:
            largest = await a_max(icons, 'size')
            return largest
        return None

    def append(self, icon: Icon):
        self._data.append(icon)

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


class Favicon:
    '''
    The favicon manager object

    Args:
            download_dir (pathlib.Path) : The location to save the icons on

            headers (dict) : The headers to send with each request
    '''
    DOWNLOAD_DIR = None
    HEADERS = {}

    def __init__(self, download_dir: pathlib.Path = None,
                 headers={}):
        Favicon.HEADERS = headers
        Favicon.DOWNLOAD_DIR = download_dir

    async def from_url(self, url: str) -> Icons:
        '''Fetch all the favicons from a URL

        Args:
            url (str) : The website url to load the favicons from

        Returns:
            Icons
        '''
        # Read the html content of the page async
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url, headers=Favicon.HEADERS)
            html_content = await resp.text()
            favicons = await self._find_favicons_links(html_content,
                                                       resp.url)
            return favicons
        return Icons()

    async def from_html(self, html_content: str, website_url: str = None) -> Icons:
        '''Fetch all the favicons from an HTML content

        Args:
            html_content (str) : The HTML content.

            website_url (str) : The website url, the source of the HTML file

        Returns:
            Icons
        '''
        website_url = yarl.URL(website_url) if website_url else None
        favicons = await self._find_favicons_links(html_content,
                                                   website_url)
        return favicons

    async def from_file(self, html_file: pathlib.Path, website_url: str = None) -> Icons:
        '''Fetch all the favicons from an HTML file.

        Args:
            html_file (pathlib.Path) : The HTML file path.

            website_url (str) : The website url, the source of the HTML file

        Returns:
            Icons
        '''
        with html_file.open() as f:
            html_content = f.read()
        favicons = await self.from_html(html_content, website_url)
        return favicons

    async def _find_favicons_links(self, html_content: str,
                                   url: yarl.URL = None) -> Icons:
        '''Find the favicon links in a parsed HTML content/

        Args:
            html_content (str) : The HTML content.

            url (yarl.URL) : The website url, the source of the HTML content

        Returns:
            Icons
        '''

        bsoup = bs4.BeautifulSoup(html_content, features="html.parser")

        icons = Icons()
        _added = []

        for tag in TAGS:
            sources = bsoup.find_all(tag['name'], attrs=tag['attrs'])
            for elem in sources:
                icon = Icon.new(elem.attrs[tag['attr']], url=url)
                if icon.link not in _added:
                    icons.append(icon)
                    _added.append(icon.link)
        return icons
