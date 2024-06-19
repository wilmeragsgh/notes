import os
import fire

class MDIndex:
    """Generates a SUMMARY.md file for a directory of markdown files."""
    def __init__(self, directory: str = "./", target_file: str = "SUMMARY.md"):
        self.directory = directory
        self.target_file = target_file
        self.paths_dict = {}
    
    def generate(self):
        all_paths = list(filter(lambda x: all(map(lambda y: y[-3:] == '.md', x[2])) and len(x[2]) > 0, os.walk(self.directory)))
        for path in all_paths:
            self.paths_dict[path[0]] = {"files": path[2], "dirs": path[1]}
        tst_out = "\n".join(list(map(lambda x: self._parse_toc(0, x), list(self.paths_dict))))

        while "\n\n" in tst_out:
            tst_out = tst_out.replace("\n\n","\n")

        tst_out = tst_out.replace("\n* [", "\n\n* [")
        tst_out = f"# Table of contents\n\n{tst_out}"

        with open(self.target_file, "w") as f:
            f.write(tst_out)

    
    def _parse_toc(self, ident, key) -> str:
        root = f'{ident*4*" "}* [{key.split("/")[-1].replace(".md", "").capitalize()}]({key[2:]}/README.md)'
        try:
            current_val = self.paths_dict[key]
        except KeyError:
            return ""

        if len(current_val["files"]) > 0:
            files = "\n".join([f'{(ident+1)*4*" "}* [{fil.replace(".md","").capitalize().replace("-"," ").replace("_"," ")}]({key[2:]}/{fil})' for fil in current_val["files"] if fil != "README.md"])
            within_dirs = [root] + [files] + [self._parse_toc(ident+1, f"{key}/{new_key}") for new_key in current_val["dirs"]]
        else:
            within_dirs = [root] + [self._parse_toc(ident+1, f"{key}/{new_key}") for new_key in current_val["dirs"]]
        for dir_ in current_val["dirs"]:
            del self.paths_dict[key + "/" + dir_]

        if ident == 0:
            res_txt = "\n".join(within_dirs)
        else:
            res_txt = "\n".join(within_dirs)
        return res_txt
        
if __name__ == '__main__':
    fire.Fire(MDIndex)
