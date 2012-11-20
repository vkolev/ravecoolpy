from gi.repository import Gtk
from gi.repository import Granite
from gi.repository import Gdk, GdkPixbuf
from gi.repository import Pango
from pyragechill import ragechill
import lxml
import InfoDialog
import gst


class MainWindow:

    def __init__(self, path):
        self.playing = False
        self.client = ragechill.RageChill()
        self.welcome_removed = 0
        self.path = path
        self.rage_level = "2.5"
        builder = Gtk.Builder()
        builder.add_from_file(path + "/data/main_window.ui")
        builder.connect_signals(self)
        self.window = builder.get_object('RaveCool')
        self.window.set_icon_from_file(path + "/data/icons/ravecool.svg")
        self.toolbar = builder.get_object('toolbar1')
        self.searchbar = Granite.WidgetsSearchBar.new("Search listened tracks")
        self.searchbar.set_pause_delay(500)
        self.searchbar.connect('text-changed-pause', self.onSearchExecuted)
        self.slider = builder.get_object('scale1')
        self.playbutton = builder.get_object('toolbutton4')
        self.search_position_holder = builder.get_object("box2")
        self.add_search(self.searchbar)
        self.toolbar.insert(self.create_appmenu(), -1)
        self.box = builder.get_object("box1")
        self.box.pack_start(self.create_welcome(), True, True, 1)
        self.playlist = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str, str, str)
        self.playlistview = Gtk.TreeView(model=self.playlist)
        self.playlistview.set_headers_visible(False)
        self.playlistview.connect('row-activated', self.song_info)
        self.setup_playlist()
        self.playbin = gst.element_factory_make("playbin2",
                                                "player")
        self.bus = self.playbin.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_player_message)

    def create_welcome(self):
        self.welcome = Granite.WidgetsWelcome.new("RaveCool",
                                                  "Discover the endless music experience...")
        self.welcome.append("media-playback-start",
                            "Start",
                            "Start exploring the music")
        self.welcome.connect('activated', self.remove_welcome)
        return self.welcome

    def setup_playlist(self):
        renderer_pixbuf = Gtk.CellRendererPixbuf()
        renderer_pixbuf.set_fixed_size(72, 72)
        column_pixbuf = Gtk.TreeViewColumn("Cover", renderer_pixbuf)
        column_pixbuf.add_attribute(renderer_pixbuf, "pixbuf", 0)
        self.playlistview.append_column(column_pixbuf)

        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property('font-desc',
                                   Pango.FontDescription('Droid Sans bold 13'))
        column_text = Gtk.TreeViewColumn("Artist", renderer_text, text=1)
        self.playlistview.append_column(column_text)

        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property('font-desc',
                                   Pango.FontDescription('Droid Sans italic 10'))
        column_text = Gtk.TreeViewColumn("Title", renderer_text, text=2)
        self.playlistview.append_column(column_text)

    def song_info(self, sender, path, data=None):
        iter = self.playlist.get_iter(path)
        postID = self.playlist[iter][3]
        songID = self.playlist[iter][4]
        InfoDialog.InfoDialog(postID, songID)

    def show_all(self):
        self.window.show_all()

    def add_search(self, widget):
        self.search_position_holder.pack_start(self.searchbar, True, True, 0)

    def remove_welcome(self, sender, data=None):
        if self.welcome_removed is 0:
            self.box.remove(self.welcome)
            scrolledWindow = Gtk.ScrolledWindow()
            scrolledWindow.set_hexpand(False)
            scrolledWindow.set_vexpand(True)
            scrolledWindow.add(self.playlistview)
            self.playlistview.show()
            scrolledWindow.show()
            self.box.pack_start(scrolledWindow, True, True, 1)
            self.welcome_removed = 1
            self.onPlayClicked(self.welcome)

    def external_remove(sender):
        self.remove_welcome(self, sender, data=None)

    def create_appmenu(self):
        menu = Gtk.Menu.new()
        about_item = Gtk.MenuItem.new_with_label("About")
        about_item.connect('activate', self.onShowAbout)
        quit_item = Gtk.MenuItem.new_with_label("Quit")
        quit_item.connect('activate', self.onQuitApp)
        menu.append(about_item)
        menu.append(quit_item)
        appmenu = Granite.WidgetsAppMenu.new(menu)
        return appmenu

    def on_player_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.playbin.set_state(gst.STATE_NULL)
            self.playing = False
            self.onPlayClicked(None, None, True)
        elif t == gst.MESSAGE_ERROR:
            self.playing = False
            self.playbin.set_state(gst.STATE_NULL)

    def onShowAbout(self, sender, data=None):
        about = Granite.WidgetsAboutDialog.new()
        about.set_program_name("RaveCool")
        about.set_comments(
            """Desktop Application for endless music expirience""")
        about.set_website("http://ravecool.bultux.org")
        about.set_help("http://ravecool.bultux.org/help")
        about.set_translate("http://ravecool.bultux.org/translate")
        about.set_bug("http://ravecool.bultux.org/bugs")
        about.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(self.path
                                                              + "/data/icons/ravecool_128.png", 128, 128))
        about.set_website_label("RaveCool @ BulTux.Org")
        about.set_version("1.0a")
        about.run()
        about.destroy()

    def onSearchExecuted(self, sender, data):
        print data

    def onQuitApp(self, sender, data=None):
        Gtk.main_quit()

    def onDestroyWindow(self, sender):
        Gtk.main_quit()

    def onDeleteWindow(self, sender, data=None):
        Gtk.main_quit()

    def onSearchEnter(seld, sender, data=None):
        print sender.get_text()

    def onRageChange(self, sender, data=None):
        test = "%.1f" % sender.get_value()
        if test is not self.rage_level:
            self.rage_level = test
            self.playing = False
            self.playbin.set_state(gst.STATE_NULL)
            self.onPlayClicked(sender, None)

    def onPlayClicked(self, sender, data=None, go=False):
        if self.playing == False:
            if self.welcome_removed is 0:
                self.remove_welcome(sender, data)
                self.welcome_removed = 1
            song = self.client.get_song(rageLevel=self.rage_level)
            image = self.client.get_image_pixbuf(
                song.post.image).scale_simple(72,
                                              72,
                                              GdkPixbuf.InterpType.NEAREST)
            self.playlist.prepend([image,
                                   str(song.post.title),
                                   str(song.post.artist),
                                   str(song.post.postID),
                                   str(song.post.songID)])
            self.playbin.set_property('uri',
                                      self.client.get_song_stream(song.post.songID))
            self.playbin.set_state(gst.STATE_PLAYING)
            self.window.set_title(
                "%s by %s" % (song.post.title, song.post.artist))
            self.playbutton.set_icon_name("media-playback-stop")
            self.playing = True
        else:
            if go == True:
                self.playbin.set_state(gst.STATE_NULL)
                self.onPlayClicked(sender, None, True)
            else:
                self.playbin.set_state(gst.STATE_NULL)
                self.playing = False
                self.playbutton.set_icon_name("media-playback-start")
                self.window.set_title("RaveCool")

    def onNextClicked(self, sender, data=None):
        self.playbin.set_state(gst.STATE_NULL)
        self.playing = False
        self.onPlayClicked(sender, None, True)
