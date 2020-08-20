import jupsource
import sys
import os
import json


if __name__ == "__main__":
    print("ARGS ARE", sys.argv)
    if len(sys.argv) < 3:
        print("Usage: python -m jupsource [notebook.ipynb] [output.py]")
    else:
        with open(sys.argv[1], "r") as rf:
            content = json.load(rf)
        ext = os.path.splitext(sys.argv[2])[1]
        if ext in jupsource.comments:
            with open(sys.argv[2], "w") as f:
                f.writelines(jupsource.convert_to_script(content, jupsource.comments[ext]))
        else:
            print("Unknown comment syntax for", ext, "files")
