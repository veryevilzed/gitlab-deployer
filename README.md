# POEditor Cli


Using .json or .yaml files
Only in Key-Value JSON files

## Instalation

```
New instalation:
pip install -e git+https://github.com/veryevilzed/poeditorcli.git#egg=poeditorcli

or

pip install -e git+git://github.com/veryevilzed/poeditorcli.git#egg=poeditorcli


Upgrade:
pip install -U -e git+https://github.com/veryevilzed/poeditorcli.git#egg=poeditorcli

or

pip install -U -e git+git://github.com/veryevilzed/poeditorcli.git#egg=poeditorcli

```




## Update all language

```
poeditorcli update --translation=lang_%s.json --project_id=(id) --api_token=(token)
```


## Update one language

```
poeditorcli update --translation=lang_%s.json --project_id=(id) --api_token=(token) --language=en
```


## Upload language

```
poeditorcli upload --translation=lang_en.json --project_id=(id) --api_token=(token) --language=en
```


