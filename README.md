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

Usage
-----

Basic result query example:

```sql
select results #>> '{myfield, agg}', count(1) from crowdflower.job_result where job_id = 123123;
```

Get all the judgments:

```sql
select jsonb_array_elements_text(fields #> '{myfield, res}') from crowdflower.job_judgment where job_id = 123123;
```
