import os
import subprocess

import git
from modules.vcs import VCSInterface


class GIT(VCSInterface):
    def __init__(self, client_socket, database):
        self.client_socket = client_socket
        self.database = database
        self.vcs_type = 'git'

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

            if repo_path is None:
                repo_path = '..'

            command = ['git', 'add'] + files
            self.run_command(command, repo_path)
            message = f"Git: Added {', '.join(files)} to the index."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'add' command: {str(e)}\n".encode('utf-8'))

    def commit(self, repo_path, comment):
        try:
            command = ['git', 'commit', '-m', comment]
            self.run_command(command, repo_path)
            message = "Git: Changes committed successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'commit' command: {str(e)}\n".encode('utf-8'))

    def update(self, repo_path):
        try:
            if repo_path is None:
                repo_path = '..'

            command = ['git', 'pull']
            self.run_command(command, repo_path)
            message = "Git: Code updated successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'update' command: {str(e)}\n".encode('utf-8'))

    def push(self, repo_path):
        try:
            if repo_path is None:
                repo_path = '..'

            command = ['git', 'push']
            self.run_command(command, repo_path)
            message = "Git: Changes pushed successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'push' command: {str(e)}\n".encode('utf-8'))

    def init_repo(self, repository_name, repo_path):
        try:
            if repo_path is None:
                repo_path = '..'

            if not os.path.exists(os.path.join(repo_path, '.git')):
                command = ['git', 'init']
                self.run_command(command, repo_path)
                message = '[*] Git: Repository initialized successfully.'
                self.database.insert_repository(repository_name, "Git", repo_path)
                self.client_socket.sendall(message.encode('utf-8'))
            else:
                message = '[*] Git: Repository already exists.'
                self.client_socket.sendall(message.encode('utf-8'))

        except Exception as e:
            self.client_socket.sendall(f"Error executing 'init_repo' command: {str(e)}\n".encode('utf-8'))

    def log(self, repo_path):
        try:
            command = ['git', 'log', '--pretty=format:Commit: %H%nAuthor: %an <%ae>%nDate: %ad%nMessage: %s%n']
            log_output = self.run_command(command, repo_path)
            self.client_socket.sendall(log_output.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'log' command: {str(e)}\n".encode('utf-8'))

    def status(self, repo_path):
        if repo_path is None:
            repo_path = '..'
        os.chdir(repo_path)
        repo = git.Repo(repo_path)
        status_result = repo.git.status()
        self.client_socket.sendall(status_result.encode('utf-8'))

    def pull(self, repo_path):
        try:
            if repo_path is None:
                repo_path = '..'

            command = ['git', 'pull']
            self.run_command(command, repo_path)
            message = "Git: Changes pulled successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'pull' command: {str(e)}\n".encode('utf-8'))

    def fetch(self, repo_path):
        try:
            if repo_path is None:
                repo_path = '..'

            command = ['git', 'fetch']
            self.run_command(command, repo_path)
            message = "Git: Remote changes fetched successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'fetch' command: {str(e)}\n".encode('utf-8'))

    def list(self, repo_path):
        try:
            command = ['git', 'branch']
            branches_output = self.run_command(command, repo_path)
            message = f"Git Branches: {branches_output}"
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            error_message = f"Error executing 'list' command: {str(e)}\n"
            self.client_socket.sendall(error_message.encode('utf-8'))

    def patch(self, repo_path, patch_file):
        try:
            if repo_path is None:
                repo_path = '..'

            command_check = ['git', 'apply', '--check', patch_file]
            self.run_command(command_check, repo_path)

            command_apply = ['git', 'apply', patch_file]
            self.run_command(command_apply, repo_path)

            message = f"Git: Patch applied successfully from {patch_file}."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error applying patch: {str(e)}\n".encode('utf-8'))

    def branch(self, repo_path, branch_name):
        try:
            command = ['git', 'branch', branch_name]
            self.run_command(command, repo_path)
            message = f"Git: Branch '{branch_name}' created successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error creating branch: {str(e)}\n".encode('utf-8'))

    def merge(self, repo_path, branch_name):
        try:
            command = ['git', 'merge', branch_name]
            self.run_command(command, repo_path)
            message = f"Git: Merged branch '{branch_name}' successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error merging branch: {str(e)}\n".encode('utf-8'))

    def tag(self, repo_path, tag_name, commit_sha=None):
        try:
            if repo_path is None:
                repo_path = '..'

            if commit_sha:
                command = ['git', 'tag', tag_name, commit_sha]
            else:
                command = ['git', 'tag', tag_name]

            self.run_command(command, repo_path)
            message = f"Git: Tag '{tag_name}' created successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error creating tag: {str(e)}\n".encode('utf-8'))
