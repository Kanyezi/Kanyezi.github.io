import os
class PathS:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # current_dir = os.path.join(current_dir, "pages/get_pachong/")
        
        data = {
            "root_path": "./data/",
            "users_path": "./data/users.json",
            "atcoder_path": "./data/atcoder/",
            "codeforces_path": "./data/codeforces/",
            "matiji_path": "./data/matiji/",
            "nowcoder_path": "./data/nowcoder/",
            "out_path": "./../public/all_data.json"
        }
        self.out_path = os.path.join(current_dir,data["out_path"])
        self.root_path = os.path.join(current_dir,data["root_path"])
        self.users_path = os.path.join(current_dir,data["users_path"])

        self.atcoder_path_contest =  os.path.join(current_dir,data["atcoder_path"]+"contest/")
        self.atcoder_path_user =  os.path.join(current_dir,data["atcoder_path"]+"user_problems/")
        
        self.codeforces_path_contest = os.path.join(current_dir,data["codeforces_path"]+"contest/")
        self.codeforces_path_user = os.path.join(current_dir,data["codeforces_path"]+"user_problems/")

        self.matiji_path_contest = os.path.join(current_dir,data["matiji_path"]+"contest/")
        self.matiji_path_user = os.path.join(current_dir,data["matiji_path"]+"user_problems/")

        self.nowcoder_path_contest = os.path.join(current_dir,data["nowcoder_path"]+"contest/")
        self.nowcoder_path_user = os.path.join(current_dir,data["nowcoder_path"]+"user_problems/")
    

if __name__ == "__main__":
    pc = PathS()
    print(pc.root_path)