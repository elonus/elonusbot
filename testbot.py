# -*- coding: utf-8 -*-
import socket
from time import sleep

def ping(data):
    irc.send( "PONG " + data.split() [ 1 ] + "\r\n" )

def answer(data, message):
    """
    sends message to channel or user depending on where it is from
    """
    sender = data.split("!")[0].strip(":")
    destination = data.split()[2]

    if destination[0] == "#":
        irc.send( "PRIVMSG " + destination + " :" + message + "\r\n")

    else:
        irc.send( "PRIVMSG " + sender + " :" + message + "\r\n")

network = "irc.freenode.net"
port = 6667
irc = socket.socket (socket.AF_INET, socket.TCP_NODELAY)
irc.connect ( ( network, port ) )
data = irc.recv ( 4096 )
print(data)

irc.send ( "NICK ElonusBot\r\n" )
irc.send ( "USER ElonusBot ElonusBot ElonusBot :Elonus testbot\r\n" )
sleep(2)
irc.send ( "PRIVMSG NickServ: identify gutta4197\r\n")

data = irc.recv(4096)
if data.find("PING"):
    ping(data)
irc.send ( "JOIN #elenusbottest\r\n" )
sleep(2)
irc.send ( "PRIVMSG #elenusbottest :Hello.\r\n" )
#irc.send("PRIVMSG elonus :test\r\n")

while True:
    data = irc.recv(4096).strip("\r\n")
    print(data)

    if data.find("PING") != -1:
        ping(data)

    elif data.find("PRIVMSG") != -1:
        message = data.split(":")[2]
        sender = data.split("!")[0].strip(":")
        message = message.capitalize()
        if str(message) == "Hello":
            answer(data, "hello " + sender)
