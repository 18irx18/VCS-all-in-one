from modules.adapters import VCSAdapter
class VCSFA:
    def create_vcs(self, client_socket,vcs_type, database):
        return VCSAdapter(client_socket,database, vcs_type)