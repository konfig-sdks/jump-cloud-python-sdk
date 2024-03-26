# coding: utf-8

"""
    JumpCloud API

    # Overview  JumpCloud's V2 API. This set of endpoints allows JumpCloud customers to manage objects, groupings and mappings and interact with the JumpCloud Graph.  ## API Best Practices  Read the linked Help Article below for guidance on retrying failed requests to JumpCloud's REST API, as well as best practices for structuring subsequent retry requests. Customizing retry mechanisms based on these recommendations will increase the reliability and dependability of your API calls.  Covered topics include: 1. Important Considerations 2. Supported HTTP Request Methods 3. Response codes 4. API Key rotation 5. Paginating 6. Error handling 7. Retry rates  [JumpCloud Help Center - API Best Practices](https://support.jumpcloud.com/support/s/article/JumpCloud-API-Best-Practices)  # Directory Objects  This API offers the ability to interact with some of our core features; otherwise known as Directory Objects. The Directory Objects are:  * Commands * Policies * Policy Groups * Applications * Systems * Users * User Groups * System Groups * Radius Servers * Directories: Office 365, LDAP,G-Suite, Active Directory * Duo accounts and applications.  The Directory Object is an important concept to understand in order to successfully use JumpCloud API.  ## JumpCloud Graph  We've also introduced the concept of the JumpCloud Graph along with  Directory Objects. The Graph is a powerful aspect of our platform which will enable you to associate objects with each other, or establish membership for certain objects to become members of other objects.  Specific `GET` endpoints will allow you to traverse the JumpCloud Graph to return all indirect and directly bound objects in your organization.  | ![alt text](https://s3.amazonaws.com/jumpcloud-kb/Knowledge+Base+Photos/API+Docs/jumpcloud_graph.png \"JumpCloud Graph Model Example\") | |:--:| | **This diagram highlights our association and membership model as it relates to Directory Objects.** |  # API Key  ## Access Your API Key  To locate your API Key:  1. Log into the [JumpCloud Admin Console](https://console.jumpcloud.com/). 2. Go to the username drop down located in the top-right of the Console. 3. Retrieve your API key from API Settings.  ## API Key Considerations  This API key is associated to the currently logged in administrator. Other admins will have different API keys.  **WARNING** Please keep this API key secret, as it grants full access to any data accessible via your JumpCloud console account.  You can also reset your API key in the same location in the JumpCloud Admin Console.  ## Recycling or Resetting Your API Key  In order to revoke access with the current API key, simply reset your API key. This will render all calls using the previous API key inaccessible.  Your API key will be passed in as a header with the header name \"x-api-key\".  ```bash curl -H \"x-api-key: [YOUR_API_KEY_HERE]\" \"https://console.jumpcloud.com/api/v2/systemgroups\" ```  # System Context  * [Introduction](https://docs.jumpcloud.com) * [Supported endpoints](https://docs.jumpcloud.com) * [Response codes](https://docs.jumpcloud.com) * [Authentication](https://docs.jumpcloud.com) * [Additional examples](https://docs.jumpcloud.com) * [Third party](https://docs.jumpcloud.com)  ## Introduction  JumpCloud System Context Authorization is an alternative way to authenticate with a subset of JumpCloud's REST APIs. Using this method, a system can manage its information and resource associations, allowing modern auto provisioning environments to scale as needed.  **Notes:**   * The following documentation applies to Linux Operating Systems only.  * Systems that have been automatically enrolled using Apple's Device Enrollment Program (DEP) or systems enrolled using the User Portal install are not eligible to use the System Context API to prevent unauthorized access to system groups and resources. If a script that utilizes the System Context API is invoked on a system enrolled in this way, it will display an error.  ## Supported Endpoints  JumpCloud System Context Authorization can be used in conjunction with Systems endpoints found in the V1 API and certain System Group endpoints found in the v2 API.  * A system may fetch, alter, and delete metadata about itself, including manipulating a system's Group and Systemuser associations,   * `/api/systems/{system_id}` | [`GET`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_get) [`PUT`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_put) * A system may delete itself from your JumpCloud organization   * `/api/systems/{system_id}` | [`DELETE`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_delete) * A system may fetch its direct resource associations under v2 (Groups)   * `/api/v2/systems/{system_id}/memberof` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemGroupMembership)   * `/api/v2/systems/{system_id}/associations` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemAssociationsList)   * `/api/v2/systems/{system_id}/users` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemTraverseUser) * A system may alter its direct resource associations under v2 (Groups)   * `/api/v2/systems/{system_id}/associations` | [`POST`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemAssociationsPost) * A system may alter its System Group associations   * `/api/v2/systemgroups/{group_id}/members` | [`POST`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemGroupMembersPost)     * _NOTE_ If a system attempts to alter the system group membership of a different system the request will be rejected  ## Response Codes  If endpoints other than those described above are called using the System Context API, the server will return a `401` response.  ## Authentication  To allow for secure access to our APIs, you must authenticate each API request. JumpCloud System Context Authorization uses [HTTP Signatures](https://tools.ietf.org/html/draft-cavage-http-signatures-00) to authenticate API requests. The HTTP Signatures sent with each request are similar to the signatures used by the Amazon Web Services REST API. To help with the request-signing process, we have provided an [example bash script](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/shell/SigningExample.sh). This example API request simply requests the entire system record. You must be root, or have permissions to access the contents of the `/opt/jc` directory to generate a signature.  Here is a breakdown of the example script with explanations.  First, the script extracts the systemKey from the JSON formatted `/opt/jc/jcagent.conf` file.  ```bash #!/bin/bash conf=\"`cat /opt/jc/jcagent.conf`\" regex=\"systemKey\\\":\\\"(\\w+)\\\"\"  if [[ $conf =~ $regex ]] ; then   systemKey=\"${BASH_REMATCH[1]}\" fi ```  Then, the script retrieves the current date in the correct format.  ```bash now=`date -u \"+%a, %d %h %Y %H:%M:%S GMT\"`; ```  Next, we build a signing string to demonstrate the expected signature format. The signed string must consist of the [request-line](https://tools.ietf.org/html/rfc2616#page-35) and the date header, separated by a newline character.  ```bash signstr=\"GET /api/systems/${systemKey} HTTP/1.1\\ndate: ${now}\" ```  The next step is to calculate and apply the signature. This is a two-step process:  1. Create a signature from the signing string using the JumpCloud Agent private key: ``printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key`` 2. Then Base64-encode the signature string and trim off the newline characters: ``| openssl enc -e -a | tr -d '\\n'``  The combined steps above result in:  ```bash signature=`printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key | openssl enc -e -a | tr -d '\\n'` ; ```  Finally, we make sure the API call sending the signature has the same Authorization and Date header values, HTTP method, and URL that were used in the signing string.  ```bash curl -iq \\   -H \"Accept: application/json\" \\   -H \"Content-Type: application/json\" \\   -H \"Date: ${now}\" \\   -H \"Authorization: Signature keyId=\\\"system/${systemKey}\\\",headers=\\\"request-line date\\\",algorithm=\\\"rsa-sha256\\\",signature=\\\"${signature}\\\"\" \\   --url https://console.jumpcloud.com/api/systems/${systemKey} ```  ### Input Data  All PUT and POST methods should use the HTTP Content-Type header with a value of 'application/json'. PUT methods are used for updating a record. POST methods are used to create a record.  The following example demonstrates how to update the `displayName` of the system.  ```bash signstr=\"PUT /api/systems/${systemKey} HTTP/1.1\\ndate: ${now}\" signature=`printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key | openssl enc -e -a | tr -d '\\n'` ;  curl -iq \\   -d \"{\\\"displayName\\\" : \\\"updated-system-name-1\\\"}\" \\   -X \"PUT\" \\   -H \"Content-Type: application/json\" \\   -H \"Accept: application/json\" \\   -H \"Date: ${now}\" \\   -H \"Authorization: Signature keyId=\\\"system/${systemKey}\\\",headers=\\\"request-line date\\\",algorithm=\\\"rsa-sha256\\\",signature=\\\"${signature}\\\"\" \\   --url https://console.jumpcloud.com/api/systems/${systemKey} ```  ### Output Data  All results will be formatted as JSON.  Here is an abbreviated example of response output:  ```json {   \"_id\": \"625ee96f52e144993e000015\",   \"agentServer\": \"lappy386\",   \"agentVersion\": \"0.9.42\",   \"arch\": \"x86_64\",   \"connectionKey\": \"127.0.0.1_51812\",   \"displayName\": \"ubuntu-1204\",   \"firstContact\": \"2013-10-16T19:30:55.611Z\",   \"hostname\": \"ubuntu-1204\"   ... ```  ## Additional Examples  ### Signing Authentication Example  This example demonstrates how to make an authenticated request to fetch the JumpCloud record for this system.  [SigningExample.sh](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/shell/SigningExample.sh)  ### Shutdown Hook  This example demonstrates how to make an authenticated request on system shutdown. Using an init.d script registered at run level 0, you can call the System Context API as the system is shutting down.  [Instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) is an example of an init.d script that only runs at system shutdown.  After customizing the [instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) script, you should install it on the system(s) running the JumpCloud agent.  1. Copy the modified [instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) to `/etc/init.d/instance-shutdown`. 2. On Ubuntu systems, run `update-rc.d instance-shutdown defaults`. On RedHat/CentOS systems, run `chkconfig --add instance-shutdown`.  ## Third Party  ### Chef Cookbooks  [https://github.com/nshenry03/jumpcloud](https://github.com/nshenry03/jumpcloud)  [https://github.com/cjs226/jumpcloud](https://github.com/cjs226/jumpcloud)  # Multi-Tenant Portal Headers  Multi-Tenant Organization API Headers are available for JumpCloud Admins to use when making API requests from Organizations that have multiple managed organizations.  The `x-org-id` is a required header for all multi-tenant admins when making API requests to JumpCloud. This header will define to which organization you would like to make the request.  **NOTE** Single Tenant Admins do not need to provide this header when making an API request.  ## Header Value  `x-org-id`  ## API Response Codes  * `400` Malformed ID. * `400` x-org-id and Organization path ID do not match. * `401` ID not included for multi-tenant admin * `403` ID included on unsupported route. * `404` Organization ID Not Found.  ```bash curl -X GET https://console.jumpcloud.com/api/v2/directories \\   -H 'accept: application/json' \\   -H 'content-type: application/json' \\   -H 'x-api-key: {API_KEY}' \\   -H 'x-org-id: {ORG_ID}'  ```  ## To Obtain an Individual Organization ID via the UI  As a prerequisite, your Primary Organization will need to be setup for Multi-Tenancy. This provides access to the Multi-Tenant Organization Admin Portal.  1. Log into JumpCloud [Admin Console](https://console.jumpcloud.com). If you are a multi-tenant Admin, you will automatically be routed to the Multi-Tenant Admin Portal. 2. From the Multi-Tenant Portal's primary navigation bar, select the Organization you'd like to access. 3. You will automatically be routed to that Organization's Admin Console. 4. Go to Settings in the sub-tenant's primary navigation. 5. You can obtain your Organization ID below your Organization's Contact Information on the Settings page.  ## To Obtain All Organization IDs via the API  * You can make an API request to this endpoint using the API key of your Primary Organization.  `https://console.jumpcloud.com/api/organizations/` This will return all your managed organizations.  ```bash curl -X GET \\   https://console.jumpcloud.com/api/organizations/ \\   -H 'Accept: application/json' \\   -H 'Content-Type: application/json' \\   -H 'x-api-key: {API_KEY}' ```  # SDKs  You can find language specific SDKs that can help you kickstart your Integration with JumpCloud in the following GitHub repositories:  * [Python](https://github.com/TheJumpCloud/jcapi-python) * [Go](https://github.com/TheJumpCloud/jcapi-go) * [Ruby](https://github.com/TheJumpCloud/jcapi-ruby) * [Java](https://github.com/TheJumpCloud/jcapi-java) 

    The version of the OpenAPI document: 2.0
    Contact: support@jumpcloud.com
    Created by: https://support.jumpcloud.com/support/s/
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from jump_cloud_python_sdk import schemas  # noqa: F401


class SoftwareAppGoogleAndroid(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    googleAndroid is an optional attribute, it will only be present on apps with a 'setting' 'package_manager' type of 'GOOGLE_ANDROID'.
    """


    class MetaOapg:
        
        class properties:
        
            @staticmethod
            def androidFeatures() -> typing.Type['SoftwareAppGoogleAndroidAndroidFeatures']:
                return SoftwareAppGoogleAndroidAndroidFeatures
            appPricing = schemas.StrSchema
            appVersion = schemas.StrSchema
            author = schemas.StrSchema
            
            
            class autoUpdateMode(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def DEFAULT(cls):
                    return cls("AUTO_UPDATE_DEFAULT")
                
                @schemas.classproperty
                def POSTPONED(cls):
                    return cls("AUTO_UPDATE_POSTPONED")
                
                @schemas.classproperty
                def HIGH_PRIORITY(cls):
                    return cls("AUTO_UPDATE_HIGH_PRIORITY")
            category = schemas.StrSchema
            contentRating = schemas.StrSchema
            displayMode = schemas.StrSchema
            distributionChannel = schemas.StrSchema
            fullDescription = schemas.StrSchema
            iconUrl = schemas.StrSchema
            
            
            class installType(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def AVAILABLE(cls):
                    return cls("AVAILABLE")
                
                @schemas.classproperty
                def FORCE_INSTALLED(cls):
                    return cls("FORCE_INSTALLED")
                
                @schemas.classproperty
                def BLOCKED(cls):
                    return cls("BLOCKED")
            managedConfigurationTemplateId = schemas.StrSchema
            managedProperties = schemas.BoolSchema
            minSdkVersion = schemas.IntSchema
            name = schemas.StrSchema
            
            
            class permissionGrants(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['SoftwareAppPermissionGrants']:
                        return SoftwareAppPermissionGrants
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['SoftwareAppPermissionGrants'], typing.List['SoftwareAppPermissionGrants']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'permissionGrants':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'SoftwareAppPermissionGrants':
                    return super().__getitem__(i)
            
            
            class runtimePermission(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def PROMPT(cls):
                    return cls("PROMPT")
                
                @schemas.classproperty
                def GRANT(cls):
                    return cls("GRANT")
                
                @schemas.classproperty
                def DENY(cls):
                    return cls("DENY")
            startUrl = schemas.StrSchema
            
            
            class type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def APP_TYPE_UNSPECIFIED(cls):
                    return cls("APP_TYPE_UNSPECIFIED")
                
                @schemas.classproperty
                def PUBLIC(cls):
                    return cls("PUBLIC")
                
                @schemas.classproperty
                def PRIVATE(cls):
                    return cls("PRIVATE")
                
                @schemas.classproperty
                def WEBAPP(cls):
                    return cls("WEBAPP")
            updateTime = schemas.StrSchema
            versionCode = schemas.IntSchema
            __annotations__ = {
                "androidFeatures": androidFeatures,
                "appPricing": appPricing,
                "appVersion": appVersion,
                "author": author,
                "autoUpdateMode": autoUpdateMode,
                "category": category,
                "contentRating": contentRating,
                "displayMode": displayMode,
                "distributionChannel": distributionChannel,
                "fullDescription": fullDescription,
                "iconUrl": iconUrl,
                "installType": installType,
                "managedConfigurationTemplateId": managedConfigurationTemplateId,
                "managedProperties": managedProperties,
                "minSdkVersion": minSdkVersion,
                "name": name,
                "permissionGrants": permissionGrants,
                "runtimePermission": runtimePermission,
                "startUrl": startUrl,
                "type": type,
                "updateTime": updateTime,
                "versionCode": versionCode,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["androidFeatures"]) -> 'SoftwareAppGoogleAndroidAndroidFeatures': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["appPricing"]) -> MetaOapg.properties.appPricing: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["appVersion"]) -> MetaOapg.properties.appVersion: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["author"]) -> MetaOapg.properties.author: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autoUpdateMode"]) -> MetaOapg.properties.autoUpdateMode: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["category"]) -> MetaOapg.properties.category: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["contentRating"]) -> MetaOapg.properties.contentRating: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["displayMode"]) -> MetaOapg.properties.displayMode: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["distributionChannel"]) -> MetaOapg.properties.distributionChannel: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["fullDescription"]) -> MetaOapg.properties.fullDescription: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["iconUrl"]) -> MetaOapg.properties.iconUrl: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["installType"]) -> MetaOapg.properties.installType: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["managedConfigurationTemplateId"]) -> MetaOapg.properties.managedConfigurationTemplateId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["managedProperties"]) -> MetaOapg.properties.managedProperties: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["minSdkVersion"]) -> MetaOapg.properties.minSdkVersion: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["permissionGrants"]) -> MetaOapg.properties.permissionGrants: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["runtimePermission"]) -> MetaOapg.properties.runtimePermission: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["startUrl"]) -> MetaOapg.properties.startUrl: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updateTime"]) -> MetaOapg.properties.updateTime: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["versionCode"]) -> MetaOapg.properties.versionCode: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["androidFeatures", "appPricing", "appVersion", "author", "autoUpdateMode", "category", "contentRating", "displayMode", "distributionChannel", "fullDescription", "iconUrl", "installType", "managedConfigurationTemplateId", "managedProperties", "minSdkVersion", "name", "permissionGrants", "runtimePermission", "startUrl", "type", "updateTime", "versionCode", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["androidFeatures"]) -> typing.Union['SoftwareAppGoogleAndroidAndroidFeatures', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["appPricing"]) -> typing.Union[MetaOapg.properties.appPricing, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["appVersion"]) -> typing.Union[MetaOapg.properties.appVersion, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["author"]) -> typing.Union[MetaOapg.properties.author, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autoUpdateMode"]) -> typing.Union[MetaOapg.properties.autoUpdateMode, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["category"]) -> typing.Union[MetaOapg.properties.category, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["contentRating"]) -> typing.Union[MetaOapg.properties.contentRating, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["displayMode"]) -> typing.Union[MetaOapg.properties.displayMode, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["distributionChannel"]) -> typing.Union[MetaOapg.properties.distributionChannel, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["fullDescription"]) -> typing.Union[MetaOapg.properties.fullDescription, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["iconUrl"]) -> typing.Union[MetaOapg.properties.iconUrl, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["installType"]) -> typing.Union[MetaOapg.properties.installType, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["managedConfigurationTemplateId"]) -> typing.Union[MetaOapg.properties.managedConfigurationTemplateId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["managedProperties"]) -> typing.Union[MetaOapg.properties.managedProperties, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["minSdkVersion"]) -> typing.Union[MetaOapg.properties.minSdkVersion, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["permissionGrants"]) -> typing.Union[MetaOapg.properties.permissionGrants, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["runtimePermission"]) -> typing.Union[MetaOapg.properties.runtimePermission, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["startUrl"]) -> typing.Union[MetaOapg.properties.startUrl, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> typing.Union[MetaOapg.properties.type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updateTime"]) -> typing.Union[MetaOapg.properties.updateTime, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["versionCode"]) -> typing.Union[MetaOapg.properties.versionCode, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["androidFeatures", "appPricing", "appVersion", "author", "autoUpdateMode", "category", "contentRating", "displayMode", "distributionChannel", "fullDescription", "iconUrl", "installType", "managedConfigurationTemplateId", "managedProperties", "minSdkVersion", "name", "permissionGrants", "runtimePermission", "startUrl", "type", "updateTime", "versionCode", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        androidFeatures: typing.Union['SoftwareAppGoogleAndroidAndroidFeatures', schemas.Unset] = schemas.unset,
        appPricing: typing.Union[MetaOapg.properties.appPricing, str, schemas.Unset] = schemas.unset,
        appVersion: typing.Union[MetaOapg.properties.appVersion, str, schemas.Unset] = schemas.unset,
        author: typing.Union[MetaOapg.properties.author, str, schemas.Unset] = schemas.unset,
        autoUpdateMode: typing.Union[MetaOapg.properties.autoUpdateMode, str, schemas.Unset] = schemas.unset,
        category: typing.Union[MetaOapg.properties.category, str, schemas.Unset] = schemas.unset,
        contentRating: typing.Union[MetaOapg.properties.contentRating, str, schemas.Unset] = schemas.unset,
        displayMode: typing.Union[MetaOapg.properties.displayMode, str, schemas.Unset] = schemas.unset,
        distributionChannel: typing.Union[MetaOapg.properties.distributionChannel, str, schemas.Unset] = schemas.unset,
        fullDescription: typing.Union[MetaOapg.properties.fullDescription, str, schemas.Unset] = schemas.unset,
        iconUrl: typing.Union[MetaOapg.properties.iconUrl, str, schemas.Unset] = schemas.unset,
        installType: typing.Union[MetaOapg.properties.installType, str, schemas.Unset] = schemas.unset,
        managedConfigurationTemplateId: typing.Union[MetaOapg.properties.managedConfigurationTemplateId, str, schemas.Unset] = schemas.unset,
        managedProperties: typing.Union[MetaOapg.properties.managedProperties, bool, schemas.Unset] = schemas.unset,
        minSdkVersion: typing.Union[MetaOapg.properties.minSdkVersion, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
        permissionGrants: typing.Union[MetaOapg.properties.permissionGrants, list, tuple, schemas.Unset] = schemas.unset,
        runtimePermission: typing.Union[MetaOapg.properties.runtimePermission, str, schemas.Unset] = schemas.unset,
        startUrl: typing.Union[MetaOapg.properties.startUrl, str, schemas.Unset] = schemas.unset,
        type: typing.Union[MetaOapg.properties.type, str, schemas.Unset] = schemas.unset,
        updateTime: typing.Union[MetaOapg.properties.updateTime, str, schemas.Unset] = schemas.unset,
        versionCode: typing.Union[MetaOapg.properties.versionCode, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'SoftwareAppGoogleAndroid':
        return super().__new__(
            cls,
            *args,
            androidFeatures=androidFeatures,
            appPricing=appPricing,
            appVersion=appVersion,
            author=author,
            autoUpdateMode=autoUpdateMode,
            category=category,
            contentRating=contentRating,
            displayMode=displayMode,
            distributionChannel=distributionChannel,
            fullDescription=fullDescription,
            iconUrl=iconUrl,
            installType=installType,
            managedConfigurationTemplateId=managedConfigurationTemplateId,
            managedProperties=managedProperties,
            minSdkVersion=minSdkVersion,
            name=name,
            permissionGrants=permissionGrants,
            runtimePermission=runtimePermission,
            startUrl=startUrl,
            type=type,
            updateTime=updateTime,
            versionCode=versionCode,
            _configuration=_configuration,
            **kwargs,
        )

from jump_cloud_python_sdk.model.software_app_google_android_android_features import SoftwareAppGoogleAndroidAndroidFeatures
from jump_cloud_python_sdk.model.software_app_permission_grants import SoftwareAppPermissionGrants
