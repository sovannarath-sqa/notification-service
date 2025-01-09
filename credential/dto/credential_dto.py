class CredentialDTO:

    def __init__(self, username, password, channel, channel_id, reservations):
        self.username = username
        self.password = password
        self.channel = channel
        self.channel_id = channel_id
        self.reservations = reservations
