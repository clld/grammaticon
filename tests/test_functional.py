from __future__ import print_function, unicode_literals

import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
