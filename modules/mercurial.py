import os
import subprocess
from modules.vcs import VCSInterface


class Mercurial(VCSInterface):
    def __init__(self, client_socket, database):
        self.client_socket = client_socket
        self.database = database
        self.vcs_type = 'mercurial'

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def run_command(self, command, repo_path):
        try:
            result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_message = f"Error executing '{' '.join(e.cmd)}' command: {e.stderr}\n"
            self.client_socket.sendall(error_message.encode('utf-8'))

    def add(self, repo_path, files):
        try:
            if files is None:
                files = ['.']
            elif not isinstance(files, list):
                files = [files]

            command = ['hg', 'add'] + files
            self.run_command(command, repo_path)
            message = f"Mercurial: Added {', '.join(files)} to the repository."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'add' command: {str(e)}\n".encode('utf-8'))

    def add_all(self, repo_path):
        try:
            command = ['hg', 'add', '-A']
            self.run_command(command, repo_path)
            message = "Mercurial: Added all changes to the repository."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'add_all' command: {str(e)}\n".encode('utf-8'))

    def commit(self, repo_path, comment):
        try:
            if comment is None:
                comment = "Default commit message"

            command = ['hg', 'commit', '-m', comment]
            self.run_command(command, repo_path)
            message = "Mercurial: Changes committed successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'commit' command: {str(e)}\n".encode('utf-8'))

    def update(self, repo_path):
        try:
            command_status = ['hg', 'status', '-q']
            status_result = self.run_command(command_status, repo_path)

            if status_result:
                message = "Mercurial: Local changes exist. Cannot update."
            else:
                command_pull = ['hg', 'pull']
                self.run_command(command_pull, repo_path)
                message = "Mercurial: Code updated successfully."

            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'update' command: {str(e)}\n".encode('utf-8'))

    def push(self, repo_path):
        try:
            command_status = ['hg', 'status', '-q']
            status_result = self.run_command(command_status, repo_path)

            if status_result:
                message = "Mercurial: Local changes exist. Cannot push."
            else:
                command_push = ['hg', 'push']
                self.run_command(command_push, repo_path)
                message = "Mercurial: Changes pushed successfully."

            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.send_message(f"Error executing 'push' command: {str(e)}\n".encode('utf-8'), self.vcs_type, repo_path)

    def init_repo(self, repository_name, repo_path):
        try:
            if not os.path.exists('.hg'):
                command_init = ['hg', 'init']
                self.run_command(command_init, repo_path)
                message = "Mercurial: Repository initialized successfully."
            else:
                message = "Mercurial: Repository already exists."

            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'init' command: {str(e)}\n".encode('utf-8'))

    def log(self, repo_path):
        try:
            command_log = ['hg', 'log', '--template',
                           'Changeset: {node|short}\nAuthor: {author} <{email}>\nDate: {date|shortdate}\nMessage: {desc}\n']
            log_output = self.run_command(command_log, repo_path)
            self.client_socket.sendall(log_output.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'log' command: {str(e)}\n".encode('utf-8'))

    def status(self, repo_path):
        try:
            command_status = ['hg', 'status']
            status_result = self.run_command(command_status, repo_path)
            self.client_socket.sendall(status_result.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'status' command: {str(e)}\n".encode('utf-8'))

    def pull(self, repo_path):
        try:
            command_pull = ['hg', 'pull']
            self.run_command(command_pull, repo_path)
            message = "Mercurial: Pull operation completed successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'pull' command: {str(e)}\n".encode('utf-8'))

    def fetch(self, repo_path):
        try:
            command_fetch = ['hg', 'fetch']
            self.run_command(command_fetch, repo_path)
            message = "Mercurial: Fetch operation completed successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'fetch' command: {str(e)}\n".encode('utf-8'))

    def list(self, repo_path):
        try:
            command_branch = ['hg', 'branches']
            branches_output = self.run_command(command_branch, repo_path)
            message = f"Mercurial branches: {branches_output}"
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.send_message(f"Error executing 'list' command: {str(e)}\n".encode('utf-8'))

    def patch(self, repo_path, patch_file_path):
        try:
            command_apply = ['hg', 'import', patch_file_path]
            self.run_command(command_apply, repo_path)
            message = f"Mercurial: Applied patch from '{patch_file_path}' successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'patch' command: {str(e)}\n".encode('utf-8'))

    def branch(self, repo_path, branch_name):
        try:
            command_branch = ['hg', 'branch', branch_name]
            self.run_command(command_branch, repo_path)
            message = f"Mercurial: Created branch '{branch_name}' successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'branch' command: {str(e)}\n".encode('utf-8'))

    def merge(self, repo_path, branch_name):
        try:
            command_update = ['hg', 'update', branch_name]
            self.run_command(command_update, repo_path)

            command_merge = ['hg', 'merge']
            self.run_command(command_merge, repo_path)

            message = f"Mercurial: Merged branch '{branch_name}' successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'merge' command: {str(e)}\n".encode('utf-8'))

    def tag(self, repo_path, tag_name):
        try:
            command_tag = ['hg', 'tag', tag_name]
            self.run_command(command_tag, repo_path)
            message = f"Mercurial: Created tag '{tag_name}' successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'tag' command: {str(e)}\n".encode('utf-8'))
