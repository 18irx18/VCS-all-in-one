import os
import socket
from colorama import Fore, Style
from config.config import SI, server_ports


def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((SI, port)) != 0

def find_free_port():
    for port in server_ports:
        if is_port_free(port):
            return port
    return None
def help(client_socket):
    help_message = (
        "Available commands:\n"
        "  - commit [comment]: Commit changes to the repository.\n"
        "  - update: Update the repository.\n"
        "  - push: Push changes to the remote repository.\n"
        "  - help: Display this help message.\n"
        "  - init [repository_name]: Initialize a new repository.\n"
        "  - log: View commit history.\n"
        "  - status: View repository status.\n"
        "  - add [file1, file2, ...]: Add specific files to the staging area.\n"
        "  - add_all: Add all changes to the staging area.\n"
        "  - back: Return to the main menu.\n"
    )
    client_socket.sendall(help_message.encode('utf-8'))


def show_active_repositories(database, client_socket):
    repositories = database.fetch_active_repositories()

    if repositories:
        response = Fore.RED + "Active Repositories:" + Style.RESET_ALL + "\n"
        for name, vcs_type, repo_path in repositories:
            response += f"Name: {name}, VCS Type: {vcs_type}, Path: {repo_path}\n"

            if vcs_type == "Git":
                if not os.path.exists(os.path.join(repo_path, '.git')):
                    response += Fore.RED + f"Repository at {repo_path} does not exist. Removing from the database." + Style.RESET_ALL + "\n"
                    database.remove_repository(name)
            elif vcs_type == "Mercurial":
                if not os.path.exists(os.path.join(repo_path, '.hg')):
                    response += Fore.RED + f"Repository at {repo_path} does not exist. Removing from the database." + Style.RESET_ALL + "\n"
                    database.remove_repository(name)
            elif vcs_type == "SVN":
                if not os.path.exists(os.path.join(repo_path, '.svn')):
                    response += Fore.RED + f"Repository at {repo_path} does not exist. Removing from the database." + Style.RESET_ALL + "\n"
                    database.remove_repository(name)
            else:
                response += Fore.RED + f"Unsupported VCS Type: {vcs_type}" + Style.RESET_ALL + "\n"

        client_socket.sendall(response.encode('utf-8'))
    else:
        client_socket.sendall((Fore.RED + "No active repositories found." + Style.RESET_ALL + "\n").encode('utf-8'))

