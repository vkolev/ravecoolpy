from gi.repository import Granite


class AboutDialog(Granite.WidgetsAboutDialog):

	def __init__(self, window):
		super(AboutDialog, self).__init__(window)
		self.set_program_name("RaveCool")
		self.set_version("1.0a")
		self.set_comments("Application for endless music expirience")
		self.set_website("http://ravecool.bultux.org")
		self.set_website_label("ravecool @ bultux.org")
		self.show_all()