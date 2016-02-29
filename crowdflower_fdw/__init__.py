import json
from itertools import chain
from zipfile import BadZipFile, ZipFile

import requests
from multicorn import ForeignDataWrapper, ANY

from io import BytesIO


class JobReportFDW(ForeignDataWrapper):
    """

    """

    def __init__(self, options, columns):
        """

        @param options:
        @param columns:
        """
        super(JobReportFDW, self).__init__(options, columns)
        self.columns = columns
        self._key = options['key']

    def _get_results(self, job_id):
        """

        @param job_id:
        @return:
        """
        resp = requests.get(
            'https://api.crowdflower.com/v1/jobs/{}.csv'.format(job_id),
            params=dict(type='json', key=self._key),
        )

        with ZipFile(BytesIO(resp.content)) as zf:
            yield from map(json.loads, chain.from_iterable(
                map(
                    lambda bs: (
                        line for line in bs.decode('utf-8').split('\n')
                        if line
                    ),
                    map(zf.read, zf.namelist())
                )
            ))

    def execute(self, quals, columns):
        """

        @param quals:
        @param columns:
        """
        job_ids = []

        for qual in quals:
            if qual.field_name == 'job_id':
                if qual.operator == '=':
                    job_ids = [qual.value]

                elif qual.is_list_operator and qual.list_any_or_all is ANY:
                    job_ids.extend(qual.value)

        if not job_ids:
            raise RuntimeError('Can not query without job_id')

        for job_id in job_ids:
            try:
                rs = self._get_results(job_id)

            except BadZipFile:
                # Try one more time... dii da dii da dii da...
                rs = self._get_results(job_id)

            for r in rs:
                r['data'] = json.dumps(r['data'])
                r['results'] = json.dumps(r.get('results', {}))

                if r:
                    yield r

                else:
                    raise RuntimeError("Unit without data")
