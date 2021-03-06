from simhash import Simhash
import json
from flask import (
    Blueprint, flash, jsonify, request
)
import urllib3


bp = Blueprint('request', __name__, url_prefix='/')


@bp.route('/request', methods=('GET', 'POST'))
def register():
    url = request.args.get('url')
    year = request.args.get('year')
    error = None
    if not url:
        error = 'URL is required.'
    elif not year:
        error = 'Year is required.'
    else:
        http = urllib3.PoolManager()
        r = http.request('GET', f'https://web.archive.org/cdx/search/cdx?url={url}&'
                                f'from={year}&to={year}&fl=timestamp&output=json&output=json&limit=3')
        snapshots = json.loads(r.data.decode('utf-8'))
        snapshots.pop(0)
        simhashes = []
        for snapshot in snapshots:
            print(f'https://web.archive.org/web/{snapshot[0]}/{url}')
            r = http.request('GET', f'https://web.archive.org/web/{snapshot[0]}/{url}')
            simhashes.append(Simhash(r.data.decode('utf-8')).value)
    flash(error)

    return jsonify(simhashes)
