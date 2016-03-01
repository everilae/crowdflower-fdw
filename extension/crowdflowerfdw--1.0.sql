create server crowdflower_srv foreign data wrapper multicorn options (
	wrapper 'crowdflower_fdw.factory'
);

create foreign table job_result (
	job_id integer,
	id integer,
	created_at timestamp without time zone,
	updated_at timestamp without time zone,
	judgments_count integer,
	agreement float,
	missed_count integer,
	state character varying,
	data jsonb,
	results jsonb
) server crowdflower_srv options (
	key 'YOURCFAPIKEY',
	type 'jobreport'
);

create foreign table job_judgment (                                                                      
	job_id integer,
	updated_at timestamp without time zone,
	agreement float,
	ids integer[],
	state character varying,
	fields jsonb
) server crowdflower_srv options (
	key 'YOURCFAPIKEY',
	type 'jobjudgment'
);

create function set_api_key(text) returns void as $$
begin
	execute format('alter foreign table job_result options (set key %L)', $1);
	execute format('alter foreign table job_judgment options (set key %L)', $1);
end;
$$ language plpgsql
   set search_path = @extschema@;
