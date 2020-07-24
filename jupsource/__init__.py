from notebook.services.contents.largefilemanager import LargeFileManager
import subprocess as sp
import json
import os
import os.path
import datetime
import pyjq
import textwrap

dir_path = os.path.dirname(__file__)
to_py = pyjq.compile(open(os.path.join(dir_path, "to_py.jq"), "r").read())
from_py_path = os.path.join(dir_path, "from_py.jq")

comments = {
    ".py": "#",
    ".jl": "#",
    ".hs": "--"
}

metadata = {
    ".py": {
      "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
      },
      "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.8.0"
      }
    },

    ".jl": {
      "kernelspec": {
        "display_name": "Julia 1.4.1",
        "language": "julia",
        "name": "julia-1.4"
      },
      "language_info": {
        "file_extension": ".jl",
        "mimetype": "application/julia",
        "name": "julia",
        "version": "1.4.0"
      }
    }
}

class TextFileManager(LargeFileManager):
    def save(self, model, path):
        path = path.strip("/")
        ext = os.path.splitext(path)[1]
        if "type" in model and model["type"] == "notebook" and ext in metadata:
            with open(path, "w") as f:
                os.environ["COMMENT"] = comments[ext]
                result = to_py.first(model["content"])
                str_results = []
                for a in result:
                    if a["wrapit"]:
                        str_results.append("\n".join([comments[ext] + " " + l for l in textwrap.wrap(
                            a["source"], width=78)]))
                    else:
                        str_results.append(a["source"])
                f.writelines("\n\n".join(str_results))
            statbuf = os.stat(path)
            name = os.path.basename(path)
            last_modified = datetime.datetime.fromtimestamp(statbuf.st_mtime)
            created = datetime.datetime.fromtimestamp(statbuf.st_ctime)
            size = statbuf.st_size
            return dict(
                name=name,
                path=path,
                size=size,
                created=created,
                last_modified=last_modified,
                mimetype=None,
                writable=True,
                format=None,
                content=None,
                type="notebook",
            )
        else:
            return super().save(model, path)

    def get(self, path, **kwargs):
        path = path.strip("/")
        ext = os.path.splitext(path)[1]
        if "type" in kwargs and kwargs["type"] == "notebook" and ext in metadata:
            statbuf = os.stat(path)
            name = os.path.basename(path)
            last_modified = datetime.datetime.fromtimestamp(statbuf.st_mtime)
            created = datetime.datetime.fromtimestamp(statbuf.st_ctime)
            size = statbuf.st_size
            if "content" in kwargs and kwargs["content"]:
                os.environ["CLEN"] = str(len(comments[ext]))
                with sp.Popen(
                    ["jq", "-s", "-R", "-f", from_py_path, path], stdout=sp.PIPE
                ) as proc:
                    content = json.load(proc.stdout)
                    content["metadata"] = metadata[ext]
                    print("Content is", content)
            else:
                content = None
            result = {
                "format": "json",
                "type": "notebook",
                "writable": True,
                "name": name,
                "path": path,
                "created": created,
                "last_modified": last_modified,
                "mimetype": None,
                "size": size,
                "content": content,
            }
        else:
            result = super().get(path, **kwargs)
            if "type" in result and result["type"] == "file":
                if "name" in result and result["name"].endswith(".py"):
                    result["type"] = "notebook"
        return result
