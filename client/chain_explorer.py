from flask import Flask
import json

peer_data_file = None # get configuration json code
chunks = []

port = 3000

def get_chain_data():
  for x in open(peer_data_file, "r").readlines():
    chunks.append(x)
    
app = Flask()
@app.route("/")
def show_chunks():
  out = str()
  for x in chunks:
    out = out + '\n' + x
    return out
 
app.run('0.0.0.0', port)
