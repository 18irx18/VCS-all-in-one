from modules.gitt import GIT
from modules.mercurial import Mercurial
from modules.svn import SVN
from modules.vcs import VCSInterface


class VCSAdapter(VCSInterface):
    def __init__(self, client_socket,database, vcs_type):
        self.database = database
        self.vcs_type = vcs_type
        self.client_socket = client_socket

        if self.vcs_type == "git":
            self.vcs_impl = GIT(client_socket,database)
        elif self.vcs_type == "mercurial":
            self.vcs_impl = Mercurial(client_socket,database)
        elif self.vcs_type == "svn":
            self.vcs_impl = SVN(client_socket,database)
        else:
            raise ValueError(f"Unsupported VCS Type: {vcs_type}")

    def __getattribute__(self, item):
        return object.__getattribute__(self,item)

    def commit(self, repo_path, comment):
        self.vcs_impl.commit(repo_path, comment)

    def update(self, repo_path):
        self.vcs_impl.update(repo_path)

    def push(self, repo_path):
        self.vcs_impl.push(repo_path)

    def init_repo(self, repository_name, repo_path):
        self.vcs_impl.init_repo(repository_name, repo_path)

    def log(self, repo_path):
        self.vcs_impl.log(repo_path)

    def status(self, repo_path):
        self.vcs_impl.status(repo_path)

    def add(self, repo_path, files):
        self.vcs_impl.add(repo_path, files)

    def add_all(self,repo_path):
        self.vcs_impl.add_all(repo_path)