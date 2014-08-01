import SocketServer, json, uuid, sys

from taskmanager import TaskManager
from pluginmanager import PluginManager


if len(sys.argv) == 3:
    port = int(sys.argv[1])
    plugin_path = sys.argv[2]
else:
    raise Exception("Usage: %s path_to_plugin_dir"%sys.argv[0])


def debug( message ):
	print message 


tm = TaskManager()
pm = PluginManager()
pm.load_plugins(plugin_path)

class PluginTCPHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        processor_dict = {"start": self.command_start, "status": self.command_status}
        data = self.rfile.readline()
        
        debug(">"+data)
        
        try:
            command = json.loads(data)
            
            command_name = command.get("command", "")
            command_callable = processor_dict.get(command_name, self.command_not_found)
            
            result = command_callable(command)
            
            json_result = json.dumps(result)
            debug( "<" + json_result )
            self.wfile.write(json_result)
            
        except Exception, ex:
            self.wfile.write(json.dumps(ex.message))
            raise

        finally:
            self.wfile.close()

    def command_not_found(self, arguments):
        return "Command not found"

    def command_start(self, arguments):
        task_name = arguments.get("task")
        task_arguments = arguments.get("arguments")
        
        task_class = pm.get(task_name)
        task = task_class(task_arguments)
        id = tm.put(task)

        return str(id)

    def command_status(self, arguments):
        id = uuid.UUID(arguments["id"])
        task = tm.get(id)
        if task is None:
            return "Job not found"
        
        status = task.status
        progress, message = task.progress()

        return [status, progress, message]

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", port

    tm.start()

    server = ThreadedTCPServer((HOST, PORT), PluginTCPHandler)
    server.serve_forever()
