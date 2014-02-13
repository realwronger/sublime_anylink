import sublime, sublime_plugin
import re, os, webbrowser

WINDOWS_PATH_PATTERN = re.compile(r"[a-zA-Z]:\\\S+")

settings = sublime.load_settings("anylink.sublime-settings")

URL_PREFIX = settings.get("url_prefix")

STACK_BACK = []
STACK_FORWARD = []

def getSelectedContents(self):
	result = []
	for region in self.view.sel(): 
		if region.empty():
			line = self.view.line(region)
			result.append(self.view.substr(line))
		else:
			result.append(self.view.substr(region))
	return result

def getCurrentFile():
	return sublime.active_window().active_view().file_name()

def gotoFileOrFolder(content):
	paths = WINDOWS_PATH_PATTERN.findall(content)
	for path in paths:
		if (os.path.isfile(path)):
			if (getCurrentFile() == path):
				print "Ignore goto self"
				break
			print "Current File: %s" % getCurrentFile()
			STACK_BACK.append(getCurrentFile())
			del STACK_FORWARD[:]
			print "Open file: %s" % path
			sublime.active_window().open_file(path)
		elif (os.path.isdir(path)):
			print "Open dir: %s" % path
			webbrowser.open(path)

def gotoUrl(content):
	for urlPrefix in URL_PREFIX:
		urlPattern = r"%s://\S+" % urlPrefix
		links = re.findall(urlPattern, content);
		for link in links:
			print "Open Browser: %s" % link
			webbrowser.open(link, 1)

class AnylinkGotoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		contents = getSelectedContents(self)
		for content in contents:
			print "Content: %s" % content
			gotoFileOrFolder(content)
			gotoUrl(content)

class AnylinkBackCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if (len(STACK_BACK) > 0):
			print "Forward append: %s" % getCurrentFile()
			STACK_FORWARD.append(getCurrentFile())
			backFile = STACK_BACK.pop()
			print "Back pop: %s" % backFile
			sublime.active_window().open_file(backFile)
		else:
			print "No back file"

class AnylinkForwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if (len(STACK_FORWARD) > 0):
			print "Back append: %s" % getCurrentFile()
			STACK_BACK.append(getCurrentFile())
			forwardFile = STACK_FORWARD.pop()
			print "Forward pop: %s" % forwardFile
			sublime.active_window().open_file(forwardFile)
		else:
			print "No forward file"
