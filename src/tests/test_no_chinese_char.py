import os.path
import re
from pathlib import Path


def test_readme_md():
    readme = Path(os.path.dirname(__file__)).parent.parent.joinpath('README.md').read_text(encoding='utf8')
    results = re.findall(r'[\u4e00-\u9fff]+', readme)
    assert len(results) == 0, f'Chinese characters in README.md: {results}'
