import logging
import socket
import threading
from config.config import db_name, SI, file_log
from db.database import DataBase
from modules.facade import VCSF
from modules.factories import VCSFA
from modules.itarator import CommandIterator
from modules.visitor import Executor
from utils.utils import show_active_repositories, find_free_port


def handle_peer(client_socket, db):
    client_socket.sendall(b"Choose a VCS type (git, mercurial, svn), write 'sar' to show active repositories, or 'exit' to quit.")
    while True:
        command = client_socket.recv(1024).decode('utf-8').strip()
        if command.lower() in ["git", "svn", "mercurial"]:
            vcs_type = command.lower()
            client_socket.sendall(b"Enter path to " + vcs_type.encode('utf-8') + b" repository: ")
            repo_path = client_socket.recv(1024).decode('utf-8').strip()
            adapter = VCSFA().create_vcs(client_socket, vcs_type, db)
            facade = VCSF(adapter)
            process_vcs_commands(client_socket, facade, vcs_type, repo_path, db)
        elif command.lower() == "sar":
            show_active_repositories(db, client_socket)
        elif command.lower() == "exit":
            client_socket.sendall(b"Exiting...\n")
            break
        else:
            client_socket.sendall(b"Invalid command. Please enter 'git', 'svn', 'mercurial', or 'exit'.\n")



def process_vcs_commands(client_socket, facade, vcs_type, repo_path, db):
    client_socket.sendall(f"[{vcs_type} [{repo_path}]]".encode('utf-8'))
    command_iterator = CommandIterator(client_socket)
    command_executor = Executor()

    while True:
        command = client_socket.recv(1024).decode('utf-8').strip()
        if command.lower() == "back":
            handle_peer(client_socket, db)
        else:
            command_iterator.add_command(command)
            for cmd in command_iterator:
                command_executor.visit(client_socket, vcs_type, cmd, facade, repo_path)


def start_client_peer():
    port = find_free_port()
    if port is None: return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SI, port))
    try:
        data = client_socket.recv(4096).decode('utf-8')
        print(data)
        while True:
            command = input('[-]')
            client_socket.sendall(command.encode('utf-8'))
            data = client_socket.recv(4096).decode('utf-8')
            print(data)
            if command.lower() == "exit":
                break
    finally:
        client_socket.close()

def handle_client_peer_wrapper(client_socket):
    try:
        db = DataBase(db_name)
        db.create_tables()
        handle_peer(client_socket, db)
    except (ConnectionAbortedError, ConnectionResetError) as exp:
        logging.error(f"Connection reset: {exp}")
    finally:
        client_socket.close()

def start_server_peer():
    logging.basicConfig(filename= file_log, level=logging.INFO)
    free_port = find_free_port()

    if free_port is None: return
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SI, free_port))
    server_socket.listen(1)
    logging.info(f"Server started on port {free_port}. Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        logging.info(f"Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client_peer_wrapper, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server_peer)
    server_thread.start()
    client_thread = threading.Thread(target=start_client_peer)
    client_thread.start()
    server_thread.join()
    client_thread.join()
