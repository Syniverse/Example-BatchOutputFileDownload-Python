
# a simple flask bot that can understand ESS messages from the Syniverse Developer Community and
# check whether it is a job complete notification from the Batch Automation system and downloads the output file.
# Written for Python 2.7
# depends on the flask and requests packages

from flask import Flask
from flask import request, json
import requests, zlib, time

def download_output_file(notification_contents): # downloads the output file if it is included
    access_token = '[PUT-YOUR-ACCESS-TOKEN-HERE]'
    company_id = notification_contents['fld-val-list']['company-id']
    headers = {'Authorization': 'Bearer ' + access_token, 'int-companyid': company_id}
    output_file_uri = notification_contents['fld-val-list']['output_file_uri']
    if output_file_uri <> 'EMPTY_FILE':
        response = requests.get(output_file_uri, headers=headers)
        data = zlib.decompress(response.content, zlib.MAX_WBITS|32)
        file_name = 'output' + time.strftime('%Y%m%d%H%M%S') + '.txt'
        f = open(file_name,'w')
        f.write(data)
        f.close
        return 'file downloaded'
    else:
        return 'empty output file so not downloaded'

app = Flask(__name__)

@app.route('/batchjob/v1/notification', methods=['POST'])
def process_notification():
    # filter out requests that arent likely to be an ESS notification
    if not request.json or not 'topic' in request.json:
        return 'hello test', '201'
    # check whether it is job complete notification
    elif request.json['topic'] == 'ABA-Messages' and request.json['event']['evt-tp'] == 'aba_job_completed':
        event_data = request.json['event']
        result = download_output_file(event_data)
        return result, 201
    else:
        return 'hello not an ABA job complete notification', 201
