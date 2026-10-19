# Releasing the Grammaticon webapp

```shell
git clone https://github.com/clld/grammaticon
git clone https://github.com/clld/grammaticon-data
cd grammaticon
pip install -e .[test]
```

Recreate the database:
```shell
clld initdb development.ini
```

```shell
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO grammaticon > grammaticon.sql
zip grammaticon.sql.zip grammaticon.sql
rm grammaticon.sql
```
