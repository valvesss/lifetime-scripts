import json, requests

class DriveSession(object):
    def __init__(self, driveID, graphURI):
        self.graphURI = graphURI + '/me/drives/' + driveID + '/root:/'

    def authenticate(self, grantType, clientID, clientSecret, scope,
                        userName, password, contentType, microsoftURL):
        payload = {
            "grant_type": grantType,
            "client_id": clientID,
            "client_secret": clientSecret,
            "scope": scope,
            "userName": userName,
            "password": password
        }
        headers = { 'Content-Type': contentType }
        response = requests.post(microsoftURL, headers=headers, data=payload)
        jsonParser = json.loads(response.text)
        accessToken = jsonParser['access_token']
        self.setHeaders(accessToken)

    def setHeaders(self, accessToken):
        self.headers = {
                        'Authorization': 'Bearer ' + accessToken,
                        'Content-Type': 'text/plain'
                        }

    def uploadFile(self, sourcePath, sourceName, destinyPath, destinyName):
        with open(sourcePath+sourceName, "rb") as f:
            file_bytes = f.read()
        sharepointPath = destinyPath + destinyName + ':/content'
        url = self.graphURI + sharepointPath
        return requests.put(url, file_bytes, headers=self.headers)

    def deleteFile(self, destinyPath, destinyName):
        sharepointPath = destinyPath + destinyName
        url = self.graphURI + sharepointPath
        return requests.delete(url, headers=self.headers)

    def downloadFile(self, destinyPath, destinyName):
        sharepointPath = destinyPath + destinyName
        url = self.graphURI + sharepointPath
        response = requests.get(url, headers=self.headers)
        json_parser = json.loads(response.content)
        downloadURL = json_parser['@microsoft.graph.downloadUrl']
        return requests.get(downloadURL)

## USAGE EXAMPLE
# Encode paths/creds to web might be recommended

graphURI = 'https://graph.microsoft.com/v1.0'
driveID = 'your_drive_id'
ds = DriveSession(driveID, graphURI)

grantType = "password" # Not a password! Itself "password"
clientID = "your_client_id"
clientSecret = "your_client_secret"
scope = "https://graph.microsoft.com/.default"
userName = "your_microsoft_user"
password = "your_microsoft_user_password"
contentType = "application/x-www-form-urlencoded"
microsoftURL = "https://login.microsoftonline.com/your_tenant_id/oauth2/v2.0/token"
ds.authenticate(grantType, clientID, clientSecret, scope, userName, password,
                    contentType, microsoftURL)

sourcePath = './'
sourceName = 'new_dummy.txt'
destinyPath = 'General/your_path'
destinyName = 'new_dummy.txt'
ds.uploadFile(sourcePath, sourceName, destinyPath, destinyName)
ds.deleteFile(destinyPath, destinyName)
rsp = ds.downloadFile(destinyPath, destinyName)
if rsp.status_code == 200:
    with open(sourcePath+'downloaded_'+sourceName, 'wb') as file:
        file.write(rsp.content)
