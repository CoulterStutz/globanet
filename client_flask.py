from flask import Flask

callsign = ''

class Server:
  def __init__(self, port, data_path="/data"):
    self.port = port
    self.datapath = datapath
    
    self.app = Flask()
    
  def run():
    @app.route("/")
    def index_page():
      return f"Hello World from {callsign}"
    
    self.app.run(port=port)
