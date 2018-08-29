# encryptedChatRoom
An encrypted chat room 

An encrypted chat room using RSA and AES encrption methods.
    Uses RSA to exchange the private keys for the AES
    Once private keys exchanged the clients will use AES to communicate with eachother

    Messages are always encrypted the server never sees the raw message.

    To Run:
        Change the ip address and the port for the sever and the clients
        Run the server
        Run a client, you must wait for the client to stop loading before you can send a message this is becuase the client is requesting the AES key from the server
        Once loading is finished you may chat with any other clients in the chat room.
