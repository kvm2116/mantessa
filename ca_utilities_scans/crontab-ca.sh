#!/bin/bash

/usr/bin/curl --silent -o "/local/mantessa/ca_utilities_scans/iid/iid+$(date "+%F-%T")" 'https://myaccount.iid.com/portal/ajax/CustomerPortal.OuterOutage,CustomerPortal.ashx?_method=loadLatLongOuterOutage&_session=rw' -H 'Origin: https://myaccount.iid.com' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8,es;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36' -H 'Content-Type: text/plain;charset=UTF-8' -H 'Accept: */*' -H 'Referer: https://myaccount.iid.com/portal/outeroutage.aspx' -H 'Connection: keep-alive' --data-binary $'Zipcode=\r\nIsPlannedOutage=C' --compressed 

#Pacific Gas + Electric
/usr/bin/curl -m 30 --silent -o "/local/mantessa/ca_utilities_scans/pacific_gas_electric/pge+$(date "+%F-%T")" https://apim.pge.com/cocoutage/outages/getOutagesRegions?regionType=city&expand=true &>/dev/null

#So Cal Edison
/usr/bin/curl --silent -o "/local/mantessa/ca_utilities_scans/so_cal_edison/sce+$(date "+%F-%T")" https://www.sce.com/wps/mapServices/mapService/outageMapData/getCurrentOutageData

#Sacramento Muni Util District
/usr/bin/curl --silent -o "/local/mantessa/ca_utilities_scans/sacramento_muni_util_dist/smud+$(date "+%F-%T")" https://usage.smud.org/omkml/api/OutageList/

#San Diego
/usr/bin/curl --silent -o "/local/mantessa/ca_utilities_scans/san_diego_gas_elec/sdge+$(date "+%F-%T")" https://www.sdge.com/sites/default/files/outagemap_json/outage.json
