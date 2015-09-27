import requests
import pytest
import json

url = 'http://qainterview.cogniance.com/candidates'
payload = {'name':'Olga','position':'QA'}
headers = {'content-type':'application/json'}
new_id = 0


def test_get_list_of_candidates():
    r = requests.get(url)
    assert r.status_code == 200

def test_add_candidate():
    global new_id
    r = requests.post(url,data=json.dumps(payload),headers=headers)
    response = r.json()
    new_id = response[u'candidate'][u'id']              #save id of new candidate
    #check that the new candidate is added correctly
    assert (response[u'candidate'][u'name'] == payload['name'] and response[u'candidate'][u'position'] == payload['position'])
    assert r.status_code == 201

def test_add_candidate_no_header():                     #negative case - posting data without the header
    r = requests.post(url,data=json.dumps(payload))
    assert r.status_code == 400

def test_add_candidate_no_name():                       #negative case - posting data without name
    payload = {'position':'QA'}
    r = requests.post(url,data=json.dumps(payload),headers=headers)
    assert r.status_code == 400

def test_get_one_candidate():
    r = requests.get(url + '/' + str(new_id))
    response = r.json()
    assert response[u'candidate'][u'id'] == new_id  #check that we get the correct candidate
    assert r.status_code == 200

def test_delete_candidate():
    r = requests.delete(url + '/' + str(new_id))
    assert r.status_code == 200
    r = requests.get(url + '/' + str(new_id))
    assert r.status_code != 200                     #check that candidate with new_id is not there anymore



if __name__ == '__main__':
    pytest.main([__file__,'-v'])
