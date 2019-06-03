from pathlib import Path
from urllib.parse import urlparse
import asyncio
from pyfavicon import Favicon
from gi.repository import Gtk, GLib


def validate_url(url: str):
    url = urlparse(url)
    return all([url.scheme, url.netloc, url.path])


class Window(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("pyfavicon example")
        self.resize(400, 400)
        self.connect("destroy", Gtk.main_quit)

        spinner = Gtk.Spinner()
        image = Gtk.Image.new_from_icon_name("image-missing",
                                             Gtk.IconSize.DIALOG)
        image.set_valign(Gtk.Align.CENTER)
        image.set_halign(Gtk.Align.CENTER)

        stack = Gtk.Stack()
        stack.add_named(spinner, "loading")
        stack.add_named(image, "favicon")
        stack.set_visible_child_name("favicon")

        entry = Gtk.Entry()
        entry.set_valign(Gtk.Align.CENTER)
        entry.set_halign(Gtk.Align.CENTER)
        entry.connect("changed", self.__on_website_changed,
                      image, stack, spinner)
        entry.set_input_purpose(Gtk.InputPurpose.URL)

        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.props.expand = True
        container.pack_start(stack, False, False, 6)
        container.pack_start(entry, False, False, 6)

        self.add(container)

    def __on_website_changed(self, entry, image, stack, spinner):
        website = entry.get_text()
        if not validate_url(website):
            entry.get_style_context().add_class("error")
            return
        entry.get_style_context().remove_class("error")
        spinner.start()
        stack.set_visible_child_name("loading")

        async def set_largest_image(*args):
            favicon = Favicon(download_dir=Path('.'))
            icons = await favicon.from_url(website)
            largest = await icons.get_largest()
            assert largest
            await largest.save()
            image.set_from_file(str(largest.path))
            spinner.stop()
            stack.set_visible_child_name("favicon")

        def run(*args):
            try:
                asyncio.run(set_largest_image())
            except AssertionError:
                image.set_from_icon_name("image-missing")
                spinner.stop()
                stack.set_visible_child_name("favicon")
        GLib.idle_add(run, GLib.PRIORITY_DEFAULT_IDLE)


window = Window()
window.show_all()
window.present()
Gtk.main()
