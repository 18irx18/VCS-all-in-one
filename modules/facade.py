class VCSF:
    def __init__(self, vcs_adapter):
        self.adapter = vcs_adapter

    def commit_changes(self, repo_path, comment):
        self.adapter.commit(repo_path, comment)

    def update_repository(self, repo_path):
        self.adapter.update(repo_path)

    def push_changes(self, repo_path):
        self.adapter.push(repo_path)

    def initialize_repository(self, repository_name, repo_path):
        self.adapter.init_repo(repository_name, repo_path)

    def view_commit_history(self, repo_path):
        self.adapter.log(repo_path)

    def view_repository_status(self, repo_path):
        self.adapter.status(repo_path)

    def add_files(self, repo_path, files):
        self.adapter.add(repo_path, files)

    def add_all_changes(self, repo_path):
        self.adapter.add_all(repo_path)

    def apply_patch(self, repo_path, patch_file_path):
        self.adapter.patch(repo_path, patch_file_path)

    def create_branch(self, repo_path, branch_name):
        self.adapter.branch(repo_path, branch_name)

    def merge_branch(self, repo_path, branch_name):
        self.adapter.merge(repo_path, branch_name)

    def create_tag(self, repo_path, tag_name):
        self.adapter.tag(repo_path, tag_name)

    def list(self, repo_path):
        self.adapter.list(repo_path)
