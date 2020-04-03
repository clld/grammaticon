import pathlib

from clld.web.assets import environment

import grammaticon


environment.append_path(
    str(pathlib.Path(grammaticon.__file__).parent.joinpath('static')),
    url='/grammaticon:static/')
environment.load_path = list(reversed(environment.load_path))
