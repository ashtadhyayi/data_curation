[![Build Status](https://travis-ci.org/ashtadhyayi/data_curation.svg?branch=master)](https://travis-ci.org/ashtadhyayi/data_curation)

## doc curation

A package for curating doc file collections, with ability to sync with youtube and archive.org doc items. 



# For contributors

## Contact

Have a problem or question? Please head to [github](https://github.com/ashtadhyayi/data_curation).

## Packaging

* ~/.pypirc should have your pypi login credentials.
```
python setup.py bdist_wheel
twine upload dist/* --skip-existing
```

## Build documentation
- sphinx html docs can be generated with `cd docs; make html`

## Testing
Run `pytest` in the root directory.

## Auxiliary tools
- [![Build Status](https://travis-ci.org/ashtadhyayi/data_curation.svg?branch=master)](https://travis-ci.org/ashtadhyayi/data_curation)
- [![Documentation Status](https://readthedocs.org/projects/doc_curation/badge/?version=latest)](http://doc_curation.readthedocs.io/en/latest/?badge=latest)
- [pyup](https://pyup.io/account/repos/github/ashtadhyayi/data_curation/)