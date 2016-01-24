import sys
import os
import json
import requests
import ncs
V = ncs.types.Value

class bodservice():
###########init object start ################

    def __init__(self, ip_or_name='127.0.0.1', port=8080, user_name='admin', pass_word='admin', content_type_str='application/vnd.yang.data+json'):
        ##init rest
        self.port=port
        self.user_name=user_name
        self.pass_word=pass_word
        self.auth_tuple=(user_name,pass_word)
        self.url_base='http://'+ip_or_name+':'+str(port)
        self.headers_json={
            'accept': 'application/json, application/vnd.yang.api+json,application/vnd.yang.data+json, application/vnd.yang.datastore+json,application/vnd.yang.collection+json',
            'content-type':content_type_str
            }
        self.cookies_dict=None
        print('Init Rest interface!')
        
###########init object finished################
        
##########maapi method start################

    def get_config(self,device, serviceNode):
        epURL='/ncs:devices/device{'+ device +'}/config' + serviceNode
        ep_list=[]
        try:
            with self.maapi.cursor(epURL) as cur :
                for k in cur :
                    ep=str(k[0])
                    ep_list.append(ep)
        except:
            e = sys.exc_info()[1]
            print "Error: %s" % e
        return ep_list
        
    def _bod_path_(self, name) :
        return '/ncs:services/BOD{'+name+'}'
        
    def create_service(self, device, serviceName, qosid, ingressDescr, egressDescr, interface) :
        path = self._bod_path_(serviceName)
        self.maapi.create_allow_exist(path)
        self.maapi.set_elem(device, path + '/device')
        self.maapi.set_elem(str(qosid), path + '/sap-ingress/id')
        self.maapi.set_elem(str(qosid), path + '/sap-egress/id')
        self.maapi.set_elem(ingressDescr, path + '/sap-ingress/description')
        self.maapi.set_elem(egressDescr, path + '/sap-egress/description')
        self.maapi.set_elem(interface, path + '/sap-ingress/interface')
        self.maapi.set_elem(interface, path + '/sap-egress/interface')
        print(serviceName + ' create!')
    
    def create_queue(self, serviceName, queueDirect, linkID, rate, cir) :
        path = self._bod_path_(serviceName)
        queuePath = path + '/sap-' + queueDirect + 'gress' + '/queue{"' + str(linkID) + '"}'
        self.maapi.create_allow_exist(queuePath)
        self.maapi.set_elem(V(rate, V.C_UINT32), queuePath + '/rate')
        self.maapi.set_elem(V(cir, V.C_UINT32), queuePath + '/cir')
        print(serviceName + ' queue create!')
        
    def commit_service(self) :
        self.maapi.apply()
        print('commited to devices!')
        
    ##init maapi
    def sync_from_devices(self,t) :
        self.maapi = t
        result = ncs._maapi.request_action(self.maapi.sock,[], 0, fmt = '/ncs:devices/sync-from')
        print('Synced from devices!')
        
##########maapi method finished################
     
##########restful method start###############     
 
    def stringifyJson(self,json_obj):
        return json.dumps(json_obj, indent=2)
    
    def return_data(self,response_obj):
        if response_obj.status_code in (200, 201, 204):
            is_successful = True
        else:
            is_successful = False
        try:
            response_json = response_obj.json()
        except Exception, e:
            response_json = response_obj.text
        return (is_successful, response_obj.status_code, self.stringifyJson(response_json))
        
    def get(self, uri_str='',doPrint=''):
        url_full=self.url_base + uri_str
        rest_session=requests.Session()
        rest_session.headers.update(self.headers_json)
        response_obj=rest_session.get(url_full,auth=self.auth_tuple) #,headers=self.headers_json) #,verify=False)
        #response_obj=requests.get(url_full,auth=self.auth_tuple,headers=self.headers_json) #,verify=False)
        #just for Test
        if doPrint:
            print
            #print rest_session.url, '\n'
            print 'headers sent:'
            print rest_session.headers, '\n'
            print 'url received:'
            print response_obj.url, '\n'
            print 'headers received:'
            print response_obj.headers, '\n'
            print 'status code received:', response_obj.status_code,'\n'
            print 'response text received:'
            print response_obj.text
            
        return self.return_data(response_obj)
        
##########restful method finished#############

    