import os
import argparse
import requests


idp_oauth = "http://edwappsrv4.poc.dum.edwdc.net:28080"
# idp_oauth = "http://auth0.dev.dum.edwdc.net:8080"
tsb_end_point = "http://localhost:6543/services/xml"
# tsb_end_point = "http://tsbweb0.dev.dum.edwdc.net/services/xml"


def send_post(self, url, data=None):
    '''
    POST request for non-json content body
    :param url: http url
    :type url:string
    :param data: data to post in the payload
    :type data: string
    '''
    return requests.post(url, data=data, **self._request_header)


def authenticate_with_oauth(user_id):
    '''
    Retrieve access token from SSO using oauth and sets the request header to use it in bearer
    '''
    password = user_id + '1234'
    oauth_server = "{http_host}/OpenAM-11.0.0/oauth2/access_token?realm=/&grant_type=password&username={user_id}&password={password}&client_id=pm&client_secret=sbac12345"\
        .format(http_host=idp_oauth, user_id=user_id, password=password)
    _request_header = {
        "content-type": "application/xml"
    }
    _response = requests.post(oauth_server, headers=_request_header)
    return _response.json()['access_token']


def send_request(xml_directory):
    access_token = authenticate_with_oauth('shall')
    _request_header = {
        "content-type": "application/xml",
        "bearer": access_token
    }
    for xml_file in os.listdir(xml_directory):
        if not xml_file.endswith(".xml"):
            continue
        xml_file = os.path.join(xml_directory, xml_file)
        with open(xml_file) as f:
            xml_payload = f.read()
        _response = requests.post(tsb_end_point, xml_payload, headers=_request_header)
        if _response.status_code == 202:
            print("Request with payload %s Succeeded" % xml_file)
        else:
            print("Request with payload %s Failed" % xml_file)


def main():
    parser = argparse.ArgumentParser(description='Send XML to TSB')
    parser.add_argument('-i', '--input', default="./output/", help='directory path to CSV files')
    args = parser.parse_args()
    send_request(args.input)


if __name__ == '__main__':
    main()
