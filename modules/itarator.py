class CommandIterator:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.commands = []
        self.index = 0

    def add_command(self, command):
        self.commands.append(command)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.commands):
            command = self.commands[self.index]
            self.index += 1
            return command
        else:
            raise StopIteration
