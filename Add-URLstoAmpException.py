from meraki import *


#use this to add urls to exempt from amp scanning on Meraki threat protection.

#SETUP#
organizationId="id"
api = API_KEY_ENVIRONMENT_VARIABLE="apikey"
dashboard = DashboardAPI(api)

networks = dashboard.organizations.getOrganizationNetworks(organizationId)
#print(networks)


for net in networks:
    netName = dashboard.networks.getNetwork(net['id'])
    print(f"{netName['name']}")
    if "appliance" not in net['productTypes']:
        continue
    malwareSettings = dashboard.appliance.getNetworkApplianceSecurityMalware(net['id'])
    
    netName = dashboard.networks.getNetwork(net['id'])
    print(f"{netName['name']}")
    print(net)
    print(type(malwareSettings))

    if malwareSettings['mode'] == "enabled":
        print(f"{netName['name']},{malwareSettings}")
        if "URL you want to add" not in malwareSettings['allowedUrls']: 
            malwareSettings['allowedUrls'].append({'url': 'YourURL', 'comment': 'addcommenthere'})
            malwareSettings['allowedUrls'].append({'url': 'YourURL', 'comment': 'addcommenthere'})
            #should use if statement in the future if url is already there.
            #print(f"{malwareSettings['allowedUrls']}")
            print(f"{netName['name']},{malwareSettings['allowedUrls']}")
            print(type(malwareSettings['allowedUrls']))
            
            
            setResult = dashboard.appliance.updateNetworkApplianceSecurityMalware(net['id'],'enabled',allowedUrls=malwareSettings['allowedUrls'])
            print(setResult)

#{'mode': 'enabled', 'allowedUrls': [], 'allowedFiles': []}

