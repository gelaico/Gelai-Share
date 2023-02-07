# gelai-sharing
Peer to Peer file sharing application. Use via command line
Host files to share in home branch /repo

To host a server run:
python3 gelai-server.py

Give the ip address of your computer and the port number generated to someone to give them files
The server will generate a log file, .gelai_log that will keep track of all IP addresses that use your server and what files they take

To connect to the server run:
python3 gelai-client.py serverIpAddress serverPortNumber

Follow in-app instructions to choose what files to save
