import os
import subprocess
from modules.vcs import VCSInterface


class SVN(VCSInterface):
    def __init__(self, client_socket, database):
        self.client_socket = client_socket
        self.database = database
        self.vcs_type = 'svn'

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

            svn_add_command = ['svn', 'add'] + files
            self.run_command(svn_add_command, repo_path)
            message = f"SVN: Added {', '.join(files)} to the repository."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'svn add' command: {str(e)}\n")

    def add_all(self, repo_path):
        try:
            svn_add_command = ['svn', 'add', '--force', '.']
            self.run_command(svn_add_command, repo_path)
            message = "SVN: Added all changes to the repository."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'add_all' command: {str(e)}\n")

    def commit(self, repo_path, comment):
        try:
            if comment is None:
                comment = "Default commit message"

            svn_commit_command = ['svn', 'commit', '-m', comment]
            self.run_command(svn_commit_command, repo_path)
            message = "SVN: Changes committed successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'commit' command: {str(e)}\n")

    def update(self, repo_path):
        try:
            svn_update_command = ['svn', 'update', '.']
            self.run_command(svn_update_command, repo_path)
            message = "SVN: Code updated successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'update' command: {str(e)}\n")

    def push(self, repo_path):
        try:
            message = ("SVN: Pushing changes is not supported in SVN. \n"
                       "You should use 'svn commit' to commit your changes to the repository.")
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'push' command: {str(e)}\n")

    def init_repo(self, repository_name, repo_path):
        try:
            if not os.path.exists(os.path.join(repo_path, '.svn')):
                svn_checkout_command = ['svn', 'checkout', repository_name, '.']
                self.run_command(svn_checkout_command, repo_path)
                message = "SVN: Repository initialized successfully."
            else:
                message = "SVN: Repository already exists."

            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'init' command: {str(e)}\n")

    def log(self, repo_path):
        try:
            svn_log_command = ['svn', 'log', '--verbose']
            log_output = self.run_command(svn_log_command, repo_path)
            self.client_socket.sendall(log_output.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'log' command: {str(e)}\n")

    def status(self, repo_path):
        try:
            svn_status_command = ['svn', 'status']
            status_output = self.run_command(svn_status_command, repo_path)
            self.client_socket.sendall(status_output.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'status' command: {str(e)}\n")

    def pull(self, repo_path):
        try:
            svn_pull_command = ['svn', 'update']
            self.run_command(svn_pull_command, repo_path)
            message = "SVN: Pull operation completed successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'pull' command: {str(e)}\n")

    def fetch(self, repo_path):
        try:
            svn_fetch_command = ['svn', 'update']
            self.run_command(svn_fetch_command, repo_path)
            message = "SVN: Fetch operation completed successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'fetch' command: {str(e)}\n")

    def list(self, repo_path):
        try:
            svn_list_command = ['svn', 'list']
            list_output = self.run_command(svn_list_command, repo_path)
            message = f"SVN repository contents:\n{list_output}"
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'list' command: {str(e)}\n")

    def patch(self, repo_path, patch_file_path):
        try:
            svn_patch_command = ['svn', 'patch', patch_file_path]
            self.run_command(svn_patch_command, repo_path)
            message = f"SVN: Applied patch from '{patch_file_path}' successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'patch' command: {str(e)}\n")

    def branch(self, repo_path, branch_name):
        try:
            svn_branch_command = ['svn', 'copy', repo_path, branch_name]
            self.run_command(svn_branch_command, repo_path)
            message = f"SVN: Created branch '{branch_name}' successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'branch' command: {str(e)}\n")

    def merge(self, repo_path, branch_name):
        try:
            svn_merge_command = ['svn', 'merge', branch_name]
            self.run_command(svn_merge_command, repo_path)
            message = f"SVN: Merged changes from branch '{branch_name}' successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'merge' command: {str(e)}\n")

    def tag(self, repo_path, tag_name):
        try:
            svn_tag_command = ['svn', 'copy', repo_path, tag_name]
            self.run_command(svn_tag_command, repo_path)
            message = f"SVN: Created tag '{tag_name}' successfully."
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.client_socket.sendall(f"Error executing 'tag' command: {str(e)}\n")
