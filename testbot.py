import socket
from time import sleep

functions = {".math" : "argument arithmetic", "hello" : "noargument hello"} 

def ping(data):
    irc.send( "PONG " + data.split() [ 1 ] + "\r\n" )

def argument(data):
    arg = ""
    for i in data.split(":")[2].split()[1:]:
        arg += i

    return(arg) 


def send(data, message):
    """
    sends message to channel or user depending on where it is from
    """
    sender = data.split("!")[0].strip(":")
    destination = data.split()[2]

    if destination[0] == "#":
        irc.send( "PRIVMSG " + destination + " :" + message + "\r\n")

    else:
        irc.send( "PRIVMSG " + sender + " :" + message + "\r\n")


def hello(data):
    sender = data.split("!")[0].strip(":")
    answer = "Hello " + sender + "!"
    send(data, answer)


def arithmetic(data):
    
    expression = argument(data)
    condition = "0123456789+-/*.()"
    newexpression = ""
    for i in expression:
        if i in condition:
            newexpression += str(i)

    if ("**" in newexpression):
        answer = "You tried to use a power. Unfortunately I do not have that functionnality at the moment."
    if (len(newexpression) > 15):
        answer = "Your expression was too long. I only accept expressions up to 15 characters long."

    else:

        try:
            answer = eval("1.0 * " + newexpression)
        except ZeroDivisionError:
            answer = "Error! You tried to divide by zero"
        except SyntaxError:
            answer = "Error! Invalid input"

    send(data, "The answer to " + expression + " is: " + str(answer))


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

while True:
    data = irc.recv(4096).strip("\r\n")
    print(data)

    if data.find("PING") != -1:
        ping(data)

    elif data.find("PRIVMSG") != -1:
        message = data.split(":")[2]
        codeword = message.split()[0]
        codeword = codeword.lower()
        sender = data.split("!")[0].strip(":")
        
        data2 = str(data)

        if codeword in functions:

            if functions[codeword].split()[0] == "argument":
                try:
                    message.split()[1]

                except IndexError:
                    send(data, codeword + " expects an argument")

                else:
                    eval(functions[codeword].split()[1] + "('" + data2 + "')")

            else:
                eval(functions[codeword].split()[1] + "('" + data2 + "')")



"""
        if codeword == "Hello":
            send(data, "hello " + sender)

        elif
        
        try:
             message.split()[1]

        except IndexError:
             send(data, "This function needs an argument")

        else:
             for 
"""
