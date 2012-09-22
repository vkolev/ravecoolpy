from gi.repository import Granite
from gi.repository import Gtk
from pyragechill import ragechill


class InfoDialog():

	def __init__(self, postID, songID):
		
		self.client = ragechill.RageChill()
		song = self.client.get_song_info(postID, songID)
		self.w = Granite.WidgetsLightWindow.new("%s by %s" % (song.title,
															song.artist))
		self.w.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.box = Gtk.VBox(False, 2)
		self.box.pack_start(self.make_image(song.image),
                False, True, 0)
		self.box.pack_start(self.add_row("Description:", song.description),
				False, True, 0)
		self.box.pack_start(self.add_row("Rage Level:", song.rageLevel),
				False, True, 0)
		self.box.pack_start(self.add_row_link("YouTube Link:", song.link),
						False, True, 0)
		self.w.add(self.box)
		self.w.show_all()
		
	def make_image(self, image_name): 
		return Gtk.Image().new_from_pixbuf(self.client.get_image_pixbuf(image_name))
	
	def add_row(self, title, content):
		box = Gtk.HBox(True, 2)
		markup_text = Gtk.Label("")
		markup_text.set_markup("<b>%s</b>" % title)
		box.pack_start(markup_text, False, True, 0)
		box.pack_start(Gtk.Label(content), False, True, 0)
		return box
	
	def add_row_link(self, title, link):
		box = Gtk.HBox(True, 2)
		markup_text = Gtk.Label("")
		markup_text.set_markup("<b>%s</b>" % title)
		box.pack_start(markup_text, False, True, 0)
		box.pack_start(Gtk.LinkButton(link, "Click to watch"), False, True, 0)
		return box