# coding: utf-8

"""
    JumpCloud API

    # Overview  JumpCloud's V2 API. This set of endpoints allows JumpCloud customers to manage objects, groupings and mappings and interact with the JumpCloud Graph.  ## API Best Practices  Read the linked Help Article below for guidance on retrying failed requests to JumpCloud's REST API, as well as best practices for structuring subsequent retry requests. Customizing retry mechanisms based on these recommendations will increase the reliability and dependability of your API calls.  Covered topics include: 1. Important Considerations 2. Supported HTTP Request Methods 3. Response codes 4. API Key rotation 5. Paginating 6. Error handling 7. Retry rates  [JumpCloud Help Center - API Best Practices](https://support.jumpcloud.com/support/s/article/JumpCloud-API-Best-Practices)  # Directory Objects  This API offers the ability to interact with some of our core features; otherwise known as Directory Objects. The Directory Objects are:  * Commands * Policies * Policy Groups * Applications * Systems * Users * User Groups * System Groups * Radius Servers * Directories: Office 365, LDAP,G-Suite, Active Directory * Duo accounts and applications.  The Directory Object is an important concept to understand in order to successfully use JumpCloud API.  ## JumpCloud Graph  We've also introduced the concept of the JumpCloud Graph along with  Directory Objects. The Graph is a powerful aspect of our platform which will enable you to associate objects with each other, or establish membership for certain objects to become members of other objects.  Specific `GET` endpoints will allow you to traverse the JumpCloud Graph to return all indirect and directly bound objects in your organization.  | ![alt text](https://s3.amazonaws.com/jumpcloud-kb/Knowledge+Base+Photos/API+Docs/jumpcloud_graph.png \"JumpCloud Graph Model Example\") | |:--:| | **This diagram highlights our association and membership model as it relates to Directory Objects.** |  # API Key  ## Access Your API Key  To locate your API Key:  1. Log into the [JumpCloud Admin Console](https://console.jumpcloud.com/). 2. Go to the username drop down located in the top-right of the Console. 3. Retrieve your API key from API Settings.  ## API Key Considerations  This API key is associated to the currently logged in administrator. Other admins will have different API keys.  **WARNING** Please keep this API key secret, as it grants full access to any data accessible via your JumpCloud console account.  You can also reset your API key in the same location in the JumpCloud Admin Console.  ## Recycling or Resetting Your API Key  In order to revoke access with the current API key, simply reset your API key. This will render all calls using the previous API key inaccessible.  Your API key will be passed in as a header with the header name \"x-api-key\".  ```bash curl -H \"x-api-key: [YOUR_API_KEY_HERE]\" \"https://console.jumpcloud.com/api/v2/systemgroups\" ```  # System Context  * [Introduction](https://docs.jumpcloud.com) * [Supported endpoints](https://docs.jumpcloud.com) * [Response codes](https://docs.jumpcloud.com) * [Authentication](https://docs.jumpcloud.com) * [Additional examples](https://docs.jumpcloud.com) * [Third party](https://docs.jumpcloud.com)  ## Introduction  JumpCloud System Context Authorization is an alternative way to authenticate with a subset of JumpCloud's REST APIs. Using this method, a system can manage its information and resource associations, allowing modern auto provisioning environments to scale as needed.  **Notes:**   * The following documentation applies to Linux Operating Systems only.  * Systems that have been automatically enrolled using Apple's Device Enrollment Program (DEP) or systems enrolled using the User Portal install are not eligible to use the System Context API to prevent unauthorized access to system groups and resources. If a script that utilizes the System Context API is invoked on a system enrolled in this way, it will display an error.  ## Supported Endpoints  JumpCloud System Context Authorization can be used in conjunction with Systems endpoints found in the V1 API and certain System Group endpoints found in the v2 API.  * A system may fetch, alter, and delete metadata about itself, including manipulating a system's Group and Systemuser associations,   * `/api/systems/{system_id}` | [`GET`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_get) [`PUT`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_put) * A system may delete itself from your JumpCloud organization   * `/api/systems/{system_id}` | [`DELETE`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_delete) * A system may fetch its direct resource associations under v2 (Groups)   * `/api/v2/systems/{system_id}/memberof` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemGroupMembership)   * `/api/v2/systems/{system_id}/associations` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemAssociationsList)   * `/api/v2/systems/{system_id}/users` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemTraverseUser) * A system may alter its direct resource associations under v2 (Groups)   * `/api/v2/systems/{system_id}/associations` | [`POST`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemAssociationsPost) * A system may alter its System Group associations   * `/api/v2/systemgroups/{group_id}/members` | [`POST`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemGroupMembersPost)     * _NOTE_ If a system attempts to alter the system group membership of a different system the request will be rejected  ## Response Codes  If endpoints other than those described above are called using the System Context API, the server will return a `401` response.  ## Authentication  To allow for secure access to our APIs, you must authenticate each API request. JumpCloud System Context Authorization uses [HTTP Signatures](https://tools.ietf.org/html/draft-cavage-http-signatures-00) to authenticate API requests. The HTTP Signatures sent with each request are similar to the signatures used by the Amazon Web Services REST API. To help with the request-signing process, we have provided an [example bash script](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/shell/SigningExample.sh). This example API request simply requests the entire system record. You must be root, or have permissions to access the contents of the `/opt/jc` directory to generate a signature.  Here is a breakdown of the example script with explanations.  First, the script extracts the systemKey from the JSON formatted `/opt/jc/jcagent.conf` file.  ```bash #!/bin/bash conf=\"`cat /opt/jc/jcagent.conf`\" regex=\"systemKey\\\":\\\"(\\w+)\\\"\"  if [[ $conf =~ $regex ]] ; then   systemKey=\"${BASH_REMATCH[1]}\" fi ```  Then, the script retrieves the current date in the correct format.  ```bash now=`date -u \"+%a, %d %h %Y %H:%M:%S GMT\"`; ```  Next, we build a signing string to demonstrate the expected signature format. The signed string must consist of the [request-line](https://tools.ietf.org/html/rfc2616#page-35) and the date header, separated by a newline character.  ```bash signstr=\"GET /api/systems/${systemKey} HTTP/1.1\\ndate: ${now}\" ```  The next step is to calculate and apply the signature. This is a two-step process:  1. Create a signature from the signing string using the JumpCloud Agent private key: ``printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key`` 2. Then Base64-encode the signature string and trim off the newline characters: ``| openssl enc -e -a | tr -d '\\n'``  The combined steps above result in:  ```bash signature=`printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key | openssl enc -e -a | tr -d '\\n'` ; ```  Finally, we make sure the API call sending the signature has the same Authorization and Date header values, HTTP method, and URL that were used in the signing string.  ```bash curl -iq \\   -H \"Accept: application/json\" \\   -H \"Content-Type: application/json\" \\   -H \"Date: ${now}\" \\   -H \"Authorization: Signature keyId=\\\"system/${systemKey}\\\",headers=\\\"request-line date\\\",algorithm=\\\"rsa-sha256\\\",signature=\\\"${signature}\\\"\" \\   --url https://console.jumpcloud.com/api/systems/${systemKey} ```  ### Input Data  All PUT and POST methods should use the HTTP Content-Type header with a value of 'application/json'. PUT methods are used for updating a record. POST methods are used to create a record.  The following example demonstrates how to update the `displayName` of the system.  ```bash signstr=\"PUT /api/systems/${systemKey} HTTP/1.1\\ndate: ${now}\" signature=`printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key | openssl enc -e -a | tr -d '\\n'` ;  curl -iq \\   -d \"{\\\"displayName\\\" : \\\"updated-system-name-1\\\"}\" \\   -X \"PUT\" \\   -H \"Content-Type: application/json\" \\   -H \"Accept: application/json\" \\   -H \"Date: ${now}\" \\   -H \"Authorization: Signature keyId=\\\"system/${systemKey}\\\",headers=\\\"request-line date\\\",algorithm=\\\"rsa-sha256\\\",signature=\\\"${signature}\\\"\" \\   --url https://console.jumpcloud.com/api/systems/${systemKey} ```  ### Output Data  All results will be formatted as JSON.  Here is an abbreviated example of response output:  ```json {   \"_id\": \"625ee96f52e144993e000015\",   \"agentServer\": \"lappy386\",   \"agentVersion\": \"0.9.42\",   \"arch\": \"x86_64\",   \"connectionKey\": \"127.0.0.1_51812\",   \"displayName\": \"ubuntu-1204\",   \"firstContact\": \"2013-10-16T19:30:55.611Z\",   \"hostname\": \"ubuntu-1204\"   ... ```  ## Additional Examples  ### Signing Authentication Example  This example demonstrates how to make an authenticated request to fetch the JumpCloud record for this system.  [SigningExample.sh](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/shell/SigningExample.sh)  ### Shutdown Hook  This example demonstrates how to make an authenticated request on system shutdown. Using an init.d script registered at run level 0, you can call the System Context API as the system is shutting down.  [Instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) is an example of an init.d script that only runs at system shutdown.  After customizing the [instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) script, you should install it on the system(s) running the JumpCloud agent.  1. Copy the modified [instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) to `/etc/init.d/instance-shutdown`. 2. On Ubuntu systems, run `update-rc.d instance-shutdown defaults`. On RedHat/CentOS systems, run `chkconfig --add instance-shutdown`.  ## Third Party  ### Chef Cookbooks  [https://github.com/nshenry03/jumpcloud](https://github.com/nshenry03/jumpcloud)  [https://github.com/cjs226/jumpcloud](https://github.com/cjs226/jumpcloud)  # Multi-Tenant Portal Headers  Multi-Tenant Organization API Headers are available for JumpCloud Admins to use when making API requests from Organizations that have multiple managed organizations.  The `x-org-id` is a required header for all multi-tenant admins when making API requests to JumpCloud. This header will define to which organization you would like to make the request.  **NOTE** Single Tenant Admins do not need to provide this header when making an API request.  ## Header Value  `x-org-id`  ## API Response Codes  * `400` Malformed ID. * `400` x-org-id and Organization path ID do not match. * `401` ID not included for multi-tenant admin * `403` ID included on unsupported route. * `404` Organization ID Not Found.  ```bash curl -X GET https://console.jumpcloud.com/api/v2/directories \\   -H 'accept: application/json' \\   -H 'content-type: application/json' \\   -H 'x-api-key: {API_KEY}' \\   -H 'x-org-id: {ORG_ID}'  ```  ## To Obtain an Individual Organization ID via the UI  As a prerequisite, your Primary Organization will need to be setup for Multi-Tenancy. This provides access to the Multi-Tenant Organization Admin Portal.  1. Log into JumpCloud [Admin Console](https://console.jumpcloud.com). If you are a multi-tenant Admin, you will automatically be routed to the Multi-Tenant Admin Portal. 2. From the Multi-Tenant Portal's primary navigation bar, select the Organization you'd like to access. 3. You will automatically be routed to that Organization's Admin Console. 4. Go to Settings in the sub-tenant's primary navigation. 5. You can obtain your Organization ID below your Organization's Contact Information on the Settings page.  ## To Obtain All Organization IDs via the API  * You can make an API request to this endpoint using the API key of your Primary Organization.  `https://console.jumpcloud.com/api/organizations/` This will return all your managed organizations.  ```bash curl -X GET \\   https://console.jumpcloud.com/api/organizations/ \\   -H 'Accept: application/json' \\   -H 'Content-Type: application/json' \\   -H 'x-api-key: {API_KEY}' ```  # SDKs  You can find language specific SDKs that can help you kickstart your Integration with JumpCloud in the following GitHub repositories:  * [Python](https://github.com/TheJumpCloud/jcapi-python) * [Go](https://github.com/TheJumpCloud/jcapi-go) * [Ruby](https://github.com/TheJumpCloud/jcapi-ruby) * [Java](https://github.com/TheJumpCloud/jcapi-java) 

    The version of the OpenAPI document: 2.0
    Contact: support@jumpcloud.com
    Created by: https://support.jumpcloud.com/support/s/
"""

from collections import defaultdict
from datetime import date, datetime, timedelta  # noqa: F401
import pydantic
import functools
import decimal
import io
import re
import types
import typing
import typing_extensions
import uuid

from dateutil.parser.isoparser import isoparser, _takes_ascii
import frozendict

from jump_cloud_python_sdk.exceptions_base import (
    ApiTypeError,
    ApiValueError,
)
from jump_cloud_python_sdk.configuration import (
    Configuration,
)
from jump_cloud_python_sdk.exceptions import SchemaValidationError
from jump_cloud_python_sdk.exceptions import render_path
from jump_cloud_python_sdk.validation_metadata import ValidationMetadata
from jump_cloud_python_sdk.exceptions import AnyOfValidationError
from jump_cloud_python_sdk.exceptions import MissingRequiredPropertiesError

Primitive: typing_extensions.TypeAlias = typing.Union[int, float, bool, str]

class Unset(object):
    """
    An instance of this class is set as the default value for object type(dict) properties that are optional
    When a property has an unset value, that property will not be assigned in the dict
    """
    pass

unset = Unset()

none_type = type(None)
file_type = io.IOBase


class FileIO(io.FileIO):
    """
    A class for storing files
    Note: this class is not immutable
    """

    def __new__(cls, arg: typing.Union[io.FileIO, io.BufferedReader]):
        if isinstance(arg, (io.FileIO, io.BufferedReader)):
            if arg.closed:
                raise ApiValueError('Invalid file state; file is closed and must be open')
            arg.close()
            inst = super(FileIO, cls).__new__(cls, arg.name)
            super(FileIO, inst).__init__(arg.name)
            return inst
        raise ApiValueError('FileIO must be passed arg which contains the open file')

    def __init__(self, arg: typing.Union[io.FileIO, io.BufferedReader]):
        pass


def update(d: dict, u: dict):
    """
    Adds u to d
    Where each dict is defaultdict(set)
    """
    if not u:
        return d
    for k, v in u.items():
        if k not in d:
            d[k] = v
        else:
            d[k] = d[k] | v


class Singleton:
    """
    Enums and singletons are the same
    The same instance is returned for a given key of (cls, arg)
    """
    _instances = {}

    def __new__(cls, arg: typing.Any, **kwargs):
        """
        cls base classes: BoolClass, NoneClass, str, decimal.Decimal
        The 3rd key is used in the tuple below for a corner case where an enum contains integer 1
        However 1.0  can also be ingested into that enum schema because 1.0 == 1 and
        Decimal('1.0') == Decimal('1')
        But if we omitted the 3rd value in the key, then Decimal('1.0') would be stored as Decimal('1')
        and json serializing that instance would be '1' rather than the expected '1.0'
        Adding the 3rd value, the str of arg ensures that 1.0 -> Decimal('1.0') which is serialized as 1.0
        """
        key = (cls, arg, str(arg))
        if key not in cls._instances:
            if isinstance(arg, (none_type, bool, BoolClass, NoneClass)):
                inst = super().__new__(cls)
                cls._instances[key] = inst
            else:
                cls._instances[key] = super().__new__(cls, arg)
        return cls._instances[key]

    def __repr__(self):
        if isinstance(self, NoneClass):
            return f'<{self.__class__.__name__}: None>'
        elif isinstance(self, BoolClass):
            if bool(self):
                return f'<{self.__class__.__name__}: True>'
            return f'<{self.__class__.__name__}: False>'
        return f'<{self.__class__.__name__}: {super().__repr__()}>'


class classproperty:

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class NoneClass(Singleton):
    @classproperty
    def NONE(cls):
        return cls(None)

    def __bool__(self) -> bool:
        return False


class BoolClass(Singleton):
    @classproperty
    def TRUE(cls):
        return cls(True)

    @classproperty
    def FALSE(cls):
        return cls(False)

    @functools.lru_cache()
    def __bool__(self) -> bool:
        for key, instance in self._instances.items():
            if self is instance:
                return bool(key[1])
        raise ValueError('Unable to find the boolean value of this instance')

    def __str__(self) -> str:
        return str(bool(self))


class MetaOapgTyped:
    exclusive_maximum: typing.Union[int, float]
    inclusive_maximum: typing.Union[int, float]
    exclusive_minimum: typing.Union[int, float]
    inclusive_minimum: typing.Union[int, float]
    max_items: int
    min_items: int
    discriminator: typing.Dict[str, typing.Dict[str, typing.Type['Schema']]]
    x_konfig_strip: bool


    class properties:
        # to hold object properties
        pass

    additional_properties: typing.Optional[typing.Type['Schema']]
    max_properties: int
    min_properties: int
    all_of: typing.Callable[[], typing.List[typing.Type['Schema']]]
    one_of: typing.Callable[[], typing.List[typing.Type['Schema']]]
    any_of: typing.Callable[[], typing.List[typing.Type['Schema']]]
    not_schema: typing.Type['Schema']
    max_length: int
    min_length: int
    items: typing.Type['Schema']


class Schema:
    """
    the base class of all swagger/openapi schemas/models
    """
    __inheritable_primitive_types_set = {decimal.Decimal, str, tuple, frozendict.frozendict, FileIO, bytes, BoolClass, NoneClass}
    _types: typing.Set[typing.Type]
    MetaOapg = MetaOapgTyped

    @staticmethod
    def __get_valid_classes_phrase(input_classes):
        """Returns a string phrase describing what types are allowed"""
        all_classes = list(input_classes)
        all_classes = sorted(all_classes, key=lambda cls: cls.__name__)
        all_class_names = [cls.__name__ for cls in all_classes]
        if len(all_class_names) == 1:
            return "is {0}".format(all_class_names[0])
        return "is one of [{0}]".format(", ".join(all_class_names))

    @staticmethod
    def _get_class_oapg(item_cls: typing.Union[types.FunctionType, staticmethod, typing.Type['Schema']]) -> typing.Type['Schema']:
        if isinstance(item_cls, types.FunctionType):
            # referenced schema
            return item_cls()
        elif isinstance(item_cls, staticmethod):
            # referenced schema
            return item_cls.__func__()
        return item_cls

    @classmethod
    def __type_error_message(
        cls, var_value=None, var_name=None, valid_classes=None, key_type=None
    ):
        """
        Keyword Args:
            var_value (any): the variable which has the type_error
            var_name (str): the name of the variable which has the typ error
            valid_classes (tuple): the accepted classes for current_item's
                                      value
            key_type (bool): False if our value is a value in a dict
                             True if it is a key in a dict
                             False if our item is an item in a tuple
        """
        key_or_value = "value"
        if key_type:
            key_or_value = "key"
        valid_classes_phrase = cls.__get_valid_classes_phrase(valid_classes)
        msg = "Invalid type. Required {0} type {1} and " "passed type was {2} for \"{3}\"".format(
            key_or_value,
            valid_classes_phrase,
            type(var_value).__name__,
            var_name,
        )
        return msg

    @classmethod
    def __get_type_error(cls, var_value, path_to_item, valid_classes, key_type=False):
        error_msg = cls.__type_error_message(
            var_name=path_to_item[-1],
            var_value=var_value,
            valid_classes=valid_classes,
            key_type=key_type,
        )
        return ApiTypeError(
            error_msg,
            invalid_value=var_value,
            path_to_item=path_to_item,
            valid_classes=valid_classes,
            key_type=key_type,
        )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ) -> typing.Dict[typing.Tuple[typing.Union[str, int], ...], typing.Set[typing.Union['Schema', str, decimal.Decimal, BoolClass, NoneClass, frozendict.frozendict, tuple]]]:
        """
        Schema _validate_oapg
        All keyword validation except for type checking was done in calling stack frames
        If those validations passed, the validated classes are collected in path_to_schemas

        Returns:
            path_to_schemas: a map of path to schemas

        Raises:
            ApiValueError: when a string can't be converted into a date or datetime and it must be one of those classes
            ApiTypeError: when the input type is not in the list of allowed spec types
        """
        base_class = type(arg)
        if base_class not in cls._types:
            raise cls.__get_type_error(
                arg,
                validation_metadata.path_to_item,
                cls._types,
                key_type=False,
            )

        path_to_schemas = {validation_metadata.path_to_item: set()}
        path_to_schemas[validation_metadata.path_to_item].add(cls)
        path_to_schemas[validation_metadata.path_to_item].add(base_class)
        return path_to_schemas

    @staticmethod
    def _process_schema_classes_oapg(
        schema_classes: typing.Set[typing.Union['Schema', str, decimal.Decimal, BoolClass, NoneClass, frozendict.frozendict, tuple]]
    ):
        """
        Processes and mutates schema_classes
        If a SomeSchema is a subclass of DictSchema then remove DictSchema because it is already included
        """
        if len(schema_classes) < 2:
            return
        if len(schema_classes) > 2 and UnsetAnyTypeSchema in schema_classes:
            schema_classes.remove(UnsetAnyTypeSchema)
        x_schema = schema_type_classes & schema_classes
        if not x_schema:
            return
        x_schema = x_schema.pop()
        if any(c is not x_schema and issubclass(c, x_schema) for c in schema_classes):
            # needed to not have a mro error in get_new_class
            schema_classes.remove(x_schema)

    @classmethod
    def __get_new_cls(
        cls,
        arg,
        validation_metadata: ValidationMetadata
    ) -> typing.Dict[typing.Tuple[typing.Union[str, int], ...], typing.Type['Schema']]:
        """
        Make a new dynamic class and return an instance of that class
        We are making an instance of cls, but instead of making cls
        make a new class, new_cls
        which includes dynamic bases including cls
        return an instance of that new class

        Dict property + List Item Assignment Use cases:
        1. value is NOT an instance of the required schema class
            the value is validated by _validate_oapg
            _validate_oapg returns a key value pair
            where the key is the path to the item, and the value will be the required manufactured class
            made out of the matching schemas
        2. value is an instance of the the correct schema type
            the value is NOT validated by _validate_oapg, _validate_oapg only checks that the instance is of the correct schema type
            for this value, _validate_oapg does NOT return an entry for it in _path_to_schemas
            and in list/dict _get_items_oapg,_get_properties_oapg the value will be directly assigned
            because value is of the correct type, and validation was run earlier when the instance was created
        """
        _path_to_schemas = {}
        if validation_metadata.validated_path_to_schemas:
            update(_path_to_schemas, validation_metadata.validated_path_to_schemas)
        if not validation_metadata.validation_ran_earlier(cls):
            other_path_to_schemas = cls._validate_oapg(arg, validation_metadata=validation_metadata)
            update(_path_to_schemas, other_path_to_schemas)
        # loop through it make a new class for each entry
        # do not modify the returned result because it is cached and we would be modifying the cached value
        path_to_schemas = {}
        for path, schema_classes in _path_to_schemas.items():
            """
            Use cases
            1. N number of schema classes + enum + type != bool/None, classes in path_to_schemas: tuple/frozendict.frozendict/str/Decimal/bytes/FileIo
                needs Singleton added
            2. N number of schema classes + enum + type == bool/None, classes in path_to_schemas: BoolClass/NoneClass
                Singleton already added
            3. N number of schema classes, classes in path_to_schemas: BoolClass/NoneClass/tuple/frozendict.frozendict/str/Decimal/bytes/FileIo
            """
            cls._process_schema_classes_oapg(schema_classes)
            enum_schema = any(
                issubclass(this_cls, EnumBase) for this_cls in schema_classes)
            inheritable_primitive_type = schema_classes.intersection(cls.__inheritable_primitive_types_set)
            chosen_schema_classes = schema_classes - inheritable_primitive_type
            suffix = tuple(inheritable_primitive_type)
            if enum_schema and suffix[0] not in {NoneClass, BoolClass}:
                suffix = (Singleton,) + suffix

            used_classes = tuple(sorted(chosen_schema_classes, key=lambda a_cls: a_cls.__name__)) + suffix
            mfg_cls = get_new_class(class_name='DynamicSchema', bases=used_classes)
            path_to_schemas[path] = mfg_cls

        return path_to_schemas

    @classmethod
    def _get_new_instance_without_conversion_oapg(
        cls,
        arg: typing.Any,
        path_to_item: typing.Tuple[typing.Union[str, int], ...],
        path_to_schemas: typing.Dict[typing.Tuple[typing.Union[str, int], ...], typing.Type['Schema']]
    ):
        # We have a Dynamic class and we are making an instance of it
        if issubclass(cls, frozendict.frozendict) and issubclass(cls, DictBase):
            properties = cls._get_properties_oapg(arg, path_to_item, path_to_schemas)
            return super(Schema, cls).__new__(cls, properties)
        elif issubclass(cls, tuple) and issubclass(cls, ListBase):
            items = cls._get_items_oapg(arg, path_to_item, path_to_schemas)
            return super(Schema, cls).__new__(cls, items)
        """
        str = openapi str, date, and datetime
        decimal.Decimal = openapi int and float
        FileIO = openapi binary type and the user inputs a file
        bytes = openapi binary type and the user inputs bytes
        """
        try:
            # In some cases (e.g. an int with enforced minimum value) this will throw an error:
            # TypeError('object.__new__(DynamicSchema) is not safe, use DynamicSchema.__new__()')
            res = super(Schema, cls).__new__(cls, arg)
        except TypeError:
            res = cls.__new__(cls, arg)
        return res

    @classmethod
    def from_openapi_data_oapg(
        cls,
        arg: typing.Union[
            str,
            date,
            datetime,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            'Schema',
            dict,
            frozendict.frozendict,
            tuple,
            list,
            io.FileIO,
            io.BufferedReader,
            bytes
        ],
        _configuration: typing.Optional[Configuration]
    ):
        """
        Schema from_openapi_data_oapg
        """
        from_server = True
        validated_path_to_schemas = {}
        arg = cast_to_allowed_types(arg, from_server, validated_path_to_schemas)
        validation_metadata = ValidationMetadata(
            from_server=from_server, configuration=_configuration, validated_path_to_schemas=validated_path_to_schemas)
        path_to_schemas = cls.__get_new_cls(arg, validation_metadata)
        new_cls = path_to_schemas[validation_metadata.path_to_item]
        new_inst = new_cls._get_new_instance_without_conversion_oapg(
            arg,
            validation_metadata.path_to_item,
            path_to_schemas
        )
        return new_inst

    @staticmethod
    def __get_input_dict(*args, **kwargs) -> frozendict.frozendict:
        input_dict = {}
        if args and isinstance(args[0], (dict, frozendict.frozendict)):
            input_dict.update(args[0])
        if kwargs:
            input_dict.update(kwargs)
        return frozendict.frozendict(input_dict)

    @staticmethod
    def __remove_unsets(kwargs):
        return {key: val for key, val in kwargs.items() if val is not unset}

    def __new__(cls, *args: typing.Union[dict, frozendict.frozendict, list, tuple, decimal.Decimal, float, int, str, date, datetime, bool, None, 'Schema'], _configuration: typing.Optional[Configuration] = None, **kwargs: typing.Union[dict, frozendict.frozendict, list, tuple, decimal.Decimal, float, int, str, date, datetime, bool, None, 'Schema', Unset]):
        """
        Schema __new__

        Args:
            args (int/float/decimal.Decimal/str/list/tuple/dict/frozendict.frozendict/bool/None): the value
            kwargs (str, int/float/decimal.Decimal/str/list/tuple/dict/frozendict.frozendict/bool/None): dict values
            _configuration: contains the Configuration that enables json schema validation keywords
                like minItems, minLength etc

        Note: double underscores are used here because pycharm thinks that these variables
        are instance properties if they are named normally :(
        """
        _kwargs = cls.__remove_unsets(kwargs)
        if not args and not _kwargs:
            raise TypeError(
                'No input given. args or kwargs must be given.'
            )
        if not _kwargs and args and not isinstance(args[0], dict):
            _arg = args[0]
        else:
            _arg = cls.__get_input_dict(*args, **_kwargs)
        _from_server = False
        _validated_path_to_schemas = {}
        _arg = cast_to_allowed_types(
            _arg, _from_server, _validated_path_to_schemas, schema=cls)
        _validation_metadata = ValidationMetadata(
            configuration=_configuration, from_server=_from_server, validated_path_to_schemas=_validated_path_to_schemas)
        _path_to_schemas = cls.__get_new_cls(_arg, _validation_metadata)
        _new_cls = _path_to_schemas[_validation_metadata.path_to_item]
        return _new_cls._get_new_instance_without_conversion_oapg(
            _arg,
            _validation_metadata.path_to_item,
            _path_to_schemas
        )

    def __init__(
        self,
        *args: typing.Union[
            dict, frozendict.frozendict, list, tuple, decimal.Decimal, float, int, str, date, datetime, bool, None, 'Schema'],
        _configuration: typing.Optional[Configuration] = None,
        **kwargs: typing.Union[
            dict, frozendict.frozendict, list, tuple, decimal.Decimal, float, int, str, date, datetime, bool, None, 'Schema', Unset
        ]
    ):
        """
        this is needed to fix 'Unexpected argument' warning in pycharm
        this code does nothing because all Schema instances are immutable
        this means that all input data is passed into and used in new, and after the new instance is made
        no new attributes are assigned and init is not used
        """
        pass

"""
import itertools
data_types = ('None', 'FrozenDict', 'Tuple', 'Str', 'Decimal', 'Bool')
type_to_cls = {
    'None': 'NoneClass',
    'FrozenDict': 'frozendict.frozendict',
    'Tuple': 'tuple',
    'Str': 'str',
    'Decimal': 'decimal.Decimal',
    'Bool': 'BoolClass'
}
cls_tuples = [v for v in itertools.combinations(data_types, 5)]
typed_classes = [f"class {''.join(cls_tuple)}Mixin({', '.join(type_to_cls[typ] for typ in cls_tuple)}):\n    pass" for cls_tuple in cls_tuples]
for cls in typed_classes:
    print(cls)
object_classes = [f"{''.join(cls_tuple)}Mixin = object" for cls_tuple in cls_tuples]
for cls in object_classes:
    print(cls)
"""
if typing.TYPE_CHECKING:
    # qty 1
    NoneMixin = NoneClass
    FrozenDictMixin = frozendict.frozendict
    IntMixin = int
    TupleMixin = tuple
    StrMixin = str
    DecimalMixin = decimal.Decimal
    BoolMixin = BoolClass
    BytesMixin = bytes
    FileMixin = FileIO
    # qty 2
    class NumberMixin(decimal.Decimal, int):
        pass
    class BinaryMixin(bytes, FileIO):
        pass
    class NoneFrozenDictMixin(NoneClass, frozendict.frozendict):
        pass
    class NoneTupleMixin(NoneClass, tuple):
        pass
    class NoneStrMixin(NoneClass, str):
        pass
    class NoneDecimalMixin(NoneClass, decimal.Decimal):
        pass
    class NoneBoolMixin(NoneClass, BoolClass):
        pass
    class FrozenDictTupleMixin(frozendict.frozendict, tuple):
        pass
    class FrozenDictStrMixin(frozendict.frozendict, str):
        pass
    class FrozenDictDecimalMixin(frozendict.frozendict, decimal.Decimal):
        pass
    class FrozenDictBoolMixin(frozendict.frozendict, BoolClass):
        pass
    class TupleStrMixin(tuple, str):
        pass
    class TupleDecimalMixin(tuple, decimal.Decimal):
        pass
    class TupleBoolMixin(tuple, BoolClass):
        pass
    class StrDecimalMixin(str, decimal.Decimal):
        pass
    class StrBoolMixin(str, BoolClass):
        pass
    class DecimalBoolMixin(decimal.Decimal, BoolClass):
        pass
    # qty 3
    class NoneFrozenDictTupleMixin(NoneClass, frozendict.frozendict, tuple):
        pass
    class NoneFrozenDictStrMixin(NoneClass, frozendict.frozendict, str):
        pass
    class NoneFrozenDictDecimalMixin(NoneClass, frozendict.frozendict, decimal.Decimal):
        pass
    class NoneFrozenDictBoolMixin(NoneClass, frozendict.frozendict, BoolClass):
        pass
    class NoneTupleStrMixin(NoneClass, tuple, str):
        pass
    class NoneTupleDecimalMixin(NoneClass, tuple, decimal.Decimal):
        pass
    class NoneTupleBoolMixin(NoneClass, tuple, BoolClass):
        pass
    class NoneStrDecimalMixin(NoneClass, str, decimal.Decimal):
        pass
    class NoneStrBoolMixin(NoneClass, str, BoolClass):
        pass
    class NoneDecimalBoolMixin(NoneClass, decimal.Decimal, BoolClass):
        pass
    class FrozenDictTupleStrMixin(frozendict.frozendict, tuple, str):
        pass
    class FrozenDictTupleDecimalMixin(frozendict.frozendict, tuple, decimal.Decimal):
        pass
    class FrozenDictTupleBoolMixin(frozendict.frozendict, tuple, BoolClass):
        pass
    class FrozenDictStrDecimalMixin(frozendict.frozendict, str, decimal.Decimal):
        pass
    class FrozenDictStrBoolMixin(frozendict.frozendict, str, BoolClass):
        pass
    class FrozenDictDecimalBoolMixin(frozendict.frozendict, decimal.Decimal, BoolClass):
        pass
    class TupleStrDecimalMixin(tuple, str, decimal.Decimal):
        pass
    class TupleStrBoolMixin(tuple, str, BoolClass):
        pass
    class TupleDecimalBoolMixin(tuple, decimal.Decimal, BoolClass):
        pass
    class StrDecimalBoolMixin(str, decimal.Decimal, BoolClass):
        pass
    # qty 4
    class NoneFrozenDictTupleStrMixin(NoneClass, frozendict.frozendict, tuple, str):
        pass
    class NoneFrozenDictTupleDecimalMixin(NoneClass, frozendict.frozendict, tuple, decimal.Decimal):
        pass
    class NoneFrozenDictTupleBoolMixin(NoneClass, frozendict.frozendict, tuple, BoolClass):
        pass
    class NoneFrozenDictStrDecimalMixin(NoneClass, frozendict.frozendict, str, decimal.Decimal):
        pass
    class NoneFrozenDictStrBoolMixin(NoneClass, frozendict.frozendict, str, BoolClass):
        pass
    class NoneFrozenDictDecimalBoolMixin(NoneClass, frozendict.frozendict, decimal.Decimal, BoolClass):
        pass
    class NoneTupleStrDecimalMixin(NoneClass, tuple, str, decimal.Decimal):
        pass
    class NoneTupleStrBoolMixin(NoneClass, tuple, str, BoolClass):
        pass
    class NoneTupleDecimalBoolMixin(NoneClass, tuple, decimal.Decimal, BoolClass):
        pass
    class NoneStrDecimalBoolMixin(NoneClass, str, decimal.Decimal, BoolClass):
        pass
    class FrozenDictTupleStrDecimalMixin(frozendict.frozendict, tuple, str, decimal.Decimal):
        pass
    class FrozenDictTupleStrBoolMixin(frozendict.frozendict, tuple, str, BoolClass):
        pass
    class FrozenDictTupleDecimalBoolMixin(frozendict.frozendict, tuple, decimal.Decimal, BoolClass):
        pass
    class FrozenDictStrDecimalBoolMixin(frozendict.frozendict, str, decimal.Decimal, BoolClass):
        pass
    class TupleStrDecimalBoolMixin(tuple, str, decimal.Decimal, BoolClass):
        pass
    # qty 5
    class NoneFrozenDictTupleStrDecimalMixin(NoneClass, frozendict.frozendict, tuple, str, decimal.Decimal):
        pass
    class NoneFrozenDictTupleStrBoolMixin(NoneClass, frozendict.frozendict, tuple, str, BoolClass):
        pass
    class NoneFrozenDictTupleDecimalBoolMixin(NoneClass, frozendict.frozendict, tuple, decimal.Decimal, BoolClass):
        pass
    class NoneFrozenDictStrDecimalBoolMixin(NoneClass, frozendict.frozendict, str, decimal.Decimal, BoolClass):
        pass
    class NoneTupleStrDecimalBoolMixin(NoneClass, tuple, str, decimal.Decimal, BoolClass):
        pass
    class FrozenDictTupleStrDecimalBoolMixin(frozendict.frozendict, tuple, str, decimal.Decimal, BoolClass):
        pass
    # qty 6
    class NoneFrozenDictTupleStrDecimalBoolMixin(NoneClass, frozendict.frozendict, tuple, str, decimal.Decimal, BoolClass):
        pass
    # qty 9
    class NoneFrozenDictTupleStrIntDecimalBoolFileBytesMixin(NoneClass, frozendict.frozendict, tuple, str, int, decimal.Decimal, BoolClass, FileIO, bytes):
        pass
else:
    # qty 1
    class NoneMixin:
        _types = {NoneClass}
    class FrozenDictMixin:
        _types = {frozendict.frozendict}
    class TupleMixin:
        _types = {tuple}
    class StrMixin:
        _types = {str}
    class DecimalMixin:
        _types = {decimal.Decimal}
    class IntMixin:
        _types = {int}
    class BoolMixin:
        _types = {BoolClass}
    class BytesMixin:
        _types = {bytes}
    class FileMixin:
        _types = {FileIO}
    # qty 2
    class NumberMixin:
        _types = {decimal.Decimal, int}
    class BinaryMixin:
        _types = {bytes, FileIO}
    class NoneFrozenDictMixin:
        _types = {NoneClass, frozendict.frozendict}
    class NoneTupleMixin:
        _types = {NoneClass, tuple}
    class NoneStrMixin:
        _types = {NoneClass, str}
    class NoneDecimalMixin:
        _types = {NoneClass, decimal.Decimal}
    class NoneBoolMixin:
        _types = {NoneClass, BoolClass}
    class FrozenDictTupleMixin:
        _types = {frozendict.frozendict, tuple}
    class FrozenDictStrMixin:
        _types = {frozendict.frozendict, str}
    class FrozenDictDecimalMixin:
        _types = {frozendict.frozendict, decimal.Decimal}
    class FrozenDictBoolMixin:
        _types = {frozendict.frozendict, BoolClass}
    class TupleStrMixin:
        _types = {tuple, str}
    class TupleDecimalMixin:
        _types = {tuple, decimal.Decimal}
    class TupleBoolMixin:
        _types = {tuple, BoolClass}
    class StrDecimalMixin:
        _types = {str, decimal.Decimal}
    class StrBoolMixin:
        _types = {str, BoolClass}
    class DecimalBoolMixin:
        _types = {decimal.Decimal, BoolClass}
    # qty 3
    class NoneFrozenDictTupleMixin:
        _types = {NoneClass, frozendict.frozendict, tuple}
    class NoneFrozenDictStrMixin:
        _types = {NoneClass, frozendict.frozendict, str}
    class NoneFrozenDictDecimalMixin:
        _types = {NoneClass, frozendict.frozendict, decimal.Decimal}
    class NoneFrozenDictBoolMixin:
        _types = {NoneClass, frozendict.frozendict, BoolClass}
    class NoneTupleStrMixin:
        _types = {NoneClass, tuple, str}
    class NoneTupleDecimalMixin:
        _types = {NoneClass, tuple, decimal.Decimal}
    class NoneTupleBoolMixin:
        _types = {NoneClass, tuple, BoolClass}
    class NoneStrDecimalMixin:
        _types = {NoneClass, str, decimal.Decimal}
    class NoneStrBoolMixin:
        _types = {NoneClass, str, BoolClass}
    class NoneDecimalBoolMixin:
        _types = {NoneClass, decimal.Decimal, BoolClass}
    class FrozenDictTupleStrMixin:
        _types = {frozendict.frozendict, tuple, str}
    class FrozenDictTupleDecimalMixin:
        _types = {frozendict.frozendict, tuple, decimal.Decimal}
    class FrozenDictTupleBoolMixin:
        _types = {frozendict.frozendict, tuple, BoolClass}
    class FrozenDictStrDecimalMixin:
        _types = {frozendict.frozendict, str, decimal.Decimal}
    class FrozenDictStrBoolMixin:
        _types = {frozendict.frozendict, str, BoolClass}
    class FrozenDictDecimalBoolMixin:
        _types = {frozendict.frozendict, decimal.Decimal, BoolClass}
    class TupleStrDecimalMixin:
        _types = {tuple, str, decimal.Decimal}
    class TupleStrBoolMixin:
        _types = {tuple, str, BoolClass}
    class TupleDecimalBoolMixin:
        _types = {tuple, decimal.Decimal, BoolClass}
    class StrDecimalBoolMixin:
        _types = {str, decimal.Decimal, BoolClass}
    # qty 4
    class NoneFrozenDictTupleStrMixin:
        _types = {NoneClass, frozendict.frozendict, tuple, str}
    class NoneFrozenDictTupleDecimalMixin:
        _types = {NoneClass, frozendict.frozendict, tuple, decimal.Decimal}
    class NoneFrozenDictTupleBoolMixin:
        _types = {NoneClass, frozendict.frozendict, tuple, BoolClass}
    class NoneFrozenDictStrDecimalMixin:
        _types = {NoneClass, frozendict.frozendict, str, decimal.Decimal}
    class NoneFrozenDictStrBoolMixin:
        _types = {NoneClass, frozendict.frozendict, str, BoolClass}
    class NoneFrozenDictDecimalBoolMixin:
        _types = {NoneClass, frozendict.frozendict, decimal.Decimal, BoolClass}
    class NoneTupleStrDecimalMixin:
        _types = {NoneClass, tuple, str, decimal.Decimal}
    class NoneTupleStrBoolMixin:
        _types = {NoneClass, tuple, str, BoolClass}
    class NoneTupleDecimalBoolMixin:
        _types = {NoneClass, tuple, decimal.Decimal, BoolClass}
    class NoneStrDecimalBoolMixin:
        _types = {NoneClass, str, decimal.Decimal, BoolClass}
    class FrozenDictTupleStrDecimalMixin:
        _types = {frozendict.frozendict, tuple, str, decimal.Decimal}
    class FrozenDictTupleStrBoolMixin:
        _types = {frozendict.frozendict, tuple, str, BoolClass}
    class FrozenDictTupleDecimalBoolMixin:
        _types = {frozendict.frozendict, tuple, decimal.Decimal, BoolClass}
    class FrozenDictStrDecimalBoolMixin:
        _types = {frozendict.frozendict, str, decimal.Decimal, BoolClass}
    class TupleStrDecimalBoolMixin:
        _types = {tuple, str, decimal.Decimal, BoolClass}
    # qty 5
    class NoneFrozenDictTupleStrDecimalMixin:
        _types = {NoneClass, frozendict.frozendict, tuple, str, decimal.Decimal}
    class NoneFrozenDictTupleStrBoolMixin:
        _types = {NoneClass, frozendict.frozendict, tuple, str, BoolClass}
    class NoneFrozenDictTupleDecimalBoolMixin:
        _types = {NoneClass, frozendict.frozendict, tuple, decimal.Decimal, BoolClass}
    class NoneFrozenDictStrDecimalBoolMixin:
        _types = {NoneClass, frozendict.frozendict, str, decimal.Decimal, BoolClass}
    class NoneTupleStrDecimalBoolMixin:
        _types = {NoneClass, tuple, str, decimal.Decimal, BoolClass}
    class FrozenDictTupleStrDecimalBoolMixin:
        _types = {frozendict.frozendict, tuple, str, decimal.Decimal, BoolClass}
    # qty 6
    class NoneFrozenDictTupleStrDecimalBoolMixin:
        _types = {NoneClass, frozendict.frozendict, tuple, str, decimal.Decimal, BoolClass}
    # qty 9
    class NoneFrozenDictTupleStrIntDecimalBoolFileBytesMixin:
        _types = {NoneClass, frozendict.frozendict, tuple, str, int, decimal.Decimal, BoolClass, FileIO, bytes}


class ValidatorBase:
    @staticmethod
    def _is_json_validation_enabled_oapg(schema_keyword, configuration=None):
        """Returns true if JSON schema validation is enabled for the specified
        validation keyword. This can be used to skip JSON schema structural validation
        as requested in the configuration.
        Note: the suffix _oapg stands for openapi python (experimental) generator and
        it has been added to prevent collisions with other methods and properties

        Args:
            schema_keyword (string): the name of a JSON schema validation keyword.
            configuration (Configuration): the configuration class.
        """

        return (configuration is None or
            not hasattr(configuration, '_disabled_client_side_validations') or
            schema_keyword not in configuration._disabled_client_side_validations)

    @staticmethod
    def _raise_validation_errror_message_oapg(value, constraint_msg, constraint_value, path_to_item, additional_txt=""):
        raise ApiValueError(
            "Invalid value `{value}`, {constraint_msg} `{constraint_value}`{additional_txt} at {path_to_item}".format(
                value=value,
                constraint_msg=constraint_msg,
                constraint_value=constraint_value,
                additional_txt=additional_txt,
                path_to_item=render_path(path_to_item),
            )
        )


class EnumBase:
    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ) -> typing.Dict[typing.Tuple[typing.Union[str, int], ...], typing.Set[typing.Union['Schema', str, decimal.Decimal, BoolClass, NoneClass, frozendict.frozendict, tuple]]]:
        """
        EnumBase _validate_oapg
        Validates that arg is in the enum's allowed values
        """
        try:
            cls.MetaOapg.enum_value_to_name[arg]
        except KeyError:
            raise ApiValueError("Invalid value {} passed in to {}, allowed_values={}".format(arg, cls, cls.MetaOapg.enum_value_to_name.keys()))
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)


class BoolBase:
    def is_true_oapg(self) -> bool:
        """
        A replacement for x is True
        True if the instance is a BoolClass True Singleton
        """
        if not issubclass(self.__class__, BoolClass):
            return False
        return bool(self)

    def is_false_oapg(self) -> bool:
        """
        A replacement for x is False
        True if the instance is a BoolClass False Singleton
        """
        if not issubclass(self.__class__, BoolClass):
            return False
        return bool(self) is False


class NoneBase:
    def is_none_oapg(self) -> bool:
        """
        A replacement for x is None
        True if the instance is a NoneClass None Singleton
        """
        if issubclass(self.__class__, NoneClass):
            return True
        return False


class StrBase(ValidatorBase):
    MetaOapg: MetaOapgTyped

    @property
    def as_str_oapg(self) -> str:
        return self

    @property
    def as_date_oapg(self) -> date:
        raise Exception('not implemented')

    @property
    def as_datetime_oapg(self) -> datetime:
        raise Exception('not implemented')

    @property
    def as_decimal_oapg(self) -> decimal.Decimal:
        raise Exception('not implemented')

    @property
    def as_uuid_oapg(self) -> uuid.UUID:
        raise Exception('not implemented')

    @classmethod
    def __check_str_validations(
        cls,
        arg: str,
        validation_metadata: ValidationMetadata
    ):
        if not hasattr(cls, 'MetaOapg'):
            return
        if (cls._is_json_validation_enabled_oapg('maxLength', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'max_length') and
                len(arg) > cls.MetaOapg.max_length):
            cls._raise_validation_errror_message_oapg(
                value=arg,
                constraint_msg="length must be less than or equal to",
                constraint_value=cls.MetaOapg.max_length,
                path_to_item=validation_metadata.path_to_item
            )

        if (cls._is_json_validation_enabled_oapg('minLength', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'min_length') and
                len(arg) < cls.MetaOapg.min_length):
            cls._raise_validation_errror_message_oapg(
                value=arg,
                constraint_msg="length must be greater than or equal to",
                constraint_value=cls.MetaOapg.min_length,
                path_to_item=validation_metadata.path_to_item
            )

        if (cls._is_json_validation_enabled_oapg('pattern', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'regex')):
            for regex_dict in cls.MetaOapg.regex:
                flags = regex_dict.get('flags', 0)
                if not re.search(regex_dict['pattern'], arg, flags=flags):
                    if flags != 0:
                        # Don't print the regex flags if the flags are not
                        # specified in the OAS document.
                        cls._raise_validation_errror_message_oapg(
                            value=arg,
                            constraint_msg="must match regular expression",
                            constraint_value=regex_dict['pattern'],
                            path_to_item=validation_metadata.path_to_item,
                            additional_txt=" with flags=`{}`".format(flags)
                        )
                    cls._raise_validation_errror_message_oapg(
                        value=arg,
                        constraint_msg="must match regular expression",
                        constraint_value=regex_dict['pattern'],
                        path_to_item=validation_metadata.path_to_item
                    )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ) -> typing.Dict[typing.Tuple[typing.Union[str, int], ...], typing.Set[typing.Union['Schema', str, decimal.Decimal, BoolClass, NoneClass, frozendict.frozendict, tuple]]]:
        """
        StrBase _validate_oapg
        Validates that validations pass
        """
        if isinstance(arg, str):
            if hasattr(cls.MetaOapg, 'x_konfig_strip') and cls.MetaOapg.x_konfig_strip:
                arg = arg.strip()
            cls.__check_str_validations(arg, validation_metadata)
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)


class UUIDBase:
    @property
    @functools.lru_cache()
    def as_uuid_oapg(self) -> uuid.UUID:
        return uuid.UUID(self)

    @classmethod
    def __validate_format(cls, arg: typing.Optional[str], validation_metadata: ValidationMetadata):
        if isinstance(arg, str):
            try:
                uuid.UUID(arg)
                return True
            except ValueError:
                raise ApiValueError(
                    "Invalid value '{}' for type UUID at {}".format(arg, validation_metadata.path_to_item)
                )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: typing.Optional[ValidationMetadata] = None,
    ):
        """
        UUIDBase _validate_oapg
        """
        cls.__validate_format(arg, validation_metadata=validation_metadata)
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)


class CustomIsoparser(isoparser):

    @_takes_ascii
    def parse_isodatetime(self, dt_str):
        components, pos = self._parse_isodate(dt_str)
        if len(dt_str) > pos:
            if self._sep is None or dt_str[pos:pos + 1] == self._sep:
                components += self._parse_isotime(dt_str[pos + 1:])
            else:
                raise ValueError('String contains unknown ISO components')

        if len(components) > 3 and components[3] == 24:
            components[3] = 0
            return datetime(*components) + timedelta(days=1)

        if len(components) <= 3:
            raise ValueError('Value is not a datetime')

        return datetime(*components)

    @_takes_ascii
    def parse_isodate(self, datestr):
        components, pos = self._parse_isodate(datestr)

        if len(datestr) > pos:
            raise ValueError('String contains invalid time components')

        if len(components) > 3:
            raise ValueError('String contains invalid time components')

        return date(*components)


DEFAULT_ISOPARSER = CustomIsoparser()


class DateBase:
    @property
    @functools.lru_cache()
    def as_date_oapg(self) -> date:
        return DEFAULT_ISOPARSER.parse_isodate(self)

    @classmethod
    def __validate_format(cls, arg: typing.Optional[str], validation_metadata: ValidationMetadata):
        if isinstance(arg, str):
            try:
                DEFAULT_ISOPARSER.parse_isodate(arg)
                return True
            except ValueError:
                raise ApiValueError(
                    "Value does not conform to the required ISO-8601 date format. "
                    "Invalid value '{}' for type date at {}".format(arg, validation_metadata.path_to_item)
                )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: typing.Optional[ValidationMetadata] = None,
    ):
        """
        DateBase _validate_oapg
        """
        cls.__validate_format(arg, validation_metadata=validation_metadata)
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)


class DateTimeBase:
    @property
    @functools.lru_cache()
    def as_datetime_oapg(self) -> datetime:
        return DEFAULT_ISOPARSER.parse_isodatetime(self)

    @classmethod
    def __validate_format(cls, arg: typing.Optional[str], validation_metadata: ValidationMetadata):
        if isinstance(arg, str):
            try:
                DEFAULT_ISOPARSER.parse_isodatetime(arg)
                return True
            except ValueError:
                raise ApiValueError(
                    "Value does not conform to the required ISO-8601 datetime format. "
                    "Invalid value '{}' for type datetime at {}".format(arg, validation_metadata.path_to_item)
                )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ):
        """
        DateTimeBase _validate_oapg
        """
        cls.__validate_format(arg, validation_metadata=validation_metadata)
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)


class DecimalBase:
    """
    A class for storing decimals that are sent over the wire as strings
    These schemas must remain based on StrBase rather than NumberBase
    because picking base classes must be deterministic
    """

    @property
    @functools.lru_cache()
    def as_decimal_oapg(self) -> decimal.Decimal:
        return decimal.Decimal(self)

    @classmethod
    def __validate_format(cls, arg: typing.Optional[str], validation_metadata: ValidationMetadata):
        if isinstance(arg, str):
            try:
                decimal.Decimal(arg)
                return True
            except decimal.InvalidOperation:
                raise ApiValueError(
                    "Value cannot be converted to a decimal. "
                    "Invalid value '{}' for type decimal at {}".format(arg, validation_metadata.path_to_item)
                )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ):
        """
        DecimalBase _validate_oapg
        """
        cls.__validate_format(arg, validation_metadata=validation_metadata)
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)


class NumberBase(ValidatorBase):
    MetaOapg: MetaOapgTyped

    @property
    def as_int_oapg(self) -> int:
        try:
            return self._as_int
        except AttributeError:
            """
            Note: for some numbers like 9.0 they could be represented as an
            integer but our code chooses to store them as
            >>> Decimal('9.0').as_tuple()
            DecimalTuple(sign=0, digits=(9, 0), exponent=-1)
            so we can tell that the value came from a float and convert it back to a float
            during later serialization
            """
            if self.as_tuple().exponent < 0:
                # this could be represented as an integer but should be represented as a float
                # because that's what it was serialized from
                raise ApiValueError(f'{self} is not an integer')
            self._as_int = int(self)
            return self._as_int

    @property
    def as_float_oapg(self) -> float:
        try:
            return self._as_float
        except AttributeError:
            if self.as_tuple().exponent >= 0:
                raise ApiValueError(f'{self} is not an float')
            self._as_float = float(self)
            return self._as_float

    @classmethod
    def __check_numeric_validations(
        cls,
        arg,
        validation_metadata: ValidationMetadata
    ):
        if not hasattr(cls, 'MetaOapg'):
            return
        if cls._is_json_validation_enabled_oapg('multipleOf',
                                      validation_metadata.configuration) and hasattr(cls.MetaOapg, 'multiple_of'):
            multiple_of_value = cls.MetaOapg.multiple_of
            if (not (float(arg) / multiple_of_value).is_integer()):
                # Note 'multipleOf' will be as good as the floating point arithmetic.
                cls._raise_validation_errror_message_oapg(
                    value=arg,
                    constraint_msg="value must be a multiple of",
                    constraint_value=multiple_of_value,
                    path_to_item=validation_metadata.path_to_item
                )

        checking_max_or_min_values = any(
            hasattr(cls.MetaOapg, validation_key) for validation_key in {
                'exclusive_maximum',
                'inclusive_maximum',
                'exclusive_minimum',
                'inclusive_minimum',
            }
        )
        if not checking_max_or_min_values:
            return

        if (cls._is_json_validation_enabled_oapg('exclusiveMaximum', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'exclusive_maximum') and
                arg >= cls.MetaOapg.exclusive_maximum):
            cls._raise_validation_errror_message_oapg(
                value=arg,
                constraint_msg="must be a value less than",
                constraint_value=cls.MetaOapg.exclusive_maximum,
                path_to_item=validation_metadata.path_to_item
            )

        if (cls._is_json_validation_enabled_oapg('maximum', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'inclusive_maximum') and
                arg > cls.MetaOapg.inclusive_maximum):
            cls._raise_validation_errror_message_oapg(
                value=arg,
                constraint_msg="must be a value less than or equal to",
                constraint_value=cls.MetaOapg.inclusive_maximum,
                path_to_item=validation_metadata.path_to_item
            )

        if (cls._is_json_validation_enabled_oapg('exclusiveMinimum', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'exclusive_minimum') and
                arg <= cls.MetaOapg.exclusive_minimum):
            cls._raise_validation_errror_message_oapg(
                value=arg,
                constraint_msg="must be a value greater than",
                constraint_value=cls.MetaOapg.exclusive_maximum,
                path_to_item=validation_metadata.path_to_item
            )

        if (cls._is_json_validation_enabled_oapg('minimum', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'inclusive_minimum') and
                arg < cls.MetaOapg.inclusive_minimum):
            cls._raise_validation_errror_message_oapg(
                value=arg,
                constraint_msg="must be a value greater than or equal to",
                constraint_value=cls.MetaOapg.inclusive_minimum,
                path_to_item=validation_metadata.path_to_item
            )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ) -> typing.Dict[typing.Tuple[typing.Union[str, int], ...], typing.Set[typing.Union['Schema', str, decimal.Decimal, BoolClass, NoneClass, frozendict.frozendict, tuple]]]:
        """
        NumberBase _validate_oapg
        Validates that validations pass
        """
        if isinstance(arg, decimal.Decimal):
            cls.__check_numeric_validations(arg, validation_metadata)
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)


class ListBase(ValidatorBase):
    MetaOapg: MetaOapgTyped

    @classmethod
    def __validate_items(cls, list_items, validation_metadata: ValidationMetadata):
        """
        Ensures that:
        - values passed in for items are valid
        Exceptions will be raised if:
        - invalid arguments were passed in

        Args:
            list_items: the input list of items

        Raises:
            ApiTypeError - for missing required arguments, or for invalid properties
        """

        # if we have definitions for an items schema, use it
        # otherwise accept anything
        item_cls = getattr(cls.MetaOapg, 'items', UnsetAnyTypeSchema)
        item_cls = cls._get_class_oapg(item_cls)
        path_to_schemas = {}
        for i, value in enumerate(list_items):
            item_validation_metadata = ValidationMetadata(
                from_server=validation_metadata.from_server,
                configuration=validation_metadata.configuration,
                path_to_item=validation_metadata.path_to_item+(i,),
                validated_path_to_schemas=validation_metadata.validated_path_to_schemas
            )
            if item_validation_metadata.validation_ran_earlier(item_cls):
                continue
            other_path_to_schemas = item_cls._validate_oapg(
                value, validation_metadata=item_validation_metadata)
            update(path_to_schemas, other_path_to_schemas)
        return path_to_schemas

    @classmethod
    def __check_tuple_validations(
            cls, arg,
            validation_metadata: ValidationMetadata):
        if not hasattr(cls, 'MetaOapg'):
            return
        if (cls._is_json_validation_enabled_oapg('maxItems', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'max_items') and
                len(arg) > cls.MetaOapg.max_items):
            cls._raise_validation_errror_message_oapg(
                value=arg,
                constraint_msg="number of items must be less than or equal to",
                constraint_value=cls.MetaOapg.max_items,
                path_to_item=validation_metadata.path_to_item
            )

        if (cls._is_json_validation_enabled_oapg('minItems', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'min_items') and
                len(arg) < cls.MetaOapg.min_items):
            cls._raise_validation_errror_message_oapg(
                value=arg,
                constraint_msg="number of items must be greater than or equal to",
                constraint_value=cls.MetaOapg.min_items,
                path_to_item=validation_metadata.path_to_item
            )

        if (cls._is_json_validation_enabled_oapg('uniqueItems', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'unique_items') and cls.MetaOapg.unique_items and arg):
            unique_items = set(arg)
            if len(arg) > len(unique_items):
                cls._raise_validation_errror_message_oapg(
                    value=arg,
                    constraint_msg="duplicate items were found, and the tuple must not contain duplicates because",
                    constraint_value='unique_items==True',
                    path_to_item=validation_metadata.path_to_item
                )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ):
        """
        ListBase _validate_oapg
        We return dynamic classes of different bases depending upon the inputs
        This makes it so:
        - the returned instance is always a subclass of our defining schema
            - this allows us to check type based on whether an instance is a subclass of a schema
        - the returned instance is a serializable type (except for None, True, and False) which are enums

        Returns:
            new_cls (type): the new class

        Raises:
            ApiValueError: when a string can't be converted into a date or datetime and it must be one of those classes
            ApiTypeError: when the input type is not in the list of allowed spec types
        """
        if isinstance(arg, tuple):
            cls.__check_tuple_validations(arg, validation_metadata)
        _path_to_schemas = super()._validate_oapg(arg, validation_metadata=validation_metadata)
        if not isinstance(arg, tuple):
            return _path_to_schemas
        updated_vm = ValidationMetadata(
            configuration=validation_metadata.configuration,
            from_server=validation_metadata.from_server,
            path_to_item=validation_metadata.path_to_item,
            seen_classes=validation_metadata.seen_classes | frozenset({cls}),
            validated_path_to_schemas=validation_metadata.validated_path_to_schemas
        )
        other_path_to_schemas = cls.__validate_items(arg, validation_metadata=updated_vm)
        update(_path_to_schemas, other_path_to_schemas)
        return _path_to_schemas

    @classmethod
    def _get_items_oapg(
        cls: 'Schema',
        arg: typing.List[typing.Any],
        path_to_item: typing.Tuple[typing.Union[str, int], ...],
        path_to_schemas: typing.Dict[typing.Tuple[typing.Union[str, int], ...], typing.Type['Schema']]
    ):
        '''
        ListBase _get_items_oapg
        '''
        cast_items = []

        for i, value in enumerate(arg):
            item_path_to_item = path_to_item + (i,)
            item_cls = path_to_schemas[item_path_to_item]
            new_value = item_cls._get_new_instance_without_conversion_oapg(
                value,
                item_path_to_item,
                path_to_schemas
            )
            cast_items.append(new_value)

        return cast_items


class Discriminable:
    MetaOapg: MetaOapgTyped

    @classmethod
    def _ensure_discriminator_value_present_oapg(cls, disc_property_name: str, validation_metadata: ValidationMetadata, *args):
        if not args or args and disc_property_name not in args[0]:
            # The input data does not contain the discriminator property
            raise ApiValueError(
                "Cannot deserialize input data due to missing discriminator. "
                "The discriminator property '{}' is missing at path: {}".format(disc_property_name, validation_metadata.path_to_item)
            )

    @classmethod
    def get_discriminated_class_oapg(cls, disc_property_name: str, disc_payload_value: str):
        """
        Used in schemas with discriminators
        """
        if not hasattr(cls.MetaOapg, 'discriminator'):
            return None
        disc = cls.MetaOapg.discriminator()
        if disc_property_name not in disc:
            return None
        discriminated_cls = disc[disc_property_name].get(disc_payload_value)
        if discriminated_cls is not None:
            return discriminated_cls
        if not hasattr(cls, 'MetaOapg'):
            return None
        elif not (
            hasattr(cls.MetaOapg, 'all_of') or
            hasattr(cls.MetaOapg, 'one_of') or
            hasattr(cls.MetaOapg, 'any_of')
        ):
            return None
        # TODO stop traveling if a cycle is hit
        if hasattr(cls.MetaOapg, 'all_of'):
            for allof_cls in cls.MetaOapg.all_of():
                discriminated_cls = allof_cls.get_discriminated_class_oapg(
                    disc_property_name=disc_property_name, disc_payload_value=disc_payload_value)
                if discriminated_cls is not None:
                    return discriminated_cls
        if hasattr(cls.MetaOapg, 'one_of'):
            for oneof_cls in cls.MetaOapg.one_of():
                discriminated_cls = oneof_cls.get_discriminated_class_oapg(
                    disc_property_name=disc_property_name, disc_payload_value=disc_payload_value)
                if discriminated_cls is not None:
                    return discriminated_cls
        if hasattr(cls.MetaOapg, 'any_of'):
            for anyof_cls in cls.MetaOapg.any_of():
                discriminated_cls = anyof_cls.get_discriminated_class_oapg(
                    disc_property_name=disc_property_name, disc_payload_value=disc_payload_value)
                if discriminated_cls is not None:
                    return discriminated_cls
        return None


class DictBase(Discriminable, ValidatorBase):

    @classmethod
    def __validate_arg_presence(cls, arg, validation_metadata: ValidationMetadata):
        """
        Ensures that:
        - all required arguments are passed in
        - the input variable names are valid
            - present in properties or
            - accepted because additionalProperties exists
        Exceptions will be raised if:
        - invalid arguments were passed in
            - a var_name is invalid if additional_properties == NotAnyTypeSchema
            and var_name not in properties.__annotations__
        - required properties were not passed in

        Args:
            arg: the input dict

        Raises:
            ApiTypeError - for missing required arguments, or for invalid properties
        """
        seen_required_properties = set()
        invalid_arguments = []
        required_property_names = getattr(cls.MetaOapg, 'required', set())
        additional_properties = getattr(cls.MetaOapg, 'additional_properties', UnsetAnyTypeSchema)
        properties = getattr(cls.MetaOapg, 'properties', {})
        property_annotations = getattr(properties, '__annotations__', {})
        for property_name in arg:
            if property_name in required_property_names:
                seen_required_properties.add(property_name)
            elif property_name in property_annotations:
                continue
            elif additional_properties is not NotAnyTypeSchema:
                continue
            else:
                invalid_arguments.append(property_name)
        missing_required_arguments = list(required_property_names - seen_required_properties)
        if missing_required_arguments:
            missing_required_arguments.sort()
            raise MissingRequiredPropertiesError(
                "{} is missing {} required propert{}{}: {}".format(
                    cls.__name__,
                    len(missing_required_arguments),
                    "ies" if len(missing_required_arguments) > 1 else "y",
                    " at '{}'".format('.'.join([str(i) for i in validation_metadata.path_to_item[1:]])) if len(validation_metadata.path_to_item) > 1 else "",
                    missing_required_arguments
                )
            )
        if invalid_arguments:
            invalid_arguments.sort()
            raise ApiTypeError(
                "{} was passed {} invalid argument{}: {}".format(
                    cls.__name__,
                    len(invalid_arguments),
                    "s" if len(invalid_arguments) > 1 else "",
                    invalid_arguments
                )
            )

    @classmethod
    def __validate_args(cls, arg, validation_metadata: ValidationMetadata):
        """
        Ensures that:
        - values passed in for properties are valid
        Exceptions will be raised if:
        - invalid arguments were passed in

        Args:
            arg: the input dict

        Raises:
            ApiTypeError - for missing required arguments, or for invalid properties
        """
        path_to_schemas = {}
        additional_properties = getattr(cls.MetaOapg, 'additional_properties', UnsetAnyTypeSchema)
        properties = getattr(cls.MetaOapg, 'properties', {})
        property_annotations = getattr(properties, '__annotations__', {})
        validation_errors = []
        for property_name, value in arg.items():
            path_to_item = validation_metadata.path_to_item+(property_name,)
            if property_name in property_annotations:
                schema = property_annotations[property_name]
            elif additional_properties is not NotAnyTypeSchema:
                if additional_properties is UnsetAnyTypeSchema:
                    """
                    If additionalProperties is unset and this path_to_item does not yet have
                    any validations on it, validate it.
                    If it already has validations on it, skip this validation.
                    """
                    if path_to_item in path_to_schemas:
                        continue
                schema = additional_properties
            else:
                raise ApiTypeError('Unable to find schema for value={} in class={} at path_to_item={}'.format(
                    value, cls, validation_metadata.path_to_item+(property_name,)
                ))
            schema = cls._get_class_oapg(schema)
            arg_validation_metadata = ValidationMetadata(
                from_server=validation_metadata.from_server,
                configuration=validation_metadata.configuration,
                path_to_item=path_to_item,
                validated_path_to_schemas=validation_metadata.validated_path_to_schemas
            )
            if arg_validation_metadata.validation_ran_earlier(schema):
                continue
            try:
                other_path_to_schemas = schema._validate_oapg(value, validation_metadata=arg_validation_metadata)
                update(path_to_schemas, other_path_to_schemas)
            except (ApiTypeError, ApiValueError, MissingRequiredPropertiesError) as e:
                validation_errors.append(e)
        if len(validation_errors) > 0:
            raise SchemaValidationError(validation_errors)
        return path_to_schemas

    @classmethod
    def __check_dict_validations(
        cls,
        arg,
        validation_metadata: ValidationMetadata
    ):
        if not hasattr(cls, 'MetaOapg'):
            return
        if (cls._is_json_validation_enabled_oapg('maxProperties', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'max_properties') and
                len(arg) > cls.MetaOapg.max_properties):
            cls._raise_validation_errror_message_oapg(
                value=arg,
                constraint_msg="number of properties must be less than or equal to",
                constraint_value=cls.MetaOapg.max_properties,
                path_to_item=validation_metadata.path_to_item
            )

        if (cls._is_json_validation_enabled_oapg('minProperties', validation_metadata.configuration) and
                hasattr(cls.MetaOapg, 'min_properties') and
                len(arg) < cls.MetaOapg.min_properties):
            cls._raise_validation_errror_message_oapg(
                value=arg,
                constraint_msg="number of properties must be greater than or equal to",
                constraint_value=cls.MetaOapg.min_properties,
                path_to_item=validation_metadata.path_to_item
            )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ):
        """
        DictBase _validate_oapg
        We return dynamic classes of different bases depending upon the inputs
        This makes it so:
        - the returned instance is always a subclass of our defining schema
            - this allows us to check type based on whether an instance is a subclass of a schema
        - the returned instance is a serializable type (except for None, True, and False) which are enums

        Returns:
            new_cls (type): the new class

        Raises:
            ApiValueError: when a string can't be converted into a date or datetime and it must be one of those classes
            ApiTypeError: when the input type is not in the list of allowed spec types
        """
        if isinstance(arg, frozendict.frozendict):
            cls.__check_dict_validations(arg, validation_metadata)
        _path_to_schemas = super()._validate_oapg(arg, validation_metadata=validation_metadata)
        if not isinstance(arg, frozendict.frozendict):
            return _path_to_schemas
        cls.__validate_arg_presence(arg, validation_metadata)
        other_path_to_schemas = cls.__validate_args(arg, validation_metadata=validation_metadata)
        update(_path_to_schemas, other_path_to_schemas)
        try:
            discriminator = cls.MetaOapg.discriminator()
        except AttributeError:
            return _path_to_schemas
        # discriminator exists
        disc_prop_name = list(discriminator.keys())[0]
        cls._ensure_discriminator_value_present_oapg(disc_prop_name, validation_metadata, arg)
        discriminated_cls = cls.get_discriminated_class_oapg(
            disc_property_name=disc_prop_name, disc_payload_value=arg[disc_prop_name])
        if discriminated_cls is None:
            raise ApiValueError(
                "Invalid discriminator value was passed in to {}.{} Only the values {} are allowed at {}".format(
                    cls.__name__,
                    disc_prop_name,
                    list(discriminator[disc_prop_name].keys()),
                    validation_metadata.path_to_item + (disc_prop_name,)
                )
            )
        updated_vm = ValidationMetadata(
            configuration=validation_metadata.configuration,
            from_server=validation_metadata.from_server,
            path_to_item=validation_metadata.path_to_item,
            seen_classes=validation_metadata.seen_classes | frozenset({cls}),
            validated_path_to_schemas=validation_metadata.validated_path_to_schemas
        )
        if updated_vm.validation_ran_earlier(discriminated_cls):
            return _path_to_schemas
        other_path_to_schemas = discriminated_cls._validate_oapg(arg, validation_metadata=updated_vm)
        update(_path_to_schemas, other_path_to_schemas)
        return _path_to_schemas

    @classmethod
    def _get_properties_oapg(
        cls,
        arg: typing.Dict[str, typing.Any],
        path_to_item: typing.Tuple[typing.Union[str, int], ...],
        path_to_schemas: typing.Dict[typing.Tuple[typing.Union[str, int], ...], typing.Type['Schema']]
    ):
        """
        DictBase _get_properties_oapg, this is how properties are set
        These values already passed validation
        """
        dict_items = {}

        for property_name_js, value in arg.items():
            property_path_to_item = path_to_item + (property_name_js,)
            property_cls = path_to_schemas[property_path_to_item]
            new_value = property_cls._get_new_instance_without_conversion_oapg(
                value,
                property_path_to_item,
                path_to_schemas
            )
            dict_items[property_name_js] = new_value

        return dict_items

    def __setattr__(self, name: str, value: typing.Any):
        if not isinstance(self, FileIO):
            raise AttributeError('property setting not supported on immutable instances')

    def __getattr__(self, name: str):
        """
        for instance.name access
        Properties are only type hinted for required properties
        so that hasattr(instance, 'optionalProp') is False when that key is not present
        """
        if not isinstance(self, frozendict.frozendict):
            return super().__getattr__(name)
        if name not in self.__class__.__annotations__:
            raise AttributeError(f"{self} has no attribute '{name}'")
        try:
            value = self[name]
            return value
        except KeyError as ex:
            raise AttributeError(str(ex))

    def __getitem__(self, name: str):
        """
        dict_instance[name] accessor
        key errors thrown
        """
        if not isinstance(self, frozendict.frozendict):
            return super().__getattr__(name)
        return super().__getitem__(name)

    def get_item_oapg(self, name: str) -> typing.Union['AnyTypeSchema', Unset]:
        # dict_instance[name] accessor
        if not isinstance(self, frozendict.frozendict):
            raise NotImplementedError()
        try:
            return super().__getitem__(name)
        except KeyError:
            return unset


def cast_to_allowed_types(
    arg: typing.Union[str, date, datetime, uuid.UUID, decimal.Decimal, int, float, None, dict, frozendict.frozendict, list, tuple, bytes, Schema, io.FileIO, io.BufferedReader],
    from_server: bool,
    validated_path_to_schemas: typing.Dict[typing.Tuple[typing.Union[str, int], ...], typing.Set[typing.Union['Schema', str, decimal.Decimal, BoolClass, NoneClass, frozendict.frozendict, tuple]]],
    path_to_item: typing.Tuple[typing.Union[str, int], ...] = tuple(['args[0]']),
    schema: Schema = None,
) -> typing.Union[frozendict.frozendict, tuple, decimal.Decimal, str, bytes, BoolClass, NoneClass, FileIO]:
    """
    Casts the input payload arg into the allowed types
    The input validated_path_to_schemas is mutated by running this function

    When from_server is False then
    - date/datetime is cast to str
    - int/float is cast to Decimal

    If a Schema instance is passed in it is converted back to a primitive instance because
    One may need to validate that data to the original Schema class AND additional different classes
    those additional classes will need to be added to the new manufactured class for that payload
    If the code didn't do this and kept the payload as a Schema instance it would fail to validate to other
    Schema classes and the code wouldn't be able to mfg a new class that includes all valid schemas
    TODO: store the validated schema classes in validation_metadata

    Args:
        arg: the payload
        from_server: whether this payload came from the server or not
        validated_path_to_schemas: a dict that stores the validated classes at any path location in the payload
    """
    if isinstance(arg, Schema):
        # store the already run validations
        schema_classes = set()
        source_schema_was_unset = len(arg.__class__.__bases__) == 2 and UnsetAnyTypeSchema in arg.__class__.__bases__
        if not source_schema_was_unset:
            """
            Do not include UnsetAnyTypeSchema and its base class because
            it did not exist in the original spec schema definition
            It was added to ensure that all instances are of type Schema and the allowed base types
            """
            for cls in arg.__class__.__bases__:
                if cls is Singleton:
                    # Skip Singleton
                    continue
                schema_classes.add(cls)
        validated_path_to_schemas[path_to_item] = schema_classes

    type_error = ApiTypeError(f"Invalid type. Required value type is str and passed type was {type(arg)} at {path_to_item}")
    if isinstance(arg, str):
        return str(arg)
    elif isinstance(arg, (dict, frozendict.frozendict)):
        return frozendict.frozendict({key: cast_to_allowed_types(val, from_server, validated_path_to_schemas, path_to_item + (key,)) for key, val in arg.items()})
    elif isinstance(arg, (bool, BoolClass)):
        """
        this check must come before isinstance(arg, (int, float))
        because isinstance(True, int) is True
        """
        if arg:
            return BoolClass.TRUE
        return BoolClass.FALSE
    elif isinstance(arg, int):
        return arg
    elif isinstance(arg, float):
        decimal_from_float = decimal.Decimal(arg)
        if decimal_from_float.as_integer_ratio()[1] == 1:
            # 9.0 -> Decimal('9.0')
            # 3.4028234663852886e+38 -> Decimal('340282346638528859811704183484516925440.0')
            return decimal.Decimal(str(decimal_from_float)+'.0')
        return decimal_from_float
    elif isinstance(arg, (tuple, list)):
        return tuple([cast_to_allowed_types(item, from_server, validated_path_to_schemas, path_to_item + (i,)) for i, item in enumerate(arg)])
    elif isinstance(arg, (none_type, NoneClass)):
        return NoneClass.NONE
    elif isinstance(arg, (date, datetime)):
        if not from_server:
            # if schema itself is the DateTimeSchema class then convert to isoformat
            # if schema itself is the DateSchema class then convert to yyyy-mm-dd using strftime
            if schema is None:
                return arg.isoformat()
            if schema is DateTimeSchema:
                return arg.isoformat()
            if schema is DateSchema:
                return arg.strftime('%Y-%m-%d')
        raise type_error
    elif isinstance(arg, uuid.UUID):
        if not from_server:
            return str(arg)
        raise type_error
    elif isinstance(arg, decimal.Decimal):
        return decimal.Decimal(arg)
    elif isinstance(arg, bytes):
        return bytes(arg)
    elif isinstance(arg, (io.FileIO, io.BufferedReader)):
        return FileIO(arg)
    elif isinstance(arg, pydantic.BaseModel):
        return cast_to_allowed_types({ k:v for k, v in dict(arg).items() if v is not None }, from_server, validated_path_to_schemas, path_to_item)
    raise ValueError('Invalid type passed in got input={} type={}'.format(arg, type(arg)))


class ComposedBase(Discriminable):

    @classmethod
    def __get_allof_classes(cls, arg, validation_metadata: ValidationMetadata):
        path_to_schemas = defaultdict(set)
        for allof_cls in cls.MetaOapg.all_of():
            if validation_metadata.validation_ran_earlier(allof_cls):
                continue
            other_path_to_schemas = allof_cls._validate_oapg(arg, validation_metadata=validation_metadata)
            update(path_to_schemas, other_path_to_schemas)
        return path_to_schemas

    @classmethod
    def __get_oneof_class(
        cls,
        arg,
        discriminated_cls,
        validation_metadata: ValidationMetadata,
    ):
        oneof_classes = []
        path_to_schemas = defaultdict(set)
        for oneof_cls in cls.MetaOapg.one_of():
            if oneof_cls in path_to_schemas[validation_metadata.path_to_item]:
                oneof_classes.append(oneof_cls)
                continue
            if validation_metadata.validation_ran_earlier(oneof_cls):
                oneof_classes.append(oneof_cls)
                continue
            try:
                path_to_schemas = oneof_cls._validate_oapg(arg, validation_metadata=validation_metadata)
            except (ApiValueError, ApiTypeError) as ex:
                if discriminated_cls is not None and oneof_cls is discriminated_cls:
                    raise ex
                continue
            oneof_classes.append(oneof_cls)
        if not oneof_classes:
            raise ApiValueError(
                "Invalid inputs given to generate an instance of {}. None "
                "of the oneOf schemas matched the input data.".format(cls)
            )
        elif len(oneof_classes) > 1:
            raise ApiValueError(
                "Invalid inputs given to generate an instance of {}. Multiple "
                "oneOf schemas {} matched the inputs, but a max of one is allowed.".format(cls, oneof_classes)
            )
        # exactly one class matches
        return path_to_schemas

    @classmethod
    def __get_anyof_classes(
        cls,
        arg,
        discriminated_cls,
        validation_metadata: ValidationMetadata
    ):
        anyof_classes = []
        exceptions: typing.List[typing.Union[ApiTypeError, ApiValueError]] = []
        path_to_schemas = defaultdict(set)
        for anyof_cls in cls.MetaOapg.any_of():
            if validation_metadata.validation_ran_earlier(anyof_cls):
                anyof_classes.append(anyof_cls)
                continue

            try:
                other_path_to_schemas = anyof_cls._validate_oapg(arg, validation_metadata=validation_metadata)
            except (ApiValueError, ApiTypeError) as ex:
                if discriminated_cls is not None and anyof_cls is discriminated_cls:
                    raise ex
                exceptions.append(ex)
                continue
            anyof_classes.append(anyof_cls)
            update(path_to_schemas, other_path_to_schemas)
        if not anyof_classes:
            raise AnyOfValidationError(error_list=exceptions)
        return path_to_schemas

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ) -> typing.Dict[typing.Tuple[typing.Union[str, int], ...], typing.Set[typing.Union['Schema', str, decimal.Decimal, BoolClass, NoneClass, frozendict.frozendict, tuple]]]:
        """
        ComposedBase _validate_oapg
        We return dynamic classes of different bases depending upon the inputs
        This makes it so:
        - the returned instance is always a subclass of our defining schema
            - this allows us to check type based on whether an instance is a subclass of a schema
        - the returned instance is a serializable type (except for None, True, and False) which are enums

        Returns:
            new_cls (type): the new class

        Raises:
            ApiValueError: when a string can't be converted into a date or datetime and it must be one of those classes
            ApiTypeError: when the input type is not in the list of allowed spec types
        """
        # validation checking on types, validations, and enums
        path_to_schemas = super()._validate_oapg(arg, validation_metadata=validation_metadata)

        updated_vm = ValidationMetadata(
            configuration=validation_metadata.configuration,
            from_server=validation_metadata.from_server,
            path_to_item=validation_metadata.path_to_item,
            seen_classes=validation_metadata.seen_classes | frozenset({cls}),
            validated_path_to_schemas=validation_metadata.validated_path_to_schemas
        )

        # process composed schema
        discriminator = None
        if hasattr(cls, 'MetaOapg') and hasattr(cls.MetaOapg, 'discriminator'):
            discriminator = cls.MetaOapg.discriminator()
        discriminated_cls = None
        if discriminator and arg and isinstance(arg, frozendict.frozendict):
            disc_property_name = list(discriminator.keys())[0]
            cls._ensure_discriminator_value_present_oapg(disc_property_name, updated_vm, arg)
            # get discriminated_cls by looking at the dict in the current class
            discriminated_cls = cls.get_discriminated_class_oapg(
                disc_property_name=disc_property_name, disc_payload_value=arg[disc_property_name])
            if discriminated_cls is None:
                raise ApiValueError(
                    "Invalid discriminator value '{}' was passed in to {}.{} Only the values {} are allowed at {}".format(
                        arg[disc_property_name],
                        cls.__name__,
                        disc_property_name,
                        list(discriminator[disc_property_name].keys()),
                        updated_vm.path_to_item + (disc_property_name,)
                    )
                )

        if hasattr(cls, 'MetaOapg') and hasattr(cls.MetaOapg, 'all_of'):
            other_path_to_schemas = cls.__get_allof_classes(arg, validation_metadata=updated_vm)
            update(path_to_schemas, other_path_to_schemas)
        if hasattr(cls, 'MetaOapg') and hasattr(cls.MetaOapg, 'one_of'):
            other_path_to_schemas = cls.__get_oneof_class(
                arg,
                discriminated_cls=discriminated_cls,
                validation_metadata=updated_vm
            )
            update(path_to_schemas, other_path_to_schemas)
        if hasattr(cls, 'MetaOapg') and hasattr(cls.MetaOapg, 'any_of'):
            other_path_to_schemas = cls.__get_anyof_classes(
                arg,
                discriminated_cls=discriminated_cls,
                validation_metadata=updated_vm
            )
            update(path_to_schemas, other_path_to_schemas)
        not_cls = None
        if hasattr(cls, 'MetaOapg') and hasattr(cls.MetaOapg, 'not_schema'):
            not_cls = cls.MetaOapg.not_schema
            not_cls = cls._get_class_oapg(not_cls)
        if not_cls:
            other_path_to_schemas = None
            not_exception = ApiValueError(
                "Invalid value '{}' was passed in to {}. Value is invalid because it is disallowed by {}".format(
                    arg,
                    cls.__name__,
                    not_cls.__name__,
                )
            )
            if updated_vm.validation_ran_earlier(not_cls):
                raise not_exception

            try:
                other_path_to_schemas = not_cls._validate_oapg(arg, validation_metadata=updated_vm)
            except (ApiValueError, ApiTypeError):
                pass
            if other_path_to_schemas:
                raise not_exception

        if discriminated_cls is not None and not updated_vm.validation_ran_earlier(discriminated_cls):
            if discriminated_cls not in path_to_schemas[updated_vm.path_to_item]:
                raise ApiValueError("Could not find discriminator in value")
        return path_to_schemas


# DictBase, ListBase, NumberBase, StrBase, BoolBase, NoneBase
class ComposedSchema(
    ComposedBase,
    DictBase,
    ListBase,
    NumberBase,
    StrBase,
    BoolBase,
    NoneBase,
    Schema,
    NoneFrozenDictTupleStrDecimalBoolMixin
):
    @classmethod
    def from_openapi_data_oapg(cls, *args: typing.Any, _configuration: typing.Optional[Configuration] = None, **kwargs):
        if not args:
            if not kwargs:
                raise ApiTypeError('{} is missing required input data in args or kwargs'.format(cls.__name__))
            args = (kwargs, )
        return super().from_openapi_data_oapg(args[0], _configuration=_configuration)


class ListSchema(
    ListBase,
    Schema,
    TupleMixin
):

    @classmethod
    def from_openapi_data_oapg(cls, arg: typing.List[typing.Any], _configuration: typing.Optional[Configuration] = None):
        return super().from_openapi_data_oapg(arg, _configuration=_configuration)

    def __new__(cls, arg: typing.Union[typing.List[typing.Any], typing.Tuple[typing.Any]], **kwargs: Configuration):
        return super().__new__(cls, arg, **kwargs)


class NoneSchema(
    NoneBase,
    Schema,
    NoneMixin
):

    @classmethod
    def from_openapi_data_oapg(cls, arg: None, _configuration: typing.Optional[Configuration] = None):
        return super().from_openapi_data_oapg(arg, _configuration=_configuration)

    def __new__(cls, arg: None, **kwargs: Configuration):
        return super().__new__(cls, arg, **kwargs)


class NumberSchema(
    NumberBase,
    Schema,
    NumberMixin
):
    """
    This is used for type: number with no format
    Both integers AND floats are accepted
    """

    @classmethod
    def from_openapi_data_oapg(cls, arg: typing.Union[int, float], _configuration: typing.Optional[Configuration] = None):
        return super().from_openapi_data_oapg(arg, _configuration=_configuration)

    def __new__(cls, arg: typing.Union[decimal.Decimal, int, float], **kwargs: Configuration):
        return super().__new__(cls, arg, **kwargs)


class IntBase:
    @property
    def as_int_oapg(self) -> int:
        try:
            return self._as_int
        except AttributeError:
            self._as_int = int(self)
            return self._as_int

    @classmethod
    def __validate_format(cls, arg: typing.Optional[decimal.Decimal], validation_metadata: ValidationMetadata):
        if isinstance(arg, decimal.Decimal):

            denominator = arg.as_integer_ratio()[-1]
            if denominator != 1:
                raise ApiValueError(
                    "Invalid value '{}' for type integer at {}".format(arg, validation_metadata.path_to_item)
                )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ):
        """
        IntBase _validate_oapg
        TODO what about types = (int, number) -> IntBase, NumberBase? We could drop int and keep number only
        """
        cls.__validate_format(arg, validation_metadata=validation_metadata)
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)


class IntSchema(IntBase, NumberBase, Schema, IntMixin):

    @classmethod
    def from_openapi_data_oapg(cls, arg: int, _configuration: typing.Optional[Configuration] = None):
        return super().from_openapi_data_oapg(arg, _configuration=_configuration)

    def __new__(cls, arg: typing.Union[decimal.Decimal, int], **kwargs: Configuration):
        return super().__new__(cls, arg, **kwargs)


class Int32Base:
    __inclusive_minimum = decimal.Decimal(-2147483648)
    __inclusive_maximum = decimal.Decimal(2147483647)

    @classmethod
    def __validate_format(cls, arg: typing.Optional[decimal.Decimal], validation_metadata: ValidationMetadata):
        if isinstance(arg, decimal.Decimal) and arg.as_tuple().exponent == 0:
            if not cls.__inclusive_minimum <= arg <= cls.__inclusive_maximum:
                raise ApiValueError(
                    "Invalid value '{}' for type int32 at {}".format(arg, validation_metadata.path_to_item)
                )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ):
        """
        Int32Base _validate_oapg
        """
        cls.__validate_format(arg, validation_metadata=validation_metadata)
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)


class Int32Schema(
    Int32Base,
    IntSchema
):
    pass


class Int64Base:
    __inclusive_minimum = decimal.Decimal(-9223372036854775808)
    __inclusive_maximum = decimal.Decimal(9223372036854775807)

    @classmethod
    def __validate_format(cls, arg: typing.Optional[decimal.Decimal], validation_metadata: ValidationMetadata):
        if isinstance(arg, decimal.Decimal) and arg.as_tuple().exponent == 0:
            if not cls.__inclusive_minimum <= arg <= cls.__inclusive_maximum:
                raise ApiValueError(
                    "Invalid value '{}' for type int64 at {}".format(arg, validation_metadata.path_to_item)
                )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ):
        """
        Int64Base _validate_oapg
        """
        cls.__validate_format(arg, validation_metadata=validation_metadata)
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)


class Int64Schema(
    Int64Base,
    IntSchema
):
    pass


class Float32Base:
    __inclusive_minimum = decimal.Decimal(-3.4028234663852886e+38)
    __inclusive_maximum = decimal.Decimal(3.4028234663852886e+38)

    @classmethod
    def __validate_format(cls, arg: typing.Optional[decimal.Decimal], validation_metadata: ValidationMetadata):
        if isinstance(arg, decimal.Decimal):
            if not cls.__inclusive_minimum <= arg <= cls.__inclusive_maximum:
                raise ApiValueError(
                    "Invalid value '{}' for type float at {}".format(arg, validation_metadata.path_to_item)
                )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ):
        """
        Float32Base _validate_oapg
        """
        cls.__validate_format(arg, validation_metadata=validation_metadata)
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)


class Float32Schema(
    Float32Base,
    NumberSchema
):

    @classmethod
    def from_openapi_data_oapg(cls, arg: float, _configuration: typing.Optional[Configuration] = None):
        return super().from_openapi_data_oapg(arg, _configuration=_configuration)


class Float64Base:
    __inclusive_minimum = decimal.Decimal(-1.7976931348623157E+308)
    __inclusive_maximum = decimal.Decimal(1.7976931348623157E+308)

    @classmethod
    def __validate_format(cls, arg: typing.Optional[decimal.Decimal], validation_metadata: ValidationMetadata):
        if isinstance(arg, decimal.Decimal):
            if not cls.__inclusive_minimum <= arg <= cls.__inclusive_maximum:
                raise ApiValueError(
                    "Invalid value '{}' for type double at {}".format(arg, validation_metadata.path_to_item)
                )

    @classmethod
    def _validate_oapg(
        cls,
        arg,
        validation_metadata: ValidationMetadata,
    ):
        """
        Float64Base _validate_oapg
        """
        cls.__validate_format(arg, validation_metadata=validation_metadata)
        return super()._validate_oapg(arg, validation_metadata=validation_metadata)

class Float64Schema(
    Float64Base,
    NumberSchema
):

    @classmethod
    def from_openapi_data_oapg(cls, arg: float, _configuration: typing.Optional[Configuration] = None):
        # todo check format
        return super().from_openapi_data_oapg(arg, _configuration=_configuration)


class StrSchema(
    StrBase,
    Schema,
    StrMixin
):
    """
    date + datetime string types must inherit from this class
    That is because one can validate a str payload as both:
    - type: string (format unset)
    - type: string, format: date
    """

    @classmethod
    def from_openapi_data_oapg(cls, arg: str, _configuration: typing.Optional[Configuration] = None) -> 'StrSchema':
        return super().from_openapi_data_oapg(arg, _configuration=_configuration)

    def __new__(cls, arg: typing.Union[str, date, datetime, uuid.UUID], **kwargs: Configuration):
        return super().__new__(cls, arg, **kwargs)


class UUIDSchema(UUIDBase, StrSchema):

    def __new__(cls, arg: typing.Union[str, uuid.UUID], **kwargs: Configuration):
        return super().__new__(cls, arg, **kwargs)


class DateSchema(DateBase, StrSchema):

    def __new__(cls, arg: typing.Union[str, date], **kwargs: Configuration):
        return super().__new__(cls, arg, **kwargs)


class DateTimeSchema(DateTimeBase, StrSchema):

    def __new__(cls, arg: typing.Union[str, datetime], **kwargs: Configuration):
        return super().__new__(cls, arg, **kwargs)


class DecimalSchema(DecimalBase, StrSchema):

    def __new__(cls, arg: str, **kwargs: Configuration):
        """
        Note: Decimals may not be passed in because cast_to_allowed_types is only invoked once for payloads
        which can be simple (str) or complex (dicts or lists with nested values)
        Because casting is only done once and recursively casts all values prior to validation then for a potential
        client side Decimal input if Decimal was accepted as an input in DecimalSchema then one would not know
        if one was using it for a StrSchema (where it should be cast to str) or one is using it for NumberSchema
        where it should stay as Decimal.
        """
        return super().__new__(cls, arg, **kwargs)


class BytesSchema(
    Schema,
    BytesMixin
):
    """
    this class will subclass bytes and is immutable
    """
    def __new__(cls, arg: bytes, **kwargs: Configuration):
        return super(Schema, cls).__new__(cls, arg)


class FileSchema(
    Schema,
    FileMixin
):
    """
    This class is NOT immutable
    Dynamic classes are built using it for example when AnyType allows in binary data
    Al other schema classes ARE immutable
    If one wanted to make this immutable one could make this a DictSchema with required properties:
    - data = BytesSchema (which would be an immutable bytes based schema)
    - file_name = StrSchema
    and cast_to_allowed_types would convert bytes and file instances into dicts containing data + file_name
    The downside would be that data would be stored in memory which one may not want to do for very large files

    The developer is responsible for closing this file and deleting it

    This class was kept as mutable:
    - to allow file reading and writing to disk
    - to be able to preserve file name info
    """

    def __new__(cls, arg: typing.Union[io.FileIO, io.BufferedReader], **kwargs: Configuration):
        return super(Schema, cls).__new__(cls, arg)


class BinaryBase:
    pass


class BinarySchema(
    ComposedBase,
    BinaryBase,
    Schema,
    BinaryMixin
):
    class MetaOapg:
        @staticmethod
        def one_of():
            return [
                BytesSchema,
                FileSchema,
            ]

    def __new__(cls, arg: typing.Union[io.FileIO, io.BufferedReader, bytes], **kwargs: Configuration):
        return super().__new__(cls, arg)


class BoolSchema(
    BoolBase,
    Schema,
    BoolMixin
):

    @classmethod
    def from_openapi_data_oapg(cls, arg: bool, _configuration: typing.Optional[Configuration] = None):
        return super().from_openapi_data_oapg(arg, _configuration=_configuration)

    def __new__(cls, arg: bool, **kwargs: ValidationMetadata):
        return super().__new__(cls, arg, **kwargs)


class AnyTypeSchema(
    DictBase,
    ListBase,
    NumberBase,
    StrBase,
    BoolBase,
    NoneBase,
    Schema,
    NoneFrozenDictTupleStrIntDecimalBoolFileBytesMixin
):
    # Python representation of a schema defined as true or {}
    pass


class UnsetAnyTypeSchema(AnyTypeSchema):
    # Used when additionalProperties/items was not explicitly defined and a defining schema is needed
    pass


class NotAnyTypeSchema(
    ComposedSchema,
):
    """
    Python representation of a schema defined as false or {'not': {}}
    Does not allow inputs in of AnyType
    Note: validations on this class are never run because the code knows that no inputs will ever validate
    """

    class MetaOapg:
        not_schema = AnyTypeSchema

    def __new__(
        cls,
        *args,
        _configuration: typing.Optional[Configuration] = None,
    ) -> 'NotAnyTypeSchema':
        return super().__new__(
            cls,
            *args,
            _configuration=_configuration,
        )


class DictSchema(
    DictBase,
    Schema,
    FrozenDictMixin
):
    @classmethod
    def from_openapi_data_oapg(cls, arg: typing.Dict[str, typing.Any], _configuration: typing.Optional[Configuration] = None):
        return super().from_openapi_data_oapg(arg, _configuration=_configuration)

    def __new__(cls, *args: typing.Union[dict, frozendict.frozendict], **kwargs: typing.Union[dict, frozendict.frozendict, list, tuple, decimal.Decimal, float, int, str, date, datetime, bool, None, bytes, Schema, Unset, ValidationMetadata]):
        return super().__new__(cls, *args, **kwargs)


schema_type_classes = {NoneSchema, DictSchema, ListSchema, NumberSchema, StrSchema, BoolSchema, AnyTypeSchema}


@functools.lru_cache()
def get_new_class(
    class_name: str,
    bases: typing.Tuple[typing.Type[typing.Union[Schema, typing.Any]], ...]
) -> typing.Type[Schema]:
    """
    Returns a new class that is made with the subclass bases
    """
    new_cls: typing.Type[Schema] = type(class_name, bases, {})
    return new_cls


LOG_CACHE_USAGE = False


def log_cache_usage(cache_fn):
    if LOG_CACHE_USAGE:
        print(cache_fn.__name__, cache_fn.cache_info())
