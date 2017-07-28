from clld.web.assets import environment
from clldutils.path import Path

import grammaticon


environment.append_path(
    Path(grammaticon.__file__).parent.joinpath('static').as_posix(),
    url='/grammaticon:static/')
environment.load_path = list(reversed(environment.load_path))
