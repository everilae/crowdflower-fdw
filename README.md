CrowdFlower Foreign Data Wrapper
================================

CrowdFlower API v1 foreign data wrapper for PostgreSQL.

Installation
------------

Install the python package. It must be accessible to PostgreSQL, so the easiest
way is to install it globally.

```bash
git clone https://github.com/everilae/crowdflower-fdw.git
cd crowdflower-fdw
python setup.py install
```

Install [Multicorn](http://multicorn.org) and install the extensions.

```bash
make -C extension install
```

In your database run the following commands.

```sql
create extension plpgsql;
create extension multicorn;
create extension crowdflowerfdw;
select crowdflower.set_api_key('YOURAPIKEY');
```
