from gi.repository import Gtk
from gi.repository import Granite
from gi.repository import GdkPixbuf

class MainWindow:

	def __init__(self, path):
		self.path = path
		builder = Gtk.Builder()
		builder.add_from_file(path+"/data/main_window.ui")
		builder.connect_signals(SignalHandler())
		self.window = builder.get_object('RaveCool')
		self.toolbar = builder.get_object('toolbar1')
		self.toolbar.insert(self.create_appmenu(), -1)

	def show_all(self):
		self.window.show_all()

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

	def onShowAbout(self, sender, data=None):
		about = Granite.WidgetsAboutDialog.new()
		about.set_program_name("RaveCool")
		about.set_comments("""Desktop Application for endless music expirience""")
		about.set_website("http://ravecool.bultux.org")
		about.set_logo(
			GdkPixbuf.Pixbuf.new_from_file_at_size(self.path+"/data/icons/ravecool_128.png", 128, 128)
			)
		about.set_website_label("RaveCool @ BulTux.Org")
		about.set_version("1.0a")
		about.run()
		about.destroy()

	def onQuitApp(self, sender, data=None):
		Gtk.main_quit()

class SignalHandler:

	def onDestroyWindow(self, sender):
		Gtk.main_quit()

	def onDeleteWindow(self, sender, data=None):
		Gtk.main_quit()

	def onSearchEnter(seld, sender, data=None):
		print sender.get_text()

	def onRageChange(self, sender, data=None):
		print "Rage level changed to %.1f" % sender.get_value()

	def onPlayClicked(self, sender, data=None):
		print "Play Button clicked"

	def onNextClicked(self, sender, data=None):
		print "Next Button clicked"
		

	def onVolumeChanged(self, sender, data=None):
		print "Volume changed to: %f" % data
