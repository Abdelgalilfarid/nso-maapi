
#code by python 2.7, author jasonqi

#Depend on ncs/nso/tailf framework, using yang model and java templet service,  create interface to deploy alu and cisco devices, including iosxr and alu:sr.

example:
python ./test.py 
Init Rest interface!
Synced from devices!
Service create!
{
  "collection": {
    "BOD:BOD": [
      {
        "device": "SR1-YN-7750", 
        "operations": {
          "deep-check-sync": "/api/running/services/BOD:BOD/BOD1/_operations/deep-check-sync", 
          "re-deploy": "/api/running/services/BOD:BOD/BOD1/_operations/re-deploy", 
          "check-sync": "/api/running/services/BOD:BOD/BOD1/_operations/check-sync", 
          "un-deploy": "/api/running/services/BOD:BOD/BOD1/_operations/un-deploy", 
          "get-modifications": "/api/running/services/BOD:BOD/BOD1/_operations/get-modifications", 
          "self-test": "/api/running/services/BOD:BOD/BOD1/_operations/self-test"
        }, 
        "sap-egress": {
          "queue": [
            {
              "link-id": 1, 
              "rate": 102400, 
              "cir": 102400
            }
          ], 
          "interface": "4/1/20", 
          "id": "103", 
          "description": "Test-1"
        }, 
        "name": "BOD1", 
        "sap-ingress": {
          "queue": [
            {
              "link-id": 1, 
              "rate": 102400, 
              "cir": 102400
            }
          ], 
          "interface": "4/1/20", 
          "id": "103", 
          "description": "Test-1"
        }
      }
    ]
  }
}





