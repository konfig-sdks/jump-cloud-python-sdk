# coding: utf-8

"""
    JumpCloud API

    # Overview  JumpCloud's V2 API. This set of endpoints allows JumpCloud customers to manage objects, groupings and mappings and interact with the JumpCloud Graph.  ## API Best Practices  Read the linked Help Article below for guidance on retrying failed requests to JumpCloud's REST API, as well as best practices for structuring subsequent retry requests. Customizing retry mechanisms based on these recommendations will increase the reliability and dependability of your API calls.  Covered topics include: 1. Important Considerations 2. Supported HTTP Request Methods 3. Response codes 4. API Key rotation 5. Paginating 6. Error handling 7. Retry rates  [JumpCloud Help Center - API Best Practices](https://support.jumpcloud.com/support/s/article/JumpCloud-API-Best-Practices)  # Directory Objects  This API offers the ability to interact with some of our core features; otherwise known as Directory Objects. The Directory Objects are:  * Commands * Policies * Policy Groups * Applications * Systems * Users * User Groups * System Groups * Radius Servers * Directories: Office 365, LDAP,G-Suite, Active Directory * Duo accounts and applications.  The Directory Object is an important concept to understand in order to successfully use JumpCloud API.  ## JumpCloud Graph  We've also introduced the concept of the JumpCloud Graph along with  Directory Objects. The Graph is a powerful aspect of our platform which will enable you to associate objects with each other, or establish membership for certain objects to become members of other objects.  Specific `GET` endpoints will allow you to traverse the JumpCloud Graph to return all indirect and directly bound objects in your organization.  | ![alt text](https://s3.amazonaws.com/jumpcloud-kb/Knowledge+Base+Photos/API+Docs/jumpcloud_graph.png \"JumpCloud Graph Model Example\") | |:--:| | **This diagram highlights our association and membership model as it relates to Directory Objects.** |  # API Key  ## Access Your API Key  To locate your API Key:  1. Log into the [JumpCloud Admin Console](https://console.jumpcloud.com/). 2. Go to the username drop down located in the top-right of the Console. 3. Retrieve your API key from API Settings.  ## API Key Considerations  This API key is associated to the currently logged in administrator. Other admins will have different API keys.  **WARNING** Please keep this API key secret, as it grants full access to any data accessible via your JumpCloud console account.  You can also reset your API key in the same location in the JumpCloud Admin Console.  ## Recycling or Resetting Your API Key  In order to revoke access with the current API key, simply reset your API key. This will render all calls using the previous API key inaccessible.  Your API key will be passed in as a header with the header name \"x-api-key\".  ```bash curl -H \"x-api-key: [YOUR_API_KEY_HERE]\" \"https://console.jumpcloud.com/api/v2/systemgroups\" ```  # System Context  * [Introduction](https://docs.jumpcloud.com) * [Supported endpoints](https://docs.jumpcloud.com) * [Response codes](https://docs.jumpcloud.com) * [Authentication](https://docs.jumpcloud.com) * [Additional examples](https://docs.jumpcloud.com) * [Third party](https://docs.jumpcloud.com)  ## Introduction  JumpCloud System Context Authorization is an alternative way to authenticate with a subset of JumpCloud's REST APIs. Using this method, a system can manage its information and resource associations, allowing modern auto provisioning environments to scale as needed.  **Notes:**   * The following documentation applies to Linux Operating Systems only.  * Systems that have been automatically enrolled using Apple's Device Enrollment Program (DEP) or systems enrolled using the User Portal install are not eligible to use the System Context API to prevent unauthorized access to system groups and resources. If a script that utilizes the System Context API is invoked on a system enrolled in this way, it will display an error.  ## Supported Endpoints  JumpCloud System Context Authorization can be used in conjunction with Systems endpoints found in the V1 API and certain System Group endpoints found in the v2 API.  * A system may fetch, alter, and delete metadata about itself, including manipulating a system's Group and Systemuser associations,   * `/api/systems/{system_id}` | [`GET`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_get) [`PUT`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_put) * A system may delete itself from your JumpCloud organization   * `/api/systems/{system_id}` | [`DELETE`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_delete) * A system may fetch its direct resource associations under v2 (Groups)   * `/api/v2/systems/{system_id}/memberof` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemGroupMembership)   * `/api/v2/systems/{system_id}/associations` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemAssociationsList)   * `/api/v2/systems/{system_id}/users` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemTraverseUser) * A system may alter its direct resource associations under v2 (Groups)   * `/api/v2/systems/{system_id}/associations` | [`POST`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemAssociationsPost) * A system may alter its System Group associations   * `/api/v2/systemgroups/{group_id}/members` | [`POST`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemGroupMembersPost)     * _NOTE_ If a system attempts to alter the system group membership of a different system the request will be rejected  ## Response Codes  If endpoints other than those described above are called using the System Context API, the server will return a `401` response.  ## Authentication  To allow for secure access to our APIs, you must authenticate each API request. JumpCloud System Context Authorization uses [HTTP Signatures](https://tools.ietf.org/html/draft-cavage-http-signatures-00) to authenticate API requests. The HTTP Signatures sent with each request are similar to the signatures used by the Amazon Web Services REST API. To help with the request-signing process, we have provided an [example bash script](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/shell/SigningExample.sh). This example API request simply requests the entire system record. You must be root, or have permissions to access the contents of the `/opt/jc` directory to generate a signature.  Here is a breakdown of the example script with explanations.  First, the script extracts the systemKey from the JSON formatted `/opt/jc/jcagent.conf` file.  ```bash #!/bin/bash conf=\"`cat /opt/jc/jcagent.conf`\" regex=\"systemKey\\\":\\\"(\\w+)\\\"\"  if [[ $conf =~ $regex ]] ; then   systemKey=\"${BASH_REMATCH[1]}\" fi ```  Then, the script retrieves the current date in the correct format.  ```bash now=`date -u \"+%a, %d %h %Y %H:%M:%S GMT\"`; ```  Next, we build a signing string to demonstrate the expected signature format. The signed string must consist of the [request-line](https://tools.ietf.org/html/rfc2616#page-35) and the date header, separated by a newline character.  ```bash signstr=\"GET /api/systems/${systemKey} HTTP/1.1\\ndate: ${now}\" ```  The next step is to calculate and apply the signature. This is a two-step process:  1. Create a signature from the signing string using the JumpCloud Agent private key: ``printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key`` 2. Then Base64-encode the signature string and trim off the newline characters: ``| openssl enc -e -a | tr -d '\\n'``  The combined steps above result in:  ```bash signature=`printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key | openssl enc -e -a | tr -d '\\n'` ; ```  Finally, we make sure the API call sending the signature has the same Authorization and Date header values, HTTP method, and URL that were used in the signing string.  ```bash curl -iq \\   -H \"Accept: application/json\" \\   -H \"Content-Type: application/json\" \\   -H \"Date: ${now}\" \\   -H \"Authorization: Signature keyId=\\\"system/${systemKey}\\\",headers=\\\"request-line date\\\",algorithm=\\\"rsa-sha256\\\",signature=\\\"${signature}\\\"\" \\   --url https://console.jumpcloud.com/api/systems/${systemKey} ```  ### Input Data  All PUT and POST methods should use the HTTP Content-Type header with a value of 'application/json'. PUT methods are used for updating a record. POST methods are used to create a record.  The following example demonstrates how to update the `displayName` of the system.  ```bash signstr=\"PUT /api/systems/${systemKey} HTTP/1.1\\ndate: ${now}\" signature=`printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key | openssl enc -e -a | tr -d '\\n'` ;  curl -iq \\   -d \"{\\\"displayName\\\" : \\\"updated-system-name-1\\\"}\" \\   -X \"PUT\" \\   -H \"Content-Type: application/json\" \\   -H \"Accept: application/json\" \\   -H \"Date: ${now}\" \\   -H \"Authorization: Signature keyId=\\\"system/${systemKey}\\\",headers=\\\"request-line date\\\",algorithm=\\\"rsa-sha256\\\",signature=\\\"${signature}\\\"\" \\   --url https://console.jumpcloud.com/api/systems/${systemKey} ```  ### Output Data  All results will be formatted as JSON.  Here is an abbreviated example of response output:  ```json {   \"_id\": \"625ee96f52e144993e000015\",   \"agentServer\": \"lappy386\",   \"agentVersion\": \"0.9.42\",   \"arch\": \"x86_64\",   \"connectionKey\": \"127.0.0.1_51812\",   \"displayName\": \"ubuntu-1204\",   \"firstContact\": \"2013-10-16T19:30:55.611Z\",   \"hostname\": \"ubuntu-1204\"   ... ```  ## Additional Examples  ### Signing Authentication Example  This example demonstrates how to make an authenticated request to fetch the JumpCloud record for this system.  [SigningExample.sh](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/shell/SigningExample.sh)  ### Shutdown Hook  This example demonstrates how to make an authenticated request on system shutdown. Using an init.d script registered at run level 0, you can call the System Context API as the system is shutting down.  [Instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) is an example of an init.d script that only runs at system shutdown.  After customizing the [instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) script, you should install it on the system(s) running the JumpCloud agent.  1. Copy the modified [instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) to `/etc/init.d/instance-shutdown`. 2. On Ubuntu systems, run `update-rc.d instance-shutdown defaults`. On RedHat/CentOS systems, run `chkconfig --add instance-shutdown`.  ## Third Party  ### Chef Cookbooks  [https://github.com/nshenry03/jumpcloud](https://github.com/nshenry03/jumpcloud)  [https://github.com/cjs226/jumpcloud](https://github.com/cjs226/jumpcloud)  # Multi-Tenant Portal Headers  Multi-Tenant Organization API Headers are available for JumpCloud Admins to use when making API requests from Organizations that have multiple managed organizations.  The `x-org-id` is a required header for all multi-tenant admins when making API requests to JumpCloud. This header will define to which organization you would like to make the request.  **NOTE** Single Tenant Admins do not need to provide this header when making an API request.  ## Header Value  `x-org-id`  ## API Response Codes  * `400` Malformed ID. * `400` x-org-id and Organization path ID do not match. * `401` ID not included for multi-tenant admin * `403` ID included on unsupported route. * `404` Organization ID Not Found.  ```bash curl -X GET https://console.jumpcloud.com/api/v2/directories \\   -H 'accept: application/json' \\   -H 'content-type: application/json' \\   -H 'x-api-key: {API_KEY}' \\   -H 'x-org-id: {ORG_ID}'  ```  ## To Obtain an Individual Organization ID via the UI  As a prerequisite, your Primary Organization will need to be setup for Multi-Tenancy. This provides access to the Multi-Tenant Organization Admin Portal.  1. Log into JumpCloud [Admin Console](https://console.jumpcloud.com). If you are a multi-tenant Admin, you will automatically be routed to the Multi-Tenant Admin Portal. 2. From the Multi-Tenant Portal's primary navigation bar, select the Organization you'd like to access. 3. You will automatically be routed to that Organization's Admin Console. 4. Go to Settings in the sub-tenant's primary navigation. 5. You can obtain your Organization ID below your Organization's Contact Information on the Settings page.  ## To Obtain All Organization IDs via the API  * You can make an API request to this endpoint using the API key of your Primary Organization.  `https://console.jumpcloud.com/api/organizations/` This will return all your managed organizations.  ```bash curl -X GET \\   https://console.jumpcloud.com/api/organizations/ \\   -H 'Accept: application/json' \\   -H 'Content-Type: application/json' \\   -H 'x-api-key: {API_KEY}' ```  # SDKs  You can find language specific SDKs that can help you kickstart your Integration with JumpCloud in the following GitHub repositories:  * [Python](https://github.com/TheJumpCloud/jcapi-python) * [Go](https://github.com/TheJumpCloud/jcapi-go) * [Ruby](https://github.com/TheJumpCloud/jcapi-ruby) * [Java](https://github.com/TheJumpCloud/jcapi-java) 

    The version of the OpenAPI document: 2.0
    Contact: support@jumpcloud.com
    Created by: https://support.jumpcloud.com/support/s/
"""

from dataclasses import dataclass
import typing_extensions
import urllib3
from pydantic import RootModel
from jump_cloud_python_sdk.request_before_hook import request_before_hook
import json
from urllib3._collections import HTTPHeaderDict

from jump_cloud_python_sdk.api_response import AsyncGeneratorResponse
from jump_cloud_python_sdk import api_client, exceptions
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

from jump_cloud_python_sdk.model.google_rpc_status import GoogleRpcStatus as GoogleRpcStatusSchema
from jump_cloud_python_sdk.model.jumpcloud_ingresso_create_access_requests_response import JumpcloudIngressoCreateAccessRequestsResponse as JumpcloudIngressoCreateAccessRequestsResponseSchema
from jump_cloud_python_sdk.model.jumpcloud_ingresso_create_access_requests_request import JumpcloudIngressoCreateAccessRequestsRequest as JumpcloudIngressoCreateAccessRequestsRequestSchema

from jump_cloud_python_sdk.type.google_rpc_status import GoogleRpcStatus
from jump_cloud_python_sdk.type.jumpcloud_ingresso_create_access_requests_response import JumpcloudIngressoCreateAccessRequestsResponse
from jump_cloud_python_sdk.type.jumpcloud_ingresso_create_access_requests_request import JumpcloudIngressoCreateAccessRequestsRequest

from ...api_client import Dictionary
from jump_cloud_python_sdk.pydantic.jumpcloud_ingresso_create_access_requests_response import JumpcloudIngressoCreateAccessRequestsResponse as JumpcloudIngressoCreateAccessRequestsResponsePydantic
from jump_cloud_python_sdk.pydantic.google_rpc_status import GoogleRpcStatus as GoogleRpcStatusPydantic
from jump_cloud_python_sdk.pydantic.jumpcloud_ingresso_create_access_requests_request import JumpcloudIngressoCreateAccessRequestsRequest as JumpcloudIngressoCreateAccessRequestsRequestPydantic

# body param
SchemaForRequestBodyApplicationJson = JumpcloudIngressoCreateAccessRequestsRequestSchema


request_body_jumpcloud_ingresso_create_access_requests_request = api_client.RequestBody(
    content={
        'application/json': api_client.MediaType(
            schema=SchemaForRequestBodyApplicationJson),
    },
    required=True,
)
SchemaFor200ResponseBodyApplicationJson = JumpcloudIngressoCreateAccessRequestsResponseSchema


@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    body: JumpcloudIngressoCreateAccessRequestsResponse


@dataclass
class ApiResponseFor200Async(api_client.AsyncApiResponse):
    body: JumpcloudIngressoCreateAccessRequestsResponse


_response_for_200 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor200,
    response_cls_async=ApiResponseFor200Async,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor200ResponseBodyApplicationJson),
    },
)
SchemaFor0ResponseBodyApplicationJson = GoogleRpcStatusSchema


@dataclass
class ApiResponseForDefault(api_client.ApiResponse):
    body: GoogleRpcStatus


@dataclass
class ApiResponseForDefaultAsync(api_client.AsyncApiResponse):
    body: GoogleRpcStatus


_response_for_default = api_client.OpenApiResponse(
    response_cls=ApiResponseForDefault,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor0ResponseBodyApplicationJson),
    },
)
_all_accept_content_types = (
    'application/json',
)


class BaseApi(api_client.Api):

    def _create_access_request_mapped_args(
        self,
        operation_id: typing.Optional[str] = None,
        additional_attributes: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
        application_int_id: typing.Optional[str] = None,
        expiry: typing.Optional[datetime] = None,
        organization_object_id: typing.Optional[str] = None,
        remarks: typing.Optional[str] = None,
        requestor_id: typing.Optional[str] = None,
        resource_id: typing.Optional[str] = None,
        resource_type: typing.Optional[str] = None,
    ) -> api_client.MappedArgs:
        args: api_client.MappedArgs = api_client.MappedArgs()
        _body = {}
        if operation_id is not None:
            _body["operationId"] = operation_id
        if additional_attributes is not None:
            _body["additionalAttributes"] = additional_attributes
        if application_int_id is not None:
            _body["applicationIntId"] = application_int_id
        if expiry is not None:
            _body["expiry"] = expiry
        if organization_object_id is not None:
            _body["organizationObjectId"] = organization_object_id
        if remarks is not None:
            _body["remarks"] = remarks
        if requestor_id is not None:
            _body["requestorId"] = requestor_id
        if resource_id is not None:
            _body["resourceId"] = resource_id
        if resource_type is not None:
            _body["resourceType"] = resource_type
        args.body = _body
        return args

    async def _acreate_access_request_oapg(
        self,
        body: typing.Any = None,
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        content_type: str = 'application/json',
        stream: bool = False,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        ApiResponseForDefaultAsync,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        """
        Create Access Request
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        used_path = path.value
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add('Accept', accept_content_type)
        method = 'post'.upper()
        _headers.add('Content-Type', content_type)
    
        if body is schemas.unset:
            raise exceptions.ApiValueError(
                'The required body parameter has an invalid value of: unset. Set a valid value instead')
        _fields = None
        _body = None
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            path_template='/accessrequests',
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_jumpcloud_ingresso_create_access_requests_request.serialize(body, content_type)
        if 'fields' in serialized_data:
            _fields = serialized_data['fields']
        elif 'body' in serialized_data:
            _body = serialized_data['body']
    
        response = await self.api_client.async_call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            fields=_fields,
            serialized_body=_body,
            body=body,
            auth_settings=_auth,
            timeout=timeout,
            **kwargs
        )
    
        if stream:
            if not 200 <= response.http_response.status <= 299:
                body = (await response.http_response.content.read()).decode("utf-8")
                raise exceptions.ApiStreamingException(
                    status=response.http_response.status,
                    reason=response.http_response.reason,
                    body=body,
                )
    
            async def stream_iterator():
                """
                iterates over response.http_response.content and closes connection once iteration has finished
                """
                async for line in response.http_response.content:
                    if line == b'\r\n':
                        continue
                    yield line
                response.http_response.close()
                await response.session.close()
            return AsyncGeneratorResponse(
                content=stream_iterator(),
                headers=response.http_response.headers,
                status=response.http_response.status,
                response=response.http_response
            )
    
        response_for_status = _status_code_to_response.get(str(response.http_response.status))
        if response_for_status:
            api_response = await response_for_status.deserialize_async(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
        else:
            default_response = _status_code_to_response.get('default')
            if default_response:
                api_response = default_response.deserialize(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
            else:
                api_response = api_client.ApiResponseWithoutDeserializationAsync(
                    response=response.http_response,
                    round_trip_time=response.round_trip_time,
                    status=response.http_response.status,
                    headers=response.http_response.headers,
                )
    
        if not 200 <= api_response.status <= 299:
            raise exceptions.ApiException(api_response=api_response)
    
        # cleanup session / response
        response.http_response.close()
        await response.session.close()
    
        return api_response


    def _create_access_request_oapg(
        self,
        body: typing.Any = None,
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        content_type: str = 'application/json',
        stream: bool = False,
    ) -> typing.Union[
        ApiResponseFor200,
        ApiResponseForDefault,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """
        Create Access Request
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        used_path = path.value
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add('Accept', accept_content_type)
        method = 'post'.upper()
        _headers.add('Content-Type', content_type)
    
        if body is schemas.unset:
            raise exceptions.ApiValueError(
                'The required body parameter has an invalid value of: unset. Set a valid value instead')
        _fields = None
        _body = None
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            path_template='/accessrequests',
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_jumpcloud_ingresso_create_access_requests_request.serialize(body, content_type)
        if 'fields' in serialized_data:
            _fields = serialized_data['fields']
        elif 'body' in serialized_data:
            _body = serialized_data['body']
    
        response = self.api_client.call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            fields=_fields,
            serialized_body=_body,
            body=body,
            auth_settings=_auth,
            timeout=timeout,
        )
    
        response_for_status = _status_code_to_response.get(str(response.http_response.status))
        if response_for_status:
            api_response = response_for_status.deserialize(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
        else:
            default_response = _status_code_to_response.get('default')
            if default_response:
                api_response = default_response.deserialize(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
            else:
                api_response = api_client.ApiResponseWithoutDeserialization(
                    response=response.http_response,
                    round_trip_time=response.round_trip_time,
                    status=response.http_response.status,
                    headers=response.http_response.headers,
                )
    
        if not 200 <= api_response.status <= 299:
            raise exceptions.ApiException(api_response=api_response)
    
        return api_response


class CreateAccessRequestRaw(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    async def acreate_access_request(
        self,
        operation_id: typing.Optional[str] = None,
        additional_attributes: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
        application_int_id: typing.Optional[str] = None,
        expiry: typing.Optional[datetime] = None,
        organization_object_id: typing.Optional[str] = None,
        remarks: typing.Optional[str] = None,
        requestor_id: typing.Optional[str] = None,
        resource_id: typing.Optional[str] = None,
        resource_type: typing.Optional[str] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        ApiResponseForDefaultAsync,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._create_access_request_mapped_args(
            operation_id=operation_id,
            additional_attributes=additional_attributes,
            application_int_id=application_int_id,
            expiry=expiry,
            organization_object_id=organization_object_id,
            remarks=remarks,
            requestor_id=requestor_id,
            resource_id=resource_id,
            resource_type=resource_type,
        )
        return await self._acreate_access_request_oapg(
            body=args.body,
            **kwargs,
        )
    
    def create_access_request(
        self,
        operation_id: typing.Optional[str] = None,
        additional_attributes: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
        application_int_id: typing.Optional[str] = None,
        expiry: typing.Optional[datetime] = None,
        organization_object_id: typing.Optional[str] = None,
        remarks: typing.Optional[str] = None,
        requestor_id: typing.Optional[str] = None,
        resource_id: typing.Optional[str] = None,
        resource_type: typing.Optional[str] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        ApiResponseForDefault,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        args = self._create_access_request_mapped_args(
            operation_id=operation_id,
            additional_attributes=additional_attributes,
            application_int_id=application_int_id,
            expiry=expiry,
            organization_object_id=organization_object_id,
            remarks=remarks,
            requestor_id=requestor_id,
            resource_id=resource_id,
            resource_type=resource_type,
        )
        return self._create_access_request_oapg(
            body=args.body,
        )

class CreateAccessRequest(BaseApi):

    async def acreate_access_request(
        self,
        operation_id: typing.Optional[str] = None,
        additional_attributes: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
        application_int_id: typing.Optional[str] = None,
        expiry: typing.Optional[datetime] = None,
        organization_object_id: typing.Optional[str] = None,
        remarks: typing.Optional[str] = None,
        requestor_id: typing.Optional[str] = None,
        resource_id: typing.Optional[str] = None,
        resource_type: typing.Optional[str] = None,
        validate: bool = False,
        **kwargs,
    ) -> JumpcloudIngressoCreateAccessRequestsResponsePydantic:
        raw_response = await self.raw.acreate_access_request(
            operation_id=operation_id,
            additional_attributes=additional_attributes,
            application_int_id=application_int_id,
            expiry=expiry,
            organization_object_id=organization_object_id,
            remarks=remarks,
            requestor_id=requestor_id,
            resource_id=resource_id,
            resource_type=resource_type,
            **kwargs,
        )
        if validate:
            return JumpcloudIngressoCreateAccessRequestsResponsePydantic(**raw_response.body)
        return api_client.construct_model_instance(JumpcloudIngressoCreateAccessRequestsResponsePydantic, raw_response.body)
    
    
    def create_access_request(
        self,
        operation_id: typing.Optional[str] = None,
        additional_attributes: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
        application_int_id: typing.Optional[str] = None,
        expiry: typing.Optional[datetime] = None,
        organization_object_id: typing.Optional[str] = None,
        remarks: typing.Optional[str] = None,
        requestor_id: typing.Optional[str] = None,
        resource_id: typing.Optional[str] = None,
        resource_type: typing.Optional[str] = None,
        validate: bool = False,
    ) -> JumpcloudIngressoCreateAccessRequestsResponsePydantic:
        raw_response = self.raw.create_access_request(
            operation_id=operation_id,
            additional_attributes=additional_attributes,
            application_int_id=application_int_id,
            expiry=expiry,
            organization_object_id=organization_object_id,
            remarks=remarks,
            requestor_id=requestor_id,
            resource_id=resource_id,
            resource_type=resource_type,
        )
        if validate:
            return JumpcloudIngressoCreateAccessRequestsResponsePydantic(**raw_response.body)
        return api_client.construct_model_instance(JumpcloudIngressoCreateAccessRequestsResponsePydantic, raw_response.body)


class ApiForpost(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    async def apost(
        self,
        operation_id: typing.Optional[str] = None,
        additional_attributes: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
        application_int_id: typing.Optional[str] = None,
        expiry: typing.Optional[datetime] = None,
        organization_object_id: typing.Optional[str] = None,
        remarks: typing.Optional[str] = None,
        requestor_id: typing.Optional[str] = None,
        resource_id: typing.Optional[str] = None,
        resource_type: typing.Optional[str] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        ApiResponseForDefaultAsync,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._create_access_request_mapped_args(
            operation_id=operation_id,
            additional_attributes=additional_attributes,
            application_int_id=application_int_id,
            expiry=expiry,
            organization_object_id=organization_object_id,
            remarks=remarks,
            requestor_id=requestor_id,
            resource_id=resource_id,
            resource_type=resource_type,
        )
        return await self._acreate_access_request_oapg(
            body=args.body,
            **kwargs,
        )
    
    def post(
        self,
        operation_id: typing.Optional[str] = None,
        additional_attributes: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
        application_int_id: typing.Optional[str] = None,
        expiry: typing.Optional[datetime] = None,
        organization_object_id: typing.Optional[str] = None,
        remarks: typing.Optional[str] = None,
        requestor_id: typing.Optional[str] = None,
        resource_id: typing.Optional[str] = None,
        resource_type: typing.Optional[str] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        ApiResponseForDefault,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        args = self._create_access_request_mapped_args(
            operation_id=operation_id,
            additional_attributes=additional_attributes,
            application_int_id=application_int_id,
            expiry=expiry,
            organization_object_id=organization_object_id,
            remarks=remarks,
            requestor_id=requestor_id,
            resource_id=resource_id,
            resource_type=resource_type,
        )
        return self._create_access_request_oapg(
            body=args.body,
        )

