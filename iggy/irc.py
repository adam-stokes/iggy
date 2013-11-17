import os
from socket import gethostname

from circuits.io import stdin
from circuits import handler, Component
from circuits import __version__ as systemVersion
from circuits.net.sockets import TCPClient, Connect
from circuits.net.protocols.irc import IRC, PRIVMSG, USER, NICK, JOIN

class ServerConnect(Component):
    channel = "ircclient"

    def __init__(self, **kwds):
        self.nick = kwds.get('nick')
        self.ircchannel = kwds.get('ircchannel')
        self.server = kwds.get('server')
        self.serverpass = kwds.get('serverpass')
        self.ssl = kwds.get('ssl')
        self.port = kwds.get('port')
        self.hostname = gethostname()
        self += (TCPClient(channel=self.channel) + IRC(channel=self.channel))

    def ready(self, component):
        """Ready Event

        This event is triggered by the underlying ``TCPClient`` Component
        when it is ready to start making a new connection.
        """

        self.fire(Connect(self.host, self.port))

    def connected(self, host, port):
        """Connected Event

        This event is triggered by the underlying ``TCPClient`` Component
        when a successfully connection has been made.
        """

        print("Connected to %s:%d" % (host, port))

        nick = self.nick
        hostname = self.hostname
        name = "%s on %s using circuits/%s" % (nick, hostname, systemVersion)

        self.fire(USER(nick, hostname, host, name))
        self.fire(NICK(nick))

    def numeric(self, source, target, numeric, args, message):
        """Numeric Event

        This event is triggered by the ``IRC`` Protocol Component when we have
        received an IRC Numberic Event from server we are connected to.
        """

        if numeric == 1:
            self.fire(JOIN(self.ircchannel))
        elif numeric == 433:
            self.nick = newnick = "%s_" % self.nick
            self.fire(NICK(newnick))

    def join(self, source, channel):
        """Join Event

        This event is triggered by the ``IRC`` Protocol Component when a
        user has joined a channel.
        """

        if source[0].lower() == self.nick.lower():
            print("Joined %s" % channel)
        else:
            print("--> %s (%s) has joined %s" % (source[0], source, channel))

    def notice(self, source, target, message):
        """Notice Event

        This event is triggered by the ``IRC`` Protocol Component for each
        notice we receieve from the server.
        """

        print("-%s- %s" % (source[0], message))

    def message(self, source, target, message):
        """Message Event

        This event is triggered by the ``IRC`` Protocol Component for each
        message we receieve from the server.
        """

        if target[0] == "#":
            print("<%s> %s" % (target, message))
        else:
            print("-%s- %s" % (source, message))

    @handler("read", channel="stdin")
    def stdin_read(self, data):
        """Read Event (on channel ``stdin``)

        This is the event handler for ``read`` events specifically from the
        ``stdin`` channel. This is triggered each time stdin has data that
        it has read.
        """

        self.fire(PRIVMSG(self.ircchannel, data.strip()))
