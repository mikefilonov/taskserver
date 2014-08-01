import imp
import importlib

class PluginManager(object):
	def __init__(self):
		self.plugin_dict = {}

	def load_plugins(self, path):
		f,p,d = imp.find_module(".", [path]) #load a module (directory, not file) by path
		plugins_module = imp.load_module("plugins", f,p,d) #sorry, the simpliest way

		for plugin_name in plugins_module.__all__:
			m = importlib.import_module("plugins.%s"%(plugin_name))
			m.register_plugin( self ) #should call plugin_manager.register(name, class) to put himself back to dict

	def register(self, plugin_name, plugin_class):
		self.plugin_dict[plugin_name] = plugin_class

	def get(self, plugin_name):
		return self.plugin_dict.get(plugin_name)

	def keys(self):
		return self.plugin_dict.keys()