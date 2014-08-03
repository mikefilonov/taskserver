import json, sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

from taskmanager import TaskManager
from pluginmanager import PluginManager

tm = TaskManager()
pm = PluginManager()

class ManagerRESTHandler(BaseHTTPRequestHandler):
 
 	def do_GET(self):
 		taskid, cmd = self.path.lstrip('/').split('/')


 		task = tm.get(taskid)

 		if not task or cmd not in ["status", "answer"]:
 			return self.do_notfound()

 		if cmd == "status":
 			answer = [task.status] + list(task.progress())

 		if cmd == "answer":
 			answer = task.answer()
 			if task.is_finished():
 				tm.remove(taskid)

 		json_answer = json.dumps(answer)

 		self.send_response(200)
		self.send_header("Content-type", "text/json")
		self.send_header("Content-Length", len(json_answer))
		self.end_headers()
		self.wfile.write( json_answer )
		self.rfile.close()
		self.wfile.close()

	def do_notfound(self):
		json_answer = 'Not found'
 		self.send_response(404)
		self.send_header("Content-type", "text/json")
		self.send_header("Content-Length", len(json_answer))
		self.end_headers()
		self.wfile.write( json_answer )
		self.rfile.close()
		self.wfile.close()
 	

	def do_POST(self):

		try:
			cmd, plugin = self.path.lstrip('/').split('/')

			content_length = int(self.headers.get('Content-Length', 0))
			if content_length:
				content = self.rfile.read(content_length)
				arguments = json.loads(content)
			else:
				arguments = None
			
			task_class = pm.get(plugin)
			task = task_class(arguments)

			if cmd == 'queue':
				answer = tm.put(task)
			elif cmd == 'execute':
				task.execute()
				answer = task.answer()

			json_answer = json.dumps(answer)

			self.send_response(200)
			self.send_header("Content-type", "text/json")
			self.send_header("Content-Length", len(json_answer))
			self.end_headers()
			self.wfile.write( json_answer )
			self.rfile.close()
			self.wfile.close()

		except Exception, ex:
			self.send_response(500)
			self.send_header("Content-type", "text/json")
			self.end_headers()
			self.wfile.write(json.dumps(ex.message))
			self.wfile.close()
			raise
			
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""



if __name__ == "__main__":
	if len(sys.argv) == 3:
	    port = int(sys.argv[1])
	    plugin_path = sys.argv[2]
	else:
	    raise Exception("Usage: %s path_to_plugin_dir"%sys.argv[0])
	

	pm.load_plugins(plugin_path)
	tm.start()

	server = ThreadedHTTPServer(('', port), ManagerRESTHandler)
	server.serve_forever()