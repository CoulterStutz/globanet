import os
client_path = os.path("/client")

if not client_path.exists():
    os.mkdir("/client")

os.system("curl https://raw.githubusercontent.com/coulterminer/globanet/main/client/client.py >> client.py")
os.system("curl https://raw.githubusercontent.com/coulterminer/globanet/main/client/chain_explorer.py >> chain_explorer.py")
os.system("curl https://raw.githubusercontent.com/coulterminer/globanet/main/client/references.py >> references.py")

os.system("python client.py")
