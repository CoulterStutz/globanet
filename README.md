# Python based global AWS network

### Commands 
|   Command           |             What it does                        |  Implemented  |
|---------------------|-------------------------------------------------|---------------|
| echo                | Repeats something on the peers side             |      Yes      |
| cmd                 | Runs the request as a command in command prompt |      Yes      |
| areyouawake         | Checks if a peer is awake                       |      Yes      |             
| response            | Standard peer response                          |      Yes      |
| cloud-translate     | Translates messages into languages              |      No       |

### Current Locations
| Location  | Country       | Continent     | Status             |
|-----------|---------------|---------------|--------------------|
| Oregon    | United States | North America | :white_check_mark: |
| Ohio      | United States | North America | :white_check_mark: |
| Quebec    | Canada        | North America | :white_check_mark: |
| Frankfurt | Germany       | Eroupe        | :white_check_mark: |
| Stockholm | Sweden        | Eroupe        | :white_check_mark: |
| Mumbai    | India         | Asia          | :white_check_mark: |
| Tokyo     | Japan         | Asia          | :white_check_mark: |
| Sydney    | Australia     | South Asia    | :white_check_mark: |


## Script Glossery
| Script             | Usage                                                                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| server.py          | bundles it all together and enforces blockchain esc peer syncing + is a homebase for the network                                             |
| client.py          | The client script that allows clients to connect on to the network                                                                           |
| peer_management.py | Is a server tool for starting and stopping all ec2 instances                                                                                 |
