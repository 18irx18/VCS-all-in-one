class VCSInterface:

    def __getattribute__(self, item):
        if item == 'send_message':
            raise NotImplementedError('This interface is not intended for direct use')
        else:
            object.__getattribute__(self,item)

    def commit(self, repo_path, comment):pass

    def update(self, repo_path):pass

    def push(self, repo_path):pass

    def init_repo(self, repository_name, repo_path):pass

    def log(self, repo_path):pass

    def status(self, repo_path):pass

    def add(self, repo_path, files):pass

    def add_all(self,repo_path):pass

    def pull(self, repo_path):pass

    def fetch(self, repo_path):pass

    def list(self, repo_path):pass

    def patch(self, repo_path, patch_file):pass

    def branch(self, repo_path, branch_name):pass

    def merge(self, repo_path, branch_name):pass

    def tag(self, repo_path, tag_name, commit_sha=None):pass


