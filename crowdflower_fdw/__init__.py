import json
from itertools import count
from zipfile import BadZipFile, ZipFile

import requests
from multicorn import ForeignDataWrapper, ANY

from io import BytesIO, TextIOWrapper


def api_request(path, *, key, params, method='get', **kwgs):
    """

    @param path:
    @param params:
    @param kwgs:
    @return:
    """
    params['key'] = key
    resp = requests.request(
        method=method,
        url='https://api.crowdflower.com/v1/{}'.format(path),
        params=params,
        **kwgs
    )
    if resp.status_code == 401:
        raise RuntimeError("401 Unauthorized, you should probably "
                           "call crowdflower.set_api_key")
    # Raise for everything else
    resp.raise_for_status()
    return resp


def get_job_ids_from(quals):
    job_ids = []
    for qual in quals:
        if qual.field_name == 'job_id':
            if qual.operator == '=':
                job_ids = [qual.value]

            elif qual.is_list_operator and qual.list_any_or_all is ANY:
                job_ids.extend(qual.value)

    return job_ids


def factory(options, columns):
    type_ = options['type'].lower()
    if type_ == 'jobreport':
        return JobReportFDW(options, columns)

    elif type_ == 'jobjudgment':
        return JobJudgmentFDW(options, columns)

    raise RuntimeError('Unknown type: {!r}'.format(type_))


class JobReportFDW(ForeignDataWrapper):
    """

    """

    def __init__(self, options, columns):
        """

        @param options:
        @param columns:
        """
        super(JobReportFDW, self).__init__(options, columns)
        self._key = options['key']

    def _get_results(self, job_id):
        """

        @param job_id:
        @return:
        """
        resp = api_request(
            'jobs/{}.csv'.format(job_id),
            key=self._key,
            params=dict(type='json'),
        )

        with ZipFile(BytesIO(resp.content)) as zf:
            for name in zf.namelist():
                with zf.open(name) as f:
                    yield from map(json.loads,
                                   TextIOWrapper(f, encoding='utf-8'))

    def execute(self, quals, columns):
        """

        @param quals:
        @param columns:
        """
        job_ids = get_job_ids_from(quals)

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
                r['results'] = json.dumps(r.get('results'))

                if r:
                    yield r

                else:
                    raise RuntimeError("Unit without data")


class JobJudgmentFDW(ForeignDataWrapper):
    """

    """

    def __init__(self, options, columns):
        """

        @param options:
        @param columns:
        """
        super(JobJudgmentFDW, self).__init__(options, columns)
        self._key = options['key']

    def _get_judgments(self, job_id):
        page = count(1)
        path = 'jobs/{}/judgments.json'.format(job_id)

        def fetch():
           return api_request(path, params=dict(page=next(page), limit=100),
                              key=self._key).json()

        for resp in iter(fetch, {}):
            yield from resp.values()

    def execute(self, quals, columns):
        job_ids = get_job_ids_from(quals)

        if not job_ids:
            raise RuntimeError('Can not query without job_id')

        for job_id in job_ids:
            for r in self._get_judgments(job_id):
                row = {k[1:]: v for k, v in r.items() if k.startswith('_')}
                fields = json.dumps({k: v for k, v in r.items()
                                     if not k.startswith('_')})
                row['fields'] = fields
                row['job_id'] = job_id
                yield row
