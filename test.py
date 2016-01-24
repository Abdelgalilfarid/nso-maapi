from service import *
if __name__ == '__main__' :
    
    #argv
    device = 'SR1-YN-7750'
    serviceName = 'BOD1'
    qosid = 103
    ingressDescr = 'Test-1'
    egressDescr = 'Test-1'
    interface = '4/1/20'
    ncs_cli=bodservice(ip_or_name='127.0.0.1')
    linkID = 1
    rate = 102400
    cir = 102400
    
    #maapi for edit-config
    with ncs.maapi.wctx.connect(ip = '127.0.0.1', port = ncs._constants.NCS_PORT) as c :
            with ncs.maapi.wctx.session(c, 'admin') as s :
                with ncs.maapi.wctx.trans(s, readWrite = ncs._constants.READ_WRITE) as t :
                    ncs_cli.sync_from_devices(t)
                    ncs_cli.create_service(device, serviceName, qosid, ingressDescr, egressDescr, interface)
                    ncs_cli.create_queue(serviceName, 'in', linkID, rate, cir)
                    ncs_cli.create_queue(serviceName, 'e', linkID, rate, cir)
                    ncs_cli.commit_service()
                    
                    #cursor
                    bod_configs = ncs_cli.get_config(device,'/alu:qos/sap-ingress')
                    for i in range(0, len(bod_configs)):
                        print i, bod_configs[i]
                        
    #rest for get-config
    (is_successful, response_code, response_json) = ncs_cli.get('/api/running/devices/device/'+ device + '/config?deep',False);
    print response_json
    (is_successful, response_code, response_json) = ncs_cli.get('/api/running/services/BOD?deep',False);
    print response_json
