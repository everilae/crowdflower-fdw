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

Install [Multicorn](http://multicorn.org) and create foreign server and table
definitions.

```sql
create extension multicorn;

create server crowdflower_srv foreign data wrapper multicorn options (
        wrapper 'crowdflower_fdw.factory'
);

create foreign table cf_job_result (
        job_id integer,
        id integer,
        created_at timestamp without time zone,
        updated_at timestamp without time zone,
        judgments_count integer,
        agreement float,
        missed_count integer,
        state character varying
        data jsonb,
        results jsonb,
) server crowdflower_srv options (
        key 'YOURCFAPIKEY',
	type 'jobreport'
);

create foreign table cf_job_judgment (                                                                      
	job_id integer,
	updated_at timestamp without time zone,
	agreement float,
	ids integer[],
	state character varying
	fields jsonb,
) server crowdflower_srv options (
	key 'YOURCFAPIKEY',
	type 'jobjudgment'
);
```
