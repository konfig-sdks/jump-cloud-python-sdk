<div align="left">

[![Visit Jumpcloud](./header.png)](https://jumpcloud.com)

# Jumpcloud<a id="jumpcloud"></a>

# Overview<a id="overview"></a>

JumpCloud's V2 API. This set of endpoints allows JumpCloud customers to manage objects, groupings and mappings and interact with the JumpCloud Graph.

## API Best Practices<a id="api-best-practices"></a>

Read the linked Help Article below for guidance on retrying failed requests to JumpCloud's REST API, as well as best practices for structuring subsequent retry requests. Customizing retry mechanisms based on these recommendations will increase the reliability and dependability of your API calls.

Covered topics include:
1. Important Considerations
2. Supported HTTP Request Methods
3. Response codes
4. API Key rotation
5. Paginating
6. Error handling
7. Retry rates

[JumpCloud Help Center - API Best Practices](https://support.jumpcloud.com/support/s/article/JumpCloud-API-Best-Practices)

# Directory Objects<a id="directory-objects"></a>

This API offers the ability to interact with some of our core features; otherwise known as Directory Objects. The Directory Objects are:

* Commands
* Policies
* Policy Groups
* Applications
* Systems
* Users
* User Groups
* System Groups
* Radius Servers
* Directories: Office 365, LDAP,G-Suite, Active Directory
* Duo accounts and applications.

The Directory Object is an important concept to understand in order to successfully use JumpCloud API.

## JumpCloud Graph<a id="jumpcloud-graph"></a>

We've also introduced the concept of the JumpCloud Graph along with  Directory Objects. The Graph is a powerful aspect of our platform which will enable you to associate objects with each other, or establish membership for certain objects to become members of other objects.

Specific `GET` endpoints will allow you to traverse the JumpCloud Graph to return all indirect and directly bound objects in your organization.

| ![alt text](https://s3.amazonaws.com/jumpcloud-kb/Knowledge+Base+Photos/API+Docs/jumpcloud_graph.png \"JumpCloud Graph Model Example\") |
|:--:|
| **This diagram highlights our association and membership model as it relates to Directory Objects.** |

# API Key<a id="api-key"></a>

## Access Your API Key<a id="access-your-api-key"></a>

To locate your API Key:

1. Log into the [JumpCloud Admin Console](https://console.jumpcloud.com/).
2. Go to the username drop down located in the top-right of the Console.
3. Retrieve your API key from API Settings.

## API Key Considerations<a id="api-key-considerations"></a>

This API key is associated to the currently logged in administrator. Other admins will have different API keys.

**WARNING** Please keep this API key secret, as it grants full access to any data accessible via your JumpCloud console account.

You can also reset your API key in the same location in the JumpCloud Admin Console.

## Recycling or Resetting Your API Key<a id="recycling-or-resetting-your-api-key"></a>

In order to revoke access with the current API key, simply reset your API key. This will render all calls using the previous API key inaccessible.

Your API key will be passed in as a header with the header name \"x-api-key\".

```bash
curl -H \"x-api-key: [YOUR_API_KEY_HERE]\" \"https://console.jumpcloud.com/api/v2/systemgroups\"
```

# System Context<a id="system-context"></a>

* [Introduction](https://docs.jumpcloud.com)
* [Supported endpoints](https://docs.jumpcloud.com)
* [Response codes](https://docs.jumpcloud.com)
* [Authentication](https://docs.jumpcloud.com)
* [Additional examples](https://docs.jumpcloud.com)
* [Third party](https://docs.jumpcloud.com)

## Introduction<a id="introduction"></a>

JumpCloud System Context Authorization is an alternative way to authenticate with a subset of JumpCloud's REST APIs. Using this method, a system can manage its information and resource associations, allowing modern auto provisioning environments to scale as needed.

**Notes:**

 * The following documentation applies to Linux Operating Systems only.
 * Systems that have been automatically enrolled using Apple's Device Enrollment Program (DEP) or systems enrolled using the User Portal install are not eligible to use the System Context API to prevent unauthorized access to system groups and resources. If a script that utilizes the System Context API is invoked on a system enrolled in this way, it will display an error.

## Supported Endpoints<a id="supported-endpoints"></a>

JumpCloud System Context Authorization can be used in conjunction with Systems endpoints found in the V1 API and certain System Group endpoints found in the v2 API.

* A system may fetch, alter, and delete metadata about itself, including manipulating a system's Group and Systemuser associations,
  * `/api/systems/{system_id}` | [`GET`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_get) [`PUT`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_put)
* A system may delete itself from your JumpCloud organization
  * `/api/systems/{system_id}` | [`DELETE`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_delete)
* A system may fetch its direct resource associations under v2 (Groups)
  * `/api/v2/systems/{system_id}/memberof` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemGroupMembership)
  * `/api/v2/systems/{system_id}/associations` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemAssociationsList)
  * `/api/v2/systems/{system_id}/users` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemTraverseUser)
* A system may alter its direct resource associations under v2 (Groups)
  * `/api/v2/systems/{system_id}/associations` | [`POST`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemAssociationsPost)
* A system may alter its System Group associations
  * `/api/v2/systemgroups/{group_id}/members` | [`POST`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemGroupMembersPost)
    * _NOTE_ If a system attempts to alter the system group membership of a different system the request will be rejected

## Response Codes<a id="response-codes"></a>

If endpoints other than those described above are called using the System Context API, the server will return a `401` response.

## Authentication<a id="authentication"></a>

To allow for secure access to our APIs, you must authenticate each API request.
JumpCloud System Context Authorization uses [HTTP Signatures](https://tools.ietf.org/html/draft-cavage-http-signatures-00) to authenticate API requests.
The HTTP Signatures sent with each request are similar to the signatures used by the Amazon Web Services REST API.
To help with the request-signing process, we have provided an [example bash script](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/shell/SigningExample.sh). This example API request simply requests the entire system record. You must be root, or have permissions to access the contents of the `/opt/jc` directory to generate a signature.

Here is a breakdown of the example script with explanations.

First, the script extracts the systemKey from the JSON formatted `/opt/jc/jcagent.conf` file.

```bash
#!/bin/bash
conf=\"`cat /opt/jc/jcagent.conf`\"
regex=\"systemKey\\\":\\\"(\\w+)\\\"\"

if [[ $conf =~ $regex ]] ; then
  systemKey=\"${BASH_REMATCH[1]}\"
fi
```

Then, the script retrieves the current date in the correct format.

```bash
now=`date -u \"+%a, %d %h %Y %H:%M:%S GMT\"`;
```

Next, we build a signing string to demonstrate the expected signature format. The signed string must consist of the [request-line](https://tools.ietf.org/html/rfc2616#page-35) and the date header, separated by a newline character.

```bash
signstr=\"GET /api/systems/${systemKey} HTTP/1.1\\ndate: ${now}\"
```

The next step is to calculate and apply the signature. This is a two-step process:

1. Create a signature from the signing string using the JumpCloud Agent private key: ``printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key``
2. Then Base64-encode the signature string and trim off the newline characters: ``| openssl enc -e -a | tr -d '\\n'``

The combined steps above result in:

```bash
signature=`printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key | openssl enc -e -a | tr -d '\\n'` ;
```

Finally, we make sure the API call sending the signature has the same Authorization and Date header values, HTTP method, and URL that were used in the signing string.

```bash
curl -iq \\
  -H \"Accept: application/json\" \\
  -H \"Content-Type: application/json\" \\
  -H \"Date: ${now}\" \\
  -H \"Authorization: Signature keyId=\\\"system/${systemKey}\\\",headers=\\\"request-line date\\\",algorithm=\\\"rsa-sha256\\\",signature=\\\"${signature}\\\"\" \\
  --url https://console.jumpcloud.com/api/systems/${systemKey}
```

### Input Data<a id="input-data"></a>

All PUT and POST methods should use the HTTP Content-Type header with a value of 'application/json'. PUT methods are used for updating a record. POST methods are used to create a record.

The following example demonstrates how to update the `displayName` of the system.

```bash
signstr=\"PUT /api/systems/${systemKey} HTTP/1.1\\ndate: ${now}\"
signature=`printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key | openssl enc -e -a | tr -d '\\n'` ;

curl -iq \\
  -d \"{\\\"displayName\\\" : \\\"updated-system-name-1\\\"}\" \\
  -X \"PUT\" \\
  -H \"Content-Type: application/json\" \\
  -H \"Accept: application/json\" \\
  -H \"Date: ${now}\" \\
  -H \"Authorization: Signature keyId=\\\"system/${systemKey}\\\",headers=\\\"request-line date\\\",algorithm=\\\"rsa-sha256\\\",signature=\\\"${signature}\\\"\" \\
  --url https://console.jumpcloud.com/api/systems/${systemKey}
```

### Output Data<a id="output-data"></a>

All results will be formatted as JSON.

Here is an abbreviated example of response output:

```json
{
  \"_id\": \"625ee96f52e144993e000015\",
  \"agentServer\": \"lappy386\",
  \"agentVersion\": \"0.9.42\",
  \"arch\": \"x86_64\",
  \"connectionKey\": \"127.0.0.1_51812\",
  \"displayName\": \"ubuntu-1204\",
  \"firstContact\": \"2013-10-16T19:30:55.611Z\",
  \"hostname\": \"ubuntu-1204\"
  ...
```

## Additional Examples<a id="additional-examples"></a>

### Signing Authentication Example<a id="signing-authentication-example"></a>

This example demonstrates how to make an authenticated request to fetch the JumpCloud record for this system.

[SigningExample.sh](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/shell/SigningExample.sh)

### Shutdown Hook<a id="shutdown-hook"></a>

This example demonstrates how to make an authenticated request on system shutdown.
Using an init.d script registered at run level 0, you can call the System Context API as the system is shutting down.

[Instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) is an example of an init.d script that only runs at system shutdown.

After customizing the [instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) script, you should install it on the system(s) running the JumpCloud agent.

1. Copy the modified [instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) to `/etc/init.d/instance-shutdown`.
2. On Ubuntu systems, run `update-rc.d instance-shutdown defaults`. On RedHat/CentOS systems, run `chkconfig --add instance-shutdown`.

## Third Party<a id="third-party"></a>

### Chef Cookbooks<a id="chef-cookbooks"></a>

[https://github.com/nshenry03/jumpcloud](https://github.com/nshenry03/jumpcloud)

[https://github.com/cjs226/jumpcloud](https://github.com/cjs226/jumpcloud)

# Multi-Tenant Portal Headers<a id="multi-tenant-portal-headers"></a>

Multi-Tenant Organization API Headers are available for JumpCloud Admins to use when making API requests from Organizations that have multiple managed organizations.

The `x-org-id` is a required header for all multi-tenant admins when making API requests to JumpCloud. This header will define to which organization you would like to make the request.

**NOTE** Single Tenant Admins do not need to provide this header when making an API request.

## Header Value<a id="header-value"></a>

`x-org-id`

## API Response Codes<a id="api-response-codes"></a>

* `400` Malformed ID.
* `400` x-org-id and Organization path ID do not match.
* `401` ID not included for multi-tenant admin
* `403` ID included on unsupported route.
* `404` Organization ID Not Found.

```bash
curl -X GET https://console.jumpcloud.com/api/v2/directories \\
  -H 'accept: application/json' \\
  -H 'content-type: application/json' \\
  -H 'x-api-key: {API_KEY}' \\
  -H 'x-org-id: {ORG_ID}'

```

## To Obtain an Individual Organization ID via the UI<a id="to-obtain-an-individual-organization-id-via-the-ui"></a>

As a prerequisite, your Primary Organization will need to be setup for Multi-Tenancy. This provides access to the Multi-Tenant Organization Admin Portal.

1. Log into JumpCloud [Admin Console](https://console.jumpcloud.com). If you are a multi-tenant Admin, you will automatically be routed to the Multi-Tenant Admin Portal.
2. From the Multi-Tenant Portal's primary navigation bar, select the Organization you'd like to access.
3. You will automatically be routed to that Organization's Admin Console.
4. Go to Settings in the sub-tenant's primary navigation.
5. You can obtain your Organization ID below your Organization's Contact Information on the Settings page.

## To Obtain All Organization IDs via the API<a id="to-obtain-all-organization-ids-via-the-api"></a>

* You can make an API request to this endpoint using the API key of your Primary Organization.  `https://console.jumpcloud.com/api/organizations/` This will return all your managed organizations.

```bash
curl -X GET \\
  https://console.jumpcloud.com/api/organizations/ \\
  -H 'Accept: application/json' \\
  -H 'Content-Type: application/json' \\
  -H 'x-api-key: {API_KEY}'
```

# SDKs<a id="sdks"></a>

You can find language specific SDKs that can help you kickstart your Integration with JumpCloud in the following GitHub repositories:

* [Python](https://github.com/TheJumpCloud/jcapi-python)
* [Go](https://github.com/TheJumpCloud/jcapi-go)
* [Ruby](https://github.com/TheJumpCloud/jcapi-ruby)
* [Java](https://github.com/TheJumpCloud/jcapi-java)



</div>

## Table of Contents<a id="table-of-contents"></a>

<!-- toc -->

- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Async](#async)
- [Raw HTTP Response](#raw-http-response)
- [Reference](#reference)
  * [`jumpcloud.active_directory.active_directory_associations_list`](#jumpcloudactive_directoryactive_directory_associations_list)
  * [`jumpcloud.active_directory.active_directory_associations_post`](#jumpcloudactive_directoryactive_directory_associations_post)
  * [`jumpcloud.active_directory.active_directory_traverse_user`](#jumpcloudactive_directoryactive_directory_traverse_user)
  * [`jumpcloud.active_directory.active_directory_traverse_user_group`](#jumpcloudactive_directoryactive_directory_traverse_user_group)
  * [`jumpcloud.active_directory.agents_delete`](#jumpcloudactive_directoryagents_delete)
  * [`jumpcloud.active_directory.agents_get`](#jumpcloudactive_directoryagents_get)
  * [`jumpcloud.active_directory.agents_list`](#jumpcloudactive_directoryagents_list)
  * [`jumpcloud.active_directory.agents_post`](#jumpcloudactive_directoryagents_post)
  * [`jumpcloud.active_directory.delete`](#jumpcloudactive_directorydelete)
  * [`jumpcloud.active_directory.get`](#jumpcloudactive_directoryget)
  * [`jumpcloud.active_directory.list`](#jumpcloudactive_directorylist)
  * [`jumpcloud.active_directory.patch`](#jumpcloudactive_directorypatch)
  * [`jumpcloud.active_directory.post`](#jumpcloudactive_directorypost)
  * [`jumpcloud.administrators.create_by_administrator`](#jumpcloudadministratorscreate_by_administrator)
  * [`jumpcloud.administrators.list_by_administrator`](#jumpcloudadministratorslist_by_administrator)
  * [`jumpcloud.administrators.list_by_organization`](#jumpcloudadministratorslist_by_organization)
  * [`jumpcloud.administrators.remove_by_administrator`](#jumpcloudadministratorsremove_by_administrator)
  * [`jumpcloud.aggregated_policy_stats.get`](#jumpcloudaggregated_policy_statsget)
  * [`jumpcloud.apple_mdm.csrget`](#jumpcloudapple_mdmcsrget)
  * [`jumpcloud.apple_mdm.delete`](#jumpcloudapple_mdmdelete)
  * [`jumpcloud.apple_mdm.deletedevice`](#jumpcloudapple_mdmdeletedevice)
  * [`jumpcloud.apple_mdm.depkeyget`](#jumpcloudapple_mdmdepkeyget)
  * [`jumpcloud.apple_mdm.devices_clear_activation_lock`](#jumpcloudapple_mdmdevices_clear_activation_lock)
  * [`jumpcloud.apple_mdm.devices_os_update_status`](#jumpcloudapple_mdmdevices_os_update_status)
  * [`jumpcloud.apple_mdm.devices_refresh_activation_lock_information`](#jumpcloudapple_mdmdevices_refresh_activation_lock_information)
  * [`jumpcloud.apple_mdm.devices_schedule_os_update`](#jumpcloudapple_mdmdevices_schedule_os_update)
  * [`jumpcloud.apple_mdm.deviceserase`](#jumpcloudapple_mdmdeviceserase)
  * [`jumpcloud.apple_mdm.deviceslist`](#jumpcloudapple_mdmdeviceslist)
  * [`jumpcloud.apple_mdm.deviceslock`](#jumpcloudapple_mdmdeviceslock)
  * [`jumpcloud.apple_mdm.devicesrestart`](#jumpcloudapple_mdmdevicesrestart)
  * [`jumpcloud.apple_mdm.devicesshutdown`](#jumpcloudapple_mdmdevicesshutdown)
  * [`jumpcloud.apple_mdm.enrollmentprofilesget`](#jumpcloudapple_mdmenrollmentprofilesget)
  * [`jumpcloud.apple_mdm.enrollmentprofileslist`](#jumpcloudapple_mdmenrollmentprofileslist)
  * [`jumpcloud.apple_mdm.getdevice`](#jumpcloudapple_mdmgetdevice)
  * [`jumpcloud.apple_mdm.list`](#jumpcloudapple_mdmlist)
  * [`jumpcloud.apple_mdm.put`](#jumpcloudapple_mdmput)
  * [`jumpcloud.apple_mdm.refreshdepdevices`](#jumpcloudapple_mdmrefreshdepdevices)
  * [`jumpcloud.applications.application_associations_list`](#jumpcloudapplicationsapplication_associations_list)
  * [`jumpcloud.applications.application_associations_post`](#jumpcloudapplicationsapplication_associations_post)
  * [`jumpcloud.applications.application_traverse_user`](#jumpcloudapplicationsapplication_traverse_user)
  * [`jumpcloud.applications.application_traverse_user_group`](#jumpcloudapplicationsapplication_traverse_user_group)
  * [`jumpcloud.applications.create`](#jumpcloudapplicationscreate)
  * [`jumpcloud.applications.delete_logo`](#jumpcloudapplicationsdelete_logo)
  * [`jumpcloud.applications.get`](#jumpcloudapplicationsget)
  * [`jumpcloud.applications.post_logo`](#jumpcloudapplicationspost_logo)
  * [`jumpcloud.applications.users`](#jumpcloudapplicationsusers)
  * [`jumpcloud.authentication_policies.delete`](#jumpcloudauthentication_policiesdelete)
  * [`jumpcloud.authentication_policies.get`](#jumpcloudauthentication_policiesget)
  * [`jumpcloud.authentication_policies.list`](#jumpcloudauthentication_policieslist)
  * [`jumpcloud.authentication_policies.patch`](#jumpcloudauthentication_policiespatch)
  * [`jumpcloud.authentication_policies.post`](#jumpcloudauthentication_policiespost)
  * [`jumpcloud.bulk_job_requests.user_expires`](#jumpcloudbulk_job_requestsuser_expires)
  * [`jumpcloud.bulk_job_requests.user_states_create`](#jumpcloudbulk_job_requestsuser_states_create)
  * [`jumpcloud.bulk_job_requests.user_states_delete`](#jumpcloudbulk_job_requestsuser_states_delete)
  * [`jumpcloud.bulk_job_requests.user_states_get_next_scheduled`](#jumpcloudbulk_job_requestsuser_states_get_next_scheduled)
  * [`jumpcloud.bulk_job_requests.user_states_list`](#jumpcloudbulk_job_requestsuser_states_list)
  * [`jumpcloud.bulk_job_requests.user_unlocks`](#jumpcloudbulk_job_requestsuser_unlocks)
  * [`jumpcloud.bulk_job_requests.users_create`](#jumpcloudbulk_job_requestsusers_create)
  * [`jumpcloud.bulk_job_requests.users_create_results`](#jumpcloudbulk_job_requestsusers_create_results)
  * [`jumpcloud.bulk_job_requests.users_update`](#jumpcloudbulk_job_requestsusers_update)
  * [`jumpcloud.commands.cancel_queued_commands_by_workflow_instance_id`](#jumpcloudcommandscancel_queued_commands_by_workflow_instance_id)
  * [`jumpcloud.commands.command_associations_list`](#jumpcloudcommandscommand_associations_list)
  * [`jumpcloud.commands.command_associations_post`](#jumpcloudcommandscommand_associations_post)
  * [`jumpcloud.commands.command_traverse_system`](#jumpcloudcommandscommand_traverse_system)
  * [`jumpcloud.commands.command_traverse_system_group`](#jumpcloudcommandscommand_traverse_system_group)
  * [`jumpcloud.commands.get_queued_commands_by_workflow`](#jumpcloudcommandsget_queued_commands_by_workflow)
  * [`jumpcloud.custom_emails.create`](#jumpcloudcustom_emailscreate)
  * [`jumpcloud.custom_emails.destroy`](#jumpcloudcustom_emailsdestroy)
  * [`jumpcloud.custom_emails.get_templates`](#jumpcloudcustom_emailsget_templates)
  * [`jumpcloud.custom_emails.read`](#jumpcloudcustom_emailsread)
  * [`jumpcloud.custom_emails.update`](#jumpcloudcustom_emailsupdate)
  * [`jumpcloud.directories.list`](#jumpclouddirectorieslist)
  * [`jumpcloud.duo.account_delete`](#jumpcloudduoaccount_delete)
  * [`jumpcloud.duo.account_get`](#jumpcloudduoaccount_get)
  * [`jumpcloud.duo.account_list`](#jumpcloudduoaccount_list)
  * [`jumpcloud.duo.account_post`](#jumpcloudduoaccount_post)
  * [`jumpcloud.duo.application_delete`](#jumpcloudduoapplication_delete)
  * [`jumpcloud.duo.application_get`](#jumpcloudduoapplication_get)
  * [`jumpcloud.duo.application_list`](#jumpcloudduoapplication_list)
  * [`jumpcloud.duo.application_post`](#jumpcloudduoapplication_post)
  * [`jumpcloud.duo.application_update`](#jumpcloudduoapplication_update)
  * [`jumpcloud.feature_trials.get_feature_trials`](#jumpcloudfeature_trialsget_feature_trials)
  * [`jumpcloud.g_suite.add_domain`](#jumpcloudg_suiteadd_domain)
  * [`jumpcloud.g_suite.configured_domains_list`](#jumpcloudg_suiteconfigured_domains_list)
  * [`jumpcloud.g_suite.delete_domain`](#jumpcloudg_suitedelete_domain)
  * [`jumpcloud.g_suite.g_suite_associations_list`](#jumpcloudg_suiteg_suite_associations_list)
  * [`jumpcloud.g_suite.g_suite_associations_post`](#jumpcloudg_suiteg_suite_associations_post)
  * [`jumpcloud.g_suite.g_suite_delete`](#jumpcloudg_suiteg_suite_delete)
  * [`jumpcloud.g_suite.g_suite_get`](#jumpcloudg_suiteg_suite_get)
  * [`jumpcloud.g_suite.g_suite_list`](#jumpcloudg_suiteg_suite_list)
  * [`jumpcloud.g_suite.g_suite_post`](#jumpcloudg_suiteg_suite_post)
  * [`jumpcloud.g_suite.g_suite_traverse_user`](#jumpcloudg_suiteg_suite_traverse_user)
  * [`jumpcloud.g_suite.g_suite_traverse_user_group`](#jumpcloudg_suiteg_suite_traverse_user_group)
  * [`jumpcloud.g_suite.get`](#jumpcloudg_suiteget)
  * [`jumpcloud.g_suite.list_import_jumpcloud_users`](#jumpcloudg_suitelist_import_jumpcloud_users)
  * [`jumpcloud.g_suite.list_import_users`](#jumpcloudg_suitelist_import_users)
  * [`jumpcloud.g_suite.patch`](#jumpcloudg_suitepatch)
  * [`jumpcloud.g_suite_import.list_import_jumpcloud_users`](#jumpcloudg_suite_importlist_import_jumpcloud_users)
  * [`jumpcloud.g_suite_import.list_import_users`](#jumpcloudg_suite_importlist_import_users)
  * [`jumpcloud.google_emm.create`](#jumpcloudgoogle_emmcreate)
  * [`jumpcloud.google_emm.create_enrollment_token`](#jumpcloudgoogle_emmcreate_enrollment_token)
  * [`jumpcloud.google_emm.create_enterprise`](#jumpcloudgoogle_emmcreate_enterprise)
  * [`jumpcloud.google_emm.create_enterprises_enrollment_token`](#jumpcloudgoogle_emmcreate_enterprises_enrollment_token)
  * [`jumpcloud.google_emm.create_web_token`](#jumpcloudgoogle_emmcreate_web_token)
  * [`jumpcloud.google_emm.delete_enrollment_token`](#jumpcloudgoogle_emmdelete_enrollment_token)
  * [`jumpcloud.google_emm.delete_enterprise`](#jumpcloudgoogle_emmdelete_enterprise)
  * [`jumpcloud.google_emm.erase_device`](#jumpcloudgoogle_emmerase_device)
  * [`jumpcloud.google_emm.get_connection_status`](#jumpcloudgoogle_emmget_connection_status)
  * [`jumpcloud.google_emm.get_device`](#jumpcloudgoogle_emmget_device)
  * [`jumpcloud.google_emm.get_device_android_policy`](#jumpcloudgoogle_emmget_device_android_policy)
  * [`jumpcloud.google_emm.list_devices`](#jumpcloudgoogle_emmlist_devices)
  * [`jumpcloud.google_emm.list_enrollment_tokens`](#jumpcloudgoogle_emmlist_enrollment_tokens)
  * [`jumpcloud.google_emm.list_enterprises`](#jumpcloudgoogle_emmlist_enterprises)
  * [`jumpcloud.google_emm.lock_device`](#jumpcloudgoogle_emmlock_device)
  * [`jumpcloud.google_emm.patch_enterprise`](#jumpcloudgoogle_emmpatch_enterprise)
  * [`jumpcloud.google_emm.reboot_device`](#jumpcloudgoogle_emmreboot_device)
  * [`jumpcloud.google_emm.reset_password`](#jumpcloudgoogle_emmreset_password)
  * [`jumpcloud.graph.active_directory_associations_list`](#jumpcloudgraphactive_directory_associations_list)
  * [`jumpcloud.graph.active_directory_associations_post`](#jumpcloudgraphactive_directory_associations_post)
  * [`jumpcloud.graph.active_directory_traverse_user`](#jumpcloudgraphactive_directory_traverse_user)
  * [`jumpcloud.graph.active_directory_traverse_user_group`](#jumpcloudgraphactive_directory_traverse_user_group)
  * [`jumpcloud.graph.application_associations_list`](#jumpcloudgraphapplication_associations_list)
  * [`jumpcloud.graph.application_associations_post`](#jumpcloudgraphapplication_associations_post)
  * [`jumpcloud.graph.application_traverse_user`](#jumpcloudgraphapplication_traverse_user)
  * [`jumpcloud.graph.application_traverse_user_group`](#jumpcloudgraphapplication_traverse_user_group)
  * [`jumpcloud.graph.command_associations_list`](#jumpcloudgraphcommand_associations_list)
  * [`jumpcloud.graph.command_associations_post`](#jumpcloudgraphcommand_associations_post)
  * [`jumpcloud.graph.command_traverse_system`](#jumpcloudgraphcommand_traverse_system)
  * [`jumpcloud.graph.command_traverse_system_group`](#jumpcloudgraphcommand_traverse_system_group)
  * [`jumpcloud.graph.g_suite_associations_list`](#jumpcloudgraphg_suite_associations_list)
  * [`jumpcloud.graph.g_suite_associations_post`](#jumpcloudgraphg_suite_associations_post)
  * [`jumpcloud.graph.g_suite_traverse_user`](#jumpcloudgraphg_suite_traverse_user)
  * [`jumpcloud.graph.g_suite_traverse_user_group`](#jumpcloudgraphg_suite_traverse_user_group)
  * [`jumpcloud.graph.idp_routing_policy_associations_list`](#jumpcloudgraphidp_routing_policy_associations_list)
  * [`jumpcloud.graph.idp_routing_policy_associations_post`](#jumpcloudgraphidp_routing_policy_associations_post)
  * [`jumpcloud.graph.idp_routing_policy_traverse_user`](#jumpcloudgraphidp_routing_policy_traverse_user)
  * [`jumpcloud.graph.idp_routing_policy_traverse_user_group`](#jumpcloudgraphidp_routing_policy_traverse_user_group)
  * [`jumpcloud.graph.ldap_server_associations_list`](#jumpcloudgraphldap_server_associations_list)
  * [`jumpcloud.graph.ldap_server_associations_post`](#jumpcloudgraphldap_server_associations_post)
  * [`jumpcloud.graph.ldap_server_traverse_user`](#jumpcloudgraphldap_server_traverse_user)
  * [`jumpcloud.graph.ldap_server_traverse_user_group`](#jumpcloudgraphldap_server_traverse_user_group)
  * [`jumpcloud.graph.office365_associations_list`](#jumpcloudgraphoffice365_associations_list)
  * [`jumpcloud.graph.office365_associations_post`](#jumpcloudgraphoffice365_associations_post)
  * [`jumpcloud.graph.office365_traverse_user`](#jumpcloudgraphoffice365_traverse_user)
  * [`jumpcloud.graph.office365_traverse_user_group`](#jumpcloudgraphoffice365_traverse_user_group)
  * [`jumpcloud.graph.policy_associations_list`](#jumpcloudgraphpolicy_associations_list)
  * [`jumpcloud.graph.policy_associations_post`](#jumpcloudgraphpolicy_associations_post)
  * [`jumpcloud.graph.policy_group_associations_list`](#jumpcloudgraphpolicy_group_associations_list)
  * [`jumpcloud.graph.policy_group_associations_post`](#jumpcloudgraphpolicy_group_associations_post)
  * [`jumpcloud.graph.policy_group_members_list`](#jumpcloudgraphpolicy_group_members_list)
  * [`jumpcloud.graph.policy_group_members_post`](#jumpcloudgraphpolicy_group_members_post)
  * [`jumpcloud.graph.policy_group_membership`](#jumpcloudgraphpolicy_group_membership)
  * [`jumpcloud.graph.policy_group_traverse_system`](#jumpcloudgraphpolicy_group_traverse_system)
  * [`jumpcloud.graph.policy_group_traverse_system_group`](#jumpcloudgraphpolicy_group_traverse_system_group)
  * [`jumpcloud.graph.policy_member_of`](#jumpcloudgraphpolicy_member_of)
  * [`jumpcloud.graph.policy_traverse_system`](#jumpcloudgraphpolicy_traverse_system)
  * [`jumpcloud.graph.policy_traverse_system_group`](#jumpcloudgraphpolicy_traverse_system_group)
  * [`jumpcloud.graph.radius_server_associations_list`](#jumpcloudgraphradius_server_associations_list)
  * [`jumpcloud.graph.radius_server_associations_post`](#jumpcloudgraphradius_server_associations_post)
  * [`jumpcloud.graph.radius_server_traverse_user`](#jumpcloudgraphradius_server_traverse_user)
  * [`jumpcloud.graph.radius_server_traverse_user_group`](#jumpcloudgraphradius_server_traverse_user_group)
  * [`jumpcloud.graph.softwareapps_associations_list`](#jumpcloudgraphsoftwareapps_associations_list)
  * [`jumpcloud.graph.softwareapps_associations_post`](#jumpcloudgraphsoftwareapps_associations_post)
  * [`jumpcloud.graph.softwareapps_traverse_system`](#jumpcloudgraphsoftwareapps_traverse_system)
  * [`jumpcloud.graph.softwareapps_traverse_system_group`](#jumpcloudgraphsoftwareapps_traverse_system_group)
  * [`jumpcloud.graph.system_associations_list`](#jumpcloudgraphsystem_associations_list)
  * [`jumpcloud.graph.system_associations_post`](#jumpcloudgraphsystem_associations_post)
  * [`jumpcloud.graph.system_group_associations_list`](#jumpcloudgraphsystem_group_associations_list)
  * [`jumpcloud.graph.system_group_associations_post`](#jumpcloudgraphsystem_group_associations_post)
  * [`jumpcloud.graph.system_group_members_list`](#jumpcloudgraphsystem_group_members_list)
  * [`jumpcloud.graph.system_group_members_post`](#jumpcloudgraphsystem_group_members_post)
  * [`jumpcloud.graph.system_group_membership`](#jumpcloudgraphsystem_group_membership)
  * [`jumpcloud.graph.system_group_traverse_command`](#jumpcloudgraphsystem_group_traverse_command)
  * [`jumpcloud.graph.system_group_traverse_policy`](#jumpcloudgraphsystem_group_traverse_policy)
  * [`jumpcloud.graph.system_group_traverse_policy_group`](#jumpcloudgraphsystem_group_traverse_policy_group)
  * [`jumpcloud.graph.system_group_traverse_user`](#jumpcloudgraphsystem_group_traverse_user)
  * [`jumpcloud.graph.system_group_traverse_user_group`](#jumpcloudgraphsystem_group_traverse_user_group)
  * [`jumpcloud.graph.system_member_of`](#jumpcloudgraphsystem_member_of)
  * [`jumpcloud.graph.system_traverse_command`](#jumpcloudgraphsystem_traverse_command)
  * [`jumpcloud.graph.system_traverse_policy`](#jumpcloudgraphsystem_traverse_policy)
  * [`jumpcloud.graph.system_traverse_policy_group`](#jumpcloudgraphsystem_traverse_policy_group)
  * [`jumpcloud.graph.system_traverse_user`](#jumpcloudgraphsystem_traverse_user)
  * [`jumpcloud.graph.system_traverse_user_group`](#jumpcloudgraphsystem_traverse_user_group)
  * [`jumpcloud.graph.systems_list`](#jumpcloudgraphsystems_list)
  * [`jumpcloud.graph.user_associations_list`](#jumpcloudgraphuser_associations_list)
  * [`jumpcloud.graph.user_associations_post`](#jumpcloudgraphuser_associations_post)
  * [`jumpcloud.graph.user_group_associations_list`](#jumpcloudgraphuser_group_associations_list)
  * [`jumpcloud.graph.user_group_associations_post`](#jumpcloudgraphuser_group_associations_post)
  * [`jumpcloud.graph.user_group_members_list`](#jumpcloudgraphuser_group_members_list)
  * [`jumpcloud.graph.user_group_members_post`](#jumpcloudgraphuser_group_members_post)
  * [`jumpcloud.graph.user_group_membership`](#jumpcloudgraphuser_group_membership)
  * [`jumpcloud.graph.user_group_traverse_active_directory`](#jumpcloudgraphuser_group_traverse_active_directory)
  * [`jumpcloud.graph.user_group_traverse_application`](#jumpcloudgraphuser_group_traverse_application)
  * [`jumpcloud.graph.user_group_traverse_directory`](#jumpcloudgraphuser_group_traverse_directory)
  * [`jumpcloud.graph.user_group_traverse_g_suite`](#jumpcloudgraphuser_group_traverse_g_suite)
  * [`jumpcloud.graph.user_group_traverse_ldap_server`](#jumpcloudgraphuser_group_traverse_ldap_server)
  * [`jumpcloud.graph.user_group_traverse_office365`](#jumpcloudgraphuser_group_traverse_office365)
  * [`jumpcloud.graph.user_group_traverse_radius_server`](#jumpcloudgraphuser_group_traverse_radius_server)
  * [`jumpcloud.graph.user_group_traverse_system`](#jumpcloudgraphuser_group_traverse_system)
  * [`jumpcloud.graph.user_group_traverse_system_group`](#jumpcloudgraphuser_group_traverse_system_group)
  * [`jumpcloud.graph.user_member_of`](#jumpcloudgraphuser_member_of)
  * [`jumpcloud.graph.user_traverse_active_directory`](#jumpcloudgraphuser_traverse_active_directory)
  * [`jumpcloud.graph.user_traverse_application`](#jumpcloudgraphuser_traverse_application)
  * [`jumpcloud.graph.user_traverse_directory`](#jumpcloudgraphuser_traverse_directory)
  * [`jumpcloud.graph.user_traverse_g_suite`](#jumpcloudgraphuser_traverse_g_suite)
  * [`jumpcloud.graph.user_traverse_ldap_server`](#jumpcloudgraphuser_traverse_ldap_server)
  * [`jumpcloud.graph.user_traverse_office365`](#jumpcloudgraphuser_traverse_office365)
  * [`jumpcloud.graph.user_traverse_radius_server`](#jumpcloudgraphuser_traverse_radius_server)
  * [`jumpcloud.graph.user_traverse_system`](#jumpcloudgraphuser_traverse_system)
  * [`jumpcloud.graph.user_traverse_system_group`](#jumpcloudgraphuser_traverse_system_group)
  * [`jumpcloud.groups.list`](#jumpcloudgroupslist)
  * [`jumpcloud.ip_lists.delete`](#jumpcloudip_listsdelete)
  * [`jumpcloud.ip_lists.get`](#jumpcloudip_listsget)
  * [`jumpcloud.ip_lists.list`](#jumpcloudip_listslist)
  * [`jumpcloud.ip_lists.patch`](#jumpcloudip_listspatch)
  * [`jumpcloud.ip_lists.post`](#jumpcloudip_listspost)
  * [`jumpcloud.ip_lists.put`](#jumpcloudip_listsput)
  * [`jumpcloud.identity_providers.idp_routing_policy_associations_list`](#jumpcloudidentity_providersidp_routing_policy_associations_list)
  * [`jumpcloud.identity_providers.idp_routing_policy_associations_post`](#jumpcloudidentity_providersidp_routing_policy_associations_post)
  * [`jumpcloud.identity_providers.idp_routing_policy_traverse_user`](#jumpcloudidentity_providersidp_routing_policy_traverse_user)
  * [`jumpcloud.identity_providers.idp_routing_policy_traverse_user_group`](#jumpcloudidentity_providersidp_routing_policy_traverse_user_group)
  * [`jumpcloud.image.delete_logo`](#jumpcloudimagedelete_logo)
  * [`jumpcloud.ingresso.create_access_request`](#jumpcloudingressocreate_access_request)
  * [`jumpcloud.ingresso.get_access_request`](#jumpcloudingressoget_access_request)
  * [`jumpcloud.ingresso.revoke_access_request`](#jumpcloudingressorevoke_access_request)
  * [`jumpcloud.ingresso.update_access_request`](#jumpcloudingressoupdate_access_request)
  * [`jumpcloud.ldap_servers.get`](#jumpcloudldap_serversget)
  * [`jumpcloud.ldap_servers.ldap_server_associations_list`](#jumpcloudldap_serversldap_server_associations_list)
  * [`jumpcloud.ldap_servers.ldap_server_associations_post`](#jumpcloudldap_serversldap_server_associations_post)
  * [`jumpcloud.ldap_servers.ldap_server_traverse_user`](#jumpcloudldap_serversldap_server_traverse_user)
  * [`jumpcloud.ldap_servers.ldap_server_traverse_user_group`](#jumpcloudldap_serversldap_server_traverse_user_group)
  * [`jumpcloud.ldap_servers.list`](#jumpcloudldap_serverslist)
  * [`jumpcloud.ldap_servers.patch`](#jumpcloudldap_serverspatch)
  * [`jumpcloud.logos.get`](#jumpcloudlogosget)
  * [`jumpcloud.managed_service_provider.cases_metadata`](#jumpcloudmanaged_service_providercases_metadata)
  * [`jumpcloud.managed_service_provider.create_by_administrator`](#jumpcloudmanaged_service_providercreate_by_administrator)
  * [`jumpcloud.managed_service_provider.create_org`](#jumpcloudmanaged_service_providercreate_org)
  * [`jumpcloud.managed_service_provider.delete`](#jumpcloudmanaged_service_providerdelete)
  * [`jumpcloud.managed_service_provider.get`](#jumpcloudmanaged_service_providerget)
  * [`jumpcloud.managed_service_provider.get_configured_policy_template`](#jumpcloudmanaged_service_providerget_configured_policy_template)
  * [`jumpcloud.managed_service_provider.get_provider`](#jumpcloudmanaged_service_providerget_provider)
  * [`jumpcloud.managed_service_provider.list`](#jumpcloudmanaged_service_providerlist)
  * [`jumpcloud.managed_service_provider.list_administrators`](#jumpcloudmanaged_service_providerlist_administrators)
  * [`jumpcloud.managed_service_provider.list_by_administrator`](#jumpcloudmanaged_service_providerlist_by_administrator)
  * [`jumpcloud.managed_service_provider.list_by_organization`](#jumpcloudmanaged_service_providerlist_by_organization)
  * [`jumpcloud.managed_service_provider.list_configured_policy_templates`](#jumpcloudmanaged_service_providerlist_configured_policy_templates)
  * [`jumpcloud.managed_service_provider.list_members`](#jumpcloudmanaged_service_providerlist_members)
  * [`jumpcloud.managed_service_provider.list_organizations`](#jumpcloudmanaged_service_providerlist_organizations)
  * [`jumpcloud.managed_service_provider.post_admins`](#jumpcloudmanaged_service_providerpost_admins)
  * [`jumpcloud.managed_service_provider.provider_list_case`](#jumpcloudmanaged_service_providerprovider_list_case)
  * [`jumpcloud.managed_service_provider.remove_by_administrator`](#jumpcloudmanaged_service_providerremove_by_administrator)
  * [`jumpcloud.managed_service_provider.retrieve_invoice`](#jumpcloudmanaged_service_providerretrieve_invoice)
  * [`jumpcloud.managed_service_provider.retrieve_invoices`](#jumpcloudmanaged_service_providerretrieve_invoices)
  * [`jumpcloud.managed_service_provider.update_org`](#jumpcloudmanaged_service_providerupdate_org)
  * [`jumpcloud.microsoft_mdm.download_config_files`](#jumpcloudmicrosoft_mdmdownload_config_files)
  * [`jumpcloud.office_365.delete`](#jumpcloudoffice_365delete)
  * [`jumpcloud.office_365.get`](#jumpcloudoffice_365get)
  * [`jumpcloud.office_365.insert`](#jumpcloudoffice_365insert)
  * [`jumpcloud.office_365.list`](#jumpcloudoffice_365list)
  * [`jumpcloud.office_365.list_import_users`](#jumpcloudoffice_365list_import_users)
  * [`jumpcloud.office_365.office365_associations_list`](#jumpcloudoffice_365office365_associations_list)
  * [`jumpcloud.office_365.office365_associations_post`](#jumpcloudoffice_365office365_associations_post)
  * [`jumpcloud.office_365.office365_delete`](#jumpcloudoffice_365office365_delete)
  * [`jumpcloud.office_365.office365_get`](#jumpcloudoffice_365office365_get)
  * [`jumpcloud.office_365.office365_list`](#jumpcloudoffice_365office365_list)
  * [`jumpcloud.office_365.office365_post`](#jumpcloudoffice_365office365_post)
  * [`jumpcloud.office_365.office365_traverse_user`](#jumpcloudoffice_365office365_traverse_user)
  * [`jumpcloud.office_365.office365_traverse_user_group`](#jumpcloudoffice_365office365_traverse_user_group)
  * [`jumpcloud.office_365.patch`](#jumpcloudoffice_365patch)
  * [`jumpcloud.office_365_import.list_import_users`](#jumpcloudoffice_365_importlist_import_users)
  * [`jumpcloud.organizations.create_by_administrator`](#jumpcloudorganizationscreate_by_administrator)
  * [`jumpcloud.organizations.list_by_administrator`](#jumpcloudorganizationslist_by_administrator)
  * [`jumpcloud.organizations.list_by_organization`](#jumpcloudorganizationslist_by_organization)
  * [`jumpcloud.organizations.org_list_cases`](#jumpcloudorganizationsorg_list_cases)
  * [`jumpcloud.organizations.remove_by_administrator`](#jumpcloudorganizationsremove_by_administrator)
  * [`jumpcloud.password_manager.get_device`](#jumpcloudpassword_managerget_device)
  * [`jumpcloud.password_manager.list_devices`](#jumpcloudpassword_managerlist_devices)
  * [`jumpcloud.policies.delete`](#jumpcloudpoliciesdelete)
  * [`jumpcloud.policies.get`](#jumpcloudpoliciesget)
  * [`jumpcloud.policies.get_0`](#jumpcloudpoliciesget_0)
  * [`jumpcloud.policies.get_1`](#jumpcloudpoliciesget_1)
  * [`jumpcloud.policies.list`](#jumpcloudpolicieslist)
  * [`jumpcloud.policies.list_0`](#jumpcloudpolicieslist_0)
  * [`jumpcloud.policies.list_1`](#jumpcloudpolicieslist_1)
  * [`jumpcloud.policies.list_all_policy_results`](#jumpcloudpolicieslist_all_policy_results)
  * [`jumpcloud.policies.policies_list`](#jumpcloudpoliciespolicies_list)
  * [`jumpcloud.policies.policy_associations_list`](#jumpcloudpoliciespolicy_associations_list)
  * [`jumpcloud.policies.policy_associations_post`](#jumpcloudpoliciespolicy_associations_post)
  * [`jumpcloud.policies.policy_member_of`](#jumpcloudpoliciespolicy_member_of)
  * [`jumpcloud.policies.policy_traverse_system`](#jumpcloudpoliciespolicy_traverse_system)
  * [`jumpcloud.policies.policy_traverse_system_group`](#jumpcloudpoliciespolicy_traverse_system_group)
  * [`jumpcloud.policies.post`](#jumpcloudpoliciespost)
  * [`jumpcloud.policies.put`](#jumpcloudpoliciesput)
  * [`jumpcloud.policies.systems_list`](#jumpcloudpoliciessystems_list)
  * [`jumpcloud.policy_group_associations.policy_group_associations_list`](#jumpcloudpolicy_group_associationspolicy_group_associations_list)
  * [`jumpcloud.policy_group_associations.policy_group_associations_post`](#jumpcloudpolicy_group_associationspolicy_group_associations_post)
  * [`jumpcloud.policy_group_associations.policy_group_traverse_system`](#jumpcloudpolicy_group_associationspolicy_group_traverse_system)
  * [`jumpcloud.policy_group_associations.policy_group_traverse_system_group`](#jumpcloudpolicy_group_associationspolicy_group_traverse_system_group)
  * [`jumpcloud.policy_group_members_&amp;_membership.policy_group_members_list`](#jumpcloudpolicy_group_members_amp_membershippolicy_group_members_list)
  * [`jumpcloud.policy_group_members_&amp;_membership.policy_group_members_post`](#jumpcloudpolicy_group_members_amp_membershippolicy_group_members_post)
  * [`jumpcloud.policy_group_members_&amp;_membership.policy_group_membership`](#jumpcloudpolicy_group_members_amp_membershippolicy_group_membership)
  * [`jumpcloud.policy_group_templates.delete`](#jumpcloudpolicy_group_templatesdelete)
  * [`jumpcloud.policy_group_templates.get`](#jumpcloudpolicy_group_templatesget)
  * [`jumpcloud.policy_group_templates.get_configured_policy_template`](#jumpcloudpolicy_group_templatesget_configured_policy_template)
  * [`jumpcloud.policy_group_templates.list`](#jumpcloudpolicy_group_templateslist)
  * [`jumpcloud.policy_group_templates.list_configured_policy_templates`](#jumpcloudpolicy_group_templateslist_configured_policy_templates)
  * [`jumpcloud.policy_group_templates.list_members`](#jumpcloudpolicy_group_templateslist_members)
  * [`jumpcloud.policy_groups.create_new`](#jumpcloudpolicy_groupscreate_new)
  * [`jumpcloud.policy_groups.delete_group`](#jumpcloudpolicy_groupsdelete_group)
  * [`jumpcloud.policy_groups.get_details`](#jumpcloudpolicy_groupsget_details)
  * [`jumpcloud.policy_groups.list_all`](#jumpcloudpolicy_groupslist_all)
  * [`jumpcloud.policy_groups.policy_group_associations_list`](#jumpcloudpolicy_groupspolicy_group_associations_list)
  * [`jumpcloud.policy_groups.policy_group_associations_post`](#jumpcloudpolicy_groupspolicy_group_associations_post)
  * [`jumpcloud.policy_groups.policy_group_members_list`](#jumpcloudpolicy_groupspolicy_group_members_list)
  * [`jumpcloud.policy_groups.policy_group_members_post`](#jumpcloudpolicy_groupspolicy_group_members_post)
  * [`jumpcloud.policy_groups.policy_group_membership`](#jumpcloudpolicy_groupspolicy_group_membership)
  * [`jumpcloud.policy_groups.policy_group_traverse_system`](#jumpcloudpolicy_groupspolicy_group_traverse_system)
  * [`jumpcloud.policy_groups.policy_group_traverse_system_group`](#jumpcloudpolicy_groupspolicy_group_traverse_system_group)
  * [`jumpcloud.policy_groups.update_policy_group`](#jumpcloudpolicy_groupsupdate_policy_group)
  * [`jumpcloud.policytemplates.get`](#jumpcloudpolicytemplatesget)
  * [`jumpcloud.policytemplates.list`](#jumpcloudpolicytemplateslist)
  * [`jumpcloud.providers.cases_metadata`](#jumpcloudproviderscases_metadata)
  * [`jumpcloud.providers.create_configuration`](#jumpcloudproviderscreate_configuration)
  * [`jumpcloud.providers.create_configuration_0`](#jumpcloudproviderscreate_configuration_0)
  * [`jumpcloud.providers.create_configuration_1`](#jumpcloudproviderscreate_configuration_1)
  * [`jumpcloud.providers.create_org`](#jumpcloudproviderscreate_org)
  * [`jumpcloud.providers.delete`](#jumpcloudprovidersdelete)
  * [`jumpcloud.providers.delete_configuration`](#jumpcloudprovidersdelete_configuration)
  * [`jumpcloud.providers.delete_configuration_0`](#jumpcloudprovidersdelete_configuration_0)
  * [`jumpcloud.providers.delete_configuration_1`](#jumpcloudprovidersdelete_configuration_1)
  * [`jumpcloud.providers.get`](#jumpcloudprovidersget)
  * [`jumpcloud.providers.get_configuration`](#jumpcloudprovidersget_configuration)
  * [`jumpcloud.providers.get_configuration_0`](#jumpcloudprovidersget_configuration_0)
  * [`jumpcloud.providers.get_configuration_1`](#jumpcloudprovidersget_configuration_1)
  * [`jumpcloud.providers.get_configured_policy_template`](#jumpcloudprovidersget_configured_policy_template)
  * [`jumpcloud.providers.get_contract`](#jumpcloudprovidersget_contract)
  * [`jumpcloud.providers.get_details`](#jumpcloudprovidersget_details)
  * [`jumpcloud.providers.get_provider`](#jumpcloudprovidersget_provider)
  * [`jumpcloud.providers.list`](#jumpcloudproviderslist)
  * [`jumpcloud.providers.list_administrators`](#jumpcloudproviderslist_administrators)
  * [`jumpcloud.providers.list_configured_policy_templates`](#jumpcloudproviderslist_configured_policy_templates)
  * [`jumpcloud.providers.list_members`](#jumpcloudproviderslist_members)
  * [`jumpcloud.providers.list_organizations`](#jumpcloudproviderslist_organizations)
  * [`jumpcloud.providers.patch_mappings`](#jumpcloudproviderspatch_mappings)
  * [`jumpcloud.providers.patch_mappings_0`](#jumpcloudproviderspatch_mappings_0)
  * [`jumpcloud.providers.patch_mappings_1`](#jumpcloudproviderspatch_mappings_1)
  * [`jumpcloud.providers.patch_settings`](#jumpcloudproviderspatch_settings)
  * [`jumpcloud.providers.patch_settings_0`](#jumpcloudproviderspatch_settings_0)
  * [`jumpcloud.providers.patch_settings_1`](#jumpcloudproviderspatch_settings_1)
  * [`jumpcloud.providers.post_admins`](#jumpcloudproviderspost_admins)
  * [`jumpcloud.providers.provider_list_case`](#jumpcloudprovidersprovider_list_case)
  * [`jumpcloud.providers.remove_administrator`](#jumpcloudprovidersremove_administrator)
  * [`jumpcloud.providers.retrieve_additions`](#jumpcloudprovidersretrieve_additions)
  * [`jumpcloud.providers.retrieve_agreements`](#jumpcloudprovidersretrieve_agreements)
  * [`jumpcloud.providers.retrieve_alerts`](#jumpcloudprovidersretrieve_alerts)
  * [`jumpcloud.providers.retrieve_all_alert_configuration_options`](#jumpcloudprovidersretrieve_all_alert_configuration_options)
  * [`jumpcloud.providers.retrieve_all_alert_configuration_options_0`](#jumpcloudprovidersretrieve_all_alert_configuration_options_0)
  * [`jumpcloud.providers.retrieve_all_alert_configuration_options_1`](#jumpcloudprovidersretrieve_all_alert_configuration_options_1)
  * [`jumpcloud.providers.retrieve_all_alert_configurations`](#jumpcloudprovidersretrieve_all_alert_configurations)
  * [`jumpcloud.providers.retrieve_all_alert_configurations_0`](#jumpcloudprovidersretrieve_all_alert_configurations_0)
  * [`jumpcloud.providers.retrieve_all_alert_configurations_1`](#jumpcloudprovidersretrieve_all_alert_configurations_1)
  * [`jumpcloud.providers.retrieve_billing_mapping_configuration_options`](#jumpcloudprovidersretrieve_billing_mapping_configuration_options)
  * [`jumpcloud.providers.retrieve_companies`](#jumpcloudprovidersretrieve_companies)
  * [`jumpcloud.providers.retrieve_companies_0`](#jumpcloudprovidersretrieve_companies_0)
  * [`jumpcloud.providers.retrieve_companies_1`](#jumpcloudprovidersretrieve_companies_1)
  * [`jumpcloud.providers.retrieve_company_types`](#jumpcloudprovidersretrieve_company_types)
  * [`jumpcloud.providers.retrieve_company_types_0`](#jumpcloudprovidersretrieve_company_types_0)
  * [`jumpcloud.providers.retrieve_contracts`](#jumpcloudprovidersretrieve_contracts)
  * [`jumpcloud.providers.retrieve_contracts_fields`](#jumpcloudprovidersretrieve_contracts_fields)
  * [`jumpcloud.providers.retrieve_integrations`](#jumpcloudprovidersretrieve_integrations)
  * [`jumpcloud.providers.retrieve_invoice`](#jumpcloudprovidersretrieve_invoice)
  * [`jumpcloud.providers.retrieve_invoices`](#jumpcloudprovidersretrieve_invoices)
  * [`jumpcloud.providers.retrieve_mappings`](#jumpcloudprovidersretrieve_mappings)
  * [`jumpcloud.providers.retrieve_mappings_0`](#jumpcloudprovidersretrieve_mappings_0)
  * [`jumpcloud.providers.retrieve_mappings_1`](#jumpcloudprovidersretrieve_mappings_1)
  * [`jumpcloud.providers.retrieve_services`](#jumpcloudprovidersretrieve_services)
  * [`jumpcloud.providers.retrieve_settings`](#jumpcloudprovidersretrieve_settings)
  * [`jumpcloud.providers.retrieve_settings_0`](#jumpcloudprovidersretrieve_settings_0)
  * [`jumpcloud.providers.retrieve_settings_1`](#jumpcloudprovidersretrieve_settings_1)
  * [`jumpcloud.providers.retrieve_sync_errors`](#jumpcloudprovidersretrieve_sync_errors)
  * [`jumpcloud.providers.update_alert_configuration`](#jumpcloudprovidersupdate_alert_configuration)
  * [`jumpcloud.providers.update_alert_configuration_0`](#jumpcloudprovidersupdate_alert_configuration_0)
  * [`jumpcloud.providers.update_alert_configuration_1`](#jumpcloudprovidersupdate_alert_configuration_1)
  * [`jumpcloud.providers.update_configuration`](#jumpcloudprovidersupdate_configuration)
  * [`jumpcloud.providers.update_configuration_0`](#jumpcloudprovidersupdate_configuration_0)
  * [`jumpcloud.providers.update_configuration_1`](#jumpcloudprovidersupdate_configuration_1)
  * [`jumpcloud.providers.update_org`](#jumpcloudprovidersupdate_org)
  * [`jumpcloud.push_verification.get`](#jumpcloudpush_verificationget)
  * [`jumpcloud.push_verification.start`](#jumpcloudpush_verificationstart)
  * [`jumpcloud.radius_servers.radius_server_associations_list`](#jumpcloudradius_serversradius_server_associations_list)
  * [`jumpcloud.radius_servers.radius_server_associations_post`](#jumpcloudradius_serversradius_server_associations_post)
  * [`jumpcloud.radius_servers.radius_server_traverse_user`](#jumpcloudradius_serversradius_server_traverse_user)
  * [`jumpcloud.radius_servers.radius_server_traverse_user_group`](#jumpcloudradius_serversradius_server_traverse_user_group)
  * [`jumpcloud.scim_import.users`](#jumpcloudscim_importusers)
  * [`jumpcloud.samba_domains.samba_domains_delete`](#jumpcloudsamba_domainssamba_domains_delete)
  * [`jumpcloud.samba_domains.samba_domains_get`](#jumpcloudsamba_domainssamba_domains_get)
  * [`jumpcloud.samba_domains.samba_domains_list`](#jumpcloudsamba_domainssamba_domains_list)
  * [`jumpcloud.samba_domains.samba_domains_post`](#jumpcloudsamba_domainssamba_domains_post)
  * [`jumpcloud.samba_domains.samba_domains_put`](#jumpcloudsamba_domainssamba_domains_put)
  * [`jumpcloud.software_apps.delete`](#jumpcloudsoftware_appsdelete)
  * [`jumpcloud.software_apps.get`](#jumpcloudsoftware_appsget)
  * [`jumpcloud.software_apps.list`](#jumpcloudsoftware_appslist)
  * [`jumpcloud.software_apps.list_0`](#jumpcloudsoftware_appslist_0)
  * [`jumpcloud.software_apps.post`](#jumpcloudsoftware_appspost)
  * [`jumpcloud.software_apps.reclaim_licenses`](#jumpcloudsoftware_appsreclaim_licenses)
  * [`jumpcloud.software_apps.retry_installation`](#jumpcloudsoftware_appsretry_installation)
  * [`jumpcloud.software_apps.softwareapps_associations_list`](#jumpcloudsoftware_appssoftwareapps_associations_list)
  * [`jumpcloud.software_apps.softwareapps_associations_post`](#jumpcloudsoftware_appssoftwareapps_associations_post)
  * [`jumpcloud.software_apps.softwareapps_traverse_system`](#jumpcloudsoftware_appssoftwareapps_traverse_system)
  * [`jumpcloud.software_apps.softwareapps_traverse_system_group`](#jumpcloudsoftware_appssoftwareapps_traverse_system_group)
  * [`jumpcloud.software_apps.update`](#jumpcloudsoftware_appsupdate)
  * [`jumpcloud.software_apps.validate_application_install_package`](#jumpcloudsoftware_appsvalidate_application_install_package)
  * [`jumpcloud.subscriptions.get`](#jumpcloudsubscriptionsget)
  * [`jumpcloud.system_group_associations.system_group_associations_list`](#jumpcloudsystem_group_associationssystem_group_associations_list)
  * [`jumpcloud.system_group_associations.system_group_associations_post`](#jumpcloudsystem_group_associationssystem_group_associations_post)
  * [`jumpcloud.system_group_associations.system_group_traverse_command`](#jumpcloudsystem_group_associationssystem_group_traverse_command)
  * [`jumpcloud.system_group_associations.system_group_traverse_policy`](#jumpcloudsystem_group_associationssystem_group_traverse_policy)
  * [`jumpcloud.system_group_associations.system_group_traverse_policy_group`](#jumpcloudsystem_group_associationssystem_group_traverse_policy_group)
  * [`jumpcloud.system_group_associations.system_group_traverse_user`](#jumpcloudsystem_group_associationssystem_group_traverse_user)
  * [`jumpcloud.system_group_associations.system_group_traverse_user_group`](#jumpcloudsystem_group_associationssystem_group_traverse_user_group)
  * [`jumpcloud.system_group_members_&amp;_membership.system_group_members_list`](#jumpcloudsystem_group_members_amp_membershipsystem_group_members_list)
  * [`jumpcloud.system_group_members_&amp;_membership.system_group_members_post`](#jumpcloudsystem_group_members_amp_membershipsystem_group_members_post)
  * [`jumpcloud.system_group_members_&amp;_membership.system_group_membership`](#jumpcloudsystem_group_members_amp_membershipsystem_group_membership)
  * [`jumpcloud.system_groups.apply_suggestions`](#jumpcloudsystem_groupsapply_suggestions)
  * [`jumpcloud.system_groups.create_new_group`](#jumpcloudsystem_groupscreate_new_group)
  * [`jumpcloud.system_groups.delete_group`](#jumpcloudsystem_groupsdelete_group)
  * [`jumpcloud.system_groups.list_all`](#jumpcloudsystem_groupslist_all)
  * [`jumpcloud.system_groups.list_suggestions`](#jumpcloudsystem_groupslist_suggestions)
  * [`jumpcloud.system_groups.system_group_associations_list`](#jumpcloudsystem_groupssystem_group_associations_list)
  * [`jumpcloud.system_groups.system_group_associations_post`](#jumpcloudsystem_groupssystem_group_associations_post)
  * [`jumpcloud.system_groups.system_group_members_list`](#jumpcloudsystem_groupssystem_group_members_list)
  * [`jumpcloud.system_groups.system_group_members_post`](#jumpcloudsystem_groupssystem_group_members_post)
  * [`jumpcloud.system_groups.system_group_membership`](#jumpcloudsystem_groupssystem_group_membership)
  * [`jumpcloud.system_groups.system_group_traverse_policy`](#jumpcloudsystem_groupssystem_group_traverse_policy)
  * [`jumpcloud.system_groups.system_group_traverse_policy_group`](#jumpcloudsystem_groupssystem_group_traverse_policy_group)
  * [`jumpcloud.system_groups.system_group_traverse_user`](#jumpcloudsystem_groupssystem_group_traverse_user)
  * [`jumpcloud.system_groups.system_group_traverse_user_group`](#jumpcloudsystem_groupssystem_group_traverse_user_group)
  * [`jumpcloud.system_groups.update_group`](#jumpcloudsystem_groupsupdate_group)
  * [`jumpcloud.system_groups.view_details`](#jumpcloudsystem_groupsview_details)
  * [`jumpcloud.system_insights.get_chassis_info`](#jumpcloudsystem_insightsget_chassis_info)
  * [`jumpcloud.system_insights.get_disk_info`](#jumpcloudsystem_insightsget_disk_info)
  * [`jumpcloud.system_insights.get_ie_extensions_list`](#jumpcloudsystem_insightsget_ie_extensions_list)
  * [`jumpcloud.system_insights.get_kernel_info`](#jumpcloudsystem_insightsget_kernel_info)
  * [`jumpcloud.system_insights.get_os_version`](#jumpcloudsystem_insightsget_os_version)
  * [`jumpcloud.system_insights.get_sip_config`](#jumpcloudsystem_insightsget_sip_config)
  * [`jumpcloud.system_insights.get_system_info_list`](#jumpcloudsystem_insightsget_system_info_list)
  * [`jumpcloud.system_insights.get_tpm_info`](#jumpcloudsystem_insightsget_tpm_info)
  * [`jumpcloud.system_insights.get_user_groups`](#jumpcloudsystem_insightsget_user_groups)
  * [`jumpcloud.system_insights.list_alf`](#jumpcloudsystem_insightslist_alf)
  * [`jumpcloud.system_insights.list_alf_exceptions`](#jumpcloudsystem_insightslist_alf_exceptions)
  * [`jumpcloud.system_insights.list_alf_explicit_auths`](#jumpcloudsystem_insightslist_alf_explicit_auths)
  * [`jumpcloud.system_insights.list_appcompat_shims`](#jumpcloudsystem_insightslist_appcompat_shims)
  * [`jumpcloud.system_insights.list_apps`](#jumpcloudsystem_insightslist_apps)
  * [`jumpcloud.system_insights.list_authorized_keys`](#jumpcloudsystem_insightslist_authorized_keys)
  * [`jumpcloud.system_insights.list_azure_instance_metadata`](#jumpcloudsystem_insightslist_azure_instance_metadata)
  * [`jumpcloud.system_insights.list_azure_instance_tags`](#jumpcloudsystem_insightslist_azure_instance_tags)
  * [`jumpcloud.system_insights.list_battery_data`](#jumpcloudsystem_insightslist_battery_data)
  * [`jumpcloud.system_insights.list_bitlocker_info`](#jumpcloudsystem_insightslist_bitlocker_info)
  * [`jumpcloud.system_insights.list_browser_plugins`](#jumpcloudsystem_insightslist_browser_plugins)
  * [`jumpcloud.system_insights.list_certificates`](#jumpcloudsystem_insightslist_certificates)
  * [`jumpcloud.system_insights.list_chrome_extensions`](#jumpcloudsystem_insightslist_chrome_extensions)
  * [`jumpcloud.system_insights.list_connectivity`](#jumpcloudsystem_insightslist_connectivity)
  * [`jumpcloud.system_insights.list_crashes`](#jumpcloudsystem_insightslist_crashes)
  * [`jumpcloud.system_insights.list_cups_destinations`](#jumpcloudsystem_insightslist_cups_destinations)
  * [`jumpcloud.system_insights.list_disk_encryption`](#jumpcloudsystem_insightslist_disk_encryption)
  * [`jumpcloud.system_insights.list_dns_resolvers`](#jumpcloudsystem_insightslist_dns_resolvers)
  * [`jumpcloud.system_insights.list_etc_hosts`](#jumpcloudsystem_insightslist_etc_hosts)
  * [`jumpcloud.system_insights.list_firefox_addons`](#jumpcloudsystem_insightslist_firefox_addons)
  * [`jumpcloud.system_insights.list_groups`](#jumpcloudsystem_insightslist_groups)
  * [`jumpcloud.system_insights.list_interface_addresses`](#jumpcloudsystem_insightslist_interface_addresses)
  * [`jumpcloud.system_insights.list_interface_details`](#jumpcloudsystem_insightslist_interface_details)
  * [`jumpcloud.system_insights.list_launchd`](#jumpcloudsystem_insightslist_launchd)
  * [`jumpcloud.system_insights.list_linux_packages`](#jumpcloudsystem_insightslist_linux_packages)
  * [`jumpcloud.system_insights.list_logged_in_users`](#jumpcloudsystem_insightslist_logged_in_users)
  * [`jumpcloud.system_insights.list_logical_drives`](#jumpcloudsystem_insightslist_logical_drives)
  * [`jumpcloud.system_insights.list_managed_policies`](#jumpcloudsystem_insightslist_managed_policies)
  * [`jumpcloud.system_insights.list_mounts`](#jumpcloudsystem_insightslist_mounts)
  * [`jumpcloud.system_insights.list_patches`](#jumpcloudsystem_insightslist_patches)
  * [`jumpcloud.system_insights.list_programs`](#jumpcloudsystem_insightslist_programs)
  * [`jumpcloud.system_insights.list_python_packages`](#jumpcloudsystem_insightslist_python_packages)
  * [`jumpcloud.system_insights.list_safari_extensions`](#jumpcloudsystem_insightslist_safari_extensions)
  * [`jumpcloud.system_insights.list_scheduled_tasks`](#jumpcloudsystem_insightslist_scheduled_tasks)
  * [`jumpcloud.system_insights.list_secure_boot`](#jumpcloudsystem_insightslist_secure_boot)
  * [`jumpcloud.system_insights.list_services`](#jumpcloudsystem_insightslist_services)
  * [`jumpcloud.system_insights.list_shadow_data`](#jumpcloudsystem_insightslist_shadow_data)
  * [`jumpcloud.system_insights.list_shared_folders`](#jumpcloudsystem_insightslist_shared_folders)
  * [`jumpcloud.system_insights.list_shared_resources`](#jumpcloudsystem_insightslist_shared_resources)
  * [`jumpcloud.system_insights.list_sharing_preferences`](#jumpcloudsystem_insightslist_sharing_preferences)
  * [`jumpcloud.system_insights.list_startup_items`](#jumpcloudsystem_insightslist_startup_items)
  * [`jumpcloud.system_insights.list_system_controls`](#jumpcloudsystem_insightslist_system_controls)
  * [`jumpcloud.system_insights.list_uptime`](#jumpcloudsystem_insightslist_uptime)
  * [`jumpcloud.system_insights.list_usb_devices`](#jumpcloudsystem_insightslist_usb_devices)
  * [`jumpcloud.system_insights.list_user_assist`](#jumpcloudsystem_insightslist_user_assist)
  * [`jumpcloud.system_insights.list_user_ssh_keys`](#jumpcloudsystem_insightslist_user_ssh_keys)
  * [`jumpcloud.system_insights.list_users`](#jumpcloudsystem_insightslist_users)
  * [`jumpcloud.system_insights.list_wifi_networks`](#jumpcloudsystem_insightslist_wifi_networks)
  * [`jumpcloud.system_insights.list_wifi_status`](#jumpcloudsystem_insightslist_wifi_status)
  * [`jumpcloud.system_insights.list_windows_security_center`](#jumpcloudsystem_insightslist_windows_security_center)
  * [`jumpcloud.system_insights.list_windows_security_products`](#jumpcloudsystem_insightslist_windows_security_products)
  * [`jumpcloud.systems.get_fde_key`](#jumpcloudsystemsget_fde_key)
  * [`jumpcloud.systems.list_software_apps_with_statuses`](#jumpcloudsystemslist_software_apps_with_statuses)
  * [`jumpcloud.systems.system_associations_list`](#jumpcloudsystemssystem_associations_list)
  * [`jumpcloud.systems.system_associations_post`](#jumpcloudsystemssystem_associations_post)
  * [`jumpcloud.systems.system_member_of`](#jumpcloudsystemssystem_member_of)
  * [`jumpcloud.systems.system_traverse_command`](#jumpcloudsystemssystem_traverse_command)
  * [`jumpcloud.systems.system_traverse_policy`](#jumpcloudsystemssystem_traverse_policy)
  * [`jumpcloud.systems.system_traverse_policy_group`](#jumpcloudsystemssystem_traverse_policy_group)
  * [`jumpcloud.systems.system_traverse_user`](#jumpcloudsystemssystem_traverse_user)
  * [`jumpcloud.systems.system_traverse_user_group`](#jumpcloudsystemssystem_traverse_user_group)
  * [`jumpcloud.systems_organization_settings.get_default_password_sync_settings`](#jumpcloudsystems_organization_settingsget_default_password_sync_settings)
  * [`jumpcloud.systems_organization_settings.get_sign_in_with_jump_cloud_settings`](#jumpcloudsystems_organization_settingsget_sign_in_with_jump_cloud_settings)
  * [`jumpcloud.systems_organization_settings.set_default_password_sync_settings`](#jumpcloudsystems_organization_settingsset_default_password_sync_settings)
  * [`jumpcloud.systems_organization_settings.set_sign_in_with_jump_cloud_settings`](#jumpcloudsystems_organization_settingsset_sign_in_with_jump_cloud_settings)
  * [`jumpcloud.user_group_associations.user_group_associations_list`](#jumpclouduser_group_associationsuser_group_associations_list)
  * [`jumpcloud.user_group_associations.user_group_associations_post`](#jumpclouduser_group_associationsuser_group_associations_post)
  * [`jumpcloud.user_group_associations.user_group_traverse_active_directory`](#jumpclouduser_group_associationsuser_group_traverse_active_directory)
  * [`jumpcloud.user_group_associations.user_group_traverse_application`](#jumpclouduser_group_associationsuser_group_traverse_application)
  * [`jumpcloud.user_group_associations.user_group_traverse_directory`](#jumpclouduser_group_associationsuser_group_traverse_directory)
  * [`jumpcloud.user_group_associations.user_group_traverse_g_suite`](#jumpclouduser_group_associationsuser_group_traverse_g_suite)
  * [`jumpcloud.user_group_associations.user_group_traverse_ldap_server`](#jumpclouduser_group_associationsuser_group_traverse_ldap_server)
  * [`jumpcloud.user_group_associations.user_group_traverse_office365`](#jumpclouduser_group_associationsuser_group_traverse_office365)
  * [`jumpcloud.user_group_associations.user_group_traverse_radius_server`](#jumpclouduser_group_associationsuser_group_traverse_radius_server)
  * [`jumpcloud.user_group_associations.user_group_traverse_system`](#jumpclouduser_group_associationsuser_group_traverse_system)
  * [`jumpcloud.user_group_associations.user_group_traverse_system_group`](#jumpclouduser_group_associationsuser_group_traverse_system_group)
  * [`jumpcloud.user_group_members_&amp;_membership.user_group_members_list`](#jumpclouduser_group_members_amp_membershipuser_group_members_list)
  * [`jumpcloud.user_group_members_&amp;_membership.user_group_members_post`](#jumpclouduser_group_members_amp_membershipuser_group_members_post)
  * [`jumpcloud.user_group_members_&amp;_membership.user_group_membership`](#jumpclouduser_group_members_amp_membershipuser_group_membership)
  * [`jumpcloud.user_groups.apply_suggestions`](#jumpclouduser_groupsapply_suggestions)
  * [`jumpcloud.user_groups.create_new_group`](#jumpclouduser_groupscreate_new_group)
  * [`jumpcloud.user_groups.delete_group`](#jumpclouduser_groupsdelete_group)
  * [`jumpcloud.user_groups.get_details`](#jumpclouduser_groupsget_details)
  * [`jumpcloud.user_groups.get_suggestions`](#jumpclouduser_groupsget_suggestions)
  * [`jumpcloud.user_groups.list_all`](#jumpclouduser_groupslist_all)
  * [`jumpcloud.user_groups.update_group`](#jumpclouduser_groupsupdate_group)
  * [`jumpcloud.user_groups.user_group_associations_list`](#jumpclouduser_groupsuser_group_associations_list)
  * [`jumpcloud.user_groups.user_group_associations_post`](#jumpclouduser_groupsuser_group_associations_post)
  * [`jumpcloud.user_groups.user_group_members_list`](#jumpclouduser_groupsuser_group_members_list)
  * [`jumpcloud.user_groups.user_group_members_post`](#jumpclouduser_groupsuser_group_members_post)
  * [`jumpcloud.user_groups.user_group_membership`](#jumpclouduser_groupsuser_group_membership)
  * [`jumpcloud.user_groups.user_group_traverse_active_directory`](#jumpclouduser_groupsuser_group_traverse_active_directory)
  * [`jumpcloud.user_groups.user_group_traverse_application`](#jumpclouduser_groupsuser_group_traverse_application)
  * [`jumpcloud.user_groups.user_group_traverse_directory`](#jumpclouduser_groupsuser_group_traverse_directory)
  * [`jumpcloud.user_groups.user_group_traverse_g_suite`](#jumpclouduser_groupsuser_group_traverse_g_suite)
  * [`jumpcloud.user_groups.user_group_traverse_ldap_server`](#jumpclouduser_groupsuser_group_traverse_ldap_server)
  * [`jumpcloud.user_groups.user_group_traverse_office365`](#jumpclouduser_groupsuser_group_traverse_office365)
  * [`jumpcloud.user_groups.user_group_traverse_radius_server`](#jumpclouduser_groupsuser_group_traverse_radius_server)
  * [`jumpcloud.user_groups.user_group_traverse_system`](#jumpclouduser_groupsuser_group_traverse_system)
  * [`jumpcloud.user_groups.user_group_traverse_system_group`](#jumpclouduser_groupsuser_group_traverse_system_group)
  * [`jumpcloud.users.delete`](#jumpcloudusersdelete)
  * [`jumpcloud.users.get`](#jumpcloudusersget)
  * [`jumpcloud.users.list`](#jumpclouduserslist)
  * [`jumpcloud.users.patch`](#jumpclouduserspatch)
  * [`jumpcloud.users.user_associations_list`](#jumpcloudusersuser_associations_list)
  * [`jumpcloud.users.user_associations_post`](#jumpcloudusersuser_associations_post)
  * [`jumpcloud.users.user_member_of`](#jumpcloudusersuser_member_of)
  * [`jumpcloud.users.user_traverse_active_directory`](#jumpcloudusersuser_traverse_active_directory)
  * [`jumpcloud.users.user_traverse_application`](#jumpcloudusersuser_traverse_application)
  * [`jumpcloud.users.user_traverse_directory`](#jumpcloudusersuser_traverse_directory)
  * [`jumpcloud.users.user_traverse_g_suite`](#jumpcloudusersuser_traverse_g_suite)
  * [`jumpcloud.users.user_traverse_ldap_server`](#jumpcloudusersuser_traverse_ldap_server)
  * [`jumpcloud.users.user_traverse_office365`](#jumpcloudusersuser_traverse_office365)
  * [`jumpcloud.users.user_traverse_radius_server`](#jumpcloudusersuser_traverse_radius_server)
  * [`jumpcloud.users.user_traverse_system`](#jumpcloudusersuser_traverse_system)
  * [`jumpcloud.users.user_traverse_system_group`](#jumpcloudusersuser_traverse_system_group)
  * [`jumpcloud.workday_import.authorize`](#jumpcloudworkday_importauthorize)
  * [`jumpcloud.workday_import.deauthorize`](#jumpcloudworkday_importdeauthorize)
  * [`jumpcloud.workday_import.get`](#jumpcloudworkday_importget)
  * [`jumpcloud.workday_import.import`](#jumpcloudworkday_importimport)
  * [`jumpcloud.workday_import.importresults`](#jumpcloudworkday_importimportresults)
  * [`jumpcloud.workday_import.list`](#jumpcloudworkday_importlist)
  * [`jumpcloud.workday_import.post`](#jumpcloudworkday_importpost)
  * [`jumpcloud.workday_import.put`](#jumpcloudworkday_importput)
  * [`jumpcloud.workday_import.workers`](#jumpcloudworkday_importworkers)
  * [`jumpcloud.fde.get_fde_key`](#jumpcloudfdeget_fde_key)

<!-- tocstop -->

## Requirements<a id="requirements"></a>

Python >=3.7

## Installation<a id="installation"></a>
<div align="center">
  <a href="https://konfigthis.com/sdk-sign-up?company=JumpCloud&language=Python">
    <img src="https://raw.githubusercontent.com/konfig-dev/brand-assets/HEAD/cta-images/python-cta.png" width="70%">
  </a>
</div>

## Getting Started<a id="getting-started"></a>

```python
from pprint import pprint
from jump_cloud_python_sdk import JumpCloud, ApiException

jumpcloud = JumpCloud(

        x_api_key = 'YOUR_API_KEY',
)

try:
    # List the associations of an Active Directory instance
    active_directory_associations_list_response = jumpcloud.active_directory.active_directory_associations_list(
        activedirectory_id="activedirectory_id_example",
        targets=[
        "user"
    ],
        limit=10,
        skip=0,
        x_org_id="string_example",
    )
    print(active_directory_associations_list_response)
except ApiException as e:
    print("Exception when calling ActiveDirectoryApi.active_directory_associations_list: %s\n" % e)
    pprint(e.body)
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```

## Async<a id="async"></a>

`async` support is available by prepending `a` to any method.

```python

import asyncio
from pprint import pprint
from jump_cloud_python_sdk import JumpCloud, ApiException

jumpcloud = JumpCloud(

        x_api_key = 'YOUR_API_KEY',
)

async def main():
    try:
        # List the associations of an Active Directory instance
        active_directory_associations_list_response = await jumpcloud.active_directory.aactive_directory_associations_list(
            activedirectory_id="activedirectory_id_example",
            targets=[
        "user"
    ],
            limit=10,
            skip=0,
            x_org_id="string_example",
        )
        print(active_directory_associations_list_response)
    except ApiException as e:
        print("Exception when calling ActiveDirectoryApi.active_directory_associations_list: %s\n" % e)
        pprint(e.body)
        pprint(e.headers)
        pprint(e.status)
        pprint(e.reason)
        pprint(e.round_trip_time)

asyncio.run(main())
```

## Raw HTTP Response<a id="raw-http-response"></a>

To access raw HTTP response values, use the `.raw` namespace.

```python
from pprint import pprint
from jump_cloud_python_sdk import JumpCloud, ApiException

jumpcloud = JumpCloud(

        x_api_key = 'YOUR_API_KEY',
)

try:
    # List the associations of an Active Directory instance
    active_directory_associations_list_response = jumpcloud.active_directory.raw.active_directory_associations_list(
        activedirectory_id="activedirectory_id_example",
        targets=[
        "user"
    ],
        limit=10,
        skip=0,
        x_org_id="string_example",
    )
    pprint(active_directory_associations_list_response.body)
    pprint(active_directory_associations_list_response.headers)
    pprint(active_directory_associations_list_response.status)
    pprint(active_directory_associations_list_response.round_trip_time)
except ApiException as e:
    print("Exception when calling ActiveDirectoryApi.active_directory_associations_list: %s\n" % e)
    pprint(e.body)
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```


## Reference<a id="reference"></a>
### `jumpcloud.active_directory.active_directory_associations_list`<a id="jumpcloudactive_directoryactive_directory_associations_list"></a>

This endpoint returns the direct associations of this Active Directory instance.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Active Directory and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET 'https://console.jumpcloud.com/api/v2/activedirectories/{ActiveDirectory_ID}/associations?targets=user \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
active_directory_associations_list_response = jumpcloud.active_directory.active_directory_associations_list(
    activedirectory_id="activedirectory_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"active_directory\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphActiveDirectoryAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_active_directory_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.active_directory_associations_post`<a id="jumpcloudactive_directoryactive_directory_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of an Active Directory instance.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Active Directory and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/activedirectories/{AD_Instance_ID}/associations \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user",
    "id": "{User_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.active_directory.active_directory_associations_post(
    activedirectory_id="activedirectory_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"active_directory\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationActiveDirectory`](./jump_cloud_python_sdk/type/graph_operation_active_directory.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.active_directory_traverse_user`<a id="jumpcloudactive_directoryactive_directory_traverse_user"></a>

This endpoint will return all Users bound to an Active Directory instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Active Directory instance to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this Active Directory instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/activedirectories/{ActiveDirectory_ID}/users \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
active_directory_traverse_user_response = jumpcloud.active_directory.active_directory_traverse_user(
    activedirectory_id="activedirectory_id_example",
    filter=[],
    limit=10,
    x_org_id="string_example",
    skip=0,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

ObjectID of the Active Directory instance.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphActiveDirectoryTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_active_directory_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.active_directory_traverse_user_group`<a id="jumpcloudactive_directoryactive_directory_traverse_user_group"></a>

This endpoint will return all Users Groups bound to an Active Directory instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Active Directory instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this Active Directory instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/activedirectories/{ActiveDirectory_ID}/usergroups \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
active_directory_traverse_user_group_response = jumpcloud.active_directory.active_directory_traverse_user_group(
    activedirectory_id="activedirectory_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

ObjectID of the Active Directory instance.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphActiveDirectoryTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_active_directory_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.agents_delete`<a id="jumpcloudactive_directoryagents_delete"></a>

This endpoint deletes an Active Directory agent.

#### Sample Request<a id="sample-request"></a>
```
curl -X DELETE https://console.jumpcloud.com/api/v2/activedirectories/{activedirectory_id}/agents/{agent_id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.active_directory.agents_delete(
    activedirectory_id="activedirectory_id_example",
    agent_id="agent_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

##### agent_id: `str`<a id="agent_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/agents/{agent_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.agents_get`<a id="jumpcloudactive_directoryagents_get"></a>

This endpoint returns an Active Directory agent.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/activedirectories/{activedirectory_id}/agents/{agent_id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
agents_get_response = jumpcloud.active_directory.agents_get(
    activedirectory_id="activedirectory_id_example",
    agent_id="agent_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

##### agent_id: `str`<a id="agent_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`ActiveDirectoryAgentList`](./jump_cloud_python_sdk/pydantic/active_directory_agent_list.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/agents/{agent_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.agents_list`<a id="jumpcloudactive_directoryagents_list"></a>

This endpoint allows you to list all your Active Directory Agents for a given Instance.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/activedirectories/{activedirectory_id}/agents \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
agents_list_response = jumpcloud.active_directory.agents_list(
    activedirectory_id="activedirectory_id_example",
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`ActivedirectoriesAgentsListResponse`](./jump_cloud_python_sdk/pydantic/activedirectories_agents_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/agents` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.agents_post`<a id="jumpcloudactive_directoryagents_post"></a>

This endpoint allows you to create a new Active Directory Agent.


#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/activedirectories/{activedirectory_id}/agents \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{ "agent_type":"{SYNC}" }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
agents_post_response = jumpcloud.active_directory.agents_post(
    activedirectory_id="activedirectory_id_example",
    agent_type="SYNC",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

##### agent_type: `str`<a id="agent_type-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ActiveDirectoryAgent`](./jump_cloud_python_sdk/type/active_directory_agent.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ActiveDirectoryAgentGet`](./jump_cloud_python_sdk/pydantic/active_directory_agent_get.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/agents` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.delete`<a id="jumpcloudactive_directorydelete"></a>

This endpoint allows you to delete an Active Directory Instance.

#### Sample Request<a id="sample-request"></a>
```
curl -X DELETE https://console.jumpcloud.com/api/v2/activedirectories/{ActiveDirectory_ID} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
delete_response = jumpcloud.active_directory.delete(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

ObjectID of this Active Directory instance.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`ActiveDirectory`](./jump_cloud_python_sdk/pydantic/active_directory.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.get`<a id="jumpcloudactive_directoryget"></a>

This endpoint returns a specific Active Directory.

#### Sample Request<a id="sample-request"></a>

```
curl -X GET https://console.jumpcloud.com/api/v2/activedirectories/{ActiveDirectory_ID} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = jumpcloud.active_directory.get(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

ObjectID of this Active Directory instance.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`ActiveDirectory`](./jump_cloud_python_sdk/pydantic/active_directory.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.list`<a id="jumpcloudactive_directorylist"></a>

This endpoint allows you to list all your Active Directory Instances.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/activedirectories/ \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = jumpcloud.active_directory.list(
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### fields: List[`str`]<a id="fields-liststr"></a>

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`ActivedirectoriesListResponse`](./jump_cloud_python_sdk/pydantic/activedirectories_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.patch`<a id="jumpcloudactive_directorypatch"></a>

This endpoint allows you to update Active Directory.

- AD as Authority - password in AD - 2-way sync use case is selected.
- JC as Authority - one-way sync from AD.
- Two way sync -  2-way sync use case is selected


#### Sample Request<a id="sample-request"></a>
```
curl -X PATCH https://console.jumpcloud.com/api/v2/activedirectories/{Domain_ID} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
        "domain": "{DC=DOMAIN;DC=COM}",
        "use_case": "{ADASAUTHORITY}"
    }' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
patch_response = jumpcloud.active_directory.patch(
    id="id_example",
    domain="string_example",
    id="string_example",
    primary_agent="string_example",
    use_case="UNSET",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

ObjectID of this Active Directory instance.

##### domain: `str`<a id="domain-str"></a>

Domain name for this Active Directory instance.

##### id: `str`<a id="id-str"></a>

ObjectID of this Active Directory instance.

##### primary_agent: `str`<a id="primary_agent-str"></a>

ObjectID of the primary agent of domain.

##### use_case: `str`<a id="use_case-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ActiveDirectory`](./jump_cloud_python_sdk/type/active_directory.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ActiveDirectory`](./jump_cloud_python_sdk/pydantic/active_directory.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.active_directory.post`<a id="jumpcloudactive_directorypost"></a>

This endpoint allows you to create a new Active Directory.


#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/activedirectories/ \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "domain": "{DC=AD_domain_name;DC=com}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
post_response = jumpcloud.active_directory.post(
    domain="string_example",
    id="string_example",
    primary_agent="string_example",
    use_case="UNSET",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### domain: `str`<a id="domain-str"></a>

Domain name for this Active Directory instance.

##### id: `str`<a id="id-str"></a>

ObjectID of this Active Directory instance.

##### primary_agent: `str`<a id="primary_agent-str"></a>

ObjectID of the primary agent of domain.

##### use_case: `str`<a id="use_case-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ActiveDirectory`](./jump_cloud_python_sdk/type/active_directory.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ActiveDirectory`](./jump_cloud_python_sdk/pydantic/active_directory.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.administrators.create_by_administrator`<a id="jumpcloudadministratorscreate_by_administrator"></a>

This endpoint allows you to grant Administrator access to an Organization.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_by_administrator_response = jumpcloud.administrators.create_by_administrator(
    id="id_example",
    organization="6230a0d26a4e4bc86c6b36f1",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### organization: `str`<a id="organization-str"></a>

The identifier for an organization to link this administrator to.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AdministratorOrganizationLinkReq`](./jump_cloud_python_sdk/type/administrator_organization_link_req.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AdministratorOrganizationLink`](./jump_cloud_python_sdk/pydantic/administrator_organization_link.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/administrators/{id}/organizationlinks` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.administrators.list_by_administrator`<a id="jumpcloudadministratorslist_by_administrator"></a>

This endpoint returns the association links between an Administrator and Organizations.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_by_administrator_response = jumpcloud.administrators.list_by_administrator(
    id="id_example",
    limit=10,
    skip=0,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

#### 🔄 Return<a id="🔄-return"></a>

[`AdministratorOrganizationsListByAdministratorResponse`](./jump_cloud_python_sdk/pydantic/administrator_organizations_list_by_administrator_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/administrators/{id}/organizationlinks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.administrators.list_by_organization`<a id="jumpcloudadministratorslist_by_organization"></a>

This endpoint returns the association links between an Organization and Administrators.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_by_organization_response = jumpcloud.administrators.list_by_organization(
    id="id_example",
    limit=10,
    skip=0,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

#### 🔄 Return<a id="🔄-return"></a>

[`AdministratorOrganizationsListByOrganizationResponse`](./jump_cloud_python_sdk/pydantic/administrator_organizations_list_by_organization_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/organizations/{id}/administratorlinks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.administrators.remove_by_administrator`<a id="jumpcloudadministratorsremove_by_administrator"></a>

This endpoint removes the association link between an Administrator and an Organization.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.administrators.remove_by_administrator(
    administrator_id="administrator_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### administrator_id: `str`<a id="administrator_id-str"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/administrators/{administrator_id}/organizationlinks/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.aggregated_policy_stats.get`<a id="jumpcloudaggregated_policy_statsget"></a>

Gets the aggregated policy stats for a system.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{system_object_id}/aggregated-policy-stats \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key:{API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = jumpcloud.aggregated_policy_stats.get(
    system_object_id='YQ==',
    organization_object_id='YQ==',
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### system_object_id: `str`<a id="system_object_id-str"></a>

##### organization_object_id: `str`<a id="organization_object_id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`DevicesAggregatedPolicyResultResponse`](./jump_cloud_python_sdk/pydantic/devices_aggregated_policy_result_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systems/{systemObjectId}/aggregated-policy-stats` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.csrget`<a id="jumpcloudapple_mdmcsrget"></a>

Retrieves an Apple MDM signed CSR Plist for an organization.  The user must supply the returned plist to Apple for signing, and then provide the certificate provided by Apple back into the PUT API.

#### Sample Request<a id="sample-request"></a>
```
  curl -X GET https://console.jumpcloud.com/api/v2/applemdms/{APPLE_MDM_ID}/csr \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
csrget_response = jumpcloud.apple_mdm.csrget(
    apple_mdm_id="apple_mdm_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/csr` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.delete`<a id="jumpcloudapple_mdmdelete"></a>

Removes an Apple MDM configuration.

Warning: This is a destructive operation and will remove your Apple Push Certificates.  We will no longer be able to manage your devices and the only recovery option is to re-register all devices into MDM.

#### Sample Request<a id="sample-request"></a>
```
curl -X DELETE https://console.jumpcloud.com/api/v2/applemdms/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
delete_response = jumpcloud.apple_mdm.delete(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`AppleMDM`](./jump_cloud_python_sdk/pydantic/apple_mdm.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.deletedevice`<a id="jumpcloudapple_mdmdeletedevice"></a>

Remove a single Apple MDM device from MDM enrollment.

#### Sample Request<a id="sample-request"></a>
```
  curl -X DELETE https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/devices/{device_id} \
  -H 'accept: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
deletedevice_response = jumpcloud.apple_mdm.deletedevice(
    apple_mdm_id="apple_mdm_id_example",
    device_id="device_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### device_id: `str`<a id="device_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`AppleMdmDevice`](./jump_cloud_python_sdk/pydantic/apple_mdm_device.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/devices/{device_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.depkeyget`<a id="jumpcloudapple_mdmdepkeyget"></a>

Retrieves an Apple MDM DEP Public Key.

#### Sample Request<a id="sample-request"></a>

```
curl https://console.jumpcloud.com/api/v2/applemdms/{APPLE_MDM_ID}/depkey \
  -H 'accept: application/x-pem-file' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
depkeyget_response = jumpcloud.apple_mdm.depkeyget(
    apple_mdm_id="apple_mdm_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/depkey` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.devices_clear_activation_lock`<a id="jumpcloudapple_mdmdevices_clear_activation_lock"></a>

Clears the activation lock on the specified device.

#### Sample Request<a id="sample-request"></a>
```
  curl -X POST https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/devices/{device_id}/clearActivationLock \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.apple_mdm.devices_clear_activation_lock(
    apple_mdm_id="apple_mdm_id_example",
    device_id="device_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### device_id: `str`<a id="device_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/devices/{device_id}/clearActivationLock` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.devices_os_update_status`<a id="jumpcloudapple_mdmdevices_os_update_status"></a>

Pass through to request the status of an OS update
#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/devices/{device_id}/osUpdateStatus \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.apple_mdm.devices_os_update_status(
    apple_mdm_id="apple_mdm_id_example",
    device_id="device_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### device_id: `str`<a id="device_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/devices/{device_id}/osUpdateStatus` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.devices_refresh_activation_lock_information`<a id="jumpcloudapple_mdmdevices_refresh_activation_lock_information"></a>

Refreshes the activation lock information for a device

#### Sample Request<a id="sample-request"></a>

```
curl -X POST https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/devices/{device_id}/refreshActivationLockInformation \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.apple_mdm.devices_refresh_activation_lock_information(
    apple_mdm_id="apple_mdm_id_example",
    device_id="device_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### device_id: `str`<a id="device_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/devices/{device_id}/refreshActivationLockInformation` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.devices_schedule_os_update`<a id="jumpcloudapple_mdmdevices_schedule_os_update"></a>

Schedules an OS update for a device

#### Sample Request<a id="sample-request"></a>

```
curl -X POST https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/devices/{device_id}/scheduleOSUpdate \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{"install_action": "INSTALL_ASAP", "product_key": "key"}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.apple_mdm.devices_schedule_os_update(
    install_action="DOWNLOAD_ONLY",
    product_key="string_example",
    apple_mdm_id="apple_mdm_id_example",
    device_id="device_id_example",
    max_user_deferrals=1,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### install_action: [`InstallActionType`](./jump_cloud_python_sdk/type/install_action_type.py)<a id="install_action-installactiontypejump_cloud_python_sdktypeinstall_action_typepy"></a>

##### product_key: `str`<a id="product_key-str"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### device_id: `str`<a id="device_id-str"></a>

##### max_user_deferrals: `int`<a id="max_user_deferrals-int"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ScheduleOSUpdate`](./jump_cloud_python_sdk/type/schedule_os_update.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/devices/{device_id}/scheduleOSUpdate` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.deviceserase`<a id="jumpcloudapple_mdmdeviceserase"></a>

Erases a DEP-enrolled device.

#### Sample Request<a id="sample-request"></a>
```
  curl -X POST https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/devices/{device_id}/erase \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.apple_mdm.deviceserase(
    apple_mdm_id="apple_mdm_id_example",
    device_id="device_id_example",
    pin="123456",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### device_id: `str`<a id="device_id-str"></a>

##### pin: `str`<a id="pin-str"></a>

6-digit PIN, required for MacOS, to erase the device

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ApplemdmsDeviceseraseRequest`](./jump_cloud_python_sdk/type/applemdms_deviceserase_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/devices/{device_id}/erase` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.deviceslist`<a id="jumpcloudapple_mdmdeviceslist"></a>

Lists all Apple MDM devices.

The filter and sort queries will allow the following fields:
`createdAt`
`depRegistered`
`enrolled`
`id`
`osVersion`
`serialNumber`
`udid`

#### Sample Request<a id="sample-request"></a>
```
  curl -X GET https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/devices \
  -H 'accept: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
deviceslist_response = jumpcloud.apple_mdm.deviceslist(
    apple_mdm_id="apple_mdm_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
    sort=[],
    x_total_count=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_total_count: `int`<a id="x_total_count-int"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ApplemdmsDeviceslistResponse`](./jump_cloud_python_sdk/pydantic/applemdms_deviceslist_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/devices` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.deviceslock`<a id="jumpcloudapple_mdmdeviceslock"></a>

Locks a DEP-enrolled device.

#### Sample Request<a id="sample-request"></a>
```
  curl -X POST https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/devices/{device_id}/lock \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.apple_mdm.deviceslock(
    apple_mdm_id="apple_mdm_id_example",
    device_id="device_id_example",
    pin="123456",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### device_id: `str`<a id="device_id-str"></a>

##### pin: `str`<a id="pin-str"></a>

6-digit PIN, required for MacOS, to lock the device

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ApplemdmsDeviceslockRequest`](./jump_cloud_python_sdk/type/applemdms_deviceslock_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/devices/{device_id}/lock` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.devicesrestart`<a id="jumpcloudapple_mdmdevicesrestart"></a>

Restarts a DEP-enrolled device.

#### Sample Request<a id="sample-request"></a>
```
  curl -X POST https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/devices/{device_id}/restart \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{"kextPaths": ["Path1", "Path2"]}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.apple_mdm.devicesrestart(
    apple_mdm_id="apple_mdm_id_example",
    device_id="device_id_example",
    kext_paths=[
        "string_example"
    ],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### device_id: `str`<a id="device_id-str"></a>

##### kext_paths: [`ApplemdmsDevicesrestartRequestKextPaths`](./jump_cloud_python_sdk/type/applemdms_devicesrestart_request_kext_paths.py)<a id="kext_paths-applemdmsdevicesrestartrequestkextpathsjump_cloud_python_sdktypeapplemdms_devicesrestart_request_kext_pathspy"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ApplemdmsDevicesrestartRequest`](./jump_cloud_python_sdk/type/applemdms_devicesrestart_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/devices/{device_id}/restart` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.devicesshutdown`<a id="jumpcloudapple_mdmdevicesshutdown"></a>

Shuts down a DEP-enrolled device.

#### Sample Request<a id="sample-request"></a>
```
  curl -X POST https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/devices/{device_id}/shutdown \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.apple_mdm.devicesshutdown(
    apple_mdm_id="apple_mdm_id_example",
    device_id="device_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### device_id: `str`<a id="device_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/devices/{device_id}/shutdown` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.enrollmentprofilesget`<a id="jumpcloudapple_mdmenrollmentprofilesget"></a>

Get an enrollment profile

Currently only requesting the mobileconfig is supported.

#### Sample Request<a id="sample-request"></a>

```
curl https://console.jumpcloud.com/api/v2/applemdms/{APPLE_MDM_ID}/enrollmentprofiles/{ID} \
  -H 'accept: application/x-apple-aspen-config' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
enrollmentprofilesget_response = jumpcloud.apple_mdm.enrollmentprofilesget(
    apple_mdm_id="apple_mdm_id_example",
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### id: `str`<a id="id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/enrollmentprofiles/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.enrollmentprofileslist`<a id="jumpcloudapple_mdmenrollmentprofileslist"></a>

Get a list of enrollment profiles for an apple mdm.

Note: currently only one enrollment profile is supported.

#### Sample Request<a id="sample-request"></a>
```
 curl https://console.jumpcloud.com/api/v2/applemdms/{APPLE_MDM_ID}/enrollmentprofiles \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
enrollmentprofileslist_response = jumpcloud.apple_mdm.enrollmentprofileslist(
    apple_mdm_id="apple_mdm_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`ApplemdmsEnrollmentprofileslistResponse`](./jump_cloud_python_sdk/pydantic/applemdms_enrollmentprofileslist_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/enrollmentprofiles` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.getdevice`<a id="jumpcloudapple_mdmgetdevice"></a>

Gets a single Apple MDM device.

#### Sample Request<a id="sample-request"></a>
```
  curl -X GET https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/devices/{device_id} \
  -H 'accept: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
getdevice_response = jumpcloud.apple_mdm.getdevice(
    apple_mdm_id="apple_mdm_id_example",
    device_id="device_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### device_id: `str`<a id="device_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`AppleMdmDevice`](./jump_cloud_python_sdk/pydantic/apple_mdm_device.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/devices/{device_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.list`<a id="jumpcloudapple_mdmlist"></a>

Get a list of all Apple MDM configurations.  An empty topic indicates that a signed certificate from Apple has not been provided to the PUT endpoint yet.

Note: currently only one MDM configuration per organization is supported.

#### Sample Request<a id="sample-request"></a>
```
curl https://console.jumpcloud.com/api/v2/applemdms \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = jumpcloud.apple_mdm.list(
    x_org_id="string_example",
    limit=1,
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### limit: `int`<a id="limit-int"></a>

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`ApplemdmsListResponse`](./jump_cloud_python_sdk/pydantic/applemdms_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.put`<a id="jumpcloudapple_mdmput"></a>

Updates an Apple MDM configuration.  This endpoint is used to supply JumpCloud with a signed certificate from Apple in order to finalize the setup and allow JumpCloud to manage your devices.  It may also be used to update the DEP Settings.

#### Sample Request<a id="sample-request"></a>
```
  curl -X PUT https://console.jumpcloud.com/api/v2/applemdms/{ID} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "MDM name",
    "appleSignedCert": "{CERTIFICATE}",
    "encryptedDepServerToken": "{SERVER_TOKEN}",
    "dep": {
      "welcomeScreen": {
        "title": "Welcome",
        "paragraph": "In just a few steps, you will be working securely from your Mac.",
        "button": "continue",
      },
    },
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
put_response = jumpcloud.apple_mdm.put(
    id="id_example",
    ades={
    },
    allow_mobile_user_enrollment=True,
    apple_cert_creator_apple_id="string_example",
    apple_signed_cert="string_example",
    default_ios_user_enrollment_device_group_id="string_example",
    default_system_group_id="string_example",
    dep={
    },
    encrypted_dep_server_token="string_example",
    name="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### ades: [`ADES`](./jump_cloud_python_sdk/type/ades.py)<a id="ades-adesjump_cloud_python_sdktypeadespy"></a>


##### allow_mobile_user_enrollment: `bool`<a id="allow_mobile_user_enrollment-bool"></a>

A toggle to allow mobile device enrollment for an organization.

##### apple_cert_creator_apple_id: `str`<a id="apple_cert_creator_apple_id-str"></a>

The Apple ID of the admin who created the Apple signed certificate.

##### apple_signed_cert: `str`<a id="apple_signed_cert-str"></a>

A signed certificate obtained from Apple after providing Apple with the plist file provided on POST.

##### default_ios_user_enrollment_device_group_id: `str`<a id="default_ios_user_enrollment_device_group_id-str"></a>

ObjectId uniquely identifying the MDM default iOS user enrollment device group.

##### default_system_group_id: `str`<a id="default_system_group_id-str"></a>

ObjectId uniquely identifying the MDM default System Group.

##### dep: [`DEP`](./jump_cloud_python_sdk/type/dep.py)<a id="dep-depjump_cloud_python_sdktypedeppy"></a>


##### encrypted_dep_server_token: `str`<a id="encrypted_dep_server_token-str"></a>

The S/MIME encoded DEP Server Token returned by Apple Business Manager when creating an MDM instance.

##### name: `str`<a id="name-str"></a>

A new name for the Apple MDM configuration.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AppleMdmPatch`](./jump_cloud_python_sdk/type/apple_mdm_patch.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AppleMDM`](./jump_cloud_python_sdk/pydantic/apple_mdm.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.apple_mdm.refreshdepdevices`<a id="jumpcloudapple_mdmrefreshdepdevices"></a>

Refreshes the list of devices that a JumpCloud admin has added to their virtual MDM in Apple Business Manager - ABM so that they can be DEP enrolled with JumpCloud.

#### Sample Request<a id="sample-request"></a>
```
  curl -X POST https://console.jumpcloud.com/api/v2/applemdms/{apple_mdm_id}/refreshdepdevices \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.apple_mdm.refreshdepdevices(
    apple_mdm_id="apple_mdm_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### apple_mdm_id: `str`<a id="apple_mdm_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applemdms/{apple_mdm_id}/refreshdepdevices` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.applications.application_associations_list`<a id="jumpcloudapplicationsapplication_associations_list"></a>

This endpoint will return the _direct_ associations of an Application. A direct association can be a non-homogeneous relationship between 2 different objects, for example Applications and User Groups.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET 'https://console.jumpcloud.com/api/v2/applications/{Application_ID}/associations?targets=user_group \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
application_associations_list_response = jumpcloud.applications.application_associations_list(
    application_id="application_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

ObjectID of the Application.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"application\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphApplicationAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_application_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.applications.application_associations_post`<a id="jumpcloudapplicationsapplication_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of an Application. A direct association can be a non-homogeneous relationship between 2 different objects, for example Application and User Groups.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST 'https://console.jumpcloud.com/api/v2/applications/{Application_ID}/associations' \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user_group",
    "id": "{Group_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.applications.application_associations_post(
    application_id="application_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

ObjectID of the Application.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"application\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationApplication`](./jump_cloud_python_sdk/type/graph_operation_application.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.applications.application_traverse_user`<a id="jumpcloudapplicationsapplication_traverse_user"></a>

This endpoint will return all Users bound to an Application, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Application to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this Application.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/applications/{Application_ID}/users \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
application_traverse_user_response = jumpcloud.applications.application_traverse_user(
    application_id="application_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

ObjectID of the Application.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphApplicationTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_application_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.applications.application_traverse_user_group`<a id="jumpcloudapplicationsapplication_traverse_user_group"></a>

This endpoint will return all Users Groups bound to an Application, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates  each path from this Application to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this Application.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/applications/{Application_ID}/usergroups \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
application_traverse_user_group_response = jumpcloud.applications.application_traverse_user_group(
    application_id="application_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

ObjectID of the Application.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphApplicationTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_application_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.applications.create`<a id="jumpcloudapplicationscreate"></a>

This endpoint allows you to create a user import job that will import new users and/or update existing users in JumpCloud from the application.  The endpoint can currently only be used for applications that have an active Identity Management custom API integration.  The request will  fail with a “Not found” error for applications if that type of integration is not configured.  To learn more about configuring this type of integration, read [Import users from an external identity source using a custom API integration](https://support.jumpcloud.com/support/s/article/Import-users-from-a-custom-rest-API-integration).
#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/applications/{application_id}/import/jobs \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'x-api-key: {API_KEY}' \
-H 'x-org-id: {ORG_ID}' \
-d '{
    "allowUserReactivation": true,
    "operations": [
        "users.create",
        "users.update"
    ]
    "queryString": "location=Chicago&department=IT"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = jumpcloud.applications.create(
    application_id="application_id_example",
    allow_user_reactivation=True,
    operations=["users.create", "users.update"],
    query_string="",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

ObjectID of the Application.

##### allow_user_reactivation: `bool`<a id="allow_user_reactivation-bool"></a>

A boolean value to allow the reactivation of suspended users

##### operations: List[[`ImportOperation`](./jump_cloud_python_sdk/type/import_operation.py)]<a id="operations-listimportoperationjump_cloud_python_sdktypeimport_operationpy"></a>

Operations to be performed on the user list returned from the application

##### query_string: `str`<a id="query_string-str"></a>

Query string to filter and sort the user list returned from the application.  The supported filtering and sorting varies by application.  If no value is sent, all users are returned. **Example:** \\\"location=Chicago&department=IT\\\"Query string used to retrieve users from service

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ImportUsersRequest`](./jump_cloud_python_sdk/type/import_users_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`JobId`](./jump_cloud_python_sdk/pydantic/job_id.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/import/jobs` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.applications.delete_logo`<a id="jumpcloudapplicationsdelete_logo"></a>

Deletes the specified image from an application

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.applications.delete_logo(
    application_id="application_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/logo` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.applications.get`<a id="jumpcloudapplicationsget"></a>

The endpoint retrieves an Application.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = jumpcloud.applications.get(
    application_id="application_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

ObjectID of the Application.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.applications.post_logo`<a id="jumpcloudapplicationspost_logo"></a>

This endpoint sets the logo for an application.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST 'https://console.jumpcloud.com/api/v2/applications/{Application_ID}/logo \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.applications.post_logo(
    application_id="application_id_example",
    x_org_id="string_example",
    image=open('/path/to/file', 'rb'),
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### image: `IO`<a id="image-io"></a>

The file to upload.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ApplicationsPostLogoRequest`](./jump_cloud_python_sdk/type/applications_post_logo_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/logo` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.applications.users`<a id="jumpcloudapplicationsusers"></a>

Get a list of users to import from an Application IdM service provider.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
users_response = jumpcloud.applications.users(
    application_id="application_id_example",
    filter="",
    query="",
    sort="",
    sort_order="asc",
    x_org_id="string_example",
    limit=10,
    skip=0,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

ObjectID of the Application.

##### filter: `str`<a id="filter-str"></a>

Filter users by a search term

##### query: `str`<a id="query-str"></a>

URL query to merge with the service provider request

##### sort: `str`<a id="sort-str"></a>

Sort users by supported fields

##### sort_order: `str`<a id="sort_order-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

#### 🔄 Return<a id="🔄-return"></a>

[`ImportUsersResponse`](./jump_cloud_python_sdk/pydantic/import_users_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/import/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.authentication_policies.delete`<a id="jumpcloudauthentication_policiesdelete"></a>

Delete the specified authentication policy.

#### Sample Request<a id="sample-request"></a>
```
curl -X DELETE https://console.jumpcloud.com/api/v2/authn/policies/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
delete_response = jumpcloud.authentication_policies.delete(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

Unique identifier of the authentication policy

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`AuthnPolicy`](./jump_cloud_python_sdk/pydantic/authn_policy.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/authn/policies/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.authentication_policies.get`<a id="jumpcloudauthentication_policiesget"></a>

Return a specific authentication policy.

#### Sample Request<a id="sample-request"></a>
```
curl https://console.jumpcloud.com/api/v2/authn/policies/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = jumpcloud.authentication_policies.get(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

Unique identifier of the authentication policy

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`AuthnPolicy`](./jump_cloud_python_sdk/pydantic/authn_policy.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/authn/policies/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.authentication_policies.list`<a id="jumpcloudauthentication_policieslist"></a>

Get a list of all authentication policies.

#### Sample Request<a id="sample-request"></a>
```
curl https://console.jumpcloud.com/api/v2/authn/policies \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = jumpcloud.authentication_policies.list(
    x_org_id="string_example",
    x_total_count=1,
    limit=10,
    skip=0,
    filter=[],
    sort=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### x_total_count: `int`<a id="x_total_count-int"></a>

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return<a id="🔄-return"></a>

[`AuthnpoliciesListResponse`](./jump_cloud_python_sdk/pydantic/authnpolicies_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/authn/policies` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.authentication_policies.patch`<a id="jumpcloudauthentication_policiespatch"></a>

Patch the specified authentication policy.

#### Sample Request<a id="sample-request"></a>
```
curl -X PATCH https://console.jumpcloud.com/api/v2/authn/policies/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{ "disabled": false }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
patch_response = jumpcloud.authentication_policies.patch(
    id="id_example",
    description="string_example",
    conditions={},
    disabled=True,
    effect={
        "action": "allow",
    },
    id="string_example",
    name="string_example",
    targets={
    },
    type="user_portal",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

Unique identifier of the authentication policy

##### description: `str`<a id="description-str"></a>

##### conditions: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="conditions-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Conditions may be added to an authentication policy using the following conditional language:  ``` <conditions> ::= <expression> <expression> ::= <deviceEncrypted> | <deviceManaged> | <ipAddressIn> |                  <locationIn> | <notExpression> | <allExpression> |                  <anyExpression> <deviceEncrypted> ::= { \\\"deviceEncrypted\\\": <boolean> } <deviceManaged> ::= { \\\"deviceManaged\\\": <boolean> } <ipAddressIn> ::= { \\\"ipAddressIn\\\": [ <objectId>, ... ] } <locationIn> ::= { \\\"locationIn\\\": {                      \\\"countries\\\": [                        <iso_3166_country_code>, ...                      ]                    }                  } <notExpression> ::= { \\\"not\\\": <expression> } <allExpression> ::= { \\\"all\\\": [ <expression>, ... ] } <anyExpression> ::= { \\\"any\\\": [ <expression>, ... ] } ```  For example, to add a condition that applies to IP addresses in a given list, the following condition can be added:  ``` {\\\"ipAddressIn\\\": [ <ip_list_object_id> ]} ```  If you would rather exclude IP addresses in the given lists, the following condition could be added:  ``` {   \\\"not\\\": {     \\\"ipAddressIn\\\": [ <ip_list_object_id_1>, <ip_list_object_id_2> ]   } } ```  You may also include more than one condition and choose whether \\\"all\\\" or \\\"any\\\" of them must be met for the policy to apply:  ``` {   \\\"all\\\": [     {       \\\"ipAddressIn\\\": [ <ip_list_object_id>, ... ]     },     {       \\\"deviceManaged\\\": true     },     {       \\\"locationIn\\\": {         countries: [ <iso_3166_country_code>, ... ]       }     }   ] } ```

##### disabled: `bool`<a id="disabled-bool"></a>

##### effect: [`AuthnPolicyEffect`](./jump_cloud_python_sdk/type/authn_policy_effect.py)<a id="effect-authnpolicyeffectjump_cloud_python_sdktypeauthn_policy_effectpy"></a>


##### id: `str`<a id="id-str"></a>

##### name: `str`<a id="name-str"></a>

##### targets: [`AuthnPolicyTargets`](./jump_cloud_python_sdk/type/authn_policy_targets.py)<a id="targets-authnpolicytargetsjump_cloud_python_sdktypeauthn_policy_targetspy"></a>


##### type: [`AuthnPolicyType`](./jump_cloud_python_sdk/type/authn_policy_type.py)<a id="type-authnpolicytypejump_cloud_python_sdktypeauthn_policy_typepy"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AuthnPolicy`](./jump_cloud_python_sdk/type/authn_policy.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AuthnPolicy`](./jump_cloud_python_sdk/pydantic/authn_policy.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/authn/policies/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.authentication_policies.post`<a id="jumpcloudauthentication_policiespost"></a>

Create an authentication policy.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/authn/policies \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "Sample Policy",
    "disabled": false,
    "effect": {
      "action": "allow"
    },
    "targets": {
      "users": {
        "inclusions": ["ALL"]
      },
      "userGroups": {
        "exclusions": [{USER_GROUP_ID}]
      },
      "resources": [ {"type": "user_portal" } ]
    },
    "conditions":{
      "ipAddressIn": [{IP_LIST_ID}]
    }
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
post_response = jumpcloud.authentication_policies.post(
    description="string_example",
    conditions={},
    disabled=True,
    effect={
        "action": "allow",
    },
    id="string_example",
    name="string_example",
    targets={
    },
    type="user_portal",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

##### conditions: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="conditions-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Conditions may be added to an authentication policy using the following conditional language:  ``` <conditions> ::= <expression> <expression> ::= <deviceEncrypted> | <deviceManaged> | <ipAddressIn> |                  <locationIn> | <notExpression> | <allExpression> |                  <anyExpression> <deviceEncrypted> ::= { \\\"deviceEncrypted\\\": <boolean> } <deviceManaged> ::= { \\\"deviceManaged\\\": <boolean> } <ipAddressIn> ::= { \\\"ipAddressIn\\\": [ <objectId>, ... ] } <locationIn> ::= { \\\"locationIn\\\": {                      \\\"countries\\\": [                        <iso_3166_country_code>, ...                      ]                    }                  } <notExpression> ::= { \\\"not\\\": <expression> } <allExpression> ::= { \\\"all\\\": [ <expression>, ... ] } <anyExpression> ::= { \\\"any\\\": [ <expression>, ... ] } ```  For example, to add a condition that applies to IP addresses in a given list, the following condition can be added:  ``` {\\\"ipAddressIn\\\": [ <ip_list_object_id> ]} ```  If you would rather exclude IP addresses in the given lists, the following condition could be added:  ``` {   \\\"not\\\": {     \\\"ipAddressIn\\\": [ <ip_list_object_id_1>, <ip_list_object_id_2> ]   } } ```  You may also include more than one condition and choose whether \\\"all\\\" or \\\"any\\\" of them must be met for the policy to apply:  ``` {   \\\"all\\\": [     {       \\\"ipAddressIn\\\": [ <ip_list_object_id>, ... ]     },     {       \\\"deviceManaged\\\": true     },     {       \\\"locationIn\\\": {         countries: [ <iso_3166_country_code>, ... ]       }     }   ] } ```

##### disabled: `bool`<a id="disabled-bool"></a>

##### effect: [`AuthnPolicyEffect`](./jump_cloud_python_sdk/type/authn_policy_effect.py)<a id="effect-authnpolicyeffectjump_cloud_python_sdktypeauthn_policy_effectpy"></a>


##### id: `str`<a id="id-str"></a>

##### name: `str`<a id="name-str"></a>

##### targets: [`AuthnPolicyTargets`](./jump_cloud_python_sdk/type/authn_policy_targets.py)<a id="targets-authnpolicytargetsjump_cloud_python_sdktypeauthn_policy_targetspy"></a>


##### type: [`AuthnPolicyType`](./jump_cloud_python_sdk/type/authn_policy_type.py)<a id="type-authnpolicytypejump_cloud_python_sdktypeauthn_policy_typepy"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AuthnPolicy`](./jump_cloud_python_sdk/type/authn_policy.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AuthnPolicy`](./jump_cloud_python_sdk/pydantic/authn_policy.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/authn/policies` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.bulk_job_requests.user_expires`<a id="jumpcloudbulk_job_requestsuser_expires"></a>

The endpoint allows you to start a bulk job to asynchronously expire users.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_expires_response = jumpcloud.bulk_job_requests.user_expires(
    body=[
        {
        }
    ],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### requestBody: [`BulkUserExpiresRequest`](./jump_cloud_python_sdk/type/bulk_user_expires_request.py)<a id="requestbody-bulkuserexpiresrequestjump_cloud_python_sdktypebulk_user_expires_requestpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`JobId`](./jump_cloud_python_sdk/pydantic/job_id.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/bulk/user/expires` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.bulk_job_requests.user_states_create`<a id="jumpcloudbulk_job_requestsuser_states_create"></a>

This endpoint allows you to create scheduled statechange jobs.
#### Sample Request<a id="sample-request"></a>
```
curl -X POST "https://console.jumpcloud.com/api/v2/bulk/userstates" \
  -H 'x-api-key: {API_KEY}' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
    "user_ids": ["{User_ID_1}", "{User_ID_2}", "{User_ID_3}"],
    "state": "SUSPENDED",
    "start_date": "2000-01-01T00:00:00.000Z"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_states_create_response = jumpcloud.bulk_job_requests.user_states_create(
    start_date="1970-01-01T00:00:00.00Z",
    state="SUSPENDED",
    user_ids=[
        "string_example"
    ],
    activation_email_override="string_example",
    send_activation_emails=True,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### start_date: `datetime`<a id="start_date-datetime"></a>

Date and time that scheduled action should occur

##### state: `str`<a id="state-str"></a>

The state to move the user(s) to

##### user_ids: [`BulkScheduledStatechangeCreateUserIds`](./jump_cloud_python_sdk/type/bulk_scheduled_statechange_create_user_ids.py)<a id="user_ids-bulkscheduledstatechangecreateuseridsjump_cloud_python_sdktypebulk_scheduled_statechange_create_user_idspy"></a>

##### activation_email_override: `str`<a id="activation_email_override-str"></a>

Send the activation or welcome email to the specified email address upon activation. Can only be used with a single user_id and scheduled activation. This field will be ignored if `send_activation_emails` is explicitly set to false.

##### send_activation_emails: `bool`<a id="send_activation_emails-bool"></a>

Set to true to send activation or welcome email(s) to each user_id upon activation. Set to false to suppress emails. Can only be used with scheduled activation(s).

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`BulkScheduledStatechangeCreate`](./jump_cloud_python_sdk/type/bulk_scheduled_statechange_create.py)
#### 🔄 Return<a id="🔄-return"></a>

[`BulkUserStatesCreateResponse`](./jump_cloud_python_sdk/pydantic/bulk_user_states_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/bulk/userstates` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.bulk_job_requests.user_states_delete`<a id="jumpcloudbulk_job_requestsuser_states_delete"></a>

This endpoint deletes a scheduled statechange job.
#### Sample Request<a id="sample-request"></a>
```
curl -X DELETE "https://console.jumpcloud.com/api/v2/bulk/userstates/{ScheduledJob_ID}" \
  -H 'x-api-key: {API_KEY}' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.bulk_job_requests.user_states_delete(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

Unique identifier of the scheduled statechange job.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/bulk/userstates/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.bulk_job_requests.user_states_get_next_scheduled`<a id="jumpcloudbulk_job_requestsuser_states_get_next_scheduled"></a>

This endpoint is used to lookup the next upcoming scheduled state change for each user in the
given list. The users parameter is limited to 100 items per request. The results are also limited
to 100 items. This endpoint returns a max of 1 event per state per user. For example, if a user
has 3 ACTIVATED events scheduled it will return the next upcoming activation event. However, if a
user also has a SUSPENDED event scheduled along with the ACTIVATED events it will return the next
upcoming activation event _and_ the next upcoming suspension event.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_states_get_next_scheduled_response = jumpcloud.bulk_job_requests.user_states_get_next_scheduled(
    users=[
        "users_example"
    ],
    limit=10,
    skip=0,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### users: List[`str`]<a id="users-liststr"></a>

A list of system user IDs, limited to 100 items.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

#### 🔄 Return<a id="🔄-return"></a>

[`BulkUserStatesGetNextScheduledResponse`](./jump_cloud_python_sdk/pydantic/bulk_user_states_get_next_scheduled_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/bulk/userstates/eventlist/next` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.bulk_job_requests.user_states_list`<a id="jumpcloudbulk_job_requestsuser_states_list"></a>

The endpoint allows you to list scheduled statechange jobs.
#### Sample Request<a id="sample-request"></a>
```
curl -X GET "https://console.jumpcloud.com/api/v2/bulk/userstates" \
  -H 'x-api-key: {API_KEY}' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_states_list_response = jumpcloud.bulk_job_requests.user_states_list(
    limit=10,
    filter=[],
    skip=0,
    x_org_id="string_example",
    userid="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### userid: `str`<a id="userid-str"></a>

The systemuser id to filter by.

#### 🔄 Return<a id="🔄-return"></a>

[`BulkUserStatesListResponse`](./jump_cloud_python_sdk/pydantic/bulk_user_states_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/bulk/userstates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.bulk_job_requests.user_unlocks`<a id="jumpcloudbulk_job_requestsuser_unlocks"></a>

The endpoint allows you to start a bulk job to asynchronously unlock users.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_unlocks_response = jumpcloud.bulk_job_requests.user_unlocks(
    body=[
        {
        }
    ],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### requestBody: [`BulkUserUnlocksRequest`](./jump_cloud_python_sdk/type/bulk_user_unlocks_request.py)<a id="requestbody-bulkuserunlocksrequestjump_cloud_python_sdktypebulk_user_unlocks_requestpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`JobId`](./jump_cloud_python_sdk/pydantic/job_id.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/bulk/user/unlocks` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.bulk_job_requests.users_create`<a id="jumpcloudbulk_job_requestsusers_create"></a>

The endpoint allows you to create a bulk job to asynchronously create users.
See [Create a System User](https://docs.jumpcloud.com/api/1.0/index.html#operation/systemusers_post)
for the full list of attributes.

#### Default User State<a id="default-user-state"></a>
The `state` of each user in the request can be explicitly passed in or
omitted. If `state` is omitted, then the user will get created
using the value returned from the
[Get an Organization](https://docs.jumpcloud.com/api/1.0/index.html#operation/organizations_get)
endpoint. The default user state for bulk created users depends on the
`creation-source` header. For `creation-source:jumpcloud:bulk` the
default state is stored in `settings.newSystemUserStateDefaults.csvImport`.
For other `creation-source` header values, the default state is stored in
`settings.newSystemUserStateDefaults.applicationImport`

These default state values can be changed in the admin portal settings
or by using the
[Update an Organization](https://docs.jumpcloud.com/api/1.0/index.html#operation/organization_put)
endpoint.

#### Sample Request<a id="sample-request"></a>

```
curl -X POST https://console.jumpcloud.com/api/v2/bulk/users \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'x-api-key: {API_KEY}' \
-d '[
  {
    "email":"{email}",
    "firstname":"{firstname}",
    "lastname":"{firstname}",
    "username":"{username}",
    "attributes":[
      {
        "name":"EmployeeID",
        "value":"0000"
      },
      {
        "name":"Custom",
        "value":"attribute"
      }
    ]
  }
]'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
users_create_response = jumpcloud.bulk_job_requests.users_create(
    body=[
        {
        }
    ],
    x_org_id="string_example",
    creation_source="jumpcloud:bulk",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### creation_source: `str`<a id="creation_source-str"></a>

Defines the creation-source header for gapps, o365 and workdays requests. If the header isn't sent, the default value is `jumpcloud:bulk`, if you send the header with a malformed value you receive a 400 error. 

##### requestBody: [`BulkUsersCreateRequest`](./jump_cloud_python_sdk/type/bulk_users_create_request.py)<a id="requestbody-bulkuserscreaterequestjump_cloud_python_sdktypebulk_users_create_requestpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`JobId`](./jump_cloud_python_sdk/pydantic/job_id.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/bulk/users` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.bulk_job_requests.users_create_results`<a id="jumpcloudbulk_job_requestsusers_create_results"></a>

This endpoint will return the results of particular user import or update job request.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET \
  https://console.jumpcloud.com/api/v2/bulk/users/{ImportJobID}/results \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
users_create_results_response = jumpcloud.bulk_job_requests.users_create_results(
    job_id="job_id_example",
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### job_id: `str`<a id="job_id-str"></a>

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`BulkUsersCreateResultsResponse`](./jump_cloud_python_sdk/pydantic/bulk_users_create_results_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/bulk/users/{job_id}/results` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.bulk_job_requests.users_update`<a id="jumpcloudbulk_job_requestsusers_update"></a>

The endpoint allows you to create a bulk job to asynchronously update users. See [Update a System User](https://docs.jumpcloud.com/api/1.0/index.html#operation/systemusers_put) for full list of attributes.

#### Sample Request <a id="sample-request-"></a>
```
curl -X PATCH https://console.jumpcloud.com/api/v2/bulk/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '[
	{
	  "id":"5be9fb4ddb01290001e85109",
		"firstname":"{UPDATED_FIRSTNAME}",
		"department":"{UPDATED_DEPARTMENT}",
		"attributes":[
			{"name":"Custom","value":"{ATTRIBUTE_VALUE}"}
		]
	},
	{
	  "id":"5be9fb4ddb01290001e85109",
		"firstname":"{UPDATED_FIRSTNAME}",
		"costCenter":"{UPDATED_COST_CENTER}",
		"phoneNumbers":[
			{"type":"home","number":"{HOME_PHONE_NUMBER}"},
			{"type":"work","number":"{WORK_PHONE_NUMBER}"}
		]
	}
]
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
users_update_response = jumpcloud.bulk_job_requests.users_update(
    body=[
        {
        }
    ],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### requestBody: [`BulkUsersUpdateRequest`](./jump_cloud_python_sdk/type/bulk_users_update_request.py)<a id="requestbody-bulkusersupdaterequestjump_cloud_python_sdktypebulk_users_update_requestpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`JobId`](./jump_cloud_python_sdk/pydantic/job_id.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/bulk/users` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.commands.cancel_queued_commands_by_workflow_instance_id`<a id="jumpcloudcommandscancel_queued_commands_by_workflow_instance_id"></a>

This endpoint allows all queued commands for one workflow instance to be canceled.

#### Sample Request<a id="sample-request"></a>
```
 curl -X DELETE https://console.jumpcloud.com/api/v2/commandqueue/{workflow_instance_id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.commands.cancel_queued_commands_by_workflow_instance_id(
    workflow_instance_id="workflow_instance_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workflow_instance_id: `str`<a id="workflow_instance_id-str"></a>

Workflow instance Id of the queued commands to cancel.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/commandqueue/{workflow_instance_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.commands.command_associations_list`<a id="jumpcloudcommandscommand_associations_list"></a>

This endpoint will return the _direct_ associations of this Command.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Commands and User Groups.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/commands/{Command_ID}/associations?targets=system_group \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
command_associations_list_response = jumpcloud.commands.command_associations_list(
    command_id="command_id_example",
    targets=[
        "system"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### command_id: `str`<a id="command_id-str"></a>

ObjectID of the Command.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"command\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphCommandAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_command_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/commands/{command_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.commands.command_associations_post`<a id="jumpcloudcommandscommand_associations_post"></a>

This endpoint will allow you to manage the _direct_ associations of this Command.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Commands and User Groups.


#### Sample Request<a id="sample-request"></a>
```
 curl -X POST https://console.jumpcloud.com/api/v2/commands/{Command_ID}/associations \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system_group",
    "id": "Group_ID"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.commands.command_associations_post(
    command_id="command_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### command_id: `str`<a id="command_id-str"></a>

ObjectID of the Command.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"command\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationCommand`](./jump_cloud_python_sdk/type/graph_operation_command.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/commands/{command_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.commands.command_traverse_system`<a id="jumpcloudcommandscommand_traverse_system"></a>

This endpoint will return all Systems bound to a Command, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Command to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this Command.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/commands/{Command_ID}/systems \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
command_traverse_system_response = jumpcloud.commands.command_traverse_system(
    command_id="command_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### command_id: `str`<a id="command_id-str"></a>

ObjectID of the Command.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphCommandTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_command_traverse_system_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/commands/{command_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.commands.command_traverse_system_group`<a id="jumpcloudcommandscommand_traverse_system_group"></a>

This endpoint will return all System Groups bound to a Command, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Command to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this Command.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/commands/{Command_ID}/systemgroups \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
command_traverse_system_group_response = jumpcloud.commands.command_traverse_system_group(
    command_id="command_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### command_id: `str`<a id="command_id-str"></a>

ObjectID of the Command.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphCommandTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_command_traverse_system_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/commands/{command_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.commands.get_queued_commands_by_workflow`<a id="jumpcloudcommandsget_queued_commands_by_workflow"></a>

This endpoint will return all queued Commands for an Organization.

Each element will contain the workflow ID, the command name, the launch type (e.g. manual, triggered, or scheduled), the target OS, the number of assigned devices, and the number of pending devices that have not yet ran the command.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/queuedcommand/workflows \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_queued_commands_by_workflow_response = jumpcloud.commands.get_queued_commands_by_workflow(
    x_org_id="string_example",
    limit=10,
    filter=[],
    skip=0,
    sort=[],
    search="",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### limit: `int`<a id="limit-int"></a>

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### search: `str`<a id="search-str"></a>

The search string to query records

#### 🔄 Return<a id="🔄-return"></a>

[`QueuedCommandList`](./jump_cloud_python_sdk/pydantic/queued_command_list.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/queuedcommand/workflows` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.custom_emails.create`<a id="jumpcloudcustom_emailscreate"></a>

Create the custom email configuration for the specified custom email type.

This action is only available to paying customers.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = jumpcloud.custom_emails.create(
    subject="",
    type="activate_gapps_user",
    title="",
    body="",
    button="",
    header="",
    id="string_example",
    next_step_contact_info="",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### subject: `str`<a id="subject-str"></a>

##### type: [`CustomEmailType`](./jump_cloud_python_sdk/type/custom_email_type.py)<a id="type-customemailtypejump_cloud_python_sdktypecustom_email_typepy"></a>

##### title: `str`<a id="title-str"></a>

##### body: `str`<a id="body-str"></a>

##### button: `str`<a id="button-str"></a>

##### header: `str`<a id="header-str"></a>

##### id: `str`<a id="id-str"></a>

##### next_step_contact_info: `str`<a id="next_step_contact_info-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CustomEmail`](./jump_cloud_python_sdk/type/custom_email.py)
#### 🔄 Return<a id="🔄-return"></a>

[`CustomEmail`](./jump_cloud_python_sdk/pydantic/custom_email.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/customemails` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.custom_emails.destroy`<a id="jumpcloudcustom_emailsdestroy"></a>

Delete the custom email configuration for the specified custom email type

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.custom_emails.destroy(
    custom_email_type="custom_email_type_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### custom_email_type: `str`<a id="custom_email_type-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/customemails/{custom_email_type}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.custom_emails.get_templates`<a id="jumpcloudcustom_emailsget_templates"></a>

Get the list of custom email templates

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_templates_response = jumpcloud.custom_emails.get_templates()
```

#### 🔄 Return<a id="🔄-return"></a>

[`CustomEmailsGetTemplatesResponse`](./jump_cloud_python_sdk/pydantic/custom_emails_get_templates_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/customemail/templates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.custom_emails.read`<a id="jumpcloudcustom_emailsread"></a>

Get the custom email configuration for the specified custom email type

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
read_response = jumpcloud.custom_emails.read(
    custom_email_type="custom_email_type_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### custom_email_type: `str`<a id="custom_email_type-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`CustomEmail`](./jump_cloud_python_sdk/pydantic/custom_email.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/customemails/{custom_email_type}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.custom_emails.update`<a id="jumpcloudcustom_emailsupdate"></a>

Update the custom email configuration for the specified custom email type.

This action is only available to paying customers.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = jumpcloud.custom_emails.update(
    subject="",
    type="activate_gapps_user",
    custom_email_type="custom_email_type_example",
    title="",
    body="",
    button="",
    header="",
    id="string_example",
    next_step_contact_info="",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### subject: `str`<a id="subject-str"></a>

##### type: [`CustomEmailType`](./jump_cloud_python_sdk/type/custom_email_type.py)<a id="type-customemailtypejump_cloud_python_sdktypecustom_email_typepy"></a>

##### custom_email_type: `str`<a id="custom_email_type-str"></a>

##### title: `str`<a id="title-str"></a>

##### body: `str`<a id="body-str"></a>

##### button: `str`<a id="button-str"></a>

##### header: `str`<a id="header-str"></a>

##### id: `str`<a id="id-str"></a>

##### next_step_contact_info: `str`<a id="next_step_contact_info-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CustomEmail`](./jump_cloud_python_sdk/type/custom_email.py)
#### 🔄 Return<a id="🔄-return"></a>

[`CustomEmail`](./jump_cloud_python_sdk/pydantic/custom_email.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/customemails/{custom_email_type}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.directories.list`<a id="jumpclouddirectorieslist"></a>

This endpoint returns all active directories (LDAP, O365 Suite, G-Suite).

#### Sample Request<a id="sample-request"></a>
```
 curl -X GET https://console.jumpcloud.com/api/v2/directories \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = jumpcloud.directories.list(
    fields=[],
    limit=10,
    sort=[],
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### fields: List[`str`]<a id="fields-liststr"></a>

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`DirectoriesListResponse`](./jump_cloud_python_sdk/pydantic/directories_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/directories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.duo.account_delete`<a id="jumpcloudduoaccount_delete"></a>

Removes the specified Duo account, an error will be returned if the account has some Duo application used in a protected resource.

#### Sample Request<a id="sample-request"></a>
```
curl -X DELETE https://console.jumpcloud.com/api/v2/duo/accounts/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
account_delete_response = jumpcloud.duo.account_delete(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

ObjectID of the Duo Account

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`DuoAccount`](./jump_cloud_python_sdk/pydantic/duo_account.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/duo/accounts/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.duo.account_get`<a id="jumpcloudduoaccount_get"></a>

This endpoint returns a specific Duo account.

#### Sample Request<a id="sample-request"></a>
```
curl https://console.jumpcloud.com/api/v2/duo/accounts/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
account_get_response = jumpcloud.duo.account_get(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

ObjectID of the Duo Account

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`DuoAccount`](./jump_cloud_python_sdk/pydantic/duo_account.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/duo/accounts/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.duo.account_list`<a id="jumpcloudduoaccount_list"></a>

This endpoint returns all the Duo accounts for your organization. Note: There can currently only be one Duo account for your organization.

#### Sample Request<a id="sample-request"></a>
```
curl https://console.jumpcloud.com/api/v2/duo/accounts \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
account_list_response = jumpcloud.duo.account_list(
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`DuoAccountListResponse`](./jump_cloud_python_sdk/pydantic/duo_account_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/duo/accounts` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.duo.account_post`<a id="jumpcloudduoaccount_post"></a>

Registers a Duo account for an organization. Only one Duo account will be allowed,
in case an organization has a Duo account already a 409 (Conflict) code will be returned.

#### Sample Request<a id="sample-request"></a>
```
  curl -X POST https://console.jumpcloud.com/api/v2/duo/accounts \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
account_post_response = jumpcloud.duo.account_post(
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`DuoAccount`](./jump_cloud_python_sdk/pydantic/duo_account.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/duo/accounts` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.duo.application_delete`<a id="jumpcloudduoapplication_delete"></a>

Deletes the specified Duo application, an error will be returned if the application is used in a protected resource.

#### Sample Request<a id="sample-request"></a>
```
  curl -X DELETE https://console.jumpcloud.com/api/v2/duo/accounts/{ACCOUNT_ID}/applications/{APPLICATION_ID} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}''
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
application_delete_response = jumpcloud.duo.application_delete(
    account_id="account_id_example",
    application_id="application_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### account_id: `str`<a id="account_id-str"></a>

##### application_id: `str`<a id="application_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`DuoApplication`](./jump_cloud_python_sdk/pydantic/duo_application.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/duo/accounts/{account_id}/applications/{application_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.duo.application_get`<a id="jumpcloudduoapplication_get"></a>

This endpoint returns a specific Duo application that is associated with the specified Duo account.

#### Sample Request<a id="sample-request"></a>
```
  curl https://console.jumpcloud.com/api/v2/duo/accounts/{ACCOUNT_ID}/applications/{APPLICATION_ID} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
application_get_response = jumpcloud.duo.application_get(
    account_id="account_id_example",
    application_id="application_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### account_id: `str`<a id="account_id-str"></a>

##### application_id: `str`<a id="application_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`DuoApplication`](./jump_cloud_python_sdk/pydantic/duo_application.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/duo/accounts/{account_id}/applications/{application_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.duo.application_list`<a id="jumpcloudduoapplication_list"></a>

This endpoint returns all the Duo applications for the specified Duo account. Note: There can currently only be one Duo application for your organization.

#### Sample Request<a id="sample-request"></a>
```
  curl https://console.jumpcloud.com/api/v2/duo/accounts/{ACCOUNT_ID}/applications \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
application_list_response = jumpcloud.duo.application_list(
    account_id="account_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### account_id: `str`<a id="account_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`DuoApplicationListResponse`](./jump_cloud_python_sdk/pydantic/duo_application_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/duo/accounts/{account_id}/applications` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.duo.application_post`<a id="jumpcloudduoapplication_post"></a>

Creates a Duo application for your organization and the specified account.

#### Sample Request<a id="sample-request"></a>
```
  curl -X POST https://console.jumpcloud.com/api/v2/duo/accounts/{ACCOUNT_ID}/applications \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "Application Name",
    "apiHost": "api-1234.duosecurity.com",
    "integrationKey": "1234",
    "secretKey": "5678"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
application_post_response = jumpcloud.duo.application_post(
    api_host="string_example",
    integration_key="string_example",
    name="string_example",
    secret_key="string_example",
    account_id="account_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### api_host: `str`<a id="api_host-str"></a>

##### integration_key: `str`<a id="integration_key-str"></a>

##### name: `str`<a id="name-str"></a>

##### secret_key: `str`<a id="secret_key-str"></a>

##### account_id: `str`<a id="account_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DuoApplicationReq`](./jump_cloud_python_sdk/type/duo_application_req.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DuoApplication`](./jump_cloud_python_sdk/pydantic/duo_application.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/duo/accounts/{account_id}/applications` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.duo.application_update`<a id="jumpcloudduoapplication_update"></a>

Updates the specified Duo application.

#### Sample Request<a id="sample-request"></a>
```
  curl -X PUT https://console.jumpcloud.com/api/v2/duo/accounts/{ACCOUNT_ID}/applications/{APPLICATION_ID} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "Application Name",
    "apiHost": "api-1234.duosecurity.com",
    "integrationKey": "1234",
    "secretKey": "5678"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
application_update_response = jumpcloud.duo.application_update(
    api_host="string_example",
    integration_key="string_example",
    name="string_example",
    account_id="account_id_example",
    application_id="application_id_example",
    secret_key="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### api_host: `str`<a id="api_host-str"></a>

##### integration_key: `str`<a id="integration_key-str"></a>

##### name: `str`<a id="name-str"></a>

##### account_id: `str`<a id="account_id-str"></a>

##### application_id: `str`<a id="application_id-str"></a>

##### secret_key: `str`<a id="secret_key-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DuoApplicationUpdateReq`](./jump_cloud_python_sdk/type/duo_application_update_req.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DuoApplication`](./jump_cloud_python_sdk/pydantic/duo_application.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/duo/accounts/{account_id}/applications/{application_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.feature_trials.get_feature_trials`<a id="jumpcloudfeature_trialsget_feature_trials"></a>

This endpoint get's the current state of a feature trial for an org.

#### Sample Request<a id="sample-request"></a>

```
  curl -X GET \
  https://console.jumpcloud.local/api/v2/featureTrials/zeroTrust \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_feature_trials_response = jumpcloud.feature_trials.get_feature_trials(
    feature_code="feature_code_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### feature_code: `str`<a id="feature_code-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`FeatureTrialData`](./jump_cloud_python_sdk/pydantic/feature_trial_data.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/featureTrials/{feature_code}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.add_domain`<a id="jumpcloudg_suiteadd_domain"></a>

Add a domain to a specific Google Workspace directory sync integration instance. The domain must be a verified domain in Google Workspace.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/gsuites/{gsuite_id}/domains \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{"domain": "{domain name}"}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_domain_response = jumpcloud.g_suite.add_domain(
    gsuite_id='YQ==',
    domain="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

Id for the specific Google Workspace directory sync integration instance.

##### domain: `str`<a id="domain-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGappsDomainResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_gapps_domain_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/domains` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.configured_domains_list`<a id="jumpcloudg_suiteconfigured_domains_list"></a>

List the domains configured for a specific Google Workspace directory sync integration instance.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/gsuites/{gsuite_id}/domains \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
configured_domains_list_response = jumpcloud.g_suite.configured_domains_list(
    gsuite_id='YQ==',
    limit="100",
    skip="0",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

Id for the specific Google Workspace directory sync integration instance..

##### limit: `str`<a id="limit-str"></a>

The number of records to return at once. Limited to 100.

##### skip: `str`<a id="skip-str"></a>

The offset into the records to return.

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGappsDomainListResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_gapps_domain_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/domains` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.delete_domain`<a id="jumpcloudg_suitedelete_domain"></a>

Delete a domain from a specific Google Workspace directory sync integration instance.

#### Sample Request<a id="sample-request"></a>
```
curl -X DELETE https://console.jumpcloud.com/api/v2/gsuites/{gsuite_id}/domains/{domainId} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
delete_domain_response = jumpcloud.g_suite.delete_domain(
    gsuite_id='YQ==',
    domain_id='YQ==',
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

Id for the specific Google Workspace directory sync integration instance.

##### domain_id: `str`<a id="domain_id-str"></a>

Id for the domain.

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGappsDomainResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_gapps_domain_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/domains/{domainId}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.g_suite_associations_list`<a id="jumpcloudg_suiteg_suite_associations_list"></a>

This endpoint returns the _direct_ associations of this G Suite instance.

A direct association can be a non-homogeneous relationship between 2 different objects, for example G Suite and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET 'https://console.jumpcloud.com/api/v2/gsuites/{Gsuite_ID}/associations?targets=user_group \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
g_suite_associations_list_response = jumpcloud.g_suite.g_suite_associations_list(
    gsuite_id="gsuite_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

ObjectID of the G Suite instance.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"g_suite\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphGSuiteAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_g_suite_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.g_suite_associations_post`<a id="jumpcloudg_suiteg_suite_associations_post"></a>

This endpoint returns the _direct_ associations of this G Suite instance.

A direct association can be a non-homogeneous relationship between 2 different objects, for example G Suite and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/gsuites/{Gsuite_ID}/associations \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user_group",
    "id": "{Group_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.g_suite.g_suite_associations_post(
    gsuite_id="gsuite_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

ObjectID of the G Suite instance.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"g_suite\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationGSuite`](./jump_cloud_python_sdk/type/graph_operation_g_suite.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.g_suite_delete`<a id="jumpcloudg_suiteg_suite_delete"></a>

This endpoint allows you to delete a translation rule for a specific G Suite instance. These rules specify how JumpCloud attributes translate to [G Suite Admin SDK](https://developers.google.com/admin-sdk/directory/) attributes.

#### Sample Request<a id="sample-request"></a>

```
curl -X DELETE https://console.jumpcloud.com/api/v2/gsuites/{gsuite_id}/translationrules/{id} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.g_suite.g_suite_delete(
    gsuite_id="gsuite_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/translationrules/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.g_suite_get`<a id="jumpcloudg_suiteg_suite_get"></a>

This endpoint returns a specific translation rule for a specific G Suite instance. These rules specify how JumpCloud attributes translate to [G Suite Admin SDK](https://developers.google.com/admin-sdk/directory/) attributes.

###### Sample Request<a id="sample-request"></a>

```
  curl -X GET https://console.jumpcloud.com/api/v2/gsuites/{gsuite_id}/translationrules/{id} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
g_suite_get_response = jumpcloud.g_suite.g_suite_get(
    gsuite_id="gsuite_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`GSuiteTranslationRule`](./jump_cloud_python_sdk/pydantic/g_suite_translation_rule.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/translationrules/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.g_suite_list`<a id="jumpcloudg_suiteg_suite_list"></a>

This endpoint returns all graph translation rules for a specific G Suite instance. These rules specify how JumpCloud attributes translate to [G Suite Admin SDK](https://developers.google.com/admin-sdk/directory/) attributes.

##### Sample Request<a id="sample-request"></a>

```
curl -X GET  https://console.jumpcloud.com/api/v2/gsuites/{gsuite_id}/translationrules \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
g_suite_list_response = jumpcloud.g_suite.g_suite_list(
    gsuite_id="gsuite_id_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

##### fields: List[`str`]<a id="fields-liststr"></a>

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return<a id="🔄-return"></a>

[`TranslationRulesGSuiteListResponse`](./jump_cloud_python_sdk/pydantic/translation_rules_g_suite_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/translationrules` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.g_suite_post`<a id="jumpcloudg_suiteg_suite_post"></a>

This endpoint allows you to create a translation rule for a specific G Suite instance. These rules specify how JumpCloud attributes translate to [G Suite Admin SDK](https://developers.google.com/admin-sdk/directory/) attributes.

##### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/gsuites/{gsuite_id}/translationrules \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    {Translation Rule Parameters}
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
g_suite_post_response = jumpcloud.g_suite.g_suite_post(
    gsuite_id="gsuite_id_example",
    built_in="user_home_addresses",
    direction="export",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

##### built_in: [`GSuiteBuiltinTranslation`](./jump_cloud_python_sdk/type/g_suite_builtin_translation.py)<a id="built_in-gsuitebuiltintranslationjump_cloud_python_sdktypeg_suite_builtin_translationpy"></a>

##### direction: [`GSuiteDirectionTranslation`](./jump_cloud_python_sdk/type/g_suite_direction_translation.py)<a id="direction-gsuitedirectiontranslationjump_cloud_python_sdktypeg_suite_direction_translationpy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GSuiteTranslationRuleRequest`](./jump_cloud_python_sdk/type/g_suite_translation_rule_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`GSuiteTranslationRule`](./jump_cloud_python_sdk/pydantic/g_suite_translation_rule.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/translationrules` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.g_suite_traverse_user`<a id="jumpcloudg_suiteg_suite_traverse_user"></a>

This endpoint will return all Users bound to a G Suite instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this G Suite instance to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this G Suite instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
  curl -X GET https://console.jumpcloud.com/api/v2/gsuites/{Gsuite_ID}/users \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
g_suite_traverse_user_response = jumpcloud.g_suite.g_suite_traverse_user(
    gsuite_id="gsuite_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

ObjectID of the G Suite instance.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphGSuiteTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_g_suite_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.g_suite_traverse_user_group`<a id="jumpcloudg_suiteg_suite_traverse_user_group"></a>

This endpoint will return all User Groups bound to an G Suite instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this G Suite instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this G Suite instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
  curl -X GET https://console.jumpcloud.com/api/v2/gsuites/{GSuite_ID}/usergroups \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
g_suite_traverse_user_group_response = jumpcloud.g_suite.g_suite_traverse_user_group(
    gsuite_id="gsuite_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

ObjectID of the G Suite instance.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphGSuiteTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_g_suite_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.get`<a id="jumpcloudg_suiteget"></a>

This endpoint returns a specific G Suite.

##### Sample Request<a id="sample-request"></a>

```
 curl -X GET https://console.jumpcloud.com/api/v2/gsuites/{GSUITE_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = jumpcloud.g_suite.get(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

Unique identifier of the GSuite.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`Gsuite`](./jump_cloud_python_sdk/pydantic/gsuite.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.list_import_jumpcloud_users`<a id="jumpcloudg_suitelist_import_jumpcloud_users"></a>

Lists available G Suite users for import, translated to the Jumpcloud user schema.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_import_jumpcloud_users_response = jumpcloud.g_suite.list_import_jumpcloud_users(
    gsuite_id="gsuite_id_example",
    max_results=1,
    order_by="string_example",
    page_token="string_example",
    query="string_example",
    sort_order="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

##### max_results: `int`<a id="max_results-int"></a>

Google Directory API maximum number of results per page. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### order_by: `str`<a id="order_by-str"></a>

Google Directory API sort field parameter. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### page_token: `str`<a id="page_token-str"></a>

Google Directory API token used to access the next page of results. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### query: `str`<a id="query-str"></a>

Google Directory API search parameter. See https://developers.google.com/admin-sdk/directory/v1/guides/search-users.

##### sort_order: `str`<a id="sort_order-str"></a>

Google Directory API sort direction parameter. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

#### 🔄 Return<a id="🔄-return"></a>

[`GsuitesListImportJumpcloudUsersResponse`](./jump_cloud_python_sdk/pydantic/gsuites_list_import_jumpcloud_users_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/import/jumpcloudusers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.list_import_users`<a id="jumpcloudg_suitelist_import_users"></a>

Lists G Suite users available for import.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_import_users_response = jumpcloud.g_suite.list_import_users(
    gsuite_id="gsuite_id_example",
    limit=10,
    max_results=1,
    order_by="string_example",
    page_token="string_example",
    query="string_example",
    sort_order="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### max_results: `int`<a id="max_results-int"></a>

Google Directory API maximum number of results per page. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### order_by: `str`<a id="order_by-str"></a>

Google Directory API sort field parameter. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### page_token: `str`<a id="page_token-str"></a>

Google Directory API token used to access the next page of results. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### query: `str`<a id="query-str"></a>

Google Directory API search parameter. See https://developers.google.com/admin-sdk/directory/v1/guides/search-users.

##### sort_order: `str`<a id="sort_order-str"></a>

Google Directory API sort direction parameter. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

#### 🔄 Return<a id="🔄-return"></a>

[`GsuitesListImportUsersResponse`](./jump_cloud_python_sdk/pydantic/gsuites_list_import_users_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/import/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite.patch`<a id="jumpcloudg_suitepatch"></a>

This endpoint allows updating some attributes of a G Suite.

##### Sample Request<a id="sample-request"></a>

```
curl -X PATCH https://console.jumpcloud.com/api/v2/gsuites/{GSUITE_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "userLockoutAction": "suspend",
    "userPasswordExpirationAction": "maintain"
  }'
```
Sample Request, set a default domain

```
curl -X PATCH https://console.jumpcloud.com/api/v2/gsuites/{GSUITE_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "defaultDomain": {
        "id": "{domainObjectID}"
      }
  }'
```

Sample Request, unset the default domain

```
curl -X PATCH https://console.jumpcloud.com/api/v2/gsuites/{GSUITE_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "defaultDomain": {}
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
patch_response = jumpcloud.g_suite.patch(
    id="id_example",
    default_domain={
    },
    groups_enabled=True,
    id="string_example",
    name="string_example",
    user_lockout_action="suspend",
    user_password_expiration_action="suspend",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

Unique identifier of the GSuite.

##### default_domain: [`DefaultDomain`](./jump_cloud_python_sdk/type/default_domain.py)<a id="default_domain-defaultdomainjump_cloud_python_sdktypedefault_domainpy"></a>


##### groups_enabled: `bool`<a id="groups_enabled-bool"></a>

##### id: `str`<a id="id-str"></a>

##### name: `str`<a id="name-str"></a>

##### user_lockout_action: `str`<a id="user_lockout_action-str"></a>

##### user_password_expiration_action: `str`<a id="user_password_expiration_action-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Gsuite`](./jump_cloud_python_sdk/type/gsuite.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Gsuite`](./jump_cloud_python_sdk/pydantic/gsuite.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite_import.list_import_jumpcloud_users`<a id="jumpcloudg_suite_importlist_import_jumpcloud_users"></a>

Lists available G Suite users for import, translated to the Jumpcloud user schema.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_import_jumpcloud_users_response = jumpcloud.g_suite_import.list_import_jumpcloud_users(
    gsuite_id="gsuite_id_example",
    max_results=1,
    order_by="string_example",
    page_token="string_example",
    query="string_example",
    sort_order="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

##### max_results: `int`<a id="max_results-int"></a>

Google Directory API maximum number of results per page. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### order_by: `str`<a id="order_by-str"></a>

Google Directory API sort field parameter. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### page_token: `str`<a id="page_token-str"></a>

Google Directory API token used to access the next page of results. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### query: `str`<a id="query-str"></a>

Google Directory API search parameter. See https://developers.google.com/admin-sdk/directory/v1/guides/search-users.

##### sort_order: `str`<a id="sort_order-str"></a>

Google Directory API sort direction parameter. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

#### 🔄 Return<a id="🔄-return"></a>

[`GsuitesListImportJumpcloudUsersResponse`](./jump_cloud_python_sdk/pydantic/gsuites_list_import_jumpcloud_users_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/import/jumpcloudusers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.g_suite_import.list_import_users`<a id="jumpcloudg_suite_importlist_import_users"></a>

Lists G Suite users available for import.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_import_users_response = jumpcloud.g_suite_import.list_import_users(
    gsuite_id="gsuite_id_example",
    limit=10,
    max_results=1,
    order_by="string_example",
    page_token="string_example",
    query="string_example",
    sort_order="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### max_results: `int`<a id="max_results-int"></a>

Google Directory API maximum number of results per page. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### order_by: `str`<a id="order_by-str"></a>

Google Directory API sort field parameter. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### page_token: `str`<a id="page_token-str"></a>

Google Directory API token used to access the next page of results. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

##### query: `str`<a id="query-str"></a>

Google Directory API search parameter. See https://developers.google.com/admin-sdk/directory/v1/guides/search-users.

##### sort_order: `str`<a id="sort_order-str"></a>

Google Directory API sort direction parameter. See https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list.

#### 🔄 Return<a id="🔄-return"></a>

[`GsuitesListImportUsersResponse`](./jump_cloud_python_sdk/pydantic/gsuites_list_import_users_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/import/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.create`<a id="jumpcloudgoogle_emmcreate"></a>

Creates a Google EMM enterprise signup URL.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/google-emm/signup-urls \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = jumpcloud.google_emm.create()
```

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmSignupURL`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_signup_url.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/signup-urls` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.create_enrollment_token`<a id="jumpcloudgoogle_emmcreate_enrollment_token"></a>

Gets an enrollment token to enroll a device into Google EMM.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/google-emm/enrollment-tokens \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_enrollment_token_response = jumpcloud.google_emm.create_enrollment_token(
    allow_personal_usage="PERSONAL_USAGE_ALLOWED",
    created_where="API",
    display_name="string_example",
    duration="string_example",
    enrollment_type="WORK_PROFILE",
    enterprise_object_id='YQ==',
    one_time_only=True,
    provisioning_extras={
        "wifi_security_type": "NONE",
    },
    user_object_id='YQ==',
    zero_touch=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### allow_personal_usage: [`JumpcloudGoogleEmmAllowPersonalUsage`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_allow_personal_usage.py)<a id="allow_personal_usage-jumpcloudgoogleemmallowpersonalusagejump_cloud_python_sdktypejumpcloud_google_emm_allow_personal_usagepy"></a>

##### created_where: [`JumpcloudGoogleEmmCreatedWhere`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_created_where.py)<a id="created_where-jumpcloudgoogleemmcreatedwherejump_cloud_python_sdktypejumpcloud_google_emm_created_wherepy"></a>

##### display_name: `str`<a id="display_name-str"></a>

##### duration: `str`<a id="duration-str"></a>

##### enrollment_type: [`JumpcloudGoogleEmmEnrollmentType`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_enrollment_type.py)<a id="enrollment_type-jumpcloudgoogleemmenrollmenttypejump_cloud_python_sdktypejumpcloud_google_emm_enrollment_typepy"></a>

##### enterprise_object_id: `str`<a id="enterprise_object_id-str"></a>

##### one_time_only: `bool`<a id="one_time_only-bool"></a>

##### provisioning_extras: [`JumpcloudGoogleEmmProvisioningExtras`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_provisioning_extras.py)<a id="provisioning_extras-jumpcloudgoogleemmprovisioningextrasjump_cloud_python_sdktypejumpcloud_google_emm_provisioning_extraspy"></a>


##### user_object_id: `str`<a id="user_object_id-str"></a>

##### zero_touch: `bool`<a id="zero_touch-bool"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`JumpcloudGoogleEmmCreateEnrollmentTokenRequest`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_create_enrollment_token_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmCreateEnrollmentTokenResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_create_enrollment_token_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/enrollment-tokens` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.create_enterprise`<a id="jumpcloudgoogle_emmcreate_enterprise"></a>

Creates a Google EMM enterprise.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/google-emm/enterprises \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{ 'signupUrlName': 'string', 'enrollmentToken': 'string' }' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_enterprise_response = jumpcloud.google_emm.create_enterprise(
    enrollment_token="string_example",
    signup_url_name="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### enrollment_token: `str`<a id="enrollment_token-str"></a>

##### signup_url_name: `str`<a id="signup_url_name-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`JumpcloudGoogleEmmCreateEnterpriseRequest`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_create_enterprise_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmEnterprise`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_enterprise.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/enterprises` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.create_enterprises_enrollment_token`<a id="jumpcloudgoogle_emmcreate_enterprises_enrollment_token"></a>

Gets an enrollment token to enroll a device into Google EMM.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/google-emm/enterpries/{enterprise_object_id}/enrollment-tokens \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_enterprises_enrollment_token_response = jumpcloud.google_emm.create_enterprises_enrollment_token(
    enterprise_object_id='YQ==',
    allow_personal_usage="PERSONAL_USAGE_ALLOWED",
    created_where="API",
    display_name="string_example",
    duration="string_example",
    enrollment_type="WORK_PROFILE",
    one_time_only=True,
    provisioning_extras={
        "wifi_security_type": "NONE",
    },
    user_object_id='YQ==',
    zero_touch=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### enterprise_object_id: `str`<a id="enterprise_object_id-str"></a>

##### allow_personal_usage: [`JumpcloudGoogleEmmAllowPersonalUsage`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_allow_personal_usage.py)<a id="allow_personal_usage-jumpcloudgoogleemmallowpersonalusagejump_cloud_python_sdktypejumpcloud_google_emm_allow_personal_usagepy"></a>

##### created_where: [`JumpcloudGoogleEmmCreatedWhere`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_created_where.py)<a id="created_where-jumpcloudgoogleemmcreatedwherejump_cloud_python_sdktypejumpcloud_google_emm_created_wherepy"></a>

##### display_name: `str`<a id="display_name-str"></a>

##### duration: `str`<a id="duration-str"></a>

##### enrollment_type: [`JumpcloudGoogleEmmEnrollmentType`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_enrollment_type.py)<a id="enrollment_type-jumpcloudgoogleemmenrollmenttypejump_cloud_python_sdktypejumpcloud_google_emm_enrollment_typepy"></a>

##### one_time_only: `bool`<a id="one_time_only-bool"></a>

##### provisioning_extras: [`JumpcloudGoogleEmmProvisioningExtras`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_provisioning_extras.py)<a id="provisioning_extras-jumpcloudgoogleemmprovisioningextrasjump_cloud_python_sdktypejumpcloud_google_emm_provisioning_extraspy"></a>


##### user_object_id: `str`<a id="user_object_id-str"></a>

##### zero_touch: `bool`<a id="zero_touch-bool"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`EnrollmentTokensCreateEnterprisesEnrollmentTokenRequest`](./jump_cloud_python_sdk/type/enrollment_tokens_create_enterprises_enrollment_token_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmEnrollmentToken`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_enrollment_token.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/enterprises/{enterpriseObjectId}/enrollment-tokens` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.create_web_token`<a id="jumpcloudgoogle_emmcreate_web_token"></a>

Creates a web token to access an embeddable managed Google Play web UI for a given Google EMM enterprise.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/google-emm/web-tokens \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_web_token_response = jumpcloud.google_emm.create_web_token(
    enterprise_object_id='YQ==',
    iframe_feature="SOFTWARE_MANAGEMENT",
    parent_frame_url="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### enterprise_object_id: `str`<a id="enterprise_object_id-str"></a>

##### iframe_feature: [`JumpcloudGoogleEmmFeature`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_feature.py)<a id="iframe_feature-jumpcloudgoogleemmfeaturejump_cloud_python_sdktypejumpcloud_google_emm_featurepy"></a>

##### parent_frame_url: `str`<a id="parent_frame_url-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`JumpcloudGoogleEmmCreateWebTokenRequest`](./jump_cloud_python_sdk/type/jumpcloud_google_emm_create_web_token_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmWebToken`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_web_token.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/web-tokens` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.delete_enrollment_token`<a id="jumpcloudgoogle_emmdelete_enrollment_token"></a>

Removes an Enrollment token for a given enterprise and token id.

#### Sample Request<a id="sample-request"></a>
```
curl -X DELETE https://console.jumpcloud.com/api/v2/enterprises/{enterprise_id}/enrollment-tokens/{token_id} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
delete_enrollment_token_response = jumpcloud.google_emm.delete_enrollment_token(
    enterprise_id='YQ==',
    token_id="tokenId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### enterprise_id: `str`<a id="enterprise_id-str"></a>

##### token_id: `str`<a id="token_id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmDeleteEnrollmentTokenResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_delete_enrollment_token_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/enterprises/{enterpriseId}/enrollment-tokens/{tokenId}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.delete_enterprise`<a id="jumpcloudgoogle_emmdelete_enterprise"></a>

Removes a Google EMM enterprise.

 Warning: This is a destructive operation and will remove all data associated with Google EMM enterprise from JumpCloud including devices and applications associated with the given enterprise.

#### Sample Request<a id="sample-request"></a>
```
curl -X DELETE https://console.jumpcloud.com/api/v2/google-emm/devices/{enterpriseId} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
delete_enterprise_response = jumpcloud.google_emm.delete_enterprise(
    enterprise_id='YQ==',
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### enterprise_id: `str`<a id="enterprise_id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/enterprises/{enterpriseId}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.erase_device`<a id="jumpcloudgoogle_emmerase_device"></a>

Removes the work profile and all policies from a personal/company-owned Android 8.0+ device. Company owned devices will be relinquished for personal use. Apps and data associated with the personal profile(s) are preserved.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/google-emm/devices/{deviceId}/erase-device \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
erase_device_response = jumpcloud.google_emm.erase_device(
    device_id='YQ==',
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### device_id: `str`<a id="device_id-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

`Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/devices/{deviceId}/erase-device` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.get_connection_status`<a id="jumpcloudgoogle_emmget_connection_status"></a>

Gives a connection status between JumpCloud and Google.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/google-emm/devices/{enterpriseId}/connection-status \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_connection_status_response = jumpcloud.google_emm.get_connection_status(
    enterprise_id='YQ==',
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### enterprise_id: `str`<a id="enterprise_id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmConnectionStatus`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_connection_status.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/enterprises/{enterpriseId}/connection-status` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.get_device`<a id="jumpcloudgoogle_emmget_device"></a>

Gets a Google EMM enrolled device details.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/google-emm/devices/{deviceId} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_device_response = jumpcloud.google_emm.get_device(
    device_id='YQ==',
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### device_id: `str`<a id="device_id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmDevice`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_device.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/devices/{deviceId}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.get_device_android_policy`<a id="jumpcloudgoogle_emmget_device_android_policy"></a>

Gets an android JSON policy for a Google EMM enrolled device.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/google-emm/devices/{deviceId}/policy_results \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_device_android_policy_response = jumpcloud.google_emm.get_device_android_policy(
    device_id='YQ==',
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### device_id: `str`<a id="device_id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmDeviceAndroidPolicy`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_device_android_policy.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/devices/{deviceId}/policy_results` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.list_devices`<a id="jumpcloudgoogle_emmlist_devices"></a>

Lists google EMM enrolled devices.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/google-emm/enterprises/{enterprise_object_id}/devices \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_devices_response = jumpcloud.google_emm.list_devices(
    enterprise_object_id='YQ==',
    limit="100",
    skip="0",
    filter=[
        "string_example"
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### enterprise_object_id: `str`<a id="enterprise_object_id-str"></a>

##### limit: `str`<a id="limit-str"></a>

The number of records to return at once. Limited to 100.

##### skip: `str`<a id="skip-str"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmListDevicesResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_list_devices_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/enterprises/{enterpriseObjectId}/devices` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.list_enrollment_tokens`<a id="jumpcloudgoogle_emmlist_enrollment_tokens"></a>

Lists active, unexpired enrollement tokens for a given enterprise.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/google-emm/enterprises/{enterprise_object_id}/enrollment-tokens \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_enrollment_tokens_response = jumpcloud.google_emm.list_enrollment_tokens(
    enterprise_object_id='YQ==',
    limit="100",
    skip="0",
    filter=[
        "string_example"
    ],
    sort="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### enterprise_object_id: `str`<a id="enterprise_object_id-str"></a>

##### limit: `str`<a id="limit-str"></a>

The number of records to return at once. Limited to 100.

##### skip: `str`<a id="skip-str"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

##### sort: `str`<a id="sort-str"></a>

Use space separated sort parameters to sort the collection. Default sort is ascending. Prefix with - to sort descending.

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmListEnrollmentTokensResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_list_enrollment_tokens_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/enterprises/{enterpriseObjectId}/enrollment-tokens` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.list_enterprises`<a id="jumpcloudgoogle_emmlist_enterprises"></a>

Lists all Google EMM enterprises. An empty list indicates that the Organization is not configured with a Google EMM enterprise yet. 

 Note: Currently only one Google Enterprise per Organization is supported.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/google-emm/enterprises \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_enterprises_response = jumpcloud.google_emm.list_enterprises(
    limit="100",
    skip="0",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### limit: `str`<a id="limit-str"></a>

The number of records to return at once. Limited to 100.

##### skip: `str`<a id="skip-str"></a>

The offset into the records to return.

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmListEnterprisesResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_list_enterprises_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/enterprises` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.lock_device`<a id="jumpcloudgoogle_emmlock_device"></a>

Locks a Google EMM enrolled device, as if the lock screen timeout had expired.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/google-emm/devices/{deviceId}/lock \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
lock_device_response = jumpcloud.google_emm.lock_device(
    device_id='YQ==',
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### device_id: `str`<a id="device_id-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

`Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/devices/{deviceId}/lock` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.patch_enterprise`<a id="jumpcloudgoogle_emmpatch_enterprise"></a>

Updates a Google EMM enterprise details.

#### Sample Request<a id="sample-request"></a>
```
curl -X PATCH https://console.jumpcloud.com/api/v2/google-emm/enterprises \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{ 'allowDeviceEnrollment': true, 'deviceGroupId': 'string' }' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
patch_enterprise_response = jumpcloud.google_emm.patch_enterprise(
    enterprise_id='YQ==',
    allow_device_enrollment=True,
    device_group_id='YQ==',
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### enterprise_id: `str`<a id="enterprise_id-str"></a>

##### allow_device_enrollment: `bool`<a id="allow_device_enrollment-bool"></a>

##### device_group_id: `str`<a id="device_group_id-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`EnterprisesPatchEnterpriseRequest`](./jump_cloud_python_sdk/type/enterprises_patch_enterprise_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudGoogleEmmEnterprise`](./jump_cloud_python_sdk/pydantic/jumpcloud_google_emm_enterprise.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/enterprises/{enterpriseId}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.reboot_device`<a id="jumpcloudgoogle_emmreboot_device"></a>

Reboots a Google EMM enrolled device. Only supported on fully managed devices running Android 7.0 or higher.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/google-emm/devices/{deviceId}/reboot \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
reboot_device_response = jumpcloud.google_emm.reboot_device(
    device_id='YQ==',
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### device_id: `str`<a id="device_id-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

`Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/devices/{deviceId}/reboot` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.google_emm.reset_password`<a id="jumpcloudgoogle_emmreset_password"></a>

Reset the user's password of a Google EMM enrolled device.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/google-emm/devices/{deviceId}/resetpassword \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{ 'new_password' : 'string' }' \
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
reset_password_response = jumpcloud.google_emm.reset_password(
    device_id='YQ==',
    flags=[
        "string_example"
    ],
    new_password="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### device_id: `str`<a id="device_id-str"></a>

##### flags: [`DevicesResetPasswordRequestFlags`](./jump_cloud_python_sdk/type/devices_reset_password_request_flags.py)<a id="flags-devicesresetpasswordrequestflagsjump_cloud_python_sdktypedevices_reset_password_request_flagspy"></a>

##### new_password: `str`<a id="new_password-str"></a>

Not logging as it contains sensitive information.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DevicesResetPasswordRequest`](./jump_cloud_python_sdk/type/devices_reset_password_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/google-emm/devices/{deviceId}/resetpassword` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.active_directory_associations_list`<a id="jumpcloudgraphactive_directory_associations_list"></a>

This endpoint returns the direct associations of this Active Directory instance.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Active Directory and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET 'https://console.jumpcloud.com/api/v2/activedirectories/{ActiveDirectory_ID}/associations?targets=user \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
active_directory_associations_list_response = jumpcloud.graph.active_directory_associations_list(
    activedirectory_id="activedirectory_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"active_directory\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphActiveDirectoryAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_active_directory_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.active_directory_associations_post`<a id="jumpcloudgraphactive_directory_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of an Active Directory instance.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Active Directory and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/activedirectories/{AD_Instance_ID}/associations \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user",
    "id": "{User_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.active_directory_associations_post(
    activedirectory_id="activedirectory_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"active_directory\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationActiveDirectory`](./jump_cloud_python_sdk/type/graph_operation_active_directory.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.active_directory_traverse_user`<a id="jumpcloudgraphactive_directory_traverse_user"></a>

This endpoint will return all Users bound to an Active Directory instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Active Directory instance to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this Active Directory instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/activedirectories/{ActiveDirectory_ID}/users \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
active_directory_traverse_user_response = jumpcloud.graph.active_directory_traverse_user(
    activedirectory_id="activedirectory_id_example",
    filter=[],
    limit=10,
    x_org_id="string_example",
    skip=0,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

ObjectID of the Active Directory instance.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphActiveDirectoryTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_active_directory_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.active_directory_traverse_user_group`<a id="jumpcloudgraphactive_directory_traverse_user_group"></a>

This endpoint will return all Users Groups bound to an Active Directory instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Active Directory instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this Active Directory instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/activedirectories/{ActiveDirectory_ID}/usergroups \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
active_directory_traverse_user_group_response = jumpcloud.graph.active_directory_traverse_user_group(
    activedirectory_id="activedirectory_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### activedirectory_id: `str`<a id="activedirectory_id-str"></a>

ObjectID of the Active Directory instance.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphActiveDirectoryTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_active_directory_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/activedirectories/{activedirectory_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.application_associations_list`<a id="jumpcloudgraphapplication_associations_list"></a>

This endpoint will return the _direct_ associations of an Application. A direct association can be a non-homogeneous relationship between 2 different objects, for example Applications and User Groups.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET 'https://console.jumpcloud.com/api/v2/applications/{Application_ID}/associations?targets=user_group \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
application_associations_list_response = jumpcloud.graph.application_associations_list(
    application_id="application_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

ObjectID of the Application.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"application\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphApplicationAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_application_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.application_associations_post`<a id="jumpcloudgraphapplication_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of an Application. A direct association can be a non-homogeneous relationship between 2 different objects, for example Application and User Groups.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST 'https://console.jumpcloud.com/api/v2/applications/{Application_ID}/associations' \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user_group",
    "id": "{Group_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.application_associations_post(
    application_id="application_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

ObjectID of the Application.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"application\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationApplication`](./jump_cloud_python_sdk/type/graph_operation_application.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.application_traverse_user`<a id="jumpcloudgraphapplication_traverse_user"></a>

This endpoint will return all Users bound to an Application, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Application to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this Application.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/applications/{Application_ID}/users \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
application_traverse_user_response = jumpcloud.graph.application_traverse_user(
    application_id="application_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

ObjectID of the Application.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphApplicationTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_application_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.application_traverse_user_group`<a id="jumpcloudgraphapplication_traverse_user_group"></a>

This endpoint will return all Users Groups bound to an Application, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates  each path from this Application to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this Application.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/applications/{Application_ID}/usergroups \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
application_traverse_user_group_response = jumpcloud.graph.application_traverse_user_group(
    application_id="application_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

ObjectID of the Application.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphApplicationTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_application_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.command_associations_list`<a id="jumpcloudgraphcommand_associations_list"></a>

This endpoint will return the _direct_ associations of this Command.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Commands and User Groups.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/commands/{Command_ID}/associations?targets=system_group \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
command_associations_list_response = jumpcloud.graph.command_associations_list(
    command_id="command_id_example",
    targets=[
        "system"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### command_id: `str`<a id="command_id-str"></a>

ObjectID of the Command.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"command\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphCommandAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_command_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/commands/{command_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.command_associations_post`<a id="jumpcloudgraphcommand_associations_post"></a>

This endpoint will allow you to manage the _direct_ associations of this Command.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Commands and User Groups.


#### Sample Request<a id="sample-request"></a>
```
 curl -X POST https://console.jumpcloud.com/api/v2/commands/{Command_ID}/associations \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system_group",
    "id": "Group_ID"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.command_associations_post(
    command_id="command_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### command_id: `str`<a id="command_id-str"></a>

ObjectID of the Command.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"command\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationCommand`](./jump_cloud_python_sdk/type/graph_operation_command.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/commands/{command_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.command_traverse_system`<a id="jumpcloudgraphcommand_traverse_system"></a>

This endpoint will return all Systems bound to a Command, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Command to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this Command.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/commands/{Command_ID}/systems \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
command_traverse_system_response = jumpcloud.graph.command_traverse_system(
    command_id="command_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### command_id: `str`<a id="command_id-str"></a>

ObjectID of the Command.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphCommandTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_command_traverse_system_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/commands/{command_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.command_traverse_system_group`<a id="jumpcloudgraphcommand_traverse_system_group"></a>

This endpoint will return all System Groups bound to a Command, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Command to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this Command.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/commands/{Command_ID}/systemgroups \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
command_traverse_system_group_response = jumpcloud.graph.command_traverse_system_group(
    command_id="command_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### command_id: `str`<a id="command_id-str"></a>

ObjectID of the Command.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphCommandTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_command_traverse_system_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/commands/{command_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.g_suite_associations_list`<a id="jumpcloudgraphg_suite_associations_list"></a>

This endpoint returns the _direct_ associations of this G Suite instance.

A direct association can be a non-homogeneous relationship between 2 different objects, for example G Suite and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET 'https://console.jumpcloud.com/api/v2/gsuites/{Gsuite_ID}/associations?targets=user_group \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
g_suite_associations_list_response = jumpcloud.graph.g_suite_associations_list(
    gsuite_id="gsuite_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

ObjectID of the G Suite instance.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"g_suite\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphGSuiteAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_g_suite_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.g_suite_associations_post`<a id="jumpcloudgraphg_suite_associations_post"></a>

This endpoint returns the _direct_ associations of this G Suite instance.

A direct association can be a non-homogeneous relationship between 2 different objects, for example G Suite and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/gsuites/{Gsuite_ID}/associations \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user_group",
    "id": "{Group_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.g_suite_associations_post(
    gsuite_id="gsuite_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

ObjectID of the G Suite instance.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"g_suite\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationGSuite`](./jump_cloud_python_sdk/type/graph_operation_g_suite.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.g_suite_traverse_user`<a id="jumpcloudgraphg_suite_traverse_user"></a>

This endpoint will return all Users bound to a G Suite instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this G Suite instance to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this G Suite instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
  curl -X GET https://console.jumpcloud.com/api/v2/gsuites/{Gsuite_ID}/users \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
g_suite_traverse_user_response = jumpcloud.graph.g_suite_traverse_user(
    gsuite_id="gsuite_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

ObjectID of the G Suite instance.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphGSuiteTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_g_suite_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.g_suite_traverse_user_group`<a id="jumpcloudgraphg_suite_traverse_user_group"></a>

This endpoint will return all User Groups bound to an G Suite instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this G Suite instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this G Suite instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
  curl -X GET https://console.jumpcloud.com/api/v2/gsuites/{GSuite_ID}/usergroups \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
g_suite_traverse_user_group_response = jumpcloud.graph.g_suite_traverse_user_group(
    gsuite_id="gsuite_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### gsuite_id: `str`<a id="gsuite_id-str"></a>

ObjectID of the G Suite instance.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphGSuiteTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_g_suite_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/gsuites/{gsuite_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.idp_routing_policy_associations_list`<a id="jumpcloudgraphidp_routing_policy_associations_list"></a>

This endpoint returns the _direct_ associations of a Routing Policy.

A direct association can be a non-homogeneous relationship between 2 different objects, for example a Routing Policy and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/identity-provider/policies/{IDP_ROUTING_POLICY_ID}/associations?targets=user_group \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
idp_routing_policy_associations_list_response = jumpcloud.graph.idp_routing_policy_associations_list(
    idp_routing_policy_id="idp_routing_policy_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### idp_routing_policy_id: `str`<a id="idp_routing_policy_id-str"></a>

ObjectID of the Routing Policy.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"idp_routing_policy\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphIdpRoutingPolicyAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_idp_routing_policy_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/identity-provider/policies/{idp_routing_policy_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.idp_routing_policy_associations_post`<a id="jumpcloudgraphidp_routing_policy_associations_post"></a>

This endpoint manages the _direct_ associations of a Routing Policy.

A direct association can be a non-homogeneous relationship between 2 different objects, for example a Routing Policy and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/identity-provider/policies/{IDP_ROUTING_POLICY_ID}/associations?targets=user \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  -d '{"type":"user", "id":"{USER_ID}", "op":"add"}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.idp_routing_policy_associations_post(
    idp_routing_policy_id="idp_routing_policy_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### idp_routing_policy_id: `str`<a id="idp_routing_policy_id-str"></a>

ObjectID of the Routing Policy.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which an \\\"idp_routing_policy\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationIDPRoutingPolicy`](./jump_cloud_python_sdk/type/graph_operation_idp_routing_policy.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/identity-provider/policies/{idp_routing_policy_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.idp_routing_policy_traverse_user`<a id="jumpcloudgraphidp_routing_policy_traverse_user"></a>

This endpoint will return all Users bound to a routing policy, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this routing policy to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this routing policy.

See `/members` and `/associations` endpoints to manage those collections.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/identity-provider/policies/{id}/associations/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
idp_routing_policy_traverse_user_response = jumpcloud.graph.idp_routing_policy_traverse_user(
    idp_routing_policy_id="idp_routing_policy_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### idp_routing_policy_id: `str`<a id="idp_routing_policy_id-str"></a>

ObjectID of the Routing Policy.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphIdpRoutingPolicyTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_idp_routing_policy_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/identity-provider/policies/{idp_routing_policy_id}/associations/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.idp_routing_policy_traverse_user_group`<a id="jumpcloudgraphidp_routing_policy_traverse_user_group"></a>

This endpoint will return all Users Groups bound to a routing policy, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this routing policy instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this routing policy.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/identity-provider/policies/{id}/associations/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
idp_routing_policy_traverse_user_group_response = jumpcloud.graph.idp_routing_policy_traverse_user_group(
    idp_routing_policy_id="idp_routing_policy_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### idp_routing_policy_id: `str`<a id="idp_routing_policy_id-str"></a>

ObjectID of the Routing Policy.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphIdpRoutingPolicyTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_idp_routing_policy_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/identity-provider/policies/{idp_routing_policy_id}/associations/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.ldap_server_associations_list`<a id="jumpcloudgraphldap_server_associations_list"></a>

This endpoint returns the _direct_ associations of this LDAP Server.

A direct association can be a non-homogeneous relationship between 2 different objects, for example LDAP and Users.

#### Sample Request<a id="sample-request"></a>

```
 curl -X GET 'https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/associations?targets=user_group \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
ldap_server_associations_list_response = jumpcloud.graph.ldap_server_associations_list(
    ldapserver_id="ldapserver_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### ldapserver_id: `str`<a id="ldapserver_id-str"></a>

ObjectID of the LDAP Server.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"ldap_server\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphLdapServerAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_ldap_server_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/ldapservers/{ldapserver_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.ldap_server_associations_post`<a id="jumpcloudgraphldap_server_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of a LDAP Server.

A direct association can be a non-homogeneous relationship between 2 different objects, for example LDAP and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user",
    "id": "{User_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.ldap_server_associations_post(
    ldapserver_id="ldapserver_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### ldapserver_id: `str`<a id="ldapserver_id-str"></a>

ObjectID of the LDAP Server.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"ldap_server\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationLdapServer`](./jump_cloud_python_sdk/type/graph_operation_ldap_server.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/ldapservers/{ldapserver_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.ldap_server_traverse_user`<a id="jumpcloudgraphldap_server_traverse_user"></a>

This endpoint will return all Users bound to an LDAP Server, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this LDAP server instance to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this LDAP server instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
ldap_server_traverse_user_response = jumpcloud.graph.ldap_server_traverse_user(
    ldapserver_id="ldapserver_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### ldapserver_id: `str`<a id="ldapserver_id-str"></a>

ObjectID of the LDAP Server.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphLdapServerTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_ldap_server_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/ldapservers/{ldapserver_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.ldap_server_traverse_user_group`<a id="jumpcloudgraphldap_server_traverse_user_group"></a>

This endpoint will return all Users Groups bound to a LDAP Server, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this LDAP server instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this LDAP server instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
ldap_server_traverse_user_group_response = jumpcloud.graph.ldap_server_traverse_user_group(
    ldapserver_id="ldapserver_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### ldapserver_id: `str`<a id="ldapserver_id-str"></a>

ObjectID of the LDAP Server.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphLdapServerTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_ldap_server_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/ldapservers/{ldapserver_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.office365_associations_list`<a id="jumpcloudgraphoffice365_associations_list"></a>

This endpoint returns _direct_ associations of an Office 365 instance.


A direct association can be a non-homogeneous relationship between 2 different objects, for example Office 365 and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET 'https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID}/associations?targets=user_group' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
office365_associations_list_response = jumpcloud.graph.office365_associations_list(
    office365_id="office365_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### office365_id: `str`<a id="office365_id-str"></a>

ObjectID of the Office 365 instance.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"office_365\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphOffice365AssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_office365_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/office365s/{office365_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.office365_associations_post`<a id="jumpcloudgraphoffice365_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of a Office 365 instance.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Office 365 and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user_group",
    "id": "{Group_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.office365_associations_post(
    office365_id="office365_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### office365_id: `str`<a id="office365_id-str"></a>

ObjectID of the Office 365 instance.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"office_365\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationOffice365`](./jump_cloud_python_sdk/type/graph_operation_office365.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/office365s/{office365_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.office365_traverse_user`<a id="jumpcloudgraphoffice365_traverse_user"></a>

This endpoint will return all Users bound to an Office 365 instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Office 365 instance to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this Office 365 instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID}/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
office365_traverse_user_response = jumpcloud.graph.office365_traverse_user(
    office365_id="office365_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### office365_id: `str`<a id="office365_id-str"></a>

ObjectID of the Office 365 suite.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphOffice365TraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_office365_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/office365s/{office365_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.office365_traverse_user_group`<a id="jumpcloudgraphoffice365_traverse_user_group"></a>

This endpoint will return all Users Groups bound to an Office 365 instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Office 365 instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this Office 365 instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
  curl -X GET https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
office365_traverse_user_group_response = jumpcloud.graph.office365_traverse_user_group(
    office365_id="office365_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### office365_id: `str`<a id="office365_id-str"></a>

ObjectID of the Office 365 suite.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphOffice365TraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_office365_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/office365s/{office365_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_associations_list`<a id="jumpcloudgraphpolicy_associations_list"></a>

This endpoint returns the _direct_ associations of a Policy.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Policies and Systems.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET 'https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/associations?targets=system_group \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
policy_associations_list_response = jumpcloud.graph.policy_associations_list(
    policy_id="policy_id_example",
    targets=[
        "system"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### policy_id: `str`<a id="policy_id-str"></a>

ObjectID of the Policy.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"policy\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphPolicyAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policies/{policy_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_associations_post`<a id="jumpcloudgraphpolicy_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of a Policy.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Policies and Systems.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/associations/ \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system_group",
    "id": "{Group_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.policy_associations_post(
    policy_id="policy_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### policy_id: `str`<a id="policy_id-str"></a>

ObjectID of the Policy.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"policy\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationPolicy`](./jump_cloud_python_sdk/type/graph_operation_policy.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policies/{policy_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_group_associations_list`<a id="jumpcloudgraphpolicy_group_associations_list"></a>

This endpoint returns the _direct_ associations of this Policy Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Policy Groups and Policies.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/associations?targets=system \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
policy_group_associations_list_response = jumpcloud.graph.policy_group_associations_list(
    group_id="group_id_example",
    targets=[
        "system"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the Policy Group.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"policy_group\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphPolicyGroupAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policygroups/{group_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_group_associations_post`<a id="jumpcloudgraphpolicy_group_associations_post"></a>

This endpoint manages the _direct_ associations of this Policy Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Policy Groups and Policies.


#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system",
    "id": "{SystemID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.policy_group_associations_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the Policy Group.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"policy_group\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationPolicyGroup`](./jump_cloud_python_sdk/type/graph_operation_policy_group.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policygroups/{group_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_group_members_list`<a id="jumpcloudgraphpolicy_group_members_list"></a>

This endpoint returns the Policy members of a Policy Group.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
policy_group_members_list_response = jumpcloud.graph.policy_group_members_list(
    group_id="group_id_example",
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the Policy Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphPolicyGroupMembersListResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_members_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policygroups/{group_id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_group_members_post`<a id="jumpcloudgraphpolicy_group_members_post"></a>

This endpoint allows you to manage the Policy members of a Policy Group.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "policy",
    "id": "{Policy_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.policy_group_members_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="policy",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the Policy Group.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

The member type.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationPolicyGroupMember`](./jump_cloud_python_sdk/type/graph_operation_policy_group_member.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policygroups/{group_id}/members` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_group_membership`<a id="jumpcloudgraphpolicy_group_membership"></a>

This endpoint returns all Policy members that are a member of this Policy Group.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/membership \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
policy_group_membership_response = jumpcloud.graph.policy_group_membership(
    group_id="group_id_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the Policy Group.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphPolicyGroupMembershipResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_membership_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policygroups/{group_id}/membership` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_group_traverse_system`<a id="jumpcloudgraphpolicy_group_traverse_system"></a>

This endpoint will return all Systems bound to a Policy Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Policy Group to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this Policy Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
policy_group_traverse_system_response = jumpcloud.graph.policy_group_traverse_system(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the Policy Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphPolicyGroupTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_traverse_system_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policygroups/{group_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_group_traverse_system_group`<a id="jumpcloudgraphpolicy_group_traverse_system_group"></a>

This endpoint will return all System Groups bound to a Policy Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Policy Group to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this Policy Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
policy_group_traverse_system_group_response = jumpcloud.graph.policy_group_traverse_system_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the Policy Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphPolicyGroupTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_traverse_system_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policygroups/{group_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_member_of`<a id="jumpcloudgraphpolicy_member_of"></a>

This endpoint returns all the Policy Groups a Policy is a member of.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/memberof \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
policy_member_of_response = jumpcloud.graph.policy_member_of(
    policy_id="policy_id_example",
    filter=[],
    limit=10,
    skip=0,
    date="string_example",
    authorization="string_example",
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### policy_id: `str`<a id="policy_id-str"></a>

ObjectID of the Policy.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### date: `str`<a id="date-str"></a>

Current date header for the System Context API

##### authorization: `str`<a id="authorization-str"></a>

Authorization header for the System Context API

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphPolicyMemberOfResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_member_of_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policies/{policy_id}/memberof` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_traverse_system`<a id="jumpcloudgraphpolicy_traverse_system"></a>

This endpoint will return all Systems bound to a Policy, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Policy to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this Policy.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
policy_traverse_system_response = jumpcloud.graph.policy_traverse_system(
    policy_id="policy_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### policy_id: `str`<a id="policy_id-str"></a>

ObjectID of the Command.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphPolicyTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_traverse_system_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policies/{policy_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.policy_traverse_system_group`<a id="jumpcloudgraphpolicy_traverse_system_group"></a>

This endpoint will return all Systems Groups bound to a Policy, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Policy to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this Policy.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET  https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
policy_traverse_system_group_response = jumpcloud.graph.policy_traverse_system_group(
    policy_id="policy_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### policy_id: `str`<a id="policy_id-str"></a>

ObjectID of the Command.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphPolicyTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_traverse_system_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/policies/{policy_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.radius_server_associations_list`<a id="jumpcloudgraphradius_server_associations_list"></a>

This endpoint returns the _direct_ associations of a Radius Server.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Radius Servers and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/radiusservers/{RADIUS_ID}/associations?targets=user_group \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
radius_server_associations_list_response = jumpcloud.graph.radius_server_associations_list(
    radiusserver_id="radiusserver_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### radiusserver_id: `str`<a id="radiusserver_id-str"></a>

ObjectID of the Radius Server.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"radius_server\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphRadiusServerAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_radius_server_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/radiusservers/{radiusserver_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.radius_server_associations_post`<a id="jumpcloudgraphradius_server_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of a Radius Server.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Radius Servers and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/radiusservers/{RADIUS_ID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{

	
"type":"user", 
"id":"{USER_ID}", 
"op":"add"
	
}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.radius_server_associations_post(
    radiusserver_id="radiusserver_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### radiusserver_id: `str`<a id="radiusserver_id-str"></a>

ObjectID of the Radius Server.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"radius_server\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationRadiusServer`](./jump_cloud_python_sdk/type/graph_operation_radius_server.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/radiusservers/{radiusserver_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.radius_server_traverse_user`<a id="jumpcloudgraphradius_server_traverse_user"></a>

This endpoint will return all Users bound to a RADIUS Server, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this RADIUS server instance to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this RADIUS server instance.

See `/members` and `/associations` endpoints to manage those collections.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
radius_server_traverse_user_response = jumpcloud.graph.radius_server_traverse_user(
    radiusserver_id="radiusserver_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### radiusserver_id: `str`<a id="radiusserver_id-str"></a>

ObjectID of the Radius Server.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphRadiusServerTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_radius_server_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/radiusservers/{radiusserver_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.radius_server_traverse_user_group`<a id="jumpcloudgraphradius_server_traverse_user_group"></a>

This endpoint will return all Users Groups bound to a RADIUS Server, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this RADIUS server instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this RADIUS server instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/radiusservers/{RADIUS_ID}/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
radius_server_traverse_user_group_response = jumpcloud.graph.radius_server_traverse_user_group(
    radiusserver_id="radiusserver_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### radiusserver_id: `str`<a id="radiusserver_id-str"></a>

ObjectID of the Radius Server.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphRadiusServerTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_radius_server_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/radiusservers/{radiusserver_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.softwareapps_associations_list`<a id="jumpcloudgraphsoftwareapps_associations_list"></a>

This endpoint will return the _direct_ associations of a Software Application. A direct association can be a non-homogeneous relationship between 2 different objects, for example Software Application and System Groups.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/softwareapps/{software_app_id}/associations?targets=system_group \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
softwareapps_associations_list_response = jumpcloud.graph.softwareapps_associations_list(
    software_app_id="software_app_id_example",
    targets=[
        "system"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### software_app_id: `str`<a id="software_app_id-str"></a>

ObjectID of the Software App.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"software_app\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSoftwareappsAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_softwareapps_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/softwareapps/{software_app_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.softwareapps_associations_post`<a id="jumpcloudgraphsoftwareapps_associations_post"></a>

This endpoint allows you to associate or disassociate a software application to a system or system group.

#### Sample Request<a id="sample-request"></a>
```
$ curl -X POST https://console.jumpcloud.com/api/v2/softwareapps/{software_app_id}/associations \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'x-api-key: {API_KEY}' \
-d '{
  "id": "<object_id>",
  "op": "add",
  "type": "system"
 }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.softwareapps_associations_post(
    software_app_id="software_app_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### software_app_id: `str`<a id="software_app_id-str"></a>

ObjectID of the Software App.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"software_app\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationSoftwareApp`](./jump_cloud_python_sdk/type/graph_operation_software_app.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/softwareapps/{software_app_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.softwareapps_traverse_system`<a id="jumpcloudgraphsoftwareapps_traverse_system"></a>

This endpoint will return all Systems bound to a Software App, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Software App to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this Software App.

See `/associations` endpoint to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/softwareapps/{software_app_id}/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
softwareapps_traverse_system_response = jumpcloud.graph.softwareapps_traverse_system(
    software_app_id="software_app_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### software_app_id: `str`<a id="software_app_id-str"></a>

ObjectID of the Software App.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSoftwareappsTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_softwareapps_traverse_system_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/softwareapps/{software_app_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.softwareapps_traverse_system_group`<a id="jumpcloudgraphsoftwareapps_traverse_system_group"></a>

This endpoint will return all Systems Groups bound to a Software App, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Software App to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this Software App.

See `/associations` endpoint to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET  https://console.jumpcloud.com/api/v2/softwareapps/{software_app_id}/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
softwareapps_traverse_system_group_response = jumpcloud.graph.softwareapps_traverse_system_group(
    software_app_id="software_app_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### software_app_id: `str`<a id="software_app_id-str"></a>

ObjectID of the Software App.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSoftwareappsTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_softwareapps_traverse_system_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/softwareapps/{software_app_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_associations_list`<a id="jumpcloudgraphsystem_associations_list"></a>

This endpoint returns the _direct_ associations of a System.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Systems and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/associations?targets=user \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_associations_list_response = jumpcloud.graph.system_associations_list(
    system_id="system_id_example",
    targets=[
        "command"
    ],
    limit=10,
    skip=0,
    date="string_example",
    authorization="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### system_id: `str`<a id="system_id-str"></a>

ObjectID of the System.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"system\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### date: `str`<a id="date-str"></a>

Current date header for the System Context API

##### authorization: `str`<a id="authorization-str"></a>

Authorization header for the System Context API

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_system_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systems/{system_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_associations_post`<a id="jumpcloudgraphsystem_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of a System.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Systems and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/systems/{System_ID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "attributes": {
      "sudo": {
        "enabled": true,
        "withoutPassword": false
      }
    },
    "op": "add",
    "type": "user",
    "id": "UserID"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.system_associations_post(
    system_id="system_id_example",
    id="string_example",
    op="add",
    attributes=None,
    type="command",
    date="string_example",
    authorization="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### system_id: `str`<a id="system_id-str"></a>

ObjectID of the System.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: Union[[`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py), `GraphAttributeSudo`]<a id="attributes-uniongraphattributesjump_cloud_python_sdktypegraph_attributespy-graphattributesudo"></a>


##### type: `str`<a id="type-str"></a>

Targets which a \\\"system\\\" can be associated to.

##### date: `str`<a id="date-str"></a>

Current date header for the System Context API

##### authorization: `str`<a id="authorization-str"></a>

Authorization header for the System Context API

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationSystem`](./jump_cloud_python_sdk/type/graph_operation_system.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systems/{system_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_group_associations_list`<a id="jumpcloudgraphsystem_group_associations_list"></a>

This endpoint returns the _direct_ associations of a System Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example System Groups and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/associations?targets=user \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_group_associations_list_response = jumpcloud.graph.system_group_associations_list(
    group_id="group_id_example",
    targets=[
        "command"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the System Group.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"system_group\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemGroupAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systemgroups/{group_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_group_associations_post`<a id="jumpcloudgraphsystem_group_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of a System Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example System Groups and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user",
    "id": "{UserID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.system_group_associations_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="command",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the System Group.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"system_group\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationSystemGroup`](./jump_cloud_python_sdk/type/graph_operation_system_group.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systemgroups/{group_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_group_members_list`<a id="jumpcloudgraphsystem_group_members_list"></a>

This endpoint returns the system members of a System Group.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_group_members_list_response = jumpcloud.graph.system_group_members_list(
    group_id="group_id_example",
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the System Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemGroupMembersListResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_members_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systemgroups/{group_id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_group_members_post`<a id="jumpcloudgraphsystem_group_members_post"></a>

This endpoint allows you to manage the system members of a System Group.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system",
    "id": "{System_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.system_group_members_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    date="string_example",
    authorization="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the System Group.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

The member type.

##### date: `str`<a id="date-str"></a>

Current date header for the System Context API

##### authorization: `str`<a id="authorization-str"></a>

Authorization header for the System Context API

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationSystemGroupMember`](./jump_cloud_python_sdk/type/graph_operation_system_group_member.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systemgroups/{group_id}/members` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_group_membership`<a id="jumpcloudgraphsystem_group_membership"></a>

This endpoint returns all Systems that are a member of this System Group.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID/membership \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_group_membership_response = jumpcloud.graph.system_group_membership(
    group_id="group_id_example",
    limit=10,
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the System Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemGroupMembershipResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_membership_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systemgroups/{group_id}/membership` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_group_traverse_command`<a id="jumpcloudgraphsystem_group_traverse_command"></a>

This endpoint will return all Commands bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding Command; this array represents all grouping and/or associations that would have to be removed to deprovision the Command from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/commands \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_group_traverse_command_response = jumpcloud.graph.system_group_traverse_command(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
    details="v1",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the System Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### details: `str`<a id="details-str"></a>

This will provide detail descriptive response for the request.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemGroupTraverseCommandResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_command_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systemgroups/{group_id}/commands` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_group_traverse_policy`<a id="jumpcloudgraphsystem_group_traverse_policy"></a>

This endpoint will return all Policies bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding Policy; this array represents all grouping and/or associations that would have to be removed to deprovision the Policy from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

This endpoint is not public yet as we haven't finished the code.

##### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/policies \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_group_traverse_policy_response = jumpcloud.graph.system_group_traverse_policy(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the System Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemGroupTraversePolicyResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_policy_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systemgroups/{group_id}/policies` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_group_traverse_policy_group`<a id="jumpcloudgraphsystem_group_traverse_policy_group"></a>

This endpoint will return all Policy Groups bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding Policy Group; this array represents all grouping and/or associations that would have to be removed to deprovision the Policy Group from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/policygroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_group_traverse_policy_group_response = jumpcloud.graph.system_group_traverse_policy_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the System Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemGroupTraversePolicyGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_policy_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systemgroups/{group_id}/policygroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_group_traverse_user`<a id="jumpcloudgraphsystem_group_traverse_user"></a>

This endpoint will return all Users bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_group_traverse_user_response = jumpcloud.graph.system_group_traverse_user(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the System Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemGroupTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systemgroups/{group_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_group_traverse_user_group`<a id="jumpcloudgraphsystem_group_traverse_user_group"></a>

This endpoint will return all User Groups bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_group_traverse_user_group_response = jumpcloud.graph.system_group_traverse_user_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the System Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemGroupTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systemgroups/{group_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_member_of`<a id="jumpcloudgraphsystem_member_of"></a>

This endpoint returns all the System Groups a System is a member of.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/memberof \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_member_of_response = jumpcloud.graph.system_member_of(
    system_id="system_id_example",
    filter=[],
    limit=10,
    skip=0,
    date="string_example",
    authorization="string_example",
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### system_id: `str`<a id="system_id-str"></a>

ObjectID of the System.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### date: `str`<a id="date-str"></a>

Current date header for the System Context API

##### authorization: `str`<a id="authorization-str"></a>

Authorization header for the System Context API

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemMemberOfResponse`](./jump_cloud_python_sdk/pydantic/graph_system_member_of_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systems/{system_id}/memberof` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_traverse_command`<a id="jumpcloudgraphsystem_traverse_command"></a>

This endpoint will return all Commands bound to a System, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System to the corresponding Command; this array represents all grouping and/or associations that would have to be removed to deprovision the Command from this System.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/commands \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_traverse_command_response = jumpcloud.graph.system_traverse_command(
    system_id="system_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
    details="v1",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### system_id: `str`<a id="system_id-str"></a>

ObjectID of the System.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### details: `str`<a id="details-str"></a>

This will provide detail descriptive response for the request.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemTraverseCommandResponse`](./jump_cloud_python_sdk/pydantic/graph_system_traverse_command_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systems/{system_id}/commands` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_traverse_policy`<a id="jumpcloudgraphsystem_traverse_policy"></a>

This endpoint will return all Policies bound to a System, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System to the corresponding Policy; this array represents all grouping and/or associations that would have to be removed to deprovision the Policy from this System.

See `/members` and `/associations` endpoints to manage those collections.

This endpoint is not yet public as we have finish the code.

##### Sample Request<a id="sample-request"></a>

```
curl -X GET https://console.jumpcloud.com/api/v2/{System_ID}/policies \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_traverse_policy_response = jumpcloud.graph.system_traverse_policy(
    system_id="system_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### system_id: `str`<a id="system_id-str"></a>

ObjectID of the System.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemTraversePolicyResponse`](./jump_cloud_python_sdk/pydantic/graph_system_traverse_policy_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systems/{system_id}/policies` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_traverse_policy_group`<a id="jumpcloudgraphsystem_traverse_policy_group"></a>

This endpoint will return all Policy Groups bound to a System, either directly or indirectly essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System to the corresponding Policy Group; this array represents all grouping and/or associations that would have to be removed to deprovision the Policy Group from this System.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/policygroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_traverse_policy_group_response = jumpcloud.graph.system_traverse_policy_group(
    system_id="system_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    date="string_example",
    authorization="string_example",
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### system_id: `str`<a id="system_id-str"></a>

ObjectID of the System.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### date: `str`<a id="date-str"></a>

Current date header for the System Context API

##### authorization: `str`<a id="authorization-str"></a>

Authorization header for the System Context API

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemTraversePolicyGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_system_traverse_policy_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systems/{system_id}/policygroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_traverse_user`<a id="jumpcloudgraphsystem_traverse_user"></a>

This endpoint will return all Users bound to a System, either directly or indirectly essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this System.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_traverse_user_response = jumpcloud.graph.system_traverse_user(
    system_id="system_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    date="string_example",
    authorization="string_example",
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### system_id: `str`<a id="system_id-str"></a>

ObjectID of the System.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### date: `str`<a id="date-str"></a>

Current date header for the System Context API

##### authorization: `str`<a id="authorization-str"></a>

Authorization header for the System Context API

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_system_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systems/{system_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.system_traverse_user_group`<a id="jumpcloudgraphsystem_traverse_user_group"></a>

This endpoint will return all User Groups bound to a System, either directly or indirectly essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this System.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
system_traverse_user_group_response = jumpcloud.graph.system_traverse_user_group(
    system_id="system_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    date="string_example",
    authorization="string_example",
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### system_id: `str`<a id="system_id-str"></a>

ObjectID of the System.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### date: `str`<a id="date-str"></a>

Current date header for the System Context API

##### authorization: `str`<a id="authorization-str"></a>

Authorization header for the System Context API

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphSystemTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_system_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systems/{system_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.systems_list`<a id="jumpcloudgraphsystems_list"></a>

This endpoint returns the policy results for a particular system.

##### Sample Request<a id="sample-request"></a>

```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/policystatuses \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
systems_list_response = jumpcloud.graph.systems_list(
    system_id="system_id_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### system_id: `str`<a id="system_id-str"></a>

ObjectID of the System.

##### fields: List[`str`]<a id="fields-liststr"></a>

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`PolicystatusesSystemsListResponse`](./jump_cloud_python_sdk/pydantic/policystatuses_systems_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systems/{system_id}/policystatuses` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_associations_list`<a id="jumpcloudgraphuser_associations_list"></a>

This endpoint returns the _direct_ associations of a User.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Users and Systems.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/associations?targets=system_group \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_associations_list_response = jumpcloud.graph.user_associations_list(
    user_id="user_id_example",
    targets=[
        "active_directory"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"user\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_user_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_associations_post`<a id="jumpcloudgraphuser_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of a User.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Users and Systems.


#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/users/{UserID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "attributes": {
      "sudo": {
      "enabled": true,
        "withoutPassword": false
      }
    },
    "op": "add",
    "type": "system_group",
    "id": "{GroupID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.user_associations_post(
    user_id="user_id_example",
    id="string_example",
    op="add",
    attributes=None,
    type="active_directory",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: Union[[`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py), `GraphAttributeSudo`]<a id="attributes-uniongraphattributesjump_cloud_python_sdktypegraph_attributespy-graphattributesudo"></a>


##### type: `str`<a id="type-str"></a>

Targets which a \\\"user\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationUser`](./jump_cloud_python_sdk/type/graph_operation_user.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_associations_list`<a id="jumpcloudgraphuser_group_associations_list"></a>

This endpoint returns the _direct_ associations of this User Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example User Groups and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/associations?targets=system \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_associations_list_response = jumpcloud.graph.user_group_associations_list(
    group_id="group_id_example",
    targets=[
        "active_directory"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"user_group\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_associations_post`<a id="jumpcloudgraphuser_group_associations_post"></a>

This endpoint manages the _direct_ associations of this User Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example User Groups and Users.


#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system",
    "id": "{SystemID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.user_group_associations_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="active_directory",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"user_group\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationUserGroup`](./jump_cloud_python_sdk/type/graph_operation_user_group.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_members_list`<a id="jumpcloudgraphuser_group_members_list"></a>

This endpoint returns the user members of a User Group.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_members_list_response = jumpcloud.graph.user_group_members_list(
    group_id="group_id_example",
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupMembersListResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_members_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_members_post`<a id="jumpcloudgraphuser_group_members_post"></a>

This endpoint allows you to manage the user members of a User Group.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user",
    "id": "{User_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.graph.user_group_members_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

The member type.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationUserGroupMember`](./jump_cloud_python_sdk/type/graph_operation_user_group_member.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/members` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_membership`<a id="jumpcloudgraphuser_group_membership"></a>

This endpoint returns all users members that are a member of this User Group.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/membership \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_membership_response = jumpcloud.graph.user_group_membership(
    group_id="group_id_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupMembershipResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_membership_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/membership` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_traverse_active_directory`<a id="jumpcloudgraphuser_group_traverse_active_directory"></a>

This endpoint will return all Active Directory Instances bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Active Directory; this array represents all grouping and/or associations that would have to be removed to deprovision the Active Directory from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/activedirectories \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_traverse_active_directory_response = jumpcloud.graph.user_group_traverse_active_directory(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupTraverseActiveDirectoryResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_active_directory_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/activedirectories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_traverse_application`<a id="jumpcloudgraphuser_group_traverse_application"></a>

This endpoint will return all Applications bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Application; this array represents all grouping and/or associations that would have to be removed to deprovision the Application from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/applications \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_traverse_application_response = jumpcloud.graph.user_group_traverse_application(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupTraverseApplicationResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_application_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/applications` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_traverse_directory`<a id="jumpcloudgraphuser_group_traverse_directory"></a>

This endpoint will return all Directories bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Directory; this array represents all grouping and/or associations that would have to be removed to deprovision the Directories from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/directories \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_traverse_directory_response = jumpcloud.graph.user_group_traverse_directory(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupTraverseDirectoryResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_directory_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/directories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_traverse_g_suite`<a id="jumpcloudgraphuser_group_traverse_g_suite"></a>

This endpoint will return all G Suite Instances bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding G Suite instance; this array represents all grouping and/or associations that would have to be removed to deprovision the G Suite instance from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID/gsuites \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_traverse_g_suite_response = jumpcloud.graph.user_group_traverse_g_suite(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupTraverseGSuiteResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_g_suite_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/gsuites` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_traverse_ldap_server`<a id="jumpcloudgraphuser_group_traverse_ldap_server"></a>

This endpoint will return all LDAP Servers bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding LDAP Server; this array represents all grouping and/or associations that would have to be removed to deprovision the LDAP Server from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/ldapservers \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_traverse_ldap_server_response = jumpcloud.graph.user_group_traverse_ldap_server(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupTraverseLdapServerResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_ldap_server_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/ldapservers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_traverse_office365`<a id="jumpcloudgraphuser_group_traverse_office365"></a>

This endpoint will return all Office 365 instances bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Office 365 instance; this array represents all grouping and/or associations that would have to be removed to deprovision the Office 365 instance from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/office365s \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_traverse_office365_response = jumpcloud.graph.user_group_traverse_office365(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupTraverseOffice365Response`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_office365_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/office365s` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_traverse_radius_server`<a id="jumpcloudgraphuser_group_traverse_radius_server"></a>

This endpoint will return all RADIUS servers bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding RADIUS Server; this array represents all grouping and/or associations that would have to be removed to deprovision the RADIUS Server from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/radiusservers \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_traverse_radius_server_response = jumpcloud.graph.user_group_traverse_radius_server(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupTraverseRadiusServerResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_radius_server_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/radiusservers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_traverse_system`<a id="jumpcloudgraphuser_group_traverse_system"></a>

This endpoint will return all Systems bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_traverse_system_response = jumpcloud.graph.user_group_traverse_system(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_system_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_group_traverse_system_group`<a id="jumpcloudgraphuser_group_traverse_system_group"></a>

This endpoint will return all System Groups bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_group_traverse_system_group_response = jumpcloud.graph.user_group_traverse_system_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### group_id: `str`<a id="group_id-str"></a>

ObjectID of the User Group.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserGroupTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_system_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/usergroups/{group_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_member_of`<a id="jumpcloudgraphuser_member_of"></a>

This endpoint returns all the User Groups a User is a member of.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/memberof \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_member_of_response = jumpcloud.graph.user_member_of(
    user_id="user_id_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserMemberOfResponse`](./jump_cloud_python_sdk/pydantic/graph_user_member_of_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/memberof` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_traverse_active_directory`<a id="jumpcloudgraphuser_traverse_active_directory"></a>

This endpoint will return all Active Directory Instances bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding Active Directory instance; this array represents all grouping and/or associations that would have to be removed to deprovision the Active Directory instance from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/activedirectories \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_traverse_active_directory_response = jumpcloud.graph.user_traverse_active_directory(
    user_id="user_id_example",
    filter=[],
    limit=10,
    x_org_id="string_example",
    skip=0,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserTraverseActiveDirectoryResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_active_directory_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/activedirectories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_traverse_application`<a id="jumpcloudgraphuser_traverse_application"></a>

This endpoint will return all Applications bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding Application; this array represents all grouping and/or associations that would have to be removed to deprovision the Application from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/applications \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_traverse_application_response = jumpcloud.graph.user_traverse_application(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserTraverseApplicationResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_application_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/applications` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_traverse_directory`<a id="jumpcloudgraphuser_traverse_directory"></a>

This endpoint will return all Directories bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding Directory; this array represents all grouping and/or associations that would have to be removed to deprovision the Directory from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/directories \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_traverse_directory_response = jumpcloud.graph.user_traverse_directory(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserTraverseDirectoryResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_directory_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/directories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_traverse_g_suite`<a id="jumpcloudgraphuser_traverse_g_suite"></a>

This endpoint will return all G-Suite Instances bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding G Suite instance; this array represents all grouping and/or associations that would have to be removed to deprovision the G Suite instance from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/gsuites \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_traverse_g_suite_response = jumpcloud.graph.user_traverse_g_suite(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserTraverseGSuiteResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_g_suite_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/gsuites` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_traverse_ldap_server`<a id="jumpcloudgraphuser_traverse_ldap_server"></a>

This endpoint will return all LDAP Servers bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding LDAP Server; this array represents all grouping and/or associations that would have to be removed to deprovision the LDAP Server from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/ldapservers \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_traverse_ldap_server_response = jumpcloud.graph.user_traverse_ldap_server(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserTraverseLdapServerResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_ldap_server_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/ldapservers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_traverse_office365`<a id="jumpcloudgraphuser_traverse_office365"></a>

This endpoint will return all Office 365 Instances bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding Office 365 instance; this array represents all grouping and/or associations that would have to be removed to deprovision the Office 365 instance from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/office365s \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_traverse_office365_response = jumpcloud.graph.user_traverse_office365(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserTraverseOffice365Response`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_office365_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/office365s` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_traverse_radius_server`<a id="jumpcloudgraphuser_traverse_radius_server"></a>

This endpoint will return all RADIUS Servers bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding RADIUS Server; this array represents all grouping and/or associations that would have to be removed to deprovision the RADIUS Server from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/radiusservers \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_traverse_radius_server_response = jumpcloud.graph.user_traverse_radius_server(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserTraverseRadiusServerResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_radius_server_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/radiusservers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_traverse_system`<a id="jumpcloudgraphuser_traverse_system"></a>

This endpoint will return all Systems bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/systems\
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_traverse_system_response = jumpcloud.graph.user_traverse_system(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_system_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.graph.user_traverse_system_group`<a id="jumpcloudgraphuser_traverse_system_group"></a>

This endpoint will return all System Groups bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/systemgroups\
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
user_traverse_system_group_response = jumpcloud.graph.user_traverse_system_group(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### user_id: `str`<a id="user_id-str"></a>

ObjectID of the User.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphUserTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_system_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{user_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.groups.list`<a id="jumpcloudgroupslist"></a>

This endpoint returns all Groups that exist in your organization.

#### Available filter fields:<a id="available-filter-fields"></a>
  - `name`
  - `disabled`
  - `type`

#### Sample Request<a id="sample-request"></a>

```
  curl -X GET \
  https://console.jumpcloud.com/api/v2/groups \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = jumpcloud.groups.list(
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
    x_unfiltered_total_count=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### fields: List[`str`]<a id="fields-liststr"></a>

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### x_unfiltered_total_count: `int`<a id="x_unfiltered_total_count-int"></a>

If provided in the request with any non-empty value, this header will be returned on the response populated with the total count of objects without filters taken into account

#### 🔄 Return<a id="🔄-return"></a>

[`GroupsListResponse`](./jump_cloud_python_sdk/pydantic/groups_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/groups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ip_lists.delete`<a id="jumpcloudip_listsdelete"></a>

Delete a specific IP list.

#### Sample Request<a id="sample-request"></a>
```
curl -X DELETE https://console.jumpcloud.com/api/v2/iplists/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
delete_response = jumpcloud.ip_lists.delete(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`IPList`](./jump_cloud_python_sdk/pydantic/ip_list.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/iplists/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ip_lists.get`<a id="jumpcloudip_listsget"></a>

Return a specific IP list.

#### Sample Request<a id="sample-request"></a>
```
curl https://console.jumpcloud.com/api/v2/iplists/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = jumpcloud.ip_lists.get(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`IPList`](./jump_cloud_python_sdk/pydantic/ip_list.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/iplists/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ip_lists.list`<a id="jumpcloudip_listslist"></a>

Retrieve all IP lists.

#### Sample Request<a id="sample-request"></a>
```
curl https://console.jumpcloud.com/api/v2/iplists \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = jumpcloud.ip_lists.list(
    x_org_id="string_example",
    x_total_count=1,
    limit=10,
    skip=0,
    filter=[],
    sort=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### x_total_count: `int`<a id="x_total_count-int"></a>

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### sort: List[`str`]<a id="sort-liststr"></a>

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return<a id="🔄-return"></a>

[`IplistsListResponse`](./jump_cloud_python_sdk/pydantic/iplists_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/iplists` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ip_lists.patch`<a id="jumpcloudip_listspatch"></a>

Update a specific IP list.

#### Sample Request<a id="sample-request"></a>
```
curl -X PATCH https://console.jumpcloud.com/api/v2/iplists/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{"name": "New IP List Name"}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
patch_response = jumpcloud.ip_lists.patch(
    id="id_example",
    description="string_example",
    ips=[
        "string_example"
    ],
    name="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### description: `str`<a id="description-str"></a>

##### ips: [`IPListRequestIps`](./jump_cloud_python_sdk/type/ip_list_request_ips.py)<a id="ips-iplistrequestipsjump_cloud_python_sdktypeip_list_request_ipspy"></a>

##### name: `str`<a id="name-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`IPListRequest`](./jump_cloud_python_sdk/type/ip_list_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`IPList`](./jump_cloud_python_sdk/pydantic/ip_list.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/iplists/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ip_lists.post`<a id="jumpcloudip_listspost"></a>

Create an IP list.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/iplists \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "Sample IP List",
    "ips": [
      "192.168.10.12",
      "192.168.10.20 - 192.168.10.30",
      "123.225.10.0/32"
    ]
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
post_response = jumpcloud.ip_lists.post(
    description="string_example",
    ips=[
        "string_example"
    ],
    name="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

##### ips: [`IPListRequestIps`](./jump_cloud_python_sdk/type/ip_list_request_ips.py)<a id="ips-iplistrequestipsjump_cloud_python_sdktypeip_list_request_ipspy"></a>

##### name: `str`<a id="name-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`IPListRequest`](./jump_cloud_python_sdk/type/ip_list_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`IPList`](./jump_cloud_python_sdk/pydantic/ip_list.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/iplists` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ip_lists.put`<a id="jumpcloudip_listsput"></a>

Replace a specific IP list.

#### Sample Request<a id="sample-request"></a>
```
curl -X PUT https://console.jumpcloud.com/api/v2/iplists/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "Sample IP List",
    "ips": [
      "192.168.10.10"
    ]
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
put_response = jumpcloud.ip_lists.put(
    id="id_example",
    description="string_example",
    ips=[
        "string_example"
    ],
    name="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### description: `str`<a id="description-str"></a>

##### ips: [`IPListRequestIps`](./jump_cloud_python_sdk/type/ip_list_request_ips.py)<a id="ips-iplistrequestipsjump_cloud_python_sdktypeip_list_request_ipspy"></a>

##### name: `str`<a id="name-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`IPListRequest`](./jump_cloud_python_sdk/type/ip_list_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`IPList`](./jump_cloud_python_sdk/pydantic/ip_list.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/iplists/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.identity_providers.idp_routing_policy_associations_list`<a id="jumpcloudidentity_providersidp_routing_policy_associations_list"></a>

This endpoint returns the _direct_ associations of a Routing Policy.

A direct association can be a non-homogeneous relationship between 2 different objects, for example a Routing Policy and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/identity-provider/policies/{IDP_ROUTING_POLICY_ID}/associations?targets=user_group \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
idp_routing_policy_associations_list_response = jumpcloud.identity_providers.idp_routing_policy_associations_list(
    idp_routing_policy_id="idp_routing_policy_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### idp_routing_policy_id: `str`<a id="idp_routing_policy_id-str"></a>

ObjectID of the Routing Policy.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"idp_routing_policy\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphIdpRoutingPolicyAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_idp_routing_policy_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/identity-provider/policies/{idp_routing_policy_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.identity_providers.idp_routing_policy_associations_post`<a id="jumpcloudidentity_providersidp_routing_policy_associations_post"></a>

This endpoint manages the _direct_ associations of a Routing Policy.

A direct association can be a non-homogeneous relationship between 2 different objects, for example a Routing Policy and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/identity-provider/policies/{IDP_ROUTING_POLICY_ID}/associations?targets=user \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  -d '{"type":"user", "id":"{USER_ID}", "op":"add"}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.identity_providers.idp_routing_policy_associations_post(
    idp_routing_policy_id="idp_routing_policy_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### idp_routing_policy_id: `str`<a id="idp_routing_policy_id-str"></a>

ObjectID of the Routing Policy.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which an \\\"idp_routing_policy\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationIDPRoutingPolicy`](./jump_cloud_python_sdk/type/graph_operation_idp_routing_policy.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/identity-provider/policies/{idp_routing_policy_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.identity_providers.idp_routing_policy_traverse_user`<a id="jumpcloudidentity_providersidp_routing_policy_traverse_user"></a>

This endpoint will return all Users bound to a routing policy, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this routing policy to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this routing policy.

See `/members` and `/associations` endpoints to manage those collections.


#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/identity-provider/policies/{id}/associations/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
idp_routing_policy_traverse_user_response = jumpcloud.identity_providers.idp_routing_policy_traverse_user(
    idp_routing_policy_id="idp_routing_policy_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### idp_routing_policy_id: `str`<a id="idp_routing_policy_id-str"></a>

ObjectID of the Routing Policy.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphIdpRoutingPolicyTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_idp_routing_policy_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/identity-provider/policies/{idp_routing_policy_id}/associations/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.identity_providers.idp_routing_policy_traverse_user_group`<a id="jumpcloudidentity_providersidp_routing_policy_traverse_user_group"></a>

This endpoint will return all Users Groups bound to a routing policy, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this routing policy instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this routing policy.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/identity-provider/policies/{id}/associations/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
idp_routing_policy_traverse_user_group_response = jumpcloud.identity_providers.idp_routing_policy_traverse_user_group(
    idp_routing_policy_id="idp_routing_policy_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### idp_routing_policy_id: `str`<a id="idp_routing_policy_id-str"></a>

ObjectID of the Routing Policy.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphIdpRoutingPolicyTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_idp_routing_policy_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/identity-provider/policies/{idp_routing_policy_id}/associations/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.image.delete_logo`<a id="jumpcloudimagedelete_logo"></a>

Deletes the specified image from an application

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.image.delete_logo(
    application_id="application_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_id: `str`<a id="application_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/applications/{application_id}/logo` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ingresso.create_access_request`<a id="jumpcloudingressocreate_access_request"></a>

Endpoint for adding a new access request

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_access_request_response = jumpcloud.ingresso.create_access_request(
    operation_id="string_example",
    additional_attributes={},
    application_int_id="string_example",
    expiry="1970-01-01T00:00:00.00Z",
    organization_object_id='YQ==',
    remarks="string_example",
    requestor_id="string_example",
    resource_id="string_example",
    resource_type="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### operation_id: `str`<a id="operation_id-str"></a>

##### additional_attributes: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="additional_attributes-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

##### application_int_id: `str`<a id="application_int_id-str"></a>

##### expiry: `datetime`<a id="expiry-datetime"></a>

##### organization_object_id: `str`<a id="organization_object_id-str"></a>

##### remarks: `str`<a id="remarks-str"></a>

##### requestor_id: `str`<a id="requestor_id-str"></a>

##### resource_id: `str`<a id="resource_id-str"></a>

##### resource_type: `str`<a id="resource_type-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`JumpcloudIngressoCreateAccessRequestsRequest`](./jump_cloud_python_sdk/type/jumpcloud_ingresso_create_access_requests_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudIngressoCreateAccessRequestsResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_ingresso_create_access_requests_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/accessrequests` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ingresso.get_access_request`<a id="jumpcloudingressoget_access_request"></a>

Endpoint for getting all access requests by access id

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_access_request_response = jumpcloud.ingresso.get_access_request(
    access_id="accessId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### access_id: `str`<a id="access_id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`JumpcloudIngressoGetAccessRequestResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_ingresso_get_access_request_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/accessrequests/{accessId}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ingresso.revoke_access_request`<a id="jumpcloudingressorevoke_access_request"></a>

Endpoint for revoking access request by id

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
revoke_access_request_response = jumpcloud.ingresso.revoke_access_request(
    access_id="accessId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### access_id: `str`<a id="access_id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/accessrequests/{accessId}/revoke` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ingresso.update_access_request`<a id="jumpcloudingressoupdate_access_request"></a>

Endpoint for updating access request by id

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_access_request_response = jumpcloud.ingresso.update_access_request(
    access_id="accessId_example",
    additional_attributes={},
    expiry="1970-01-01T00:00:00.00Z",
    organization_object_id='YQ==',
    remarks="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### access_id: `str`<a id="access_id-str"></a>

##### additional_attributes: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="additional_attributes-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

##### expiry: `datetime`<a id="expiry-datetime"></a>

##### organization_object_id: `str`<a id="organization_object_id-str"></a>

##### remarks: `str`<a id="remarks-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AccessRequestApiUpdateAccessRequestRequest`](./jump_cloud_python_sdk/type/access_request_api_update_access_request_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/accessrequests/{accessId}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ldap_servers.get`<a id="jumpcloudldap_serversget"></a>

This endpoint returns a specific LDAP server.

##### Sample Request<a id="sample-request"></a>

```
 curl -X GET https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = jumpcloud.ldap_servers.get(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

Unique identifier of the LDAP server.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`LdapServer`](./jump_cloud_python_sdk/pydantic/ldap_server.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/ldapservers/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ldap_servers.ldap_server_associations_list`<a id="jumpcloudldap_serversldap_server_associations_list"></a>

This endpoint returns the _direct_ associations of this LDAP Server.

A direct association can be a non-homogeneous relationship between 2 different objects, for example LDAP and Users.

#### Sample Request<a id="sample-request"></a>

```
 curl -X GET 'https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/associations?targets=user_group \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
ldap_server_associations_list_response = jumpcloud.ldap_servers.ldap_server_associations_list(
    ldapserver_id="ldapserver_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### ldapserver_id: `str`<a id="ldapserver_id-str"></a>

ObjectID of the LDAP Server.

##### targets: List[`str`]<a id="targets-liststr"></a>

Targets which a \"ldap_server\" can be associated to.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`GraphLdapServerAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_ldap_server_associations_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/ldapservers/{ldapserver_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ldap_servers.ldap_server_associations_post`<a id="jumpcloudldap_serversldap_server_associations_post"></a>

This endpoint allows you to manage the _direct_ associations of a LDAP Server.

A direct association can be a non-homogeneous relationship between 2 different objects, for example LDAP and Users.

#### Sample Request<a id="sample-request"></a>
```
curl -X POST https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user",
    "id": "{User_ID}"
  }'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
jumpcloud.ldap_servers.ldap_server_associations_post(
    ldapserver_id="ldapserver_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### ldapserver_id: `str`<a id="ldapserver_id-str"></a>

ObjectID of the LDAP Server.

##### id: `str`<a id="id-str"></a>

The ObjectID of graph object being added or removed as an association.

##### op: `str`<a id="op-str"></a>

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)<a id="attributes-graphattributesjump_cloud_python_sdktypegraph_attributespy"></a>

##### type: `str`<a id="type-str"></a>

Targets which a \\\"ldap_server\\\" can be associated to.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`GraphOperationLdapServer`](./jump_cloud_python_sdk/type/graph_operation_ldap_server.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/ldapservers/{ldapserver_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ldap_servers.ldap_server_traverse_user`<a id="jumpcloudldap_serversldap_server_traverse_user"></a>

This endpoint will return all Users bound to an LDAP Server, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this LDAP server instance to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this LDAP server instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
ldap_server_traverse_user_response = jumpcloud.ldap_servers.ldap_server_traverse_user(
    ldapserver_id="ldapserver_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### ldapserver_id: `str`<a id="ldapserver_id-str"></a>

ObjectID of the LDAP Server.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphLdapServerTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_ldap_server_traverse_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/ldapservers/{ldapserver_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ldap_servers.ldap_server_traverse_user_group`<a id="jumpcloudldap_serversldap_server_traverse_user_group"></a>

This endpoint will return all Users Groups bound to a LDAP Server, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this LDAP server instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this LDAP server instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request<a id="sample-request"></a>
```
curl -X GET https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
ldap_server_traverse_user_group_response = jumpcloud.ldap_servers.ldap_server_traverse_user_group(
    ldapserver_id="ldapserver_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### ldapserver_id: `str`<a id="ldapserver_id-str"></a>

ObjectID of the LDAP Server.

##### limit: `int`<a id="limit-int"></a>

The number of records to return at once. Limited to 100.

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

##### skip: `int`<a id="skip-int"></a>

The offset into the records to return.

##### filter: List[`str`]<a id="filter-liststr"></a>

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return<a id="🔄-return"></a>

[`GraphLdapServerTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_ldap_server_traverse_user_group_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/ldapservers/{ldapserver_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ldap_servers.list`<a id="jumpcloudldap_serverslist"></a>

This endpoint returns the object IDs of your LDAP servers.


##### Sample Request<a id="sample-request"></a>

```
  curl -X GET https://console.jumpcloud.com/api/v2/ldapservers/ \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

#### 🛠️ Usage

```python
list_response = jumpcloud.ldap_servers.list(
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`LdapserversListResponse`](./jump_cloud_python_sdk/pydantic/ldapservers_list_response.py)

#### 🌐 Endpoint

`/ldapservers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.ldap_servers.patch`

This endpoint allows updating some attributes of an LDAP server.

Sample Request

```
curl -X PATCH https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "userLockoutAction": "remove",
    "userPasswordExpirationAction": "disable"
  }'
```

#### 🛠️ Usage

```python
patch_response = jumpcloud.ldap_servers.patch(
    id="id_example",
    id="string_example",
    user_lockout_action="disable",
    user_password_expiration_action="disable",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

Unique identifier of the LDAP server.

##### id: `str`

##### user_lockout_action: [`LdapServerAction`](./jump_cloud_python_sdk/type/ldap_server_action.py)

##### user_password_expiration_action: [`LdapServerAction`](./jump_cloud_python_sdk/type/ldap_server_action.py)

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`LdapserversPatchRequest`](./jump_cloud_python_sdk/type/ldapservers_patch_request.py)
#### 🔄 Return

[`LdapserversPatchResponse`](./jump_cloud_python_sdk/pydantic/ldapservers_patch_response.py)

#### 🌐 Endpoint

`/ldapservers/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.logos.get`

Return the logo image associated with the specified id

#### 🛠️ Usage

```python
get_response = jumpcloud.logos.get(
    id="id_example",
)
```

#### ⚙️ Parameters

##### id: `str`

#### 🌐 Endpoint

`/logos/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.cases_metadata`

This endpoint returns the metadata for cases

#### 🛠️ Usage

```python
cases_metadata_response = jumpcloud.managed_service_provider.cases_metadata()
```

#### 🔄 Return

[`CasesMetadataResponse`](./jump_cloud_python_sdk/pydantic/cases_metadata_response.py)

#### 🌐 Endpoint

`/cases/metadata` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.create_by_administrator`

This endpoint allows you to grant Administrator access to an Organization.

#### 🛠️ Usage

```python
create_by_administrator_response = jumpcloud.managed_service_provider.create_by_administrator(
    id="id_example",
    organization="6230a0d26a4e4bc86c6b36f1",
)
```

#### ⚙️ Parameters

##### id: `str`

##### organization: `str`

The identifier for an organization to link this administrator to.

#### ⚙️ Request Body

[`AdministratorOrganizationLinkReq`](./jump_cloud_python_sdk/type/administrator_organization_link_req.py)
#### 🔄 Return

[`AdministratorOrganizationLink`](./jump_cloud_python_sdk/pydantic/administrator_organization_link.py)

#### 🌐 Endpoint

`/administrators/{id}/organizationlinks` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.create_org`

This endpoint creates a new organization under the provider

#### 🛠️ Usage

```python
create_org_response = jumpcloud.managed_service_provider.create_org(
    provider_id="provider_id_example",
    max_system_users=10,
    name="Acme Inc",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### max_system_users: `int`

The maximum number of users allowed in this organization. Requires organizations.billing scope to modify.

##### name: `str`

#### ⚙️ Request Body

[`CreateOrganization`](./jump_cloud_python_sdk/type/create_organization.py)
#### 🔄 Return

[`Organization`](./jump_cloud_python_sdk/pydantic/organization.py)

#### 🌐 Endpoint

`/providers/{provider_id}/organizations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.delete`

Deletes a Policy Group Template.

#### 🛠️ Usage

```python
jumpcloud.managed_service_provider.delete(
    provider_id="provider_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.get`

Retrieves a Policy Group Template for this provider.

#### 🛠️ Usage

```python
get_response = jumpcloud.managed_service_provider.get(
    provider_id="provider_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🔄 Return

[`PolicyGroupTemplate`](./jump_cloud_python_sdk/pydantic/policy_group_template.py)

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.get_configured_policy_template`

Retrieves a Configured Policy Templates for this provider and Id.

#### 🛠️ Usage

```python
get_configured_policy_template_response = jumpcloud.managed_service_provider.get_configured_policy_template(
    provider_id="provider_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/providers/{provider_id}/configuredpolicytemplates/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.get_provider`

This endpoint returns details about a provider

#### 🛠️ Usage

```python
get_provider_response = jumpcloud.managed_service_provider.get_provider(
    provider_id="provider_id_example",
    fields=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

#### 🔄 Return

[`Provider`](./jump_cloud_python_sdk/pydantic/provider.py)

#### 🌐 Endpoint

`/providers/{provider_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.list`

Retrieves a list of Policy Group Templates for this provider.

#### 🛠️ Usage

```python
list_response = jumpcloud.managed_service_provider.list(
    provider_id="provider_id_example",
    fields=[],
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`PolicyGroupTemplates`](./jump_cloud_python_sdk/pydantic/policy_group_templates.py)

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.list_administrators`

This endpoint returns a list of the Administrators associated with the Provider. You must be associated with the provider to use this route.

#### 🛠️ Usage

```python
list_administrators_response = jumpcloud.managed_service_provider.list_administrators(
    provider_id="provider_id_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    sort_ignore_case=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### sort_ignore_case: List[`str`]

The comma separated fields used to sort the collection, ignoring case. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`ProvidersListAdministratorsResponse`](./jump_cloud_python_sdk/pydantic/providers_list_administrators_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/administrators` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.list_by_administrator`

This endpoint returns the association links between an Administrator and Organizations.

#### 🛠️ Usage

```python
list_by_administrator_response = jumpcloud.managed_service_provider.list_by_administrator(
    id="id_example",
    limit=10,
    skip=0,
)
```

#### ⚙️ Parameters

##### id: `str`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

#### 🔄 Return

[`AdministratorOrganizationsListByAdministratorResponse`](./jump_cloud_python_sdk/pydantic/administrator_organizations_list_by_administrator_response.py)

#### 🌐 Endpoint

`/administrators/{id}/organizationlinks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.list_by_organization`

This endpoint returns the association links between an Organization and Administrators.

#### 🛠️ Usage

```python
list_by_organization_response = jumpcloud.managed_service_provider.list_by_organization(
    id="id_example",
    limit=10,
    skip=0,
)
```

#### ⚙️ Parameters

##### id: `str`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

#### 🔄 Return

[`AdministratorOrganizationsListByOrganizationResponse`](./jump_cloud_python_sdk/pydantic/administrator_organizations_list_by_organization_response.py)

#### 🌐 Endpoint

`/organizations/{id}/administratorlinks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.list_configured_policy_templates`

Retrieves a list of Configured Policy Templates for this provider.

#### 🛠️ Usage

```python
list_configured_policy_templates_response = jumpcloud.managed_service_provider.list_configured_policy_templates(
    provider_id="provider_id_example",
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`PolicyGroupTemplatesListConfiguredPolicyTemplatesResponse`](./jump_cloud_python_sdk/pydantic/policy_group_templates_list_configured_policy_templates_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/configuredpolicytemplates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.list_members`

Retrieves a Policy Group Template's Members.

#### 🛠️ Usage

```python
list_members_response = jumpcloud.managed_service_provider.list_members(
    provider_id="provider_id_example",
    id="id_example",
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`PolicyGroupTemplateMembers`](./jump_cloud_python_sdk/pydantic/policy_group_template_members.py)

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates/{id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.list_organizations`

This endpoint returns a list of the Organizations associated with the Provider. You must be associated with the provider to use this route.

#### 🛠️ Usage

```python
list_organizations_response = jumpcloud.managed_service_provider.list_organizations(
    provider_id="provider_id_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    sort_ignore_case=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### sort_ignore_case: List[`str`]

The comma separated fields used to sort the collection, ignoring case. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`ProvidersListOrganizationsResponse`](./jump_cloud_python_sdk/pydantic/providers_list_organizations_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/organizations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.post_admins`

This endpoint allows you to create a provider administrator. You must be associated with the provider to use this route. You must provide either `role` or `roleName`.

#### 🛠️ Usage

```python
post_admins_response = jumpcloud.managed_service_provider.post_admins(
    email="joe@example.com",
    provider_id="provider_id_example",
    api_key_allowed=True,
    bind_no_orgs=False,
    enable_multi_factor=True,
    firstname="Joe",
    lastname="Blough",
    role="5c3536e9e0a6840001872799",
    role_name="Administrator",
)
```

#### ⚙️ Parameters

##### email: `str`

##### provider_id: `str`

##### api_key_allowed: `bool`

##### bind_no_orgs: `bool`

##### enable_multi_factor: `bool`

##### firstname: `str`

##### lastname: `str`

##### role: `str`

##### role_name: `str`

#### ⚙️ Request Body

[`ProviderAdminReq`](./jump_cloud_python_sdk/type/provider_admin_req.py)
#### 🔄 Return

[`Administrator`](./jump_cloud_python_sdk/pydantic/administrator.py)

#### 🌐 Endpoint

`/providers/{provider_id}/administrators` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.provider_list_case`

This endpoint returns the cases (Support/Feature requests) for the provider

#### 🛠️ Usage

```python
provider_list_case_response = jumpcloud.managed_service_provider.provider_list_case(
    provider_id="provider_id_example",
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`CasesResponse`](./jump_cloud_python_sdk/pydantic/cases_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/cases` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.remove_by_administrator`

This endpoint removes the association link between an Administrator and an Organization.

#### 🛠️ Usage

```python
jumpcloud.managed_service_provider.remove_by_administrator(
    administrator_id="administrator_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### administrator_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/administrators/{administrator_id}/organizationlinks/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.retrieve_invoice`

Retrieves an invoice for this provider. You must be associated to the provider to use this endpoint.

#### 🛠️ Usage

```python
retrieve_invoice_response = jumpcloud.managed_service_provider.retrieve_invoice(
    provider_id="provider_id_example",
    id="ID_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/providers/{provider_id}/invoices/{ID}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.retrieve_invoices`

Retrieves a list of invoices for this provider. You must be associated to the provider to use this endpoint.

#### 🛠️ Usage

```python
retrieve_invoices_response = jumpcloud.managed_service_provider.retrieve_invoices(
    provider_id="provider_id_example",
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`ProviderInvoiceResponse`](./jump_cloud_python_sdk/pydantic/provider_invoice_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/invoices` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.managed_service_provider.update_org`

This endpoint updates a provider's organization

#### 🛠️ Usage

```python
update_org_response = jumpcloud.managed_service_provider.update_org(
    provider_id="provider_id_example",
    id="id_example",
    id="624d9eae6849cf3b3f93dc56",
    max_system_users=1,
    name="Acme Inc",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

##### id: `str`

##### max_system_users: `int`

The maximum number of users allowed in this organization. Requires organizations.billing scope to modify.

##### name: `str`

#### ⚙️ Request Body

[`Organization`](./jump_cloud_python_sdk/type/organization.py)
#### 🔄 Return

[`Organization`](./jump_cloud_python_sdk/pydantic/organization.py)

#### 🌐 Endpoint

`/providers/{provider_id}/organizations/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.microsoft_mdm.download_config_files`

This endpoint allows you to download the config file.

#### 🛠️ Usage

```python
download_config_files_response = jumpcloud.microsoft_mdm.download_config_files(
)
```

#### ⚙️ Request Body

`Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`
#### 🌐 Endpoint

`/microsoft-mdm/configuration-files` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.delete`

Delete a domain from a specific M365/Azure AD directory sync integration instance.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID}/domains/{DOMAIN_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
delete_response = jumpcloud.office_365.delete(
    office365_id='YQ==',
    domain_id='YQ==',
)
```

#### ⚙️ Parameters

##### office365_id: `str`

Id for the specific M365/Azure AD directory sync integration instance.

##### domain_id: `str`

ObjectID of the domain to be deleted.

#### 🔄 Return

[`O365DomainResponse`](./jump_cloud_python_sdk/pydantic/o365_domain_response.py)

#### 🌐 Endpoint

`/office365s/{office365_id}/domains/{domain_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.get`

This endpoint returns a specific Office 365 instance.

#####

Sample Request

```
curl -X GET https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
get_response = jumpcloud.office_365.get(
    office365_id="office365_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### office365_id: `str`

ObjectID of the Office 365 instance.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`Office365`](./jump_cloud_python_sdk/pydantic/office365.py)

#### 🌐 Endpoint

`/office365s/{office365_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.insert`

Add a domain to a specific M365/Azure AD directory sync integration instance. The domain must be a verified domain in M365/Azure AD.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID}/domains \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{"domain": "{domain name}"}'
```

#### 🛠️ Usage

```python
insert_response = jumpcloud.office_365.insert(
    office365_id='YQ==',
    domain="string_example",
)
```

#### ⚙️ Parameters

##### office365_id: `str`

Id for the specific M365/Azure AD directory sync integration instance.

##### domain: `str`

#### ⚙️ Request Body

[`DomainsInsertRequest`](./jump_cloud_python_sdk/type/domains_insert_request.py)
#### 🔄 Return

[`O365DomainResponse`](./jump_cloud_python_sdk/pydantic/o365_domain_response.py)

#### 🌐 Endpoint

`/office365s/{office365_id}/domains` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.list`

List the domains configured for a specific M365/Azure AD directory sync integration instance.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID}/domains \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
list_response = jumpcloud.office_365.list(
    office365_id='YQ==',
    limit="100",
    skip="0",
)
```

#### ⚙️ Parameters

##### office365_id: `str`

Id for the specific M365/Azure AD directory sync integration instance.

##### limit: `str`

The number of records to return at once. Limited to 100.

##### skip: `str`

The offset into the records to return.

#### 🔄 Return

[`O365DomainsListResponse`](./jump_cloud_python_sdk/pydantic/o365_domains_list_response.py)

#### 🌐 Endpoint

`/office365s/{office365_id}/domains` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.list_import_users`

Lists Office 365 users available for import.

#### 🛠️ Usage

```python
list_import_users_response = jumpcloud.office_365.list_import_users(
    office365_id="office365_id_example",
    consistency_level="string_example",
    top=1,
    skip_token="string_example",
    filter="string_example",
    search="string_example",
    orderby="string_example",
    count=True,
)
```

#### ⚙️ Parameters

##### office365_id: `str`

##### consistency_level: `str`

Defines the consistency header for O365 requests. See https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http#request-headers

##### top: `int`

Office 365 API maximum number of results per page. See https://docs.microsoft.com/en-us/graph/paging.

##### skip_token: `str`

Office 365 API token used to access the next page of results. See https://docs.microsoft.com/en-us/graph/paging.

##### filter: `str`

Office 365 API filter parameter. See https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http#optional-query-parameters.

##### search: `str`

Office 365 API search parameter. See https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http#optional-query-parameters.

##### orderby: `str`

Office 365 API orderby parameter. See https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http#optional-query-parameters.

##### count: `bool`

Office 365 API count parameter. See https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http#optional-query-parameters.

#### 🔄 Return

[`Office365SListImportUsersResponse`](./jump_cloud_python_sdk/pydantic/office365_s_list_import_users_response.py)

#### 🌐 Endpoint

`/office365s/{office365_id}/import/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.office365_associations_list`

This endpoint returns _direct_ associations of an Office 365 instance.


A direct association can be a non-homogeneous relationship between 2 different objects, for example Office 365 and Users.

#### Sample Request
```
curl -X GET 'https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID}/associations?targets=user_group' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
office365_associations_list_response = jumpcloud.office_365.office365_associations_list(
    office365_id="office365_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### office365_id: `str`

ObjectID of the Office 365 instance.

##### targets: List[`str`]

Targets which a \"office_365\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphOffice365AssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_office365_associations_list_response.py)

#### 🌐 Endpoint

`/office365s/{office365_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.office365_associations_post`

This endpoint allows you to manage the _direct_ associations of a Office 365 instance.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Office 365 and Users.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user_group",
    "id": "{Group_ID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.office_365.office365_associations_post(
    office365_id="office365_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### office365_id: `str`

ObjectID of the Office 365 instance.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

Targets which a \\\"office_365\\\" can be associated to.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationOffice365`](./jump_cloud_python_sdk/type/graph_operation_office365.py)
#### 🌐 Endpoint

`/office365s/{office365_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.office365_delete`

This endpoint allows you to delete a translation rule for a specific Office 365 instance. These rules specify how JumpCloud attributes translate to [Microsoft Graph](https://developer.microsoft.com/en-us/graph) attributes.

#### Sample Request

```
curl -X DELETE https://console.jumpcloud.com/api/v2/office365s/{office365_id}/translationrules/{id} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
jumpcloud.office_365.office365_delete(
    office365_id="office365_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### office365_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/office365s/{office365_id}/translationrules/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.office365_get`

This endpoint returns a specific translation rule for a specific Office 365 instance. These rules specify how JumpCloud attributes translate to [Microsoft Graph](https://developer.microsoft.com/en-us/graph) attributes.

###### Sample Request

```
  curl -X GET https://console.jumpcloud.com/api/v2/office365s/{office365_id}/translationrules/{id} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
office365_get_response = jumpcloud.office_365.office365_get(
    office365_id="office365_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### office365_id: `str`

##### id: `str`

#### 🔄 Return

[`Office365TranslationRule`](./jump_cloud_python_sdk/pydantic/office365_translation_rule.py)

#### 🌐 Endpoint

`/office365s/{office365_id}/translationrules/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.office365_list`

This endpoint returns all translation rules for a specific Office 365 instance. These rules specify how JumpCloud attributes translate to [Microsoft Graph](https://developer.microsoft.com/en-us/graph) attributes.

##### Sample Request

```
 curl -X GET  https://console.jumpcloud.com/api/v2/office365s/{office365_id}/translationrules \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
office365_list_response = jumpcloud.office_365.office365_list(
    office365_id="office365_id_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### office365_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`TranslationRulesOffice365ListResponse`](./jump_cloud_python_sdk/pydantic/translation_rules_office365_list_response.py)

#### 🌐 Endpoint

`/office365s/{office365_id}/translationrules` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.office365_post`

This endpoint allows you to create a translation rule for a specific Office 365 instance. These rules specify how JumpCloud attributes translate to [Microsoft Graph](https://developer.microsoft.com/en-us/graph) attributes.

##### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/office365s/{office365_id}/translationrules \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    {Translation Rule Parameters}
  }'
```

#### 🛠️ Usage

```python
office365_post_response = jumpcloud.office_365.office365_post(
    office365_id="office365_id_example",
    built_in="user_department",
    direction="export",
)
```

#### ⚙️ Parameters

##### office365_id: `str`

##### built_in: [`Office365BuiltinTranslation`](./jump_cloud_python_sdk/type/office365_builtin_translation.py)

##### direction: [`Office365DirectionTranslation`](./jump_cloud_python_sdk/type/office365_direction_translation.py)

#### ⚙️ Request Body

[`Office365TranslationRuleRequest`](./jump_cloud_python_sdk/type/office365_translation_rule_request.py)
#### 🔄 Return

[`Office365TranslationRule`](./jump_cloud_python_sdk/pydantic/office365_translation_rule.py)

#### 🌐 Endpoint

`/office365s/{office365_id}/translationrules` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.office365_traverse_user`

This endpoint will return all Users bound to an Office 365 instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Office 365 instance to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this Office 365 instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID}/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
office365_traverse_user_response = jumpcloud.office_365.office365_traverse_user(
    office365_id="office365_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### office365_id: `str`

ObjectID of the Office 365 suite.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphOffice365TraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_office365_traverse_user_response.py)

#### 🌐 Endpoint

`/office365s/{office365_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.office365_traverse_user_group`

This endpoint will return all Users Groups bound to an Office 365 instance, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Office 365 instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this Office 365 instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
  curl -X GET https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
office365_traverse_user_group_response = jumpcloud.office_365.office365_traverse_user_group(
    office365_id="office365_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### office365_id: `str`

ObjectID of the Office 365 suite.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphOffice365TraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_office365_traverse_user_group_response.py)

#### 🌐 Endpoint

`/office365s/{office365_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365.patch`

This endpoint allows updating some attributes of an Office 365 instance.

#####

Sample Request

```
curl -X PATCH https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "userLockoutAction": "maintain",
    "userPasswordExpirationAction": "suspend",
  }'
```

Sample Request, set a default domain

```
curl -X PATCH https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "defaultDomain": {
        "id": "{domainObjectID}"
      }
  }'
```

Sample Request, unset the default domain

```
curl -X PATCH https://console.jumpcloud.com/api/v2/office365s/{OFFICE365_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "defaultDomain": {}
  }'
```

#### 🛠️ Usage

```python
patch_response = jumpcloud.office_365.patch(
    office365_id="office365_id_example",
    default_domain={
    },
    groups_enabled=True,
    id="string_example",
    name="string_example",
    user_lockout_action="suspend",
    user_password_expiration_action="suspend",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### office365_id: `str`

ObjectID of the Office 365 instance.

##### default_domain: [`DefaultDomain`](./jump_cloud_python_sdk/type/default_domain.py)


##### groups_enabled: `bool`

##### id: `str`

##### name: `str`

##### user_lockout_action: `str`

##### user_password_expiration_action: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`Office365`](./jump_cloud_python_sdk/type/office365.py)
#### 🔄 Return

[`Office365`](./jump_cloud_python_sdk/pydantic/office365.py)

#### 🌐 Endpoint

`/office365s/{office365_id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.office_365_import.list_import_users`

Lists Office 365 users available for import.

#### 🛠️ Usage

```python
list_import_users_response = jumpcloud.office_365_import.list_import_users(
    office365_id="office365_id_example",
    consistency_level="string_example",
    top=1,
    skip_token="string_example",
    filter="string_example",
    search="string_example",
    orderby="string_example",
    count=True,
)
```

#### ⚙️ Parameters

##### office365_id: `str`

##### consistency_level: `str`

Defines the consistency header for O365 requests. See https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http#request-headers

##### top: `int`

Office 365 API maximum number of results per page. See https://docs.microsoft.com/en-us/graph/paging.

##### skip_token: `str`

Office 365 API token used to access the next page of results. See https://docs.microsoft.com/en-us/graph/paging.

##### filter: `str`

Office 365 API filter parameter. See https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http#optional-query-parameters.

##### search: `str`

Office 365 API search parameter. See https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http#optional-query-parameters.

##### orderby: `str`

Office 365 API orderby parameter. See https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http#optional-query-parameters.

##### count: `bool`

Office 365 API count parameter. See https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http#optional-query-parameters.

#### 🔄 Return

[`Office365SListImportUsersResponse`](./jump_cloud_python_sdk/pydantic/office365_s_list_import_users_response.py)

#### 🌐 Endpoint

`/office365s/{office365_id}/import/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.organizations.create_by_administrator`

This endpoint allows you to grant Administrator access to an Organization.

#### 🛠️ Usage

```python
create_by_administrator_response = jumpcloud.organizations.create_by_administrator(
    id="id_example",
    organization="6230a0d26a4e4bc86c6b36f1",
)
```

#### ⚙️ Parameters

##### id: `str`

##### organization: `str`

The identifier for an organization to link this administrator to.

#### ⚙️ Request Body

[`AdministratorOrganizationLinkReq`](./jump_cloud_python_sdk/type/administrator_organization_link_req.py)
#### 🔄 Return

[`AdministratorOrganizationLink`](./jump_cloud_python_sdk/pydantic/administrator_organization_link.py)

#### 🌐 Endpoint

`/administrators/{id}/organizationlinks` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.organizations.list_by_administrator`

This endpoint returns the association links between an Administrator and Organizations.

#### 🛠️ Usage

```python
list_by_administrator_response = jumpcloud.organizations.list_by_administrator(
    id="id_example",
    limit=10,
    skip=0,
)
```

#### ⚙️ Parameters

##### id: `str`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

#### 🔄 Return

[`AdministratorOrganizationsListByAdministratorResponse`](./jump_cloud_python_sdk/pydantic/administrator_organizations_list_by_administrator_response.py)

#### 🌐 Endpoint

`/administrators/{id}/organizationlinks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.organizations.list_by_organization`

This endpoint returns the association links between an Organization and Administrators.

#### 🛠️ Usage

```python
list_by_organization_response = jumpcloud.organizations.list_by_organization(
    id="id_example",
    limit=10,
    skip=0,
)
```

#### ⚙️ Parameters

##### id: `str`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

#### 🔄 Return

[`AdministratorOrganizationsListByOrganizationResponse`](./jump_cloud_python_sdk/pydantic/administrator_organizations_list_by_organization_response.py)

#### 🌐 Endpoint

`/organizations/{id}/administratorlinks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.organizations.org_list_cases`

This endpoint returns the cases (Support/Feature requests) for the organization

#### 🛠️ Usage

```python
org_list_cases_response = jumpcloud.organizations.org_list_cases(
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`CasesResponse`](./jump_cloud_python_sdk/pydantic/cases_response.py)

#### 🌐 Endpoint

`/organizations/cases` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.organizations.remove_by_administrator`

This endpoint removes the association link between an Administrator and an Organization.

#### 🛠️ Usage

```python
jumpcloud.organizations.remove_by_administrator(
    administrator_id="administrator_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### administrator_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/administrators/{administrator_id}/organizationlinks/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.password_manager.get_device`

Get Device

#### 🛠️ Usage

```python
get_device_response = jumpcloud.password_manager.get_device(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🔄 Return

[`DevicePackageV1Device`](./jump_cloud_python_sdk/pydantic/device_package_v1_device.py)

#### 🌐 Endpoint

`/passwordmanager/devices/{UUID}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.password_manager.list_devices`

List Devices

#### 🛠️ Usage

```python
list_devices_response = jumpcloud.password_manager.list_devices(
    limit=1,
    skip=1,
    sort="string_example",
    fields=[
        "string_example"
    ],
    filter=[
        "string_example"
    ],
)
```

#### ⚙️ Parameters

##### limit: `int`

##### skip: `int`

##### sort: `str`

##### fields: List[`str`]

##### filter: List[`str`]

#### 🔄 Return

[`DevicePackageV1ListDevicesResponse`](./jump_cloud_python_sdk/pydantic/device_package_v1_list_devices_response.py)

#### 🌐 Endpoint

`/passwordmanager/devices` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.delete`

This endpoint allows you to delete a policy.

#### Sample Request

```
curl -X DELETE https://console.jumpcloud.com/api/v2/policies/5a837ecd232e110d4291e6b9 \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
jumpcloud.policies.delete(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

ObjectID of the Policy object.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint

`/policies/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.get`

This endpoint returns a specific policy.

###### Sample Request

```
  curl -X GET https://console.jumpcloud.com/api/v2/policies/{PolicyID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
get_response = jumpcloud.policies.get(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

ObjectID of the Policy object.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PolicyWithDetails`](./jump_cloud_python_sdk/pydantic/policy_with_details.py)

#### 🌐 Endpoint

`/policies/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.get_0`

This endpoint will return the policy results for a specific policy.

##### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policyresults/{Policy_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
get_0_response = jumpcloud.policies.get_0(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

ObjectID of the Policy Result.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PolicyResult`](./jump_cloud_python_sdk/pydantic/policy_result.py)

#### 🌐 Endpoint

`/policyresults/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.get_1`

This endpoint returns a specific policy template.

#### Sample Request
```
 curl -X GET https://console.jumpcloud.com/api/v2/policytemplates/{Policy_Template_ID}\
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
get_1_response = jumpcloud.policies.get_1(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

ObjectID of the Policy Template.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PolicyTemplateWithDetails`](./jump_cloud_python_sdk/pydantic/policy_template_with_details.py)

#### 🌐 Endpoint

`/policytemplates/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.list`

This endpoint returns all policies.

##### Sample Request

```
 curl -X GET  https://console.jumpcloud.com/api/v2/policies \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
list_response = jumpcloud.policies.list(
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PoliciesListResponse`](./jump_cloud_python_sdk/pydantic/policies_list_response.py)

#### 🌐 Endpoint

`/policies` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.list_0`

This endpoint returns all policies results for a specific policy.

##### Sample Request

```
 curl -X GET https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/policyresults \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
list_0_response = jumpcloud.policies.list_0(
    policy_id="policy_id_example",
    fields=[],
    filter=[],
    limit=10,
    x_org_id="string_example",
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### policy_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`PolicyresultsListResponse`](./jump_cloud_python_sdk/pydantic/policyresults_list_response.py)

#### 🌐 Endpoint

`/policies/{policy_id}/policyresults` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.list_1`

This endpoint returns all policy templates.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policytemplates \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
list_1_response = jumpcloud.policies.list_1(
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PolicytemplatesListResponse`](./jump_cloud_python_sdk/pydantic/policytemplates_list_response.py)

#### 🌐 Endpoint

`/policytemplates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.list_all_policy_results`

This endpoint returns all policy results for an organization.

##### Sample Request

```
 curl -X GET https://console.jumpcloud.com/api/v2/policyresults \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
list_all_policy_results_response = jumpcloud.policies.list_all_policy_results(
    fields=[],
    filter=[],
    limit=10,
    x_org_id="string_example",
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`PoliciesListAllPolicyResultsResponse`](./jump_cloud_python_sdk/pydantic/policies_list_all_policy_results_response.py)

#### 🌐 Endpoint

`/policyresults` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.policies_list`

This endpoint returns the latest policy results for a specific policy.

##### Sample Request

```
 curl -X GET https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/policystatuses \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
policies_list_response = jumpcloud.policies.policies_list(
    policy_id="policy_id_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### policy_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PolicystatusesPoliciesListResponse`](./jump_cloud_python_sdk/pydantic/policystatuses_policies_list_response.py)

#### 🌐 Endpoint

`/policies/{policy_id}/policystatuses` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.policy_associations_list`

This endpoint returns the _direct_ associations of a Policy.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Policies and Systems.

#### Sample Request
```
curl -X GET 'https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/associations?targets=system_group \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_associations_list_response = jumpcloud.policies.policy_associations_list(
    policy_id="policy_id_example",
    targets=[
        "system"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### policy_id: `str`

ObjectID of the Policy.

##### targets: List[`str`]

Targets which a \"policy\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphPolicyAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_associations_list_response.py)

#### 🌐 Endpoint

`/policies/{policy_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.policy_associations_post`

This endpoint allows you to manage the _direct_ associations of a Policy.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Policies and Systems.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/associations/ \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system_group",
    "id": "{Group_ID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.policies.policy_associations_post(
    policy_id="policy_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### policy_id: `str`

ObjectID of the Policy.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

Targets which a \\\"policy\\\" can be associated to.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationPolicy`](./jump_cloud_python_sdk/type/graph_operation_policy.py)
#### 🌐 Endpoint

`/policies/{policy_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.policy_member_of`

This endpoint returns all the Policy Groups a Policy is a member of.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/memberof \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
policy_member_of_response = jumpcloud.policies.policy_member_of(
    policy_id="policy_id_example",
    filter=[],
    limit=10,
    skip=0,
    date="string_example",
    authorization="string_example",
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### policy_id: `str`

ObjectID of the Policy.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### date: `str`

Current date header for the System Context API

##### authorization: `str`

Authorization header for the System Context API

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphPolicyMemberOfResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_member_of_response.py)

#### 🌐 Endpoint

`/policies/{policy_id}/memberof` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.policy_traverse_system`

This endpoint will return all Systems bound to a Policy, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Policy to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this Policy.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_traverse_system_response = jumpcloud.policies.policy_traverse_system(
    policy_id="policy_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### policy_id: `str`

ObjectID of the Command.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphPolicyTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_traverse_system_response.py)

#### 🌐 Endpoint

`/policies/{policy_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.policy_traverse_system_group`

This endpoint will return all Systems Groups bound to a Policy, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Policy to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this Policy.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET  https://console.jumpcloud.com/api/v2/policies/{Policy_ID}/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_traverse_system_group_response = jumpcloud.policies.policy_traverse_system_group(
    policy_id="policy_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### policy_id: `str`

ObjectID of the Command.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphPolicyTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_traverse_system_group_response.py)

#### 🌐 Endpoint

`/policies/{policy_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.post`

This endpoint allows you to create a policy. Given the amount of configurable parameters required to create a Policy, we suggest you use the JumpCloud Admin Console to create new policies.

##### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/policies \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    {Policy_Parameters}
  }'
```

#### 🛠️ Usage

```python
post_response = jumpcloud.policies.post(
    name="string_example",
    template={
        "id": "id_example",
    },
    notes="string_example",
    values=[
        {
        }
    ],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### name: `str`

The description for this specific Policy.

##### template: [`PolicyCreateRequestTemplate`](./jump_cloud_python_sdk/type/policy_create_request_template.py)


##### notes: `str`

The notes for this specific Policy.

##### values: List[`PolicyValue`]

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`PolicyCreateRequest`](./jump_cloud_python_sdk/type/policy_create_request.py)
#### 🔄 Return

[`PolicyWithDetails`](./jump_cloud_python_sdk/pydantic/policy_with_details.py)

#### 🌐 Endpoint

`/policies` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.put`

This endpoint allows you to update a policy. Given the amount of configurable parameters required to update a Policy, we suggest you use the JumpCloud Admin Console to create new policies.


##### Sample Request
```
curl -X PUT https://console.jumpcloud.com/api/v2/policies/59fced45c9118022172547ff \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    {Policy_Parameters}
  }'
```

#### 🛠️ Usage

```python
put_response = jumpcloud.policies.put(
    name="string_example",
    id="id_example",
    notes="string_example",
    values=[
        {
        }
    ],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### name: `str`

The description for this specific Policy.

##### id: `str`

ObjectID of the Policy object.

##### notes: `str`

The notes for this specific Policy.

##### values: List[`PolicyValue`]

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`PolicyUpdateRequest`](./jump_cloud_python_sdk/type/policy_update_request.py)
#### 🔄 Return

[`Policy`](./jump_cloud_python_sdk/pydantic/policy.py)

#### 🌐 Endpoint

`/policies/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policies.systems_list`

This endpoint returns the policy results for a particular system.

##### Sample Request

```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/policystatuses \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
systems_list_response = jumpcloud.policies.systems_list(
    system_id="system_id_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### system_id: `str`

ObjectID of the System.

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PolicystatusesSystemsListResponse`](./jump_cloud_python_sdk/pydantic/policystatuses_systems_list_response.py)

#### 🌐 Endpoint

`/systems/{system_id}/policystatuses` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_associations.policy_group_associations_list`

This endpoint returns the _direct_ associations of this Policy Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Policy Groups and Policies.


#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/associations?targets=system \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_group_associations_list_response = jumpcloud.policy_group_associations.policy_group_associations_list(
    group_id="group_id_example",
    targets=[
        "system"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### targets: List[`str`]

Targets which a \"policy_group\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphPolicyGroupAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_associations_list_response.py)

#### 🌐 Endpoint

`/policygroups/{group_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_associations.policy_group_associations_post`

This endpoint manages the _direct_ associations of this Policy Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Policy Groups and Policies.


#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system",
    "id": "{SystemID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.policy_group_associations.policy_group_associations_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

Targets which a \\\"policy_group\\\" can be associated to.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationPolicyGroup`](./jump_cloud_python_sdk/type/graph_operation_policy_group.py)
#### 🌐 Endpoint

`/policygroups/{group_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_associations.policy_group_traverse_system`

This endpoint will return all Systems bound to a Policy Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Policy Group to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this Policy Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_group_traverse_system_response = jumpcloud.policy_group_associations.policy_group_traverse_system(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphPolicyGroupTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_traverse_system_response.py)

#### 🌐 Endpoint

`/policygroups/{group_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_associations.policy_group_traverse_system_group`

This endpoint will return all System Groups bound to a Policy Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Policy Group to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this Policy Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_group_traverse_system_group_response = jumpcloud.policy_group_associations.policy_group_traverse_system_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphPolicyGroupTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_traverse_system_group_response.py)

#### 🌐 Endpoint

`/policygroups/{group_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_members_&amp;_membership.policy_group_members_list`

This endpoint returns the Policy members of a Policy Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_group_members_list_response = jumpcloud.policy_group_members_&amp;_membership.policy_group_members_list(
    group_id="group_id_example",
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphPolicyGroupMembersListResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_members_list_response.py)

#### 🌐 Endpoint

`/policygroups/{group_id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_members_&amp;_membership.policy_group_members_post`

This endpoint allows you to manage the Policy members of a Policy Group.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "policy",
    "id": "{Policy_ID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.policy_group_members_&amp;_membership.policy_group_members_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="policy",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

The member type.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationPolicyGroupMember`](./jump_cloud_python_sdk/type/graph_operation_policy_group_member.py)
#### 🌐 Endpoint

`/policygroups/{group_id}/members` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_members_&amp;_membership.policy_group_membership`

This endpoint returns all Policy members that are a member of this Policy Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/membership \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_group_membership_response = jumpcloud.policy_group_members_&amp;_membership.policy_group_membership(
    group_id="group_id_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphPolicyGroupMembershipResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_membership_response.py)

#### 🌐 Endpoint

`/policygroups/{group_id}/membership` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_templates.delete`

Deletes a Policy Group Template.

#### 🛠️ Usage

```python
jumpcloud.policy_group_templates.delete(
    provider_id="provider_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_templates.get`

Retrieves a Policy Group Template for this provider.

#### 🛠️ Usage

```python
get_response = jumpcloud.policy_group_templates.get(
    provider_id="provider_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🔄 Return

[`PolicyGroupTemplate`](./jump_cloud_python_sdk/pydantic/policy_group_template.py)

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_templates.get_configured_policy_template`

Retrieves a Configured Policy Templates for this provider and Id.

#### 🛠️ Usage

```python
get_configured_policy_template_response = jumpcloud.policy_group_templates.get_configured_policy_template(
    provider_id="provider_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/providers/{provider_id}/configuredpolicytemplates/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_templates.list`

Retrieves a list of Policy Group Templates for this provider.

#### 🛠️ Usage

```python
list_response = jumpcloud.policy_group_templates.list(
    provider_id="provider_id_example",
    fields=[],
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`PolicyGroupTemplates`](./jump_cloud_python_sdk/pydantic/policy_group_templates.py)

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_templates.list_configured_policy_templates`

Retrieves a list of Configured Policy Templates for this provider.

#### 🛠️ Usage

```python
list_configured_policy_templates_response = jumpcloud.policy_group_templates.list_configured_policy_templates(
    provider_id="provider_id_example",
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`PolicyGroupTemplatesListConfiguredPolicyTemplatesResponse`](./jump_cloud_python_sdk/pydantic/policy_group_templates_list_configured_policy_templates_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/configuredpolicytemplates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_group_templates.list_members`

Retrieves a Policy Group Template's Members.

#### 🛠️ Usage

```python
list_members_response = jumpcloud.policy_group_templates.list_members(
    provider_id="provider_id_example",
    id="id_example",
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`PolicyGroupTemplateMembers`](./jump_cloud_python_sdk/pydantic/policy_group_template_members.py)

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates/{id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.create_new`

This endpoint allows you to create a new Policy Group.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/policygroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "{Group_Name}"
  }'
```

#### 🛠️ Usage

```python
create_new_response = jumpcloud.policy_groups.create_new(
    name="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### name: `str`

Display name of a Policy Group.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`PolicyGroupData`](./jump_cloud_python_sdk/type/policy_group_data.py)
#### 🔄 Return

[`PolicyGroup`](./jump_cloud_python_sdk/pydantic/policy_group.py)

#### 🌐 Endpoint

`/policygroups` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.delete_group`

This endpoint allows you to delete a Policy Group.

#### Sample Request
```
curl -X DELETE https://console.jumpcloud.com/api/v2/policygroups/{GroupID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
delete_group_response = jumpcloud.policy_groups.delete_group(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

ObjectID of the Policy Group.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PolicyGroup`](./jump_cloud_python_sdk/pydantic/policy_group.py)

#### 🌐 Endpoint

`/policygroups/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.get_details`

This endpoint returns the details of a Policy Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
get_details_response = jumpcloud.policy_groups.get_details(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

ObjectID of the Policy Group.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PolicyGroup`](./jump_cloud_python_sdk/pydantic/policy_group.py)

#### 🌐 Endpoint

`/policygroups/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.list_all`

This endpoint returns all Policy Groups.

Available filter fields:
  - `name`
  - `disabled`
  - `type`

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
list_all_response = jumpcloud.policy_groups.list_all(
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PolicyGroupsListAllResponse`](./jump_cloud_python_sdk/pydantic/policy_groups_list_all_response.py)

#### 🌐 Endpoint

`/policygroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.policy_group_associations_list`

This endpoint returns the _direct_ associations of this Policy Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Policy Groups and Policies.


#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/associations?targets=system \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_group_associations_list_response = jumpcloud.policy_groups.policy_group_associations_list(
    group_id="group_id_example",
    targets=[
        "system"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### targets: List[`str`]

Targets which a \"policy_group\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphPolicyGroupAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_associations_list_response.py)

#### 🌐 Endpoint

`/policygroups/{group_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.policy_group_associations_post`

This endpoint manages the _direct_ associations of this Policy Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Policy Groups and Policies.


#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system",
    "id": "{SystemID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.policy_groups.policy_group_associations_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

Targets which a \\\"policy_group\\\" can be associated to.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationPolicyGroup`](./jump_cloud_python_sdk/type/graph_operation_policy_group.py)
#### 🌐 Endpoint

`/policygroups/{group_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.policy_group_members_list`

This endpoint returns the Policy members of a Policy Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_group_members_list_response = jumpcloud.policy_groups.policy_group_members_list(
    group_id="group_id_example",
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphPolicyGroupMembersListResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_members_list_response.py)

#### 🌐 Endpoint

`/policygroups/{group_id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.policy_group_members_post`

This endpoint allows you to manage the Policy members of a Policy Group.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "policy",
    "id": "{Policy_ID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.policy_groups.policy_group_members_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="policy",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

The member type.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationPolicyGroupMember`](./jump_cloud_python_sdk/type/graph_operation_policy_group_member.py)
#### 🌐 Endpoint

`/policygroups/{group_id}/members` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.policy_group_membership`

This endpoint returns all Policy members that are a member of this Policy Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/membership \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_group_membership_response = jumpcloud.policy_groups.policy_group_membership(
    group_id="group_id_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphPolicyGroupMembershipResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_membership_response.py)

#### 🌐 Endpoint

`/policygroups/{group_id}/membership` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.policy_group_traverse_system`

This endpoint will return all Systems bound to a Policy Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Policy Group to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this Policy Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_group_traverse_system_response = jumpcloud.policy_groups.policy_group_traverse_system(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphPolicyGroupTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_traverse_system_response.py)

#### 🌐 Endpoint

`/policygroups/{group_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.policy_group_traverse_system_group`

This endpoint will return all System Groups bound to a Policy Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Policy Group to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this Policy Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policygroups/{GroupID}/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
policy_group_traverse_system_group_response = jumpcloud.policy_groups.policy_group_traverse_system_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the Policy Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphPolicyGroupTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_policy_group_traverse_system_group_response.py)

#### 🌐 Endpoint

`/policygroups/{group_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policy_groups.update_policy_group`

This endpoint allows you to do a full update of the Policy Group.

#### Sample Request
```
curl -X PUT https://console.jumpcloud.com/api/v2/policygroups/{Group_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "group_update"
  }'
```

#### 🛠️ Usage

```python
update_policy_group_response = jumpcloud.policy_groups.update_policy_group(
    name="string_example",
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### name: `str`

Display name of a Policy Group.

##### id: `str`

ObjectID of the Policy Group.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`PolicyGroupData`](./jump_cloud_python_sdk/type/policy_group_data.py)
#### 🔄 Return

[`PolicyGroup`](./jump_cloud_python_sdk/pydantic/policy_group.py)

#### 🌐 Endpoint

`/policygroups/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policytemplates.get`

This endpoint returns a specific policy template.

#### Sample Request
```
 curl -X GET https://console.jumpcloud.com/api/v2/policytemplates/{Policy_Template_ID}\
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
get_response = jumpcloud.policytemplates.get(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

ObjectID of the Policy Template.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PolicyTemplateWithDetails`](./jump_cloud_python_sdk/pydantic/policy_template_with_details.py)

#### 🌐 Endpoint

`/policytemplates/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.policytemplates.list`

This endpoint returns all policy templates.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/policytemplates \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
list_response = jumpcloud.policytemplates.list(
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PolicytemplatesListResponse`](./jump_cloud_python_sdk/pydantic/policytemplates_list_response.py)

#### 🌐 Endpoint

`/policytemplates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.cases_metadata`

This endpoint returns the metadata for cases

#### 🛠️ Usage

```python
cases_metadata_response = jumpcloud.providers.cases_metadata()
```

#### 🔄 Return

[`CasesMetadataResponse`](./jump_cloud_python_sdk/pydantic/cases_metadata_response.py)

#### 🌐 Endpoint

`/cases/metadata` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.create_configuration`

Creates a new Autotask integration for the provider. You must be associated with the provider to use this route. A 422 Unprocessable Entity response means the server failed to validate with Autotask.

#### 🛠️ Usage

```python
create_configuration_response = jumpcloud.providers.create_configuration(
    secret="string_example",
    username="string_example",
    provider_id="provider_id_example",
)
```

#### ⚙️ Parameters

##### secret: `str`

The secret for connecting to Autotask.

##### username: `str`

The username for connecting to Autotask.

##### provider_id: `str`

#### ⚙️ Request Body

[`AutotaskIntegrationReq`](./jump_cloud_python_sdk/type/autotask_integration_req.py)
#### 🔄 Return

[`AutotaskCreateConfigurationResponse`](./jump_cloud_python_sdk/pydantic/autotask_create_configuration_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/autotask` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.create_configuration_0`

Creates a new ConnectWise integration for the provider. You must be associated with the provider to use this route. A 422 Unprocessable Entity response means the server failed to validate with ConnectWise.

#### 🛠️ Usage

```python
create_configuration_0_response = jumpcloud.providers.create_configuration_0(
    company_id="string_example",
    private_key="string_example",
    public_key="string_example",
    url="string_example",
    provider_id="provider_id_example",
)
```

#### ⚙️ Parameters

##### company_id: `str`

The ConnectWise company identifier.

##### private_key: `str`

The ConnectWise private key for authentication

##### public_key: `str`

The ConnectWise public key for authentication.

##### url: `str`

The base url for connecting to ConnectWise.

##### provider_id: `str`

#### ⚙️ Request Body

[`ConnectwiseIntegrationReq`](./jump_cloud_python_sdk/type/connectwise_integration_req.py)
#### 🔄 Return

[`ConnectwiseCreateConfigurationResponse`](./jump_cloud_python_sdk/pydantic/connectwise_create_configuration_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/connectwise` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.create_configuration_1`

Creates a new Syncro integration for the provider. You must be associated with the provider to use this route. A 422 Unprocessable Entity response means the server failed to validate with Syncro.

#### 🛠️ Usage

```python
create_configuration_1_response = jumpcloud.providers.create_configuration_1(
    api_token="string_example",
    subdomain="string_example",
    provider_id="provider_id_example",
)
```

#### ⚙️ Parameters

##### api_token: `str`

The Syncro API token for authentication

##### subdomain: `str`

The subdomain for the URL to connect to Syncro.

##### provider_id: `str`

#### ⚙️ Request Body

[`SyncroIntegrationReq`](./jump_cloud_python_sdk/type/syncro_integration_req.py)
#### 🔄 Return

[`SyncroCreateConfigurationResponse`](./jump_cloud_python_sdk/pydantic/syncro_create_configuration_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/syncro` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.create_org`

This endpoint creates a new organization under the provider

#### 🛠️ Usage

```python
create_org_response = jumpcloud.providers.create_org(
    provider_id="provider_id_example",
    max_system_users=10,
    name="Acme Inc",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### max_system_users: `int`

The maximum number of users allowed in this organization. Requires organizations.billing scope to modify.

##### name: `str`

#### ⚙️ Request Body

[`CreateOrganization`](./jump_cloud_python_sdk/type/create_organization.py)
#### 🔄 Return

[`Organization`](./jump_cloud_python_sdk/pydantic/organization.py)

#### 🌐 Endpoint

`/providers/{provider_id}/organizations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.delete`

Deletes a Policy Group Template.

#### 🛠️ Usage

```python
jumpcloud.providers.delete(
    provider_id="provider_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.delete_configuration`

Removes a Autotask integration.

#### 🛠️ Usage

```python
jumpcloud.providers.delete_configuration(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🌐 Endpoint

`/integrations/autotask/{UUID}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.delete_configuration_0`

Removes a ConnectWise integration.

#### 🛠️ Usage

```python
jumpcloud.providers.delete_configuration_0(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🌐 Endpoint

`/integrations/connectwise/{UUID}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.delete_configuration_1`

Removes a Syncro integration.

#### 🛠️ Usage

```python
jumpcloud.providers.delete_configuration_1(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🌐 Endpoint

`/integrations/syncro/{UUID}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.get`

Retrieves a Policy Group Template for this provider.

#### 🛠️ Usage

```python
get_response = jumpcloud.providers.get(
    provider_id="provider_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🔄 Return

[`PolicyGroupTemplate`](./jump_cloud_python_sdk/pydantic/policy_group_template.py)

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.get_configuration`

Retrieves configuration for given Autotask integration id. You must be associated to the provider the integration is tied to in order to use this api.

#### 🛠️ Usage

```python
get_configuration_response = jumpcloud.providers.get_configuration(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🔄 Return

[`AutotaskIntegration`](./jump_cloud_python_sdk/pydantic/autotask_integration.py)

#### 🌐 Endpoint

`/integrations/autotask/{UUID}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.get_configuration_0`

Retrieves configuration for given ConnectWise integration id. You must be associated to the provider the integration is tied to in order to use this api.

#### 🛠️ Usage

```python
get_configuration_0_response = jumpcloud.providers.get_configuration_0(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🔄 Return

[`ConnectwiseIntegration`](./jump_cloud_python_sdk/pydantic/connectwise_integration.py)

#### 🌐 Endpoint

`/integrations/connectwise/{UUID}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.get_configuration_1`

Retrieves configuration for given Syncro integration id. You must be associated to the provider the integration is tied to in order to use this api.

#### 🛠️ Usage

```python
get_configuration_1_response = jumpcloud.providers.get_configuration_1(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🔄 Return

[`SyncroIntegration`](./jump_cloud_python_sdk/pydantic/syncro_integration.py)

#### 🌐 Endpoint

`/integrations/syncro/{UUID}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.get_configured_policy_template`

Retrieves a Configured Policy Templates for this provider and Id.

#### 🛠️ Usage

```python
get_configured_policy_template_response = jumpcloud.providers.get_configured_policy_template(
    provider_id="provider_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/providers/{provider_id}/configuredpolicytemplates/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.get_contract`

Retrieve contract for a Provider

#### 🛠️ Usage

```python
get_contract_response = jumpcloud.providers.get_contract(
    provider_id='YQ==',
)
```

#### ⚙️ Parameters

##### provider_id: `str`

#### 🌐 Endpoint

`/providers/{provider_id}/billing/contract` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.get_details`

Retrieve billing details for a Provider

#### 🛠️ Usage

```python
get_details_response = jumpcloud.providers.get_details(
    provider_id='YQ==',
)
```

#### ⚙️ Parameters

##### provider_id: `str`

#### 🔄 Return

[`JumpcloudMspGetDetailsResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_msp_get_details_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/billing/details` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.get_provider`

This endpoint returns details about a provider

#### 🛠️ Usage

```python
get_provider_response = jumpcloud.providers.get_provider(
    provider_id="provider_id_example",
    fields=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

#### 🔄 Return

[`Provider`](./jump_cloud_python_sdk/pydantic/provider.py)

#### 🌐 Endpoint

`/providers/{provider_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.list`

Retrieves a list of Policy Group Templates for this provider.

#### 🛠️ Usage

```python
list_response = jumpcloud.providers.list(
    provider_id="provider_id_example",
    fields=[],
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`PolicyGroupTemplates`](./jump_cloud_python_sdk/pydantic/policy_group_templates.py)

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.list_administrators`

This endpoint returns a list of the Administrators associated with the Provider. You must be associated with the provider to use this route.

#### 🛠️ Usage

```python
list_administrators_response = jumpcloud.providers.list_administrators(
    provider_id="provider_id_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    sort_ignore_case=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### sort_ignore_case: List[`str`]

The comma separated fields used to sort the collection, ignoring case. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`ProvidersListAdministratorsResponse`](./jump_cloud_python_sdk/pydantic/providers_list_administrators_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/administrators` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.list_configured_policy_templates`

Retrieves a list of Configured Policy Templates for this provider.

#### 🛠️ Usage

```python
list_configured_policy_templates_response = jumpcloud.providers.list_configured_policy_templates(
    provider_id="provider_id_example",
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`PolicyGroupTemplatesListConfiguredPolicyTemplatesResponse`](./jump_cloud_python_sdk/pydantic/policy_group_templates_list_configured_policy_templates_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/configuredpolicytemplates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.list_members`

Retrieves a Policy Group Template's Members.

#### 🛠️ Usage

```python
list_members_response = jumpcloud.providers.list_members(
    provider_id="provider_id_example",
    id="id_example",
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`PolicyGroupTemplateMembers`](./jump_cloud_python_sdk/pydantic/policy_group_template_members.py)

#### 🌐 Endpoint

`/providers/{provider_id}/policygrouptemplates/{id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.list_organizations`

This endpoint returns a list of the Organizations associated with the Provider. You must be associated with the provider to use this route.

#### 🛠️ Usage

```python
list_organizations_response = jumpcloud.providers.list_organizations(
    provider_id="provider_id_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    sort_ignore_case=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### sort_ignore_case: List[`str`]

The comma separated fields used to sort the collection, ignoring case. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`ProvidersListOrganizationsResponse`](./jump_cloud_python_sdk/pydantic/providers_list_organizations_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/organizations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.patch_mappings`

Create, edit, and/or delete mappings between Jumpcloud organizations and Autotask companies/contracts/services. You must be associated to the same provider as the Autotask integration to use this api.

#### 🛠️ Usage

```python
patch_mappings_response = jumpcloud.providers.patch_mappings(
    uuid="UUID_example",
    data=[
        {
            "company": {
                "id": "id_example",
                "name": "name_example",
            },
            "organization": {
                "id": "id_example",
                "name": "name_example",
            },
        }
    ],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### data: [`AutotaskMappingRequestData`](./jump_cloud_python_sdk/type/autotask_mapping_request_data.py)

#### ⚙️ Request Body

[`AutotaskMappingRequest`](./jump_cloud_python_sdk/type/autotask_mapping_request.py)
#### 🔄 Return

[`AutotaskMappingResponse`](./jump_cloud_python_sdk/pydantic/autotask_mapping_response.py)

#### 🌐 Endpoint

`/integrations/autotask/{UUID}/mappings` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.patch_mappings_0`

Create, edit, and/or delete mappings between Jumpcloud organizations and ConnectWise companies/agreements/additions. You must be associated to the same provider as the ConnectWise integration to use this api.

#### 🛠️ Usage

```python
patch_mappings_0_response = jumpcloud.providers.patch_mappings_0(
    uuid="UUID_example",
    data=[
        {
            "company": {
                "id": "id_example",
                "name": "name_example",
            },
            "organization": {
                "id": "id_example",
                "name": "name_example",
            },
        }
    ],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### data: [`ConnectWiseMappingRequestData`](./jump_cloud_python_sdk/type/connect_wise_mapping_request_data.py)

#### ⚙️ Request Body

[`ConnectWiseMappingRequest`](./jump_cloud_python_sdk/type/connect_wise_mapping_request.py)
#### 🔄 Return

[`ConnectWiseMappingRequest`](./jump_cloud_python_sdk/pydantic/connect_wise_mapping_request.py)

#### 🌐 Endpoint

`/integrations/connectwise/{UUID}/mappings` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.patch_mappings_1`

Create, edit, and/or delete mappings between Jumpcloud organizations and Syncro companies. You must be associated to the same provider as the Syncro integration to use this api.

#### 🛠️ Usage

```python
patch_mappings_1_response = jumpcloud.providers.patch_mappings_1(
    uuid="UUID_example",
    data=[
        {
            "company": {
                "id": "id_example",
                "name": "name_example",
            },
            "organization": {
                "id": "id_example",
                "name": "name_example",
            },
        }
    ],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### data: [`SyncroMappingRequestData`](./jump_cloud_python_sdk/type/syncro_mapping_request_data.py)

#### ⚙️ Request Body

[`SyncroMappingRequest`](./jump_cloud_python_sdk/type/syncro_mapping_request.py)
#### 🔄 Return

[`SyncroMappingRequest`](./jump_cloud_python_sdk/pydantic/syncro_mapping_request.py)

#### 🌐 Endpoint

`/integrations/syncro/{UUID}/mappings` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.patch_settings`

Create, edit, and/or delete Autotask settings. You must be associated to the same provider as the Autotask integration to use this endpoint.

#### 🛠️ Usage

```python
patch_settings_response = jumpcloud.providers.patch_settings(
    uuid="UUID_example",
    automatic_ticketing=True,
    company_type_ids=[
        1
    ],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### automatic_ticketing: `bool`

Determine whether Autotask uses automatic ticketing

##### company_type_ids: [`AutotaskSettingsPatchReqCompanyTypeIds`](./jump_cloud_python_sdk/type/autotask_settings_patch_req_company_type_ids.py)

#### ⚙️ Request Body

[`AutotaskSettingsPatchReq`](./jump_cloud_python_sdk/type/autotask_settings_patch_req.py)
#### 🔄 Return

[`AutotaskSettings`](./jump_cloud_python_sdk/pydantic/autotask_settings.py)

#### 🌐 Endpoint

`/integrations/autotask/{UUID}/settings` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.patch_settings_0`

Create, edit, and/or delete ConnectWiseIntegration settings. You must be associated to the same provider as the ConnectWise integration to use this endpoint.

#### 🛠️ Usage

```python
patch_settings_0_response = jumpcloud.providers.patch_settings_0(
    uuid="UUID_example",
    automatic_ticketing=True,
    company_type_ids=[
        1
    ],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### automatic_ticketing: `bool`

Determine whether ConnectWise uses automatic ticketing

##### company_type_ids: [`ConnectWiseSettingsPatchReqCompanyTypeIds`](./jump_cloud_python_sdk/type/connect_wise_settings_patch_req_company_type_ids.py)

#### ⚙️ Request Body

[`ConnectWiseSettingsPatchReq`](./jump_cloud_python_sdk/type/connect_wise_settings_patch_req.py)
#### 🔄 Return

[`ConnectWiseSettings`](./jump_cloud_python_sdk/pydantic/connect_wise_settings.py)

#### 🌐 Endpoint

`/integrations/connectwise/{UUID}/settings` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.patch_settings_1`

Create, edit, and/or delete SyncroIntegration settings. You must be associated to the same provider as the Syncro integration to use this endpoint.

#### 🛠️ Usage

```python
patch_settings_1_response = jumpcloud.providers.patch_settings_1(
    uuid="UUID_example",
    automatic_ticketing=True,
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### automatic_ticketing: `bool`

Determine whether Syncro uses automatic ticketing

#### ⚙️ Request Body

[`SyncroSettingsPatchReq`](./jump_cloud_python_sdk/type/syncro_settings_patch_req.py)
#### 🔄 Return

[`SyncroSettings`](./jump_cloud_python_sdk/pydantic/syncro_settings.py)

#### 🌐 Endpoint

`/integrations/syncro/{UUID}/settings` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.post_admins`

This endpoint allows you to create a provider administrator. You must be associated with the provider to use this route. You must provide either `role` or `roleName`.

#### 🛠️ Usage

```python
post_admins_response = jumpcloud.providers.post_admins(
    email="joe@example.com",
    provider_id="provider_id_example",
    api_key_allowed=True,
    bind_no_orgs=False,
    enable_multi_factor=True,
    firstname="Joe",
    lastname="Blough",
    role="5c3536e9e0a6840001872799",
    role_name="Administrator",
)
```

#### ⚙️ Parameters

##### email: `str`

##### provider_id: `str`

##### api_key_allowed: `bool`

##### bind_no_orgs: `bool`

##### enable_multi_factor: `bool`

##### firstname: `str`

##### lastname: `str`

##### role: `str`

##### role_name: `str`

#### ⚙️ Request Body

[`ProviderAdminReq`](./jump_cloud_python_sdk/type/provider_admin_req.py)
#### 🔄 Return

[`Administrator`](./jump_cloud_python_sdk/pydantic/administrator.py)

#### 🌐 Endpoint

`/providers/{provider_id}/administrators` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.provider_list_case`

This endpoint returns the cases (Support/Feature requests) for the provider

#### 🛠️ Usage

```python
provider_list_case_response = jumpcloud.providers.provider_list_case(
    provider_id="provider_id_example",
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`CasesResponse`](./jump_cloud_python_sdk/pydantic/cases_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/cases` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.remove_administrator`

This endpoint removes an Administrator associated with the Provider. You must be associated with the provider to use this route.

#### 🛠️ Usage

```python
jumpcloud.providers.remove_administrator(
    provider_id="provider_id_example",
    id="id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/providers/{provider_id}/administrators/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_additions`

Retrieves a list of ConnectWise additions for the given ConnectWise id and Agreement id. You must be associated to the same provider as the ConnectWise integration to use this endpoint.

#### 🛠️ Usage

```python
retrieve_additions_response = jumpcloud.providers.retrieve_additions(
    uuid="UUID_example",
    agreement_id="agreement_ID_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### agreement_id: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`ConnectwiseRetrieveAdditionsResponse`](./jump_cloud_python_sdk/pydantic/connectwise_retrieve_additions_response.py)

#### 🌐 Endpoint

`/integrations/connectwise/{UUID}/agreements/{agreement_ID}/additions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_agreements`

Retrieves a list of ConnectWise agreements for the given ConnectWise id. You must be associated to the same provider as the ConnectWise integration to use this endpoint.

#### 🛠️ Usage

```python
retrieve_agreements_response = jumpcloud.providers.retrieve_agreements(
    uuid="UUID_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`ConnectwiseRetrieveAgreementsResponse`](./jump_cloud_python_sdk/pydantic/connectwise_retrieve_agreements_response.py)

#### 🌐 Endpoint

`/integrations/connectwise/{UUID}/agreements` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_alerts`

Get all ticketing alerts available for a provider's ticketing integration.

#### 🛠️ Usage

```python
retrieve_alerts_response = jumpcloud.providers.retrieve_alerts(
    provider_id="provider_id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

#### 🔄 Return

[`TicketingIntegrationAlertsResp`](./jump_cloud_python_sdk/pydantic/ticketing_integration_alerts_resp.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/ticketing/alerts` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_all_alert_configuration_options`

Get all Autotask ticketing alert configuration options for a provider.

#### 🛠️ Usage

```python
retrieve_all_alert_configuration_options_response = jumpcloud.providers.retrieve_all_alert_configuration_options(
    provider_id="provider_id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

#### 🔄 Return

[`AutotaskTicketingAlertConfigurationOptions`](./jump_cloud_python_sdk/pydantic/autotask_ticketing_alert_configuration_options.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/autotask/alerts/configuration/options` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_all_alert_configuration_options_0`

Get all ConnectWise ticketing alert configuration options for a provider.

#### 🛠️ Usage

```python
retrieve_all_alert_configuration_options_0_response = jumpcloud.providers.retrieve_all_alert_configuration_options_0(
    provider_id="provider_id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

#### 🔄 Return

[`ConnectWiseTicketingAlertConfigurationOptions`](./jump_cloud_python_sdk/pydantic/connect_wise_ticketing_alert_configuration_options.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/connectwise/alerts/configuration/options` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_all_alert_configuration_options_1`

Get all Syncro ticketing alert configuration options for a provider.

#### 🛠️ Usage

```python
retrieve_all_alert_configuration_options_1_response = jumpcloud.providers.retrieve_all_alert_configuration_options_1(
    provider_id="provider_id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

#### 🔄 Return

[`SyncroTicketingAlertConfigurationOptions`](./jump_cloud_python_sdk/pydantic/syncro_ticketing_alert_configuration_options.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/syncro/alerts/configuration/options` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_all_alert_configurations`

Get all Autotask ticketing alert configurations for a provider.

#### 🛠️ Usage

```python
retrieve_all_alert_configurations_response = jumpcloud.providers.retrieve_all_alert_configurations(
    provider_id="provider_id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

#### 🔄 Return

[`AutotaskTicketingAlertConfigurationList`](./jump_cloud_python_sdk/pydantic/autotask_ticketing_alert_configuration_list.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/autotask/alerts/configuration` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_all_alert_configurations_0`

Get all ConnectWise ticketing alert configurations for a provider.

#### 🛠️ Usage

```python
retrieve_all_alert_configurations_0_response = jumpcloud.providers.retrieve_all_alert_configurations_0(
    provider_id="provider_id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

#### 🔄 Return

[`ConnectWiseTicketingAlertConfigurationList`](./jump_cloud_python_sdk/pydantic/connect_wise_ticketing_alert_configuration_list.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/connectwise/alerts/configuration` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_all_alert_configurations_1`

Get all Syncro ticketing alert configurations for a provider.

#### 🛠️ Usage

```python
retrieve_all_alert_configurations_1_response = jumpcloud.providers.retrieve_all_alert_configurations_1(
    provider_id="provider_id_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

#### 🔄 Return

[`SyncroTicketingAlertConfigurationList`](./jump_cloud_python_sdk/pydantic/syncro_ticketing_alert_configuration_list.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/syncro/alerts/configuration` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_billing_mapping_configuration_options`

Retrieves a list of dependencies for Syncro billing mappings.

#### 🛠️ Usage

```python
retrieve_billing_mapping_configuration_options_response = jumpcloud.providers.retrieve_billing_mapping_configuration_options(
    uuid="UUID_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`SyncroBillingMappingConfigurationOptionsResp`](./jump_cloud_python_sdk/pydantic/syncro_billing_mapping_configuration_options_resp.py)

#### 🌐 Endpoint

`/integrations/syncro/{UUID}/billing_mapping_configuration_options` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_companies`

Retrieves a list of Autotask companies for the given Autotask id. You must be associated to the same provider as the Autotask integration to use this endpoint.

#### 🛠️ Usage

```python
retrieve_companies_response = jumpcloud.providers.retrieve_companies(
    uuid="UUID_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`AutotaskCompanyResp`](./jump_cloud_python_sdk/pydantic/autotask_company_resp.py)

#### 🌐 Endpoint

`/integrations/autotask/{UUID}/companies` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_companies_0`

Retrieves a list of ConnectWise companies for the given ConnectWise id. You must be associated to the same provider as the ConnectWise integration to use this endpoint.

#### 🛠️ Usage

```python
retrieve_companies_0_response = jumpcloud.providers.retrieve_companies_0(
    uuid="UUID_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`ConnectwiseCompanyResp`](./jump_cloud_python_sdk/pydantic/connectwise_company_resp.py)

#### 🌐 Endpoint

`/integrations/connectwise/{UUID}/companies` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_companies_1`

Retrieves a list of Syncro companies for the given Syncro id. You must be associated to the same provider as the Syncro integration to use this endpoint.

#### 🛠️ Usage

```python
retrieve_companies_1_response = jumpcloud.providers.retrieve_companies_1(
    uuid="UUID_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`SyncroCompanyResp`](./jump_cloud_python_sdk/pydantic/syncro_company_resp.py)

#### 🌐 Endpoint

`/integrations/syncro/{UUID}/companies` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_company_types`

Retrieves a list of user defined company types from Autotask for the given Autotask id.

#### 🛠️ Usage

```python
retrieve_company_types_response = jumpcloud.providers.retrieve_company_types(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🔄 Return

[`AutotaskCompanyTypeResp`](./jump_cloud_python_sdk/pydantic/autotask_company_type_resp.py)

#### 🌐 Endpoint

`/integrations/autotask/{UUID}/companytypes` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_company_types_0`

Retrieves a list of user defined company types from ConnectWise for the given ConnectWise id.

#### 🛠️ Usage

```python
retrieve_company_types_0_response = jumpcloud.providers.retrieve_company_types_0(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🔄 Return

[`ConnectwiseCompanyTypeResp`](./jump_cloud_python_sdk/pydantic/connectwise_company_type_resp.py)

#### 🌐 Endpoint

`/integrations/connectwise/{UUID}/companytypes` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_contracts`

Retrieves a list of Autotask contracts for the given Autotask integration id. You must be associated to the same provider as the Autotask integration to use this endpoint.

#### 🛠️ Usage

```python
retrieve_contracts_response = jumpcloud.providers.retrieve_contracts(
    uuid="UUID_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`AutotaskRetrieveContractsResponse`](./jump_cloud_python_sdk/pydantic/autotask_retrieve_contracts_response.py)

#### 🌐 Endpoint

`/integrations/autotask/{UUID}/contracts` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_contracts_fields`

Retrieves a list of Autotask contract fields for the given Autotask integration id. You must be associated to the same provider as the Autotask integration to use this endpoint.

#### 🛠️ Usage

```python
retrieve_contracts_fields_response = jumpcloud.providers.retrieve_contracts_fields(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🔄 Return

[`AutotaskRetrieveContractsFieldsResponse`](./jump_cloud_python_sdk/pydantic/autotask_retrieve_contracts_fields_response.py)

#### 🌐 Endpoint

`/integrations/autotask/{UUID}/contracts/fields` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_integrations`

Retrieves a list of integrations this provider has configured. You must be associated to the provider to use this endpoint.

#### 🛠️ Usage

```python
retrieve_integrations_response = jumpcloud.providers.retrieve_integrations(
    provider_id="provider_id_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`IntegrationsResponse`](./jump_cloud_python_sdk/pydantic/integrations_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_invoice`

Retrieves an invoice for this provider. You must be associated to the provider to use this endpoint.

#### 🛠️ Usage

```python
retrieve_invoice_response = jumpcloud.providers.retrieve_invoice(
    provider_id="provider_id_example",
    id="ID_example",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

#### 🌐 Endpoint

`/providers/{provider_id}/invoices/{ID}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_invoices`

Retrieves a list of invoices for this provider. You must be associated to the provider to use this endpoint.

#### 🛠️ Usage

```python
retrieve_invoices_response = jumpcloud.providers.retrieve_invoices(
    provider_id="provider_id_example",
    skip=0,
    sort=[],
    limit=10,
    filter=[],
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`ProviderInvoiceResponse`](./jump_cloud_python_sdk/pydantic/provider_invoice_response.py)

#### 🌐 Endpoint

`/providers/{provider_id}/invoices` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_mappings`

Retrieves the list of mappings for this Autotask integration. You must be associated to the same provider as the Autotask integration to use this api.

#### 🛠️ Usage

```python
retrieve_mappings_response = jumpcloud.providers.retrieve_mappings(
    uuid="UUID_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`AutotaskRetrieveMappingsResponse`](./jump_cloud_python_sdk/pydantic/autotask_retrieve_mappings_response.py)

#### 🌐 Endpoint

`/integrations/autotask/{UUID}/mappings` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_mappings_0`

Retrieves the list of mappings for this ConnectWise integration. You must be associated to the same provider as the ConnectWise integration to use this api.

#### 🛠️ Usage

```python
retrieve_mappings_0_response = jumpcloud.providers.retrieve_mappings_0(
    uuid="UUID_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`ConnectwiseRetrieveMappingsResponse`](./jump_cloud_python_sdk/pydantic/connectwise_retrieve_mappings_response.py)

#### 🌐 Endpoint

`/integrations/connectwise/{UUID}/mappings` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_mappings_1`

Retrieves the list of mappings for this Syncro integration. You must be associated to the same provider as the Syncro integration to use this api.

#### 🛠️ Usage

```python
retrieve_mappings_1_response = jumpcloud.providers.retrieve_mappings_1(
    uuid="UUID_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`SyncroRetrieveMappingsResponse`](./jump_cloud_python_sdk/pydantic/syncro_retrieve_mappings_response.py)

#### 🌐 Endpoint

`/integrations/syncro/{UUID}/mappings` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_services`

Retrieves a list of Autotask contract services for the given Autotask integration id. You must be associated to the same provider as the Autotask integration to use this endpoint.

#### 🛠️ Usage

```python
retrieve_services_response = jumpcloud.providers.retrieve_services(
    uuid="UUID_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`AutotaskRetrieveServicesResponse`](./jump_cloud_python_sdk/pydantic/autotask_retrieve_services_response.py)

#### 🌐 Endpoint

`/integrations/autotask/{UUID}/contracts/services` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_settings`

Retrieve the Autotask integration settings. You must be associated to the same provider as the Autotask integration to use this endpoint.

#### 🛠️ Usage

```python
retrieve_settings_response = jumpcloud.providers.retrieve_settings(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🔄 Return

[`AutotaskSettings`](./jump_cloud_python_sdk/pydantic/autotask_settings.py)

#### 🌐 Endpoint

`/integrations/autotask/{UUID}/settings` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_settings_0`

Retrieve the ConnectWise integration settings. You must be associated to the same provider as the ConnectWise integration to use this endpoint.

#### 🛠️ Usage

```python
retrieve_settings_0_response = jumpcloud.providers.retrieve_settings_0(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🔄 Return

[`ConnectWiseSettings`](./jump_cloud_python_sdk/pydantic/connect_wise_settings.py)

#### 🌐 Endpoint

`/integrations/connectwise/{UUID}/settings` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_settings_1`

Retrieve the Syncro integration settings. You must be associated to the same provider as the Syncro integration to use this endpoint.

#### 🛠️ Usage

```python
retrieve_settings_1_response = jumpcloud.providers.retrieve_settings_1(
    uuid="UUID_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

#### 🔄 Return

[`SyncroSettings`](./jump_cloud_python_sdk/pydantic/syncro_settings.py)

#### 🌐 Endpoint

`/integrations/syncro/{UUID}/settings` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.retrieve_sync_errors`

Retrieves recent sync errors for given integration type and integration id. You must be associated to the provider the integration is tied to in order to use this api.

#### 🛠️ Usage

```python
retrieve_sync_errors_response = jumpcloud.providers.retrieve_sync_errors(
    uuid="UUID_example",
    integration_type="integration_type_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### integration_type: `str`

#### 🔄 Return

[`IntegrationSyncErrorResp`](./jump_cloud_python_sdk/pydantic/integration_sync_error_resp.py)

#### 🌐 Endpoint

`/integrations/{integration_type}/{UUID}/errors` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.update_alert_configuration`

Update an Autotask ticketing alert's configuration

#### 🛠️ Usage

```python
update_alert_configuration_response = jumpcloud.providers.update_alert_configuration(
    destination="queue",
    due_days=1,
    priority={
    },
    should_create_tickets=True,
    status={
    },
    provider_id="provider_id_example",
    alert_uuid="alert_UUID_example",
    queue={
    },
    resource={
    },
    source={
    },
)
```

#### ⚙️ Parameters

##### destination: `str`

##### due_days: `int`

##### priority: [`AutotaskTicketingAlertConfigurationRequestPriority`](./jump_cloud_python_sdk/type/autotask_ticketing_alert_configuration_request_priority.py)


##### should_create_tickets: `bool`

##### status: [`AutotaskTicketingAlertConfigurationRequestStatus`](./jump_cloud_python_sdk/type/autotask_ticketing_alert_configuration_request_status.py)


##### provider_id: `str`

##### alert_uuid: `str`

##### queue: [`AutotaskTicketingAlertConfigurationRequestQueue`](./jump_cloud_python_sdk/type/autotask_ticketing_alert_configuration_request_queue.py)


##### resource: [`AutotaskTicketingAlertConfigurationRequestResource`](./jump_cloud_python_sdk/type/autotask_ticketing_alert_configuration_request_resource.py)


##### source: [`AutotaskTicketingAlertConfigurationRequestSource`](./jump_cloud_python_sdk/type/autotask_ticketing_alert_configuration_request_source.py)


#### ⚙️ Request Body

[`AutotaskTicketingAlertConfigurationRequest`](./jump_cloud_python_sdk/type/autotask_ticketing_alert_configuration_request.py)
#### 🔄 Return

[`AutotaskTicketingAlertConfiguration`](./jump_cloud_python_sdk/pydantic/autotask_ticketing_alert_configuration.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/autotask/alerts/{alert_UUID}/configuration` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.update_alert_configuration_0`

Update a ConnectWise ticketing alert's configuration.

#### 🛠️ Usage

```python
update_alert_configuration_0_response = jumpcloud.providers.update_alert_configuration_0(
    should_create_tickets=True,
    provider_id="provider_id_example",
    alert_uuid="alert_UUID_example",
    due_days=1,
    priority={
    },
    source={
    },
)
```

#### ⚙️ Parameters

##### should_create_tickets: `bool`

##### provider_id: `str`

##### alert_uuid: `str`

##### due_days: `int`

##### priority: [`ConnectWiseTicketingAlertConfigurationRequestPriority`](./jump_cloud_python_sdk/type/connect_wise_ticketing_alert_configuration_request_priority.py)


##### source: [`ConnectWiseTicketingAlertConfigurationRequestSource`](./jump_cloud_python_sdk/type/connect_wise_ticketing_alert_configuration_request_source.py)


#### ⚙️ Request Body

[`ConnectWiseTicketingAlertConfigurationRequest`](./jump_cloud_python_sdk/type/connect_wise_ticketing_alert_configuration_request.py)
#### 🔄 Return

[`ConnectWiseTicketingAlertConfiguration`](./jump_cloud_python_sdk/pydantic/connect_wise_ticketing_alert_configuration.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/connectwise/alerts/{alert_UUID}/configuration` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.update_alert_configuration_1`

Update a Syncro ticketing alert's configuration

#### 🛠️ Usage

```python
update_alert_configuration_1_response = jumpcloud.providers.update_alert_configuration_1(
    problem_type="string_example",
    should_create_tickets=True,
    provider_id="provider_id_example",
    alert_uuid="alert_UUID_example",
    due_days=1,
    priority="string_example",
    status="string_example",
    user_id=3.14,
    username="string_example",
)
```

#### ⚙️ Parameters

##### problem_type: `str`

##### should_create_tickets: `bool`

##### provider_id: `str`

##### alert_uuid: `str`

##### due_days: `int`

##### priority: `str`

##### status: `str`

##### user_id: `Union[int, float]`

##### username: `str`

#### ⚙️ Request Body

[`SyncroTicketingAlertConfigurationRequest`](./jump_cloud_python_sdk/type/syncro_ticketing_alert_configuration_request.py)
#### 🔄 Return

[`SyncroTicketingAlertConfiguration`](./jump_cloud_python_sdk/pydantic/syncro_ticketing_alert_configuration.py)

#### 🌐 Endpoint

`/providers/{provider_id}/integrations/syncro/alerts/{alert_UUID}/configuration` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.update_configuration`

Update the Autotask integration configuration. A 422 Unprocessable Entity response means the server failed to validate with Autotask.

#### 🛠️ Usage

```python
update_configuration_response = jumpcloud.providers.update_configuration(
    uuid="UUID_example",
    secret="string_example",
    username="string_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### secret: `str`

The secret for connecting to Autotask.

##### username: `str`

The username for connecting to Autotask.

#### ⚙️ Request Body

[`AutotaskIntegrationPatchReq`](./jump_cloud_python_sdk/type/autotask_integration_patch_req.py)
#### 🔄 Return

[`AutotaskIntegration`](./jump_cloud_python_sdk/pydantic/autotask_integration.py)

#### 🌐 Endpoint

`/integrations/autotask/{UUID}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.update_configuration_0`

Update the ConnectWise integration configuration. A 422 Unprocessable Entity response means the server failed to validate with ConnectWise.

#### 🛠️ Usage

```python
update_configuration_0_response = jumpcloud.providers.update_configuration_0(
    uuid="UUID_example",
    company_id="string_example",
    private_key="string_example",
    public_key="string_example",
    url="string_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### company_id: `str`

The ConnectWise company identifier.

##### private_key: `str`

The ConnectWise private key for authentication

##### public_key: `str`

The ConnectWise public key for authentication.

##### url: `str`

The base url for connecting to ConnectWise.

#### ⚙️ Request Body

[`ConnectwiseIntegrationPatchReq`](./jump_cloud_python_sdk/type/connectwise_integration_patch_req.py)
#### 🔄 Return

[`ConnectwiseIntegration`](./jump_cloud_python_sdk/pydantic/connectwise_integration.py)

#### 🌐 Endpoint

`/integrations/connectwise/{UUID}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.update_configuration_1`

Update the Syncro integration configuration. A 422 Unprocessable Entity response means the server failed to validate with Syncro.

#### 🛠️ Usage

```python
update_configuration_1_response = jumpcloud.providers.update_configuration_1(
    uuid="UUID_example",
    api_token="string_example",
    subdomain="string_example",
)
```

#### ⚙️ Parameters

##### uuid: `str`

##### api_token: `str`

The Syncro API token for authentication

##### subdomain: `str`

The subdomain for the URL to connect to Syncro.

#### ⚙️ Request Body

[`SyncroIntegrationPatchReq`](./jump_cloud_python_sdk/type/syncro_integration_patch_req.py)
#### 🔄 Return

[`SyncroIntegration`](./jump_cloud_python_sdk/pydantic/syncro_integration.py)

#### 🌐 Endpoint

`/integrations/syncro/{UUID}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.providers.update_org`

This endpoint updates a provider's organization

#### 🛠️ Usage

```python
update_org_response = jumpcloud.providers.update_org(
    provider_id="provider_id_example",
    id="id_example",
    id="624d9eae6849cf3b3f93dc56",
    max_system_users=1,
    name="Acme Inc",
)
```

#### ⚙️ Parameters

##### provider_id: `str`

##### id: `str`

##### id: `str`

##### max_system_users: `int`

The maximum number of users allowed in this organization. Requires organizations.billing scope to modify.

##### name: `str`

#### ⚙️ Request Body

[`Organization`](./jump_cloud_python_sdk/type/organization.py)
#### 🔄 Return

[`Organization`](./jump_cloud_python_sdk/pydantic/organization.py)

#### 🌐 Endpoint

`/providers/{provider_id}/organizations/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.push_verification.get`

Endpoint for retrieving a verification push notification status

#### 🛠️ Usage

```python
get_response = jumpcloud.push_verification.get(
    verification_id="verificationId_example",
)
```

#### ⚙️ Parameters

##### verification_id: `str`

#### 🔄 Return

[`JumpcloudAuthPushVerification`](./jump_cloud_python_sdk/pydantic/jumpcloud_auth_push_verification.py)

#### 🌐 Endpoint

`/pushendpoints/verifications/{verificationId}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.push_verification.start`

Endpoint for sending a verification push notification

#### 🛠️ Usage

```python
start_response = jumpcloud.push_verification.start(
    user_id='YQ==',
    push_endpoint_id='YQ==',
    message="string_example",
)
```

#### ⚙️ Parameters

##### user_id: `str`

##### push_endpoint_id: `str`

##### message: `str`

#### ⚙️ Request Body

[`PushVerificationsStartRequest`](./jump_cloud_python_sdk/type/push_verifications_start_request.py)
#### 🔄 Return

[`JumpcloudAuthPushVerification`](./jump_cloud_python_sdk/pydantic/jumpcloud_auth_push_verification.py)

#### 🌐 Endpoint

`/users/{userId}/pushendpoints/{pushEndpointId}/verify` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.radius_servers.radius_server_associations_list`

This endpoint returns the _direct_ associations of a Radius Server.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Radius Servers and Users.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/radiusservers/{RADIUS_ID}/associations?targets=user_group \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
radius_server_associations_list_response = jumpcloud.radius_servers.radius_server_associations_list(
    radiusserver_id="radiusserver_id_example",
    targets=[
        "user"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### radiusserver_id: `str`

ObjectID of the Radius Server.

##### targets: List[`str`]

Targets which a \"radius_server\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphRadiusServerAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_radius_server_associations_list_response.py)

#### 🌐 Endpoint

`/radiusservers/{radiusserver_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.radius_servers.radius_server_associations_post`

This endpoint allows you to manage the _direct_ associations of a Radius Server.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Radius Servers and Users.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/radiusservers/{RADIUS_ID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{

	
"type":"user", 
"id":"{USER_ID}", 
"op":"add"
	
}'
```

#### 🛠️ Usage

```python
jumpcloud.radius_servers.radius_server_associations_post(
    radiusserver_id="radiusserver_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### radiusserver_id: `str`

ObjectID of the Radius Server.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

Targets which a \\\"radius_server\\\" can be associated to.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationRadiusServer`](./jump_cloud_python_sdk/type/graph_operation_radius_server.py)
#### 🌐 Endpoint

`/radiusservers/{radiusserver_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.radius_servers.radius_server_traverse_user`

This endpoint will return all Users bound to a RADIUS Server, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this RADIUS server instance to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this RADIUS server instance.

See `/members` and `/associations` endpoints to manage those collections.


#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
radius_server_traverse_user_response = jumpcloud.radius_servers.radius_server_traverse_user(
    radiusserver_id="radiusserver_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### radiusserver_id: `str`

ObjectID of the Radius Server.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphRadiusServerTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_radius_server_traverse_user_response.py)

#### 🌐 Endpoint

`/radiusservers/{radiusserver_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.radius_servers.radius_server_traverse_user_group`

This endpoint will return all Users Groups bound to a RADIUS Server, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this RADIUS server instance to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this RADIUS server instance.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/radiusservers/{RADIUS_ID}/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
radius_server_traverse_user_group_response = jumpcloud.radius_servers.radius_server_traverse_user_group(
    radiusserver_id="radiusserver_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### radiusserver_id: `str`

ObjectID of the Radius Server.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphRadiusServerTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_radius_server_traverse_user_group_response.py)

#### 🌐 Endpoint

`/radiusservers/{radiusserver_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.scim_import.users`

Get a list of users to import from an Application IdM service provider.

#### 🛠️ Usage

```python
users_response = jumpcloud.scim_import.users(
    application_id="application_id_example",
    filter="",
    query="",
    sort="",
    sort_order="asc",
    x_org_id="string_example",
    limit=10,
    skip=0,
)
```

#### ⚙️ Parameters

##### application_id: `str`

ObjectID of the Application.

##### filter: `str`

Filter users by a search term

##### query: `str`

URL query to merge with the service provider request

##### sort: `str`

Sort users by supported fields

##### sort_order: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

#### 🔄 Return

[`ImportUsersResponse`](./jump_cloud_python_sdk/pydantic/import_users_response.py)

#### 🌐 Endpoint

`/applications/{application_id}/import/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.samba_domains.samba_domains_delete`

This endpoint allows you to delete a samba domain from an LDAP server.

##### Sample Request
```
curl -X DELETE https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/sambadomains/{SAMBA_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
samba_domains_delete_response = jumpcloud.samba_domains.samba_domains_delete(
    ldapserver_id="ldapserver_id_example",
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### ldapserver_id: `str`

Unique identifier of the LDAP server.

##### id: `str`

Unique identifier of the samba domain.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint

`/ldapservers/{ldapserver_id}/sambadomains/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.samba_domains.samba_domains_get`

This endpoint returns a specific samba domain for an LDAP server.

##### Sample Request
```
curl -X GET \
  https://console.jumpcloud.com/api/v2/ldapservers/ldapservers/{LDAP_ID}/sambadomains/{SAMBA_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
samba_domains_get_response = jumpcloud.samba_domains.samba_domains_get(
    ldapserver_id="ldapserver_id_example",
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### ldapserver_id: `str`

Unique identifier of the LDAP server.

##### id: `str`

Unique identifier of the samba domain.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`SambaDomain`](./jump_cloud_python_sdk/pydantic/samba_domain.py)

#### 🌐 Endpoint

`/ldapservers/{ldapserver_id}/sambadomains/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.samba_domains.samba_domains_list`

This endpoint returns all samba domains for an LDAP server.

##### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/sambadomains \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
samba_domains_list_response = jumpcloud.samba_domains.samba_domains_list(
    ldapserver_id="ldapserver_id_example",
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### ldapserver_id: `str`

Unique identifier of the LDAP server.

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`LdapserversSambaDomainsListResponse`](./jump_cloud_python_sdk/pydantic/ldapservers_samba_domains_list_response.py)

#### 🌐 Endpoint

`/ldapservers/{ldapserver_id}/sambadomains` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.samba_domains.samba_domains_post`

This endpoint allows you to create a samba domain for an LDAP server.

##### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/sambadomains \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "sid":"{SID_ID}",
    "name":"{WORKGROUP_NAME}"
  }'
```

#### 🛠️ Usage

```python
samba_domains_post_response = jumpcloud.samba_domains.samba_domains_post(
    name="string_example",
    sid="string_example",
    ldapserver_id="ldapserver_id_example",
    id="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### name: `str`

Name of this domain's WorkGroup

##### sid: `str`

Security identifier of this domain

##### ldapserver_id: `str`

Unique identifier of the LDAP server.

##### id: `str`

Unique identifier of this domain

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`SambaDomain`](./jump_cloud_python_sdk/type/samba_domain.py)
#### 🔄 Return

[`SambaDomain`](./jump_cloud_python_sdk/pydantic/samba_domain.py)

#### 🌐 Endpoint

`/ldapservers/{ldapserver_id}/sambadomains` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.samba_domains.samba_domains_put`

This endpoint allows you to update the samba domain information for an LDAP server.

##### Sample Request
```
curl -X PUT https://console.jumpcloud.com/api/v2/ldapservers/{LDAP_ID}/sambadomains/{SAMBA_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "sid":"{SID_ID}",
    "name":"{WORKGROUP_NAME}"
  }'
```

#### 🛠️ Usage

```python
samba_domains_put_response = jumpcloud.samba_domains.samba_domains_put(
    name="string_example",
    sid="string_example",
    ldapserver_id="ldapserver_id_example",
    id="id_example",
    id="string_example",
)
```

#### ⚙️ Parameters

##### name: `str`

Name of this domain's WorkGroup

##### sid: `str`

Security identifier of this domain

##### ldapserver_id: `str`

Unique identifier of the LDAP server.

##### id: `str`

Unique identifier of the samba domain.

##### id: `str`

Unique identifier of this domain

#### ⚙️ Request Body

[`SambaDomain`](./jump_cloud_python_sdk/type/samba_domain.py)
#### 🔄 Return

[`SambaDomain`](./jump_cloud_python_sdk/pydantic/samba_domain.py)

#### 🌐 Endpoint

`/ldapservers/{ldapserver_id}/sambadomains/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.delete`

Removes a Software Application configuration.

Warning: This is a destructive operation and will unmanage the application on all affected systems.

#### Sample Request
```
curl -X DELETE https://console.jumpcloud.com/api/v2/softwareapps/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
jumpcloud.software_apps.delete(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint

`/softwareapps/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.get`

Retrieves a Software Application.
The optional isConfigEnabled and appConfiguration apple_vpp attributes are populated in this response.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/softwareapps/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
get_response = jumpcloud.software_apps.get(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`SoftwareApp`](./jump_cloud_python_sdk/pydantic/software_app.py)

#### 🌐 Endpoint

`/softwareapps/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.list`

This endpoint allows you to get all configured Software Applications that will be managed by JumpCloud on associated JumpCloud systems.
The optional isConfigEnabled and appConfiguration apple_vpp attributes are not included in the response.

#### Sample Request
```
$ curl -X GET https://console.jumpcloud.com/api/v2/softwareapps \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage

```python
list_response = jumpcloud.software_apps.list(
    x_org_id="string_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`SoftwareAppsListResponse`](./jump_cloud_python_sdk/pydantic/software_apps_list_response.py)

#### 🌐 Endpoint

`/softwareapps` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.list_0`

This endpoint allows you to get the status of the provided Software Application on associated JumpCloud systems.

#### Sample Request
```
$ curl -X GET https://console.jumpcloud.com/api/v2/softwareapps/{software_app_id}/statuses \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'x-api-key: {API_KEY}' \
```

#### 🛠️ Usage

```python
list_0_response = jumpcloud.software_apps.list_0(
    software_app_id="software_app_id_example",
    x_org_id="string_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### software_app_id: `str`

ObjectID of the Software App.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`SoftwareAppStatusesListResponse`](./jump_cloud_python_sdk/pydantic/software_app_statuses_list_response.py)

#### 🌐 Endpoint

`/softwareapps/{software_app_id}/statuses` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.post`

This endpoint allows you to create a Software Application that will be managed by JumpCloud on associated JumpCloud systems.
The optional isConfigEnabled and appConfiguration apple_vpp attributes are not included in the response.

#### Sample Request
```
$ curl -X POST https://console.jumpcloud.com/api/v2/softwareapps \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'x-api-key: {API_KEY}' \
-d '{
  "displayName": "Adobe Reader",
  "settings": [{"packageId": "adobereader"}]
}'
```

#### 🛠️ Usage

```python
post_response = jumpcloud.software_apps.post(
    display_name="string_example",
    id="string_example",
    settings=[
        {
            "allow_update_delay": False,
            "auto_update": False,
            "desired_state": "string",
            "location": "string",
            "location_object_id": "string",
            "package_id": "string",
            "package_manager": "string",
        }
    ],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### display_name: `str`

##### id: `str`

##### settings: List[`SoftwareAppSettings`]

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`SoftwareApp`](./jump_cloud_python_sdk/type/software_app.py)
#### 🔄 Return

[`SoftwareAppCreate`](./jump_cloud_python_sdk/pydantic/software_app_create.py)

#### 🌐 Endpoint

`/softwareapps` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.reclaim_licenses`

This endpoint allows you to reclaim the licenses from a software app associated with devices that are deleted.
#### Sample Request
```
$ curl -X POST https://console.jumpcloud.com/api/v2/softwareapps/{software_app_id}/reclaim-licenses \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'x-api-key: {API_KEY}' \
-d '{}'
```

#### 🛠️ Usage

```python
reclaim_licenses_response = jumpcloud.software_apps.reclaim_licenses(
    software_app_id="software_app_id_example",
)
```

#### ⚙️ Parameters

##### software_app_id: `str`

#### 🔄 Return

[`SoftwareAppReclaimLicenses`](./jump_cloud_python_sdk/pydantic/software_app_reclaim_licenses.py)

#### 🌐 Endpoint

`/softwareapps/{software_app_id}/reclaim-licenses` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.retry_installation`

This endpoints initiates an installation retry of an Apple VPP App for the provided system IDs
#### Sample Request
```
$ curl -X POST https://console.jumpcloud.com/api/v2/softwareapps/{software_app_id}/retry-installation \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'x-api-key: {API_KEY}' \
-d '{"system_ids": "{<system_id_1>, <system_id_2>, ...}"}'
```

#### 🛠️ Usage

```python
jumpcloud.software_apps.retry_installation(
    software_app_id="software_app_id_example",
)
```

#### ⚙️ Parameters

##### software_app_id: `str`

#### 🌐 Endpoint

`/softwareapps/{software_app_id}/retry-installation` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.softwareapps_associations_list`

This endpoint will return the _direct_ associations of a Software Application. A direct association can be a non-homogeneous relationship between 2 different objects, for example Software Application and System Groups.


#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/softwareapps/{software_app_id}/associations?targets=system_group \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
softwareapps_associations_list_response = jumpcloud.software_apps.softwareapps_associations_list(
    software_app_id="software_app_id_example",
    targets=[
        "system"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### software_app_id: `str`

ObjectID of the Software App.

##### targets: List[`str`]

Targets which a \"software_app\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphSoftwareappsAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_softwareapps_associations_list_response.py)

#### 🌐 Endpoint

`/softwareapps/{software_app_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.softwareapps_associations_post`

This endpoint allows you to associate or disassociate a software application to a system or system group.

#### Sample Request
```
$ curl -X POST https://console.jumpcloud.com/api/v2/softwareapps/{software_app_id}/associations \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'x-api-key: {API_KEY}' \
-d '{
  "id": "<object_id>",
  "op": "add",
  "type": "system"
 }'
```

#### 🛠️ Usage

```python
jumpcloud.software_apps.softwareapps_associations_post(
    software_app_id="software_app_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### software_app_id: `str`

ObjectID of the Software App.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

Targets which a \\\"software_app\\\" can be associated to.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationSoftwareApp`](./jump_cloud_python_sdk/type/graph_operation_software_app.py)
#### 🌐 Endpoint

`/softwareapps/{software_app_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.softwareapps_traverse_system`

This endpoint will return all Systems bound to a Software App, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Software App to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this Software App.

See `/associations` endpoint to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/softwareapps/{software_app_id}/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
softwareapps_traverse_system_response = jumpcloud.software_apps.softwareapps_traverse_system(
    software_app_id="software_app_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### software_app_id: `str`

ObjectID of the Software App.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSoftwareappsTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_softwareapps_traverse_system_response.py)

#### 🌐 Endpoint

`/softwareapps/{software_app_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.softwareapps_traverse_system_group`

This endpoint will return all Systems Groups bound to a Software App, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this Software App to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this Software App.

See `/associations` endpoint to manage those collections.

#### Sample Request
```
curl -X GET  https://console.jumpcloud.com/api/v2/softwareapps/{software_app_id}/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
softwareapps_traverse_system_group_response = jumpcloud.software_apps.softwareapps_traverse_system_group(
    software_app_id="software_app_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### software_app_id: `str`

ObjectID of the Software App.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSoftwareappsTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_softwareapps_traverse_system_group_response.py)

#### 🌐 Endpoint

`/softwareapps/{software_app_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.update`

This endpoint updates a specific Software Application configuration for the organization.
displayName can be changed alone if no settings are provided.
If a setting is provided, it should include all its information since this endpoint will update all the settings' fields.
The optional isConfigEnabled and appConfiguration apple_vpp attributes are not included in the response.

#### Sample Request - displayName only
```
 curl -X PUT https://console.jumpcloud.com/api/v2/softwareapps/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "displayName": "My Software App"
  }'
```

#### Sample Request - all attributes
```
 curl -X PUT https://console.jumpcloud.com/api/v2/softwareapps/{id} \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "displayName": "My Software App",
    "settings": [
      {
        "packageId": "123456",
        "autoUpdate": false,
        "allowUpdateDelay": false,
        "packageManager": "APPLE_VPP",
        "locationObjectId": "123456789012123456789012",
        "location": "123456",
        "desiredState": "Install",
        "appleVpp": {
          "appConfiguration": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\"><plist version=\"1.0\"><dict><key>MyKey</key><string>My String</string></dict></plist>",
          "assignedLicenses": 20,
          "availableLicenses": 10,
          "details": {},
          "isConfigEnabled": true,
          "supportedDeviceFamilies": [
            "IPAD",
            "MAC"
          ],
          "totalLicenses": 30
        },
        "packageSubtitle": "My package subtitle",
        "packageVersion": "1.2.3",
        "packageKind": "software-package",
        "assetKind": "software",
        "assetSha256Size": 256,
        "assetSha256Strings": [
          "a123b123c123d123"
        ],
        "description": "My app description"
      }
    ]
  }'
```

#### 🛠️ Usage

```python
update_response = jumpcloud.software_apps.update(
    id="id_example",
    display_name="string_example",
    id="string_example",
    settings=[
        {
            "allow_update_delay": False,
            "auto_update": False,
            "desired_state": "string",
            "location": "string",
            "location_object_id": "string",
            "package_id": "string",
            "package_manager": "string",
        }
    ],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

##### display_name: `str`

##### id: `str`

##### settings: List[`SoftwareAppSettings`]

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`SoftwareApp`](./jump_cloud_python_sdk/type/software_app.py)
#### 🔄 Return

[`SoftwareApp`](./jump_cloud_python_sdk/pydantic/software_app.py)

#### 🌐 Endpoint

`/softwareapps/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.software_apps.validate_application_install_package`

Validates an application install package from the specified URL to calculate the SHA256 hash and extract the installer manifest details.
#### Sample Request
```
curl -H 'x-api-key: {API_KEY}' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{"url": "https://dl.google.com/dl/chrome/mac/universal/stable/gcem/GoogleChrome.pkg"}' \
-i -X POST https://console.jumpcloud.com/api/v2/softwareapps/validate
```

#### 🛠️ Usage

```python
validate_application_install_package_response = jumpcloud.software_apps.validate_application_install_package(
    url="string_example",
)
```

#### ⚙️ Parameters

##### url: `str`

#### ⚙️ Request Body

[`JumpcloudPackageValidatorValidateApplicationInstallPackageRequest`](./jump_cloud_python_sdk/type/jumpcloud_package_validator_validate_application_install_package_request.py)
#### 🔄 Return

[`JumpcloudPackageValidatorValidateApplicationInstallPackageResponse`](./jump_cloud_python_sdk/pydantic/jumpcloud_package_validator_validate_application_install_package_response.py)

#### 🌐 Endpoint

`/softwareapps/validate` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.subscriptions.get`

This endpoint returns all pricing & packaging subscriptions.

##### Sample Request

```
 curl -X GET  https://console.jumpcloud.com/api/v2/subscriptions \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
get_response = jumpcloud.subscriptions.get()
```

#### 🔄 Return

[`SubscriptionsGetResponse`](./jump_cloud_python_sdk/pydantic/subscriptions_get_response.py)

#### 🌐 Endpoint

`/subscriptions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_group_associations.system_group_associations_list`

This endpoint returns the _direct_ associations of a System Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example System Groups and Users.


#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/associations?targets=user \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
system_group_associations_list_response = jumpcloud.system_group_associations.system_group_associations_list(
    group_id="group_id_example",
    targets=[
        "command"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### targets: List[`str`]

Targets which a \"system_group\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphSystemGroupAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_associations_list_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_group_associations.system_group_associations_post`

This endpoint allows you to manage the _direct_ associations of a System Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example System Groups and Users.


#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user",
    "id": "{UserID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.system_group_associations.system_group_associations_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="command",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

Targets which a \\\"system_group\\\" can be associated to.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationSystemGroup`](./jump_cloud_python_sdk/type/graph_operation_system_group.py)
#### 🌐 Endpoint

`/systemgroups/{group_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_group_associations.system_group_traverse_command`

This endpoint will return all Commands bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the group's type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding Command; this array represents all grouping and/or associations that would have to be removed to deprovision the Command from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/commands \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
system_group_traverse_command_response = jumpcloud.system_group_associations.system_group_traverse_command(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
    details="v1",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### details: `str`

This will provide detail descriptive response for the request.

#### 🔄 Return

[`GraphSystemGroupTraverseCommandResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_command_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/commands` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_group_associations.system_group_traverse_policy`

This endpoint will return all Policies bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding Policy; this array represents all grouping and/or associations that would have to be removed to deprovision the Policy from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

This endpoint is not public yet as we haven't finished the code.

##### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/policies \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
system_group_traverse_policy_response = jumpcloud.system_group_associations.system_group_traverse_policy(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemGroupTraversePolicyResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_policy_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/policies` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_group_associations.system_group_traverse_policy_group`

This endpoint will return all Policy Groups bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding Policy Group; this array represents all grouping and/or associations that would have to be removed to deprovision the Policy Group from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/policygroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_group_traverse_policy_group_response = jumpcloud.system_group_associations.system_group_traverse_policy_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemGroupTraversePolicyGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_policy_group_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/policygroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_group_associations.system_group_traverse_user`

This endpoint will return all Users bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
system_group_traverse_user_response = jumpcloud.system_group_associations.system_group_traverse_user(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemGroupTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_user_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_group_associations.system_group_traverse_user_group`

This endpoint will return all User Groups bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_group_traverse_user_group_response = jumpcloud.system_group_associations.system_group_traverse_user_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemGroupTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_user_group_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_group_members_&amp;_membership.system_group_members_list`

This endpoint returns the system members of a System Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_group_members_list_response = jumpcloud.system_group_members_&amp;_membership.system_group_members_list(
    group_id="group_id_example",
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphSystemGroupMembersListResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_members_list_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_group_members_&amp;_membership.system_group_members_post`

This endpoint allows you to manage the system members of a System Group.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system",
    "id": "{System_ID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.system_group_members_&amp;_membership.system_group_members_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    date="string_example",
    authorization="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

The member type.

##### date: `str`

Current date header for the System Context API

##### authorization: `str`

Authorization header for the System Context API

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationSystemGroupMember`](./jump_cloud_python_sdk/type/graph_operation_system_group_member.py)
#### 🌐 Endpoint

`/systemgroups/{group_id}/members` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_group_members_&amp;_membership.system_group_membership`

This endpoint returns all Systems that are a member of this System Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID/membership \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_group_membership_response = jumpcloud.system_group_members_&amp;_membership.system_group_membership(
    group_id="group_id_example",
    limit=10,
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphSystemGroupMembershipResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_membership_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/membership` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.apply_suggestions`

This endpoint applies the suggestions for the specified system group.
#### Sample Request
```
curl -X PUT https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/suggestions \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
         "object_ids": ["212345678901234567890123",
                      "123456789012345678901234"]
     }'
```

#### 🛠️ Usage

```python
apply_suggestions_response = jumpcloud.system_groups.apply_suggestions(
    group_id="group_id_example",
    object_ids=[
        "string_example"
    ],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ID of the group

##### object_ids: [`SystemGroupsApplySuggestionsRequestObjectIds`](./jump_cloud_python_sdk/type/system_groups_apply_suggestions_request_object_ids.py)

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`SystemGroupsApplySuggestionsRequest`](./jump_cloud_python_sdk/type/system_groups_apply_suggestions_request.py)
#### 🌐 Endpoint

`/systemgroups/{group_id}/suggestions` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.create_new_group`

This endpoint allows you to create a new System Group.

See the [Dynamic Group Configuration KB article](https://jumpcloud.com/support/configure-dynamic-device-groups) for more details on maintaining a Dynamic Group.

#### Sample Request

```
curl -X POST https://console.jumpcloud.com/api/v2/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "{Group_Name}"
  }'
```

#### 🛠️ Usage

```python
create_new_group_response = jumpcloud.system_groups.create_new_group(
    name="string_example",
    description="string_example",
    attributes={},
    email="string_example",
    member_query=None,
    member_query_exemptions=[
        {
            "id": "id_example",
            "type": "type_example",
        }
    ],
    member_suggestions_notify=True,
    membership_method="NOTSET",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### name: `str`

Display name of a System Group.

##### description: `str`

Description of a System Group

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### email: `str`

Email address of a System Group

##### member_query: [`MemberQuery`](./jump_cloud_python_sdk/type/member_query.py)


##### member_query_exemptions: List[`GraphObject`]

Array of GraphObjects exempted from the query

##### member_suggestions_notify: `bool`

True if notification emails are to be sent for membership suggestions.

##### membership_method: [`GroupMembershipMethodType`](./jump_cloud_python_sdk/type/group_membership_method_type.py)

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`SystemGroupPost`](./jump_cloud_python_sdk/type/system_group_post.py)
#### 🔄 Return

[`SystemGroup`](./jump_cloud_python_sdk/pydantic/system_group.py)

#### 🌐 Endpoint

`/systemgroups` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.delete_group`

This endpoint allows you to delete a System Group.

#### Sample Request
```
curl -X DELETE https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
delete_group_response = jumpcloud.system_groups.delete_group(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

ObjectID of the System Group.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`SystemGroup`](./jump_cloud_python_sdk/pydantic/system_group.py)

#### 🌐 Endpoint

`/systemgroups/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.list_all`

This endpoint returns all System Groups.

Available filter fields:
  - `name`
  - `disabled`
  - `type`
  - `membershipMethod`

#### Sample Request

```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
list_all_response = jumpcloud.system_groups.list_all(
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`SystemGroupsListAllResponse`](./jump_cloud_python_sdk/pydantic/system_groups_list_all_response.py)

#### 🌐 Endpoint

`/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.list_suggestions`

This endpoint returns available suggestions for a given system group
#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/suggestions \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
list_suggestions_response = jumpcloud.system_groups.list_suggestions(
    group_id="group_id_example",
    x_org_id="string_example",
    limit=10,
    skip=0,
)
```

#### ⚙️ Parameters

##### group_id: `str`

ID of the group

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

#### 🔄 Return

[`SystemGroupsListSuggestionsResponse`](./jump_cloud_python_sdk/pydantic/system_groups_list_suggestions_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/suggestions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.system_group_associations_list`

This endpoint returns the _direct_ associations of a System Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example System Groups and Users.


#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/associations?targets=user \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
system_group_associations_list_response = jumpcloud.system_groups.system_group_associations_list(
    group_id="group_id_example",
    targets=[
        "command"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### targets: List[`str`]

Targets which a \"system_group\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphSystemGroupAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_associations_list_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.system_group_associations_post`

This endpoint allows you to manage the _direct_ associations of a System Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example System Groups and Users.


#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user",
    "id": "{UserID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.system_groups.system_group_associations_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="command",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

Targets which a \\\"system_group\\\" can be associated to.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationSystemGroup`](./jump_cloud_python_sdk/type/graph_operation_system_group.py)
#### 🌐 Endpoint

`/systemgroups/{group_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.system_group_members_list`

This endpoint returns the system members of a System Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_group_members_list_response = jumpcloud.system_groups.system_group_members_list(
    group_id="group_id_example",
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphSystemGroupMembersListResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_members_list_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.system_group_members_post`

This endpoint allows you to manage the system members of a System Group.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system",
    "id": "{System_ID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.system_groups.system_group_members_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="system",
    date="string_example",
    authorization="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

The member type.

##### date: `str`

Current date header for the System Context API

##### authorization: `str`

Authorization header for the System Context API

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationSystemGroupMember`](./jump_cloud_python_sdk/type/graph_operation_system_group_member.py)
#### 🌐 Endpoint

`/systemgroups/{group_id}/members` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.system_group_membership`

This endpoint returns all Systems that are a member of this System Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID/membership \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_group_membership_response = jumpcloud.system_groups.system_group_membership(
    group_id="group_id_example",
    limit=10,
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphSystemGroupMembershipResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_membership_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/membership` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.system_group_traverse_policy`

This endpoint will return all Policies bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding Policy; this array represents all grouping and/or associations that would have to be removed to deprovision the Policy from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

This endpoint is not public yet as we haven't finished the code.

##### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/policies \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
system_group_traverse_policy_response = jumpcloud.system_groups.system_group_traverse_policy(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemGroupTraversePolicyResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_policy_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/policies` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.system_group_traverse_policy_group`

This endpoint will return all Policy Groups bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding Policy Group; this array represents all grouping and/or associations that would have to be removed to deprovision the Policy Group from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/policygroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_group_traverse_policy_group_response = jumpcloud.system_groups.system_group_traverse_policy_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemGroupTraversePolicyGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_policy_group_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/policygroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.system_group_traverse_user`

This endpoint will return all Users bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
system_group_traverse_user_response = jumpcloud.system_groups.system_group_traverse_user(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemGroupTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_user_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.system_group_traverse_user_group`

This endpoint will return all User Groups bound to a System Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System Group to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this System Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{GroupID}/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_group_traverse_user_group_response = jumpcloud.system_groups.system_group_traverse_user_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the System Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemGroupTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_system_group_traverse_user_group_response.py)

#### 🌐 Endpoint

`/systemgroups/{group_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.update_group`

This endpoint allows you to do a full update of the System Group.

See the [Dynamic Group Configuration KB article](https://jumpcloud.com/support/configure-dynamic-device-groups) for more details on maintaining a Dynamic Group.

#### Sample Request
```
curl -X PUT https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "Name_Update"
  }'
```

#### 🛠️ Usage

```python
update_group_response = jumpcloud.system_groups.update_group(
    name="string_example",
    id="id_example",
    description="string_example",
    attributes={},
    email="string_example",
    member_query=None,
    member_query_exemptions=[
        {
            "id": "id_example",
            "type": "type_example",
        }
    ],
    member_suggestions_notify=True,
    membership_method="NOTSET",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### name: `str`

Display name of a System Group.

##### id: `str`

ObjectID of the System Group.

##### description: `str`

Description of a System Group

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### email: `str`

Email address of a System Group

##### member_query: [`MemberQuery`](./jump_cloud_python_sdk/type/member_query.py)


##### member_query_exemptions: List[`GraphObject`]

Array of GraphObjects exempted from the query

##### member_suggestions_notify: `bool`

True if notification emails are to be sent for membership suggestions.

##### membership_method: [`GroupMembershipMethodType`](./jump_cloud_python_sdk/type/group_membership_method_type.py)

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`SystemGroupPut`](./jump_cloud_python_sdk/type/system_group_put.py)
#### 🔄 Return

[`SystemGroup`](./jump_cloud_python_sdk/pydantic/system_group.py)

#### 🌐 Endpoint

`/systemgroups/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_groups.view_details`

This endpoint returns the details of a System Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups/{Group_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
view_details_response = jumpcloud.system_groups.view_details(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

ObjectID of the System Group.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`SystemGroup`](./jump_cloud_python_sdk/pydantic/system_group.py)

#### 🌐 Endpoint

`/systemgroups/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.get_chassis_info`

Valid filter fields are `system_id`.

#### 🛠️ Usage

```python
get_chassis_info_response = jumpcloud.system_insights.get_chassis_info(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsGetChassisInfoResponse`](./jump_cloud_python_sdk/pydantic/system_insights_get_chassis_info_response.py)

#### 🌐 Endpoint

`/systeminsights/chassis_info` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.get_disk_info`

Valid filter fields are `system_id` and `disk_index`.

#### 🛠️ Usage

```python
get_disk_info_response = jumpcloud.system_insights.get_disk_info(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsGetDiskInfoResponse`](./jump_cloud_python_sdk/pydantic/system_insights_get_disk_info_response.py)

#### 🌐 Endpoint

`/systeminsights/disk_info` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.get_ie_extensions_list`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
get_ie_extensions_list_response = jumpcloud.system_insights.get_ie_extensions_list(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsGetIeExtensionsListResponse`](./jump_cloud_python_sdk/pydantic/system_insights_get_ie_extensions_list_response.py)

#### 🌐 Endpoint

`/systeminsights/ie_extensions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.get_kernel_info`

Valid filter fields are `system_id` and `version`.

#### 🛠️ Usage

```python
get_kernel_info_response = jumpcloud.system_insights.get_kernel_info(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsGetKernelInfoResponse`](./jump_cloud_python_sdk/pydantic/system_insights_get_kernel_info_response.py)

#### 🌐 Endpoint

`/systeminsights/kernel_info` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.get_os_version`

Valid filter fields are `system_id` and `version`.

#### 🛠️ Usage

```python
get_os_version_response = jumpcloud.system_insights.get_os_version(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsGetOsVersionResponse`](./jump_cloud_python_sdk/pydantic/system_insights_get_os_version_response.py)

#### 🌐 Endpoint

`/systeminsights/os_version` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.get_sip_config`

Valid filter fields are `system_id` and `enabled`.

#### 🛠️ Usage

```python
get_sip_config_response = jumpcloud.system_insights.get_sip_config(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsGetSipConfigResponse`](./jump_cloud_python_sdk/pydantic/system_insights_get_sip_config_response.py)

#### 🌐 Endpoint

`/systeminsights/sip_config` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.get_system_info_list`

Valid filter fields are `system_id` and `cpu_subtype`.

#### 🛠️ Usage

```python
get_system_info_list_response = jumpcloud.system_insights.get_system_info_list(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsGetSystemInfoListResponse`](./jump_cloud_python_sdk/pydantic/system_insights_get_system_info_list_response.py)

#### 🌐 Endpoint

`/systeminsights/system_info` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.get_tpm_info`

Valid filter fields are `system_id`.

#### 🛠️ Usage

```python
get_tpm_info_response = jumpcloud.system_insights.get_tpm_info(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsGetTpmInfoResponse`](./jump_cloud_python_sdk/pydantic/system_insights_get_tpm_info_response.py)

#### 🌐 Endpoint

`/systeminsights/tpm_info` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.get_user_groups`

Only valid filter field is `system_id`.

#### 🛠️ Usage

```python
get_user_groups_response = jumpcloud.system_insights.get_user_groups(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsGetUserGroupsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_get_user_groups_response.py)

#### 🌐 Endpoint

`/systeminsights/user_groups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_alf`

Valid filter fields are `system_id` and `global_state`.

#### 🛠️ Usage

```python
list_alf_response = jumpcloud.system_insights.list_alf(
    x_org_id="string_example",
    filter=[],
    skip=0,
    sort=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListAlfResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_alf_response.py)

#### 🌐 Endpoint

`/systeminsights/alf` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_alf_exceptions`

Valid filter fields are `system_id` and `state`.

#### 🛠️ Usage

```python
list_alf_exceptions_response = jumpcloud.system_insights.list_alf_exceptions(
    x_org_id="string_example",
    filter=[],
    skip=0,
    sort=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListAlfExceptionsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_alf_exceptions_response.py)

#### 🌐 Endpoint

`/systeminsights/alf_exceptions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_alf_explicit_auths`

Valid filter fields are `system_id` and `process`.

#### 🛠️ Usage

```python
list_alf_explicit_auths_response = jumpcloud.system_insights.list_alf_explicit_auths(
    x_org_id="string_example",
    filter=[],
    skip=0,
    sort=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListAlfExplicitAuthsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_alf_explicit_auths_response.py)

#### 🌐 Endpoint

`/systeminsights/alf_explicit_auths` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_appcompat_shims`

Valid filter fields are `system_id` and `enabled`.

#### 🛠️ Usage

```python
list_appcompat_shims_response = jumpcloud.system_insights.list_appcompat_shims(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListAppcompatShimsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_appcompat_shims_response.py)

#### 🌐 Endpoint

`/systeminsights/appcompat_shims` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_apps`

Lists all apps for macOS devices. For Windows devices, use [List System Insights Programs](https://docs.jumpcloud.com).

Valid filter fields are `system_id` and `bundle_name`.

#### 🛠️ Usage

```python
list_apps_response = jumpcloud.system_insights.list_apps(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListAppsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_apps_response.py)

#### 🌐 Endpoint

`/systeminsights/apps` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_authorized_keys`

Valid filter fields are `system_id` and `uid`.

#### 🛠️ Usage

```python
list_authorized_keys_response = jumpcloud.system_insights.list_authorized_keys(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListAuthorizedKeysResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_authorized_keys_response.py)

#### 🌐 Endpoint

`/systeminsights/authorized_keys` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_azure_instance_metadata`

Valid filter fields are `system_id`.

#### 🛠️ Usage

```python
list_azure_instance_metadata_response = jumpcloud.system_insights.list_azure_instance_metadata(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListAzureInstanceMetadataResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_azure_instance_metadata_response.py)

#### 🌐 Endpoint

`/systeminsights/azure_instance_metadata` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_azure_instance_tags`

Valid filter fields are `system_id`.

#### 🛠️ Usage

```python
list_azure_instance_tags_response = jumpcloud.system_insights.list_azure_instance_tags(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListAzureInstanceTagsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_azure_instance_tags_response.py)

#### 🌐 Endpoint

`/systeminsights/azure_instance_tags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_battery_data`

Valid filter fields are `system_id` and `health`.

#### 🛠️ Usage

```python
list_battery_data_response = jumpcloud.system_insights.list_battery_data(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListBatteryDataResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_battery_data_response.py)

#### 🌐 Endpoint

`/systeminsights/battery` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_bitlocker_info`

Valid filter fields are `system_id` and `protection_status`.

#### 🛠️ Usage

```python
list_bitlocker_info_response = jumpcloud.system_insights.list_bitlocker_info(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListBitlockerInfoResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_bitlocker_info_response.py)

#### 🌐 Endpoint

`/systeminsights/bitlocker_info` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_browser_plugins`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_browser_plugins_response = jumpcloud.system_insights.list_browser_plugins(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListBrowserPluginsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_browser_plugins_response.py)

#### 🌐 Endpoint

`/systeminsights/browser_plugins` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_certificates`

Valid filter fields are `system_id` and `common_name`.

#### 🛠️ Usage

```python
list_certificates_response = jumpcloud.system_insights.list_certificates(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` Note: You can only filter by `system_id` and `common_name` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListCertificatesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_certificates_response.py)

#### 🌐 Endpoint

`/systeminsights/certificates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_chrome_extensions`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_chrome_extensions_response = jumpcloud.system_insights.list_chrome_extensions(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListChromeExtensionsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_chrome_extensions_response.py)

#### 🌐 Endpoint

`/systeminsights/chrome_extensions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_connectivity`

The only valid filter field is `system_id`.

#### 🛠️ Usage

```python
list_connectivity_response = jumpcloud.system_insights.list_connectivity(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListConnectivityResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_connectivity_response.py)

#### 🌐 Endpoint

`/systeminsights/connectivity` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_crashes`

Valid filter fields are `system_id` and `identifier`.

#### 🛠️ Usage

```python
list_crashes_response = jumpcloud.system_insights.list_crashes(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListCrashesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_crashes_response.py)

#### 🌐 Endpoint

`/systeminsights/crashes` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_cups_destinations`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_cups_destinations_response = jumpcloud.system_insights.list_cups_destinations(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListCupsDestinationsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_cups_destinations_response.py)

#### 🌐 Endpoint

`/systeminsights/cups_destinations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_disk_encryption`

Valid filter fields are `system_id` and `encryption_status`.

#### 🛠️ Usage

```python
list_disk_encryption_response = jumpcloud.system_insights.list_disk_encryption(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListDiskEncryptionResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_disk_encryption_response.py)

#### 🌐 Endpoint

`/systeminsights/disk_encryption` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_dns_resolvers`

Valid filter fields are `system_id` and `type`.

#### 🛠️ Usage

```python
list_dns_resolvers_response = jumpcloud.system_insights.list_dns_resolvers(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListDnsResolversResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_dns_resolvers_response.py)

#### 🌐 Endpoint

`/systeminsights/dns_resolvers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_etc_hosts`

Valid filter fields are `system_id` and `address`.

#### 🛠️ Usage

```python
list_etc_hosts_response = jumpcloud.system_insights.list_etc_hosts(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListEtcHostsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_etc_hosts_response.py)

#### 🌐 Endpoint

`/systeminsights/etc_hosts` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_firefox_addons`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_firefox_addons_response = jumpcloud.system_insights.list_firefox_addons(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListFirefoxAddonsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_firefox_addons_response.py)

#### 🌐 Endpoint

`/systeminsights/firefox_addons` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_groups`

Valid filter fields are `system_id` and `groupname`.

#### 🛠️ Usage

```python
list_groups_response = jumpcloud.system_insights.list_groups(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListGroupsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_groups_response.py)

#### 🌐 Endpoint

`/systeminsights/groups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_interface_addresses`

Valid filter fields are `system_id` and `address`.

#### 🛠️ Usage

```python
list_interface_addresses_response = jumpcloud.system_insights.list_interface_addresses(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListInterfaceAddressesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_interface_addresses_response.py)

#### 🌐 Endpoint

`/systeminsights/interface_addresses` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_interface_details`

Valid filter fields are `system_id` and `interface`.

#### 🛠️ Usage

```python
list_interface_details_response = jumpcloud.system_insights.list_interface_details(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListInterfaceDetailsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_interface_details_response.py)

#### 🌐 Endpoint

`/systeminsights/interface_details` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_launchd`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_launchd_response = jumpcloud.system_insights.list_launchd(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListLaunchdResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_launchd_response.py)

#### 🌐 Endpoint

`/systeminsights/launchd` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_linux_packages`

Lists all programs for Linux devices. For macOS devices, use [List System Insights System Apps](https://docs.jumpcloud.com). For windows devices, use [List System Insights System Apps](https://docs.jumpcloud.com).

Valid filter fields are `name` and `package_format`.

#### 🛠️ Usage

```python
list_linux_packages_response = jumpcloud.system_insights.list_linux_packages(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListLinuxPackagesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_linux_packages_response.py)

#### 🌐 Endpoint

`/systeminsights/linux_packages` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_logged_in_users`

Valid filter fields are `system_id` and `user`.

#### 🛠️ Usage

```python
list_logged_in_users_response = jumpcloud.system_insights.list_logged_in_users(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListLoggedInUsersResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_logged_in_users_response.py)

#### 🌐 Endpoint

`/systeminsights/logged_in_users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_logical_drives`

Valid filter fields are `system_id` and `device_id`.

#### 🛠️ Usage

```python
list_logical_drives_response = jumpcloud.system_insights.list_logical_drives(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListLogicalDrivesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_logical_drives_response.py)

#### 🌐 Endpoint

`/systeminsights/logical_drives` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_managed_policies`

Valid filter fields are `system_id` and `domain`.

#### 🛠️ Usage

```python
list_managed_policies_response = jumpcloud.system_insights.list_managed_policies(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListManagedPoliciesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_managed_policies_response.py)

#### 🌐 Endpoint

`/systeminsights/managed_policies` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_mounts`

Valid filter fields are `system_id` and `path`.

#### 🛠️ Usage

```python
list_mounts_response = jumpcloud.system_insights.list_mounts(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListMountsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_mounts_response.py)

#### 🌐 Endpoint

`/systeminsights/mounts` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_patches`

Valid filter fields are `system_id` and `hotfix_id`.

#### 🛠️ Usage

```python
list_patches_response = jumpcloud.system_insights.list_patches(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListPatchesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_patches_response.py)

#### 🌐 Endpoint

`/systeminsights/patches` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_programs`

Lists all programs for Windows devices. For macOS devices, use [List System Insights Apps](https://docs.jumpcloud.com).

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_programs_response = jumpcloud.system_insights.list_programs(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListProgramsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_programs_response.py)

#### 🌐 Endpoint

`/systeminsights/programs` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_python_packages`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_python_packages_response = jumpcloud.system_insights.list_python_packages(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListPythonPackagesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_python_packages_response.py)

#### 🌐 Endpoint

`/systeminsights/python_packages` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_safari_extensions`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_safari_extensions_response = jumpcloud.system_insights.list_safari_extensions(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListSafariExtensionsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_safari_extensions_response.py)

#### 🌐 Endpoint

`/systeminsights/safari_extensions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_scheduled_tasks`

Valid filter fields are `system_id` and `enabled`.

#### 🛠️ Usage

```python
list_scheduled_tasks_response = jumpcloud.system_insights.list_scheduled_tasks(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListScheduledTasksResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_scheduled_tasks_response.py)

#### 🌐 Endpoint

`/systeminsights/scheduled_tasks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_secure_boot`

Valid filter fields are `system_id`.

#### 🛠️ Usage

```python
list_secure_boot_response = jumpcloud.system_insights.list_secure_boot(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListSecureBootResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_secure_boot_response.py)

#### 🌐 Endpoint

`/systeminsights/secureboot` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_services`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_services_response = jumpcloud.system_insights.list_services(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListServicesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_services_response.py)

#### 🌐 Endpoint

`/systeminsights/services` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_shadow_data`

Valid filter fields are `system_id` and `username`.

#### 🛠️ Usage

```python
list_shadow_data_response = jumpcloud.system_insights.list_shadow_data(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListShadowDataResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_shadow_data_response.py)

#### 🌐 Endpoint

`/systeminsights/shadow` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_shared_folders`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_shared_folders_response = jumpcloud.system_insights.list_shared_folders(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListSharedFoldersResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_shared_folders_response.py)

#### 🌐 Endpoint

`/systeminsights/shared_folders` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_shared_resources`

Valid filter fields are `system_id` and `type`.

#### 🛠️ Usage

```python
list_shared_resources_response = jumpcloud.system_insights.list_shared_resources(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListSharedResourcesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_shared_resources_response.py)

#### 🌐 Endpoint

`/systeminsights/shared_resources` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_sharing_preferences`

Only valid filed field is `system_id`.

#### 🛠️ Usage

```python
list_sharing_preferences_response = jumpcloud.system_insights.list_sharing_preferences(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListSharingPreferencesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_sharing_preferences_response.py)

#### 🌐 Endpoint

`/systeminsights/sharing_preferences` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_startup_items`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_startup_items_response = jumpcloud.system_insights.list_startup_items(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListStartupItemsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_startup_items_response.py)

#### 🌐 Endpoint

`/systeminsights/startup_items` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_system_controls`

Valid filter fields are `system_id` and `name`.

#### 🛠️ Usage

```python
list_system_controls_response = jumpcloud.system_insights.list_system_controls(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` Note: You can only filter by `system_id` and `name` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListSystemControlsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_system_controls_response.py)

#### 🌐 Endpoint

`/systeminsights/system_controls` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_uptime`

Valid filter fields are `system_id` and `days`.

#### 🛠️ Usage

```python
list_uptime_response = jumpcloud.system_insights.list_uptime(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, gte, in. e.g: Filter for single value: `filter=field:gte:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListUptimeResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_uptime_response.py)

#### 🌐 Endpoint

`/systeminsights/uptime` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_usb_devices`

Valid filter fields are `system_id` and `model`.

#### 🛠️ Usage

```python
list_usb_devices_response = jumpcloud.system_insights.list_usb_devices(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListUsbDevicesResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_usb_devices_response.py)

#### 🌐 Endpoint

`/systeminsights/usb_devices` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_user_assist`

Valid filter fields are `system_id`.

#### 🛠️ Usage

```python
list_user_assist_response = jumpcloud.system_insights.list_user_assist(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListUserAssistResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_user_assist_response.py)

#### 🌐 Endpoint

`/systeminsights/userassist` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_user_ssh_keys`

Valid filter fields are `system_id` and `uid`.

#### 🛠️ Usage

```python
list_user_ssh_keys_response = jumpcloud.system_insights.list_user_ssh_keys(
    x_org_id="string_example",
    skip=0,
    sort=[],
    filter=[],
    limit=10,
)
```

#### ⚙️ Parameters

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListUserSshKeysResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_user_ssh_keys_response.py)

#### 🌐 Endpoint

`/systeminsights/user_ssh_keys` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_users`

Valid filter fields are `system_id` and `username`.

#### 🛠️ Usage

```python
list_users_response = jumpcloud.system_insights.list_users(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListUsersResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_users_response.py)

#### 🌐 Endpoint

`/systeminsights/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_wifi_networks`

Valid filter fields are `system_id` and `security_type`.

#### 🛠️ Usage

```python
list_wifi_networks_response = jumpcloud.system_insights.list_wifi_networks(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListWifiNetworksResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_wifi_networks_response.py)

#### 🌐 Endpoint

`/systeminsights/wifi_networks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_wifi_status`

Valid filter fields are `system_id` and `security_type`.

#### 🛠️ Usage

```python
list_wifi_status_response = jumpcloud.system_insights.list_wifi_status(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListWifiStatusResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_wifi_status_response.py)

#### 🌐 Endpoint

`/systeminsights/wifi_status` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_windows_security_center`

Valid filter fields are `system_id`.

#### 🛠️ Usage

```python
list_windows_security_center_response = jumpcloud.system_insights.list_windows_security_center(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListWindowsSecurityCenterResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_windows_security_center_response.py)

#### 🌐 Endpoint

`/systeminsights/windows_security_center` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.system_insights.list_windows_security_products`

Valid filter fields are `system_id` and `state`.

#### 🛠️ Usage

```python
list_windows_security_products_response = jumpcloud.system_insights.list_windows_security_products(
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
    limit=10,
)
```

#### ⚙️ Parameters

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. e.g: Sort by single field: `sort=field` Sort descending by single field: `sort=-field` Sort by multiple fields: `sort=field1,-field2,field3` 

##### filter: List[`str`]

Supported operators are: eq, in. e.g: Filter for single value: `filter=field:eq:value` Filter for any value in a list: (note \"pipe\" character: `|` separating values) `filter=field:in:value1|value2|value3` 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

#### 🔄 Return

[`SystemInsightsListWindowsSecurityProductsResponse`](./jump_cloud_python_sdk/pydantic/system_insights_list_windows_security_products_response.py)

#### 🌐 Endpoint

`/systeminsights/windows_security_products` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems.get_fde_key`

This endpoint will return the current (latest) fde key saved for a system.

#### 🛠️ Usage

```python
get_fde_key_response = jumpcloud.systems.get_fde_key(
    system_id="system_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### system_id: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`Systemfdekey`](./jump_cloud_python_sdk/pydantic/systemfdekey.py)

#### 🌐 Endpoint

`/systems/{system_id}/fdekey` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems.list_software_apps_with_statuses`

This endpoint returns all the statuses of the associated Software Applications from the provided JumpCloud system ID.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{system_id}/softwareappstatuses \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
list_software_apps_with_statuses_response = jumpcloud.systems.list_software_apps_with_statuses(
    system_id="system_id_example",
    x_org_id="string_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
)
```

#### ⚙️ Parameters

##### system_id: `str`

ObjectID of the System.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

#### 🔄 Return

[`SystemsListSoftwareAppsWithStatusesResponse`](./jump_cloud_python_sdk/pydantic/systems_list_software_apps_with_statuses_response.py)

#### 🌐 Endpoint

`/systems/{system_id}/softwareappstatuses` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems.system_associations_list`

This endpoint returns the _direct_ associations of a System.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Systems and Users.


#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/associations?targets=user \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_associations_list_response = jumpcloud.systems.system_associations_list(
    system_id="system_id_example",
    targets=[
        "command"
    ],
    limit=10,
    skip=0,
    date="string_example",
    authorization="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### system_id: `str`

ObjectID of the System.

##### targets: List[`str`]

Targets which a \"system\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### date: `str`

Current date header for the System Context API

##### authorization: `str`

Authorization header for the System Context API

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphSystemAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_system_associations_list_response.py)

#### 🌐 Endpoint

`/systems/{system_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems.system_associations_post`

This endpoint allows you to manage the _direct_ associations of a System.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Systems and Users.


#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/systems/{System_ID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "attributes": {
      "sudo": {
        "enabled": true,
        "withoutPassword": false
      }
    },
    "op": "add",
    "type": "user",
    "id": "UserID"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.systems.system_associations_post(
    system_id="system_id_example",
    id="string_example",
    op="add",
    attributes=None,
    type="command",
    date="string_example",
    authorization="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### system_id: `str`

ObjectID of the System.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: Union[[`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py), `GraphAttributeSudo`]


##### type: `str`

Targets which a \\\"system\\\" can be associated to.

##### date: `str`

Current date header for the System Context API

##### authorization: `str`

Authorization header for the System Context API

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationSystem`](./jump_cloud_python_sdk/type/graph_operation_system.py)
#### 🌐 Endpoint

`/systems/{system_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems.system_member_of`

This endpoint returns all the System Groups a System is a member of.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/memberof \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_member_of_response = jumpcloud.systems.system_member_of(
    system_id="system_id_example",
    filter=[],
    limit=10,
    skip=0,
    date="string_example",
    authorization="string_example",
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### system_id: `str`

ObjectID of the System.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### date: `str`

Current date header for the System Context API

##### authorization: `str`

Authorization header for the System Context API

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphSystemMemberOfResponse`](./jump_cloud_python_sdk/pydantic/graph_system_member_of_response.py)

#### 🌐 Endpoint

`/systems/{system_id}/memberof` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems.system_traverse_command`

This endpoint will return all Commands bound to a System, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System to the corresponding Command; this array represents all grouping and/or associations that would have to be removed to deprovision the Command from this System.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/commands \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_traverse_command_response = jumpcloud.systems.system_traverse_command(
    system_id="system_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
    details="v1",
)
```

#### ⚙️ Parameters

##### system_id: `str`

ObjectID of the System.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### details: `str`

This will provide detail descriptive response for the request.

#### 🔄 Return

[`GraphSystemTraverseCommandResponse`](./jump_cloud_python_sdk/pydantic/graph_system_traverse_command_response.py)

#### 🌐 Endpoint

`/systems/{system_id}/commands` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems.system_traverse_policy`

This endpoint will return all Policies bound to a System, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System to the corresponding Policy; this array represents all grouping and/or associations that would have to be removed to deprovision the Policy from this System.

See `/members` and `/associations` endpoints to manage those collections.

This endpoint is not yet public as we have finish the code.

##### Sample Request

```
curl -X GET https://console.jumpcloud.com/api/v2/{System_ID}/policies \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_traverse_policy_response = jumpcloud.systems.system_traverse_policy(
    system_id="system_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### system_id: `str`

ObjectID of the System.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemTraversePolicyResponse`](./jump_cloud_python_sdk/pydantic/graph_system_traverse_policy_response.py)

#### 🌐 Endpoint

`/systems/{system_id}/policies` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems.system_traverse_policy_group`

This endpoint will return all Policy Groups bound to a System, either directly or indirectly essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System to the corresponding Policy Group; this array represents all grouping and/or associations that would have to be removed to deprovision the Policy Group from this System.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/policygroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_traverse_policy_group_response = jumpcloud.systems.system_traverse_policy_group(
    system_id="system_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    date="string_example",
    authorization="string_example",
    filter=[],
)
```

#### ⚙️ Parameters

##### system_id: `str`

ObjectID of the System.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### date: `str`

Current date header for the System Context API

##### authorization: `str`

Authorization header for the System Context API

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemTraversePolicyGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_system_traverse_policy_group_response.py)

#### 🌐 Endpoint

`/systems/{system_id}/policygroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems.system_traverse_user`

This endpoint will return all Users bound to a System, either directly or indirectly essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System to the corresponding User; this array represents all grouping and/or associations that would have to be removed to deprovision the User from this System.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/users \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_traverse_user_response = jumpcloud.systems.system_traverse_user(
    system_id="system_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    date="string_example",
    authorization="string_example",
    filter=[],
)
```

#### ⚙️ Parameters

##### system_id: `str`

ObjectID of the System.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### date: `str`

Current date header for the System Context API

##### authorization: `str`

Authorization header for the System Context API

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemTraverseUserResponse`](./jump_cloud_python_sdk/pydantic/graph_system_traverse_user_response.py)

#### 🌐 Endpoint

`/systems/{system_id}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems.system_traverse_user_group`

This endpoint will return all User Groups bound to a System, either directly or indirectly essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this System to the corresponding User Group; this array represents all grouping and/or associations that would have to be removed to deprovision the User Group from this System.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/systems/{System_ID}/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
system_traverse_user_group_response = jumpcloud.systems.system_traverse_user_group(
    system_id="system_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    date="string_example",
    authorization="string_example",
    filter=[],
)
```

#### ⚙️ Parameters

##### system_id: `str`

ObjectID of the System.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### date: `str`

Current date header for the System Context API

##### authorization: `str`

Authorization header for the System Context API

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphSystemTraverseUserGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_system_traverse_user_group_response.py)

#### 🌐 Endpoint

`/systems/{system_id}/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems_organization_settings.get_default_password_sync_settings`

Gets the Default Password Sync Setting for an Organization.

#### 🛠️ Usage

```python
get_default_password_sync_settings_response = jumpcloud.systems_organization_settings.get_default_password_sync_settings(
    organization_object_id='YQ==',
)
```

#### ⚙️ Parameters

##### organization_object_id: `str`

#### 🔄 Return

[`DevicesGetDefaultPasswordSyncSettingsResponse`](./jump_cloud_python_sdk/pydantic/devices_get_default_password_sync_settings_response.py)

#### 🌐 Endpoint

`/devices/settings/defaultpasswordsync` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems_organization_settings.get_sign_in_with_jump_cloud_settings`

Gets the Sign In with JumpCloud Settings for an Organization.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/devices/settings/signinwithjumpcloud \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key:{API_KEY}'
```

#### 🛠️ Usage

```python
get_sign_in_with_jump_cloud_settings_response = jumpcloud.systems_organization_settings.get_sign_in_with_jump_cloud_settings(
    organization_object_id='YQ==',
)
```

#### ⚙️ Parameters

##### organization_object_id: `str`

#### 🔄 Return

[`DevicesGetSignInWithJumpCloudSettingsResponse`](./jump_cloud_python_sdk/pydantic/devices_get_sign_in_with_jump_cloud_settings_response.py)

#### 🌐 Endpoint

`/devices/settings/signinwithjumpcloud` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems_organization_settings.set_default_password_sync_settings`

Sets the Default Password Sync Setting for an Organization.

#### 🛠️ Usage

```python
set_default_password_sync_settings_response = jumpcloud.systems_organization_settings.set_default_password_sync_settings(
    enabled=True,
    organization_object_id='YQ==',
)
```

#### ⚙️ Parameters

##### enabled: `bool`

##### organization_object_id: `str`

#### ⚙️ Request Body

[`DevicesSetDefaultPasswordSyncSettingsRequest`](./jump_cloud_python_sdk/type/devices_set_default_password_sync_settings_request.py)
#### 🌐 Endpoint

`/devices/settings/defaultpasswordsync` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.systems_organization_settings.set_sign_in_with_jump_cloud_settings`

Sets the Sign In with JumpCloud Settings for an Organization.

#### Sample Request
```
curl -X PUT https://console.jumpcloud.com/api/v2/devices/settings/signinwithjumpcloud \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key:{API_KEY}' \
  -d '{"settings":[{"osFamily":"WINDOWS","enabled":true,"defaultPermission":"STANDARD"}]}'
```

#### 🛠️ Usage

```python
set_sign_in_with_jump_cloud_settings_response = jumpcloud.systems_organization_settings.set_sign_in_with_jump_cloud_settings(
    organization_object_id='YQ==',
    settings=[
        {
            "default_permission": "STANDARD",
            "os_family": "UNKNOWN",
        }
    ],
)
```

#### ⚙️ Parameters

##### organization_object_id: `str`

##### settings: List[`DevicesSignInWithJumpCloudSetting`]

#### ⚙️ Request Body

[`DevicesSetSignInWithJumpCloudSettingsRequest`](./jump_cloud_python_sdk/type/devices_set_sign_in_with_jump_cloud_settings_request.py)
#### 🌐 Endpoint

`/devices/settings/signinwithjumpcloud` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_associations.user_group_associations_list`

This endpoint returns the _direct_ associations of this User Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example User Groups and Users.


#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/associations?targets=system \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_associations_list_response = jumpcloud.user_group_associations.user_group_associations_list(
    group_id="group_id_example",
    targets=[
        "active_directory"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### targets: List[`str`]

Targets which a \"user_group\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphUserGroupAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_associations_list_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_associations.user_group_associations_post`

This endpoint manages the _direct_ associations of this User Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example User Groups and Users.


#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system",
    "id": "{SystemID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.user_group_associations.user_group_associations_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="active_directory",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

Targets which a \\\"user_group\\\" can be associated to.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationUserGroup`](./jump_cloud_python_sdk/type/graph_operation_user_group.py)
#### 🌐 Endpoint

`/usergroups/{group_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_associations.user_group_traverse_active_directory`

This endpoint will return all Active Directory Instances bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Active Directory; this array represents all grouping and/or associations that would have to be removed to deprovision the Active Directory from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/activedirectories \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_active_directory_response = jumpcloud.user_group_associations.user_group_traverse_active_directory(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseActiveDirectoryResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_active_directory_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/activedirectories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_associations.user_group_traverse_application`

This endpoint will return all Applications bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Application; this array represents all grouping and/or associations that would have to be removed to deprovision the Application from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/applications \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_application_response = jumpcloud.user_group_associations.user_group_traverse_application(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseApplicationResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_application_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/applications` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_associations.user_group_traverse_directory`

This endpoint will return all Directories bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Directory; this array represents all grouping and/or associations that would have to be removed to deprovision the Directories from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/directories \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
user_group_traverse_directory_response = jumpcloud.user_group_associations.user_group_traverse_directory(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseDirectoryResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_directory_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/directories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_associations.user_group_traverse_g_suite`

This endpoint will return all G Suite Instances bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding G Suite instance; this array represents all grouping and/or associations that would have to be removed to deprovision the G Suite instance from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID/gsuites \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
user_group_traverse_g_suite_response = jumpcloud.user_group_associations.user_group_traverse_g_suite(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseGSuiteResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_g_suite_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/gsuites` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_associations.user_group_traverse_ldap_server`

This endpoint will return all LDAP Servers bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding LDAP Server; this array represents all grouping and/or associations that would have to be removed to deprovision the LDAP Server from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/ldapservers \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_ldap_server_response = jumpcloud.user_group_associations.user_group_traverse_ldap_server(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseLdapServerResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_ldap_server_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/ldapservers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_associations.user_group_traverse_office365`

This endpoint will return all Office 365 instances bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Office 365 instance; this array represents all grouping and/or associations that would have to be removed to deprovision the Office 365 instance from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/office365s \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_office365_response = jumpcloud.user_group_associations.user_group_traverse_office365(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseOffice365Response`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_office365_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/office365s` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_associations.user_group_traverse_radius_server`

This endpoint will return all RADIUS servers bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding RADIUS Server; this array represents all grouping and/or associations that would have to be removed to deprovision the RADIUS Server from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/radiusservers \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
user_group_traverse_radius_server_response = jumpcloud.user_group_associations.user_group_traverse_radius_server(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseRadiusServerResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_radius_server_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/radiusservers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_associations.user_group_traverse_system`

This endpoint will return all Systems bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_system_response = jumpcloud.user_group_associations.user_group_traverse_system(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_system_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_associations.user_group_traverse_system_group`

This endpoint will return all System Groups bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_system_group_response = jumpcloud.user_group_associations.user_group_traverse_system_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_system_group_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_members_&amp;_membership.user_group_members_list`

This endpoint returns the user members of a User Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_members_list_response = jumpcloud.user_group_members_&amp;_membership.user_group_members_list(
    group_id="group_id_example",
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphUserGroupMembersListResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_members_list_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_members_&amp;_membership.user_group_members_post`

This endpoint allows you to manage the user members of a User Group.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user",
    "id": "{User_ID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.user_group_members_&amp;_membership.user_group_members_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

The member type.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationUserGroupMember`](./jump_cloud_python_sdk/type/graph_operation_user_group_member.py)
#### 🌐 Endpoint

`/usergroups/{group_id}/members` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_group_members_&amp;_membership.user_group_membership`

This endpoint returns all users members that are a member of this User Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/membership \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_membership_response = jumpcloud.user_group_members_&amp;_membership.user_group_membership(
    group_id="group_id_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphUserGroupMembershipResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_membership_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/membership` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.apply_suggestions`

This endpoint applies the suggestions for the specified user group.
#### Sample Request
```
curl -X PUT https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/suggestions \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
         "user_ids": ["212345678901234567890123",
                      "123456789012345678901234"]
     }'
```

#### 🛠️ Usage

```python
apply_suggestions_response = jumpcloud.user_groups.apply_suggestions(
    group_id="group_id_example",
    user_ids=[
        "string_example"
    ],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ID of the group

##### user_ids: [`UserGroupsApplySuggestionsRequestUserIds`](./jump_cloud_python_sdk/type/user_groups_apply_suggestions_request_user_ids.py)

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`UserGroupsApplySuggestionsRequest`](./jump_cloud_python_sdk/type/user_groups_apply_suggestions_request.py)
#### 🌐 Endpoint

`/usergroups/{group_id}/suggestions` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.create_new_group`

This endpoint allows you to create a new User Group.

See the [Dynamic Group Configuration KB article](https://jumpcloud.com/support/configure-dynamic-device-groups) for more details on maintaining a Dynamic Group.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "{Group_Name}"
  }'
```

#### 🛠️ Usage

```python
create_new_group_response = jumpcloud.user_groups.create_new_group(
    name="string_example",
    description="string_example",
    attributes={},
    email="string_example",
    member_query=None,
    member_query_exemptions=[
        {
            "id": "id_example",
            "type": "type_example",
        }
    ],
    member_suggestions_notify=True,
    membership_method="NOTSET",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### name: `str`

Display name of a User Group.

##### description: `str`

Description of a User Group

##### attributes: [`GroupAttributesUserGroup`](./jump_cloud_python_sdk/type/group_attributes_user_group.py)


##### email: `str`

Email address of a User Group

##### member_query: [`MemberQuery`](./jump_cloud_python_sdk/type/member_query.py)


##### member_query_exemptions: List[`GraphObject`]

Array of GraphObjects exempted from the query

##### member_suggestions_notify: `bool`

True if notification emails are to be sent for membership suggestions.

##### membership_method: [`GroupMembershipMethodType`](./jump_cloud_python_sdk/type/group_membership_method_type.py)

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`UserGroupPost`](./jump_cloud_python_sdk/type/user_group_post.py)
#### 🔄 Return

[`UserGroup`](./jump_cloud_python_sdk/pydantic/user_group.py)

#### 🌐 Endpoint

`/usergroups` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.delete_group`

This endpoint allows you to delete a User Group.

#### Sample Request
```
curl -X DELETE https://console.jumpcloud.com/api/v2/usergroups/{GroupID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
delete_group_response = jumpcloud.user_groups.delete_group(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

ObjectID of the User Group.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`UserGroup`](./jump_cloud_python_sdk/pydantic/user_group.py)

#### 🌐 Endpoint

`/usergroups/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.get_details`

This endpoint returns the details of a User Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
get_details_response = jumpcloud.user_groups.get_details(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

ObjectID of the User Group.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`UserGroup`](./jump_cloud_python_sdk/pydantic/user_group.py)

#### 🌐 Endpoint

`/usergroups/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.get_suggestions`

This endpoint returns available suggestions for a given group
#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/suggestions \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
get_suggestions_response = jumpcloud.user_groups.get_suggestions(
    group_id="group_id_example",
    x_org_id="string_example",
    limit=10,
    skip=0,
)
```

#### ⚙️ Parameters

##### group_id: `str`

ID of the group

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

#### 🔄 Return

[`UserGroupsGetSuggestionsResponse`](./jump_cloud_python_sdk/pydantic/user_groups_get_suggestions_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/suggestions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.list_all`

This endpoint returns all User Groups.

Available filter fields:
  - `name`
  - `disabled`
  - `type`
  - `membershipMethod`
  - `suggestionCounts.add`
  - `suggestionCounts.remove`
  - `suggestionCounts.total`
  - `attributes.sudo.enabled`
  - `attributes.sudo.withoutPassword`

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
list_all_response = jumpcloud.user_groups.list_all(
    fields=[],
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`UserGroupsListAllResponse`](./jump_cloud_python_sdk/pydantic/user_groups_list_all_response.py)

#### 🌐 Endpoint

`/usergroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.update_group`

This endpoint allows you to do a full update of the User Group.

See the [Dynamic Group Configuration KB article](https://jumpcloud.com/support/configure-dynamic-device-groups) for more details on maintaining a Dynamic Group.

#### Sample Request
```
curl -X PUT https://console.jumpcloud.com/api/v2/usergroups/{Group_ID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "group_update"
  }'
```

#### 🛠️ Usage

```python
update_group_response = jumpcloud.user_groups.update_group(
    name="string_example",
    id="id_example",
    description="string_example",
    attributes={},
    email="string_example",
    member_query=None,
    member_query_exemptions=[
        {
            "id": "id_example",
            "type": "type_example",
        }
    ],
    member_suggestions_notify=True,
    membership_method="NOTSET",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### name: `str`

Display name of a User Group.

##### id: `str`

ObjectID of the User Group.

##### description: `str`

Description of a User Group

##### attributes: [`GroupAttributesUserGroup`](./jump_cloud_python_sdk/type/group_attributes_user_group.py)


##### email: `str`

Email address of a User Group

##### member_query: [`MemberQuery`](./jump_cloud_python_sdk/type/member_query.py)


##### member_query_exemptions: List[`GraphObject`]

Array of GraphObjects exempted from the query

##### member_suggestions_notify: `bool`

True if notification emails are to be sent for membership suggestions.

##### membership_method: [`GroupMembershipMethodType`](./jump_cloud_python_sdk/type/group_membership_method_type.py)

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`UserGroupPut`](./jump_cloud_python_sdk/type/user_group_put.py)
#### 🔄 Return

[`UserGroup`](./jump_cloud_python_sdk/pydantic/user_group.py)

#### 🌐 Endpoint

`/usergroups/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_associations_list`

This endpoint returns the _direct_ associations of this User Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example User Groups and Users.


#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/associations?targets=system \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_associations_list_response = jumpcloud.user_groups.user_group_associations_list(
    group_id="group_id_example",
    targets=[
        "active_directory"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### targets: List[`str`]

Targets which a \"user_group\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphUserGroupAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_associations_list_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_associations_post`

This endpoint manages the _direct_ associations of this User Group.

A direct association can be a non-homogeneous relationship between 2 different objects, for example User Groups and Users.


#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "system",
    "id": "{SystemID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.user_groups.user_group_associations_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="active_directory",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

Targets which a \\\"user_group\\\" can be associated to.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationUserGroup`](./jump_cloud_python_sdk/type/graph_operation_user_group.py)
#### 🌐 Endpoint

`/usergroups/{group_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_members_list`

This endpoint returns the user members of a User Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_members_list_response = jumpcloud.user_groups.user_group_members_list(
    group_id="group_id_example",
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphUserGroupMembersListResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_members_list_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_members_post`

This endpoint allows you to manage the user members of a User Group.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/members \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "op": "add",
    "type": "user",
    "id": "{User_ID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.user_groups.user_group_members_post(
    group_id="group_id_example",
    id="string_example",
    op="add",
    attributes={},
    type="user",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: [`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py)

##### type: `str`

The member type.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationUserGroupMember`](./jump_cloud_python_sdk/type/graph_operation_user_group_member.py)
#### 🌐 Endpoint

`/usergroups/{group_id}/members` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_membership`

This endpoint returns all users members that are a member of this User Group.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/membership \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_membership_response = jumpcloud.user_groups.user_group_membership(
    group_id="group_id_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphUserGroupMembershipResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_membership_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/membership` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_traverse_active_directory`

This endpoint will return all Active Directory Instances bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Active Directory; this array represents all grouping and/or associations that would have to be removed to deprovision the Active Directory from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/activedirectories \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_active_directory_response = jumpcloud.user_groups.user_group_traverse_active_directory(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseActiveDirectoryResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_active_directory_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/activedirectories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_traverse_application`

This endpoint will return all Applications bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Application; this array represents all grouping and/or associations that would have to be removed to deprovision the Application from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/applications \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_application_response = jumpcloud.user_groups.user_group_traverse_application(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseApplicationResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_application_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/applications` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_traverse_directory`

This endpoint will return all Directories bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Directory; this array represents all grouping and/or associations that would have to be removed to deprovision the Directories from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/directories \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
user_group_traverse_directory_response = jumpcloud.user_groups.user_group_traverse_directory(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseDirectoryResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_directory_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/directories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_traverse_g_suite`

This endpoint will return all G Suite Instances bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding G Suite instance; this array represents all grouping and/or associations that would have to be removed to deprovision the G Suite instance from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID/gsuites \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
user_group_traverse_g_suite_response = jumpcloud.user_groups.user_group_traverse_g_suite(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseGSuiteResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_g_suite_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/gsuites` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_traverse_ldap_server`

This endpoint will return all LDAP Servers bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding LDAP Server; this array represents all grouping and/or associations that would have to be removed to deprovision the LDAP Server from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/ldapservers \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_ldap_server_response = jumpcloud.user_groups.user_group_traverse_ldap_server(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseLdapServerResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_ldap_server_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/ldapservers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_traverse_office365`

This endpoint will return all Office 365 instances bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding Office 365 instance; this array represents all grouping and/or associations that would have to be removed to deprovision the Office 365 instance from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/office365s \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_office365_response = jumpcloud.user_groups.user_group_traverse_office365(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseOffice365Response`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_office365_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/office365s` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_traverse_radius_server`

This endpoint will return all RADIUS servers bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding RADIUS Server; this array represents all grouping and/or associations that would have to be removed to deprovision the RADIUS Server from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/radiusservers \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
user_group_traverse_radius_server_response = jumpcloud.user_groups.user_group_traverse_radius_server(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseRadiusServerResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_radius_server_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/radiusservers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_traverse_system`

This endpoint will return all Systems bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_system_response = jumpcloud.user_groups.user_group_traverse_system(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_system_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.user_groups.user_group_traverse_system_group`

This endpoint will return all System Groups bound to a User Group, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User Group to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this User Group.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/usergroups/{GroupID}/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_group_traverse_system_group_response = jumpcloud.user_groups.user_group_traverse_system_group(
    group_id="group_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### group_id: `str`

ObjectID of the User Group.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserGroupTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_user_group_traverse_system_group_response.py)

#### 🌐 Endpoint

`/usergroups/{group_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.delete`

This endpoint will delete a push endpoint associated with a user.

#### 🛠️ Usage

```python
delete_response = jumpcloud.users.delete(
    user_id="user_id_example",
    push_endpoint_id="push_endpoint_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### user_id: `str`

##### push_endpoint_id: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PushEndpointResponse`](./jump_cloud_python_sdk/pydantic/push_endpoint_response.py)

#### 🌐 Endpoint

`/users/{user_id}/pushendpoints/{push_endpoint_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.get`

This endpoint will retrieve a push endpoint associated with a user.

#### 🛠️ Usage

```python
get_response = jumpcloud.users.get(
    user_id="user_id_example",
    push_endpoint_id="push_endpoint_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### user_id: `str`

##### push_endpoint_id: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PushEndpointResponse`](./jump_cloud_python_sdk/pydantic/push_endpoint_response.py)

#### 🌐 Endpoint

`/users/{user_id}/pushendpoints/{push_endpoint_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.list`

This endpoint returns the list of push endpoints associated with a user.

#### Sample Request

```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/pushendpoints \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: ${API_KEY}'
```

#### 🛠️ Usage

```python
list_response = jumpcloud.users.list(
    user_id="user_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### user_id: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`PushEndpointsListResponse`](./jump_cloud_python_sdk/pydantic/push_endpoints_list_response.py)

#### 🌐 Endpoint

`/users/{user_id}/pushendpoints` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.patch`

This endpoint will update a push endpoint associated with a user.

#### 🛠️ Usage

```python
patch_response = jumpcloud.users.patch(
    user_id="user_id_example",
    push_endpoint_id="push_endpoint_id_example",
    name="string_example",
    state="active",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### user_id: `str`

##### push_endpoint_id: `str`

##### name: `str`

##### state: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`PushEndpointsPatchRequest`](./jump_cloud_python_sdk/type/push_endpoints_patch_request.py)
#### 🔄 Return

[`PushEndpointResponse`](./jump_cloud_python_sdk/pydantic/push_endpoint_response.py)

#### 🌐 Endpoint

`/users/{user_id}/pushendpoints/{push_endpoint_id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_associations_list`

This endpoint returns the _direct_ associations of a User.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Users and Systems.


#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/associations?targets=system_group \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'

```

#### 🛠️ Usage

```python
user_associations_list_response = jumpcloud.users.user_associations_list(
    user_id="user_id_example",
    targets=[
        "active_directory"
    ],
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### targets: List[`str`]

Targets which a \"user\" can be associated to.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphUserAssociationsListResponse`](./jump_cloud_python_sdk/pydantic/graph_user_associations_list_response.py)

#### 🌐 Endpoint

`/users/{user_id}/associations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_associations_post`

This endpoint allows you to manage the _direct_ associations of a User.

A direct association can be a non-homogeneous relationship between 2 different objects, for example Users and Systems.


#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/users/{UserID}/associations \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "attributes": {
      "sudo": {
      "enabled": true,
        "withoutPassword": false
      }
    },
    "op": "add",
    "type": "system_group",
    "id": "{GroupID}"
  }'
```

#### 🛠️ Usage

```python
jumpcloud.users.user_associations_post(
    user_id="user_id_example",
    id="string_example",
    op="add",
    attributes=None,
    type="active_directory",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### id: `str`

The ObjectID of graph object being added or removed as an association.

##### op: `str`

How to modify the graph connection.

##### attributes: Union[[`GraphAttributes`](./jump_cloud_python_sdk/type/graph_attributes.py), `GraphAttributeSudo`]


##### type: `str`

Targets which a \\\"user\\\" can be associated to.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`GraphOperationUser`](./jump_cloud_python_sdk/type/graph_operation_user.py)
#### 🌐 Endpoint

`/users/{user_id}/associations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_member_of`

This endpoint returns all the User Groups a User is a member of.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/memberof \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_member_of_response = jumpcloud.users.user_member_of(
    user_id="user_id_example",
    filter=[],
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`GraphUserMemberOfResponse`](./jump_cloud_python_sdk/pydantic/graph_user_member_of_response.py)

#### 🌐 Endpoint

`/users/{user_id}/memberof` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_traverse_active_directory`

This endpoint will return all Active Directory Instances bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding Active Directory instance; this array represents all grouping and/or associations that would have to be removed to deprovision the Active Directory instance from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/activedirectories \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_traverse_active_directory_response = jumpcloud.users.user_traverse_active_directory(
    user_id="user_id_example",
    filter=[],
    limit=10,
    x_org_id="string_example",
    skip=0,
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

#### 🔄 Return

[`GraphUserTraverseActiveDirectoryResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_active_directory_response.py)

#### 🌐 Endpoint

`/users/{user_id}/activedirectories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_traverse_application`

This endpoint will return all Applications bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding Application; this array represents all grouping and/or associations that would have to be removed to deprovision the Application from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/applications \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_traverse_application_response = jumpcloud.users.user_traverse_application(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserTraverseApplicationResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_application_response.py)

#### 🌐 Endpoint

`/users/{user_id}/applications` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_traverse_directory`

This endpoint will return all Directories bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding Directory; this array represents all grouping and/or associations that would have to be removed to deprovision the Directory from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/directories \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_traverse_directory_response = jumpcloud.users.user_traverse_directory(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserTraverseDirectoryResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_directory_response.py)

#### 🌐 Endpoint

`/users/{user_id}/directories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_traverse_g_suite`

This endpoint will return all G-Suite Instances bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding G Suite instance; this array represents all grouping and/or associations that would have to be removed to deprovision the G Suite instance from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/gsuites \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_traverse_g_suite_response = jumpcloud.users.user_traverse_g_suite(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserTraverseGSuiteResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_g_suite_response.py)

#### 🌐 Endpoint

`/users/{user_id}/gsuites` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_traverse_ldap_server`

This endpoint will return all LDAP Servers bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding LDAP Server; this array represents all grouping and/or associations that would have to be removed to deprovision the LDAP Server from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/ldapservers \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_traverse_ldap_server_response = jumpcloud.users.user_traverse_ldap_server(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserTraverseLdapServerResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_ldap_server_response.py)

#### 🌐 Endpoint

`/users/{user_id}/ldapservers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_traverse_office365`

This endpoint will return all Office 365 Instances bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding Office 365 instance; this array represents all grouping and/or associations that would have to be removed to deprovision the Office 365 instance from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/office365s \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_traverse_office365_response = jumpcloud.users.user_traverse_office365(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserTraverseOffice365Response`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_office365_response.py)

#### 🌐 Endpoint

`/users/{user_id}/office365s` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_traverse_radius_server`

This endpoint will return all RADIUS Servers bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding RADIUS Server; this array represents all grouping and/or associations that would have to be removed to deprovision the RADIUS Server from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/radiusservers \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_traverse_radius_server_response = jumpcloud.users.user_traverse_radius_server(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserTraverseRadiusServerResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_radius_server_response.py)

#### 🌐 Endpoint

`/users/{user_id}/radiusservers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_traverse_system`

This endpoint will return all Systems bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding System; this array represents all grouping and/or associations that would have to be removed to deprovision the System from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/systems\
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_traverse_system_response = jumpcloud.users.user_traverse_system(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserTraverseSystemResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_system_response.py)

#### 🌐 Endpoint

`/users/{user_id}/systems` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.users.user_traverse_system_group`

This endpoint will return all System Groups bound to a User, either directly or indirectly, essentially traversing the JumpCloud Graph for your Organization.

Each element will contain the type, id, attributes and paths.

The `attributes` object is a key/value hash of compiled graph attributes for all paths followed.

The `paths` array enumerates each path from this User to the corresponding System Group; this array represents all grouping and/or associations that would have to be removed to deprovision the System Group from this User.

See `/members` and `/associations` endpoints to manage those collections.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/users/{UserID}/systemgroups\
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
user_traverse_system_group_response = jumpcloud.users.user_traverse_system_group(
    user_id="user_id_example",
    limit=10,
    x_org_id="string_example",
    skip=0,
    filter=[],
)
```

#### ⚙️ Parameters

##### user_id: `str`

ObjectID of the User.

##### limit: `int`

The number of records to return at once. Limited to 100.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### skip: `int`

The offset into the records to return.

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

#### 🔄 Return

[`GraphUserTraverseSystemGroupResponse`](./jump_cloud_python_sdk/pydantic/graph_user_traverse_system_group_response.py)

#### 🌐 Endpoint

`/users/{user_id}/systemgroups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.workday_import.authorize`

This endpoint adds an authorization method to a workday instance.

You must supply a username and password for `Basic Authentication` that is the same as your WorkDay Integrator System User.  Failure to provide these credentials  will result in the request being rejected.

Currently `O-Auth` isn't a supported authentication protocol for WorkDay, but will be in the future.

#### Sample Request

```
curl -X POST https://console.jumpcloud.com/api/v2/workdays/{WorkDayID}/auth \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
	"auth":{
	  "basic": {
		"username": "someDeveloper",	  
		"password": "notTheRealPassword"

	  }
	}
}'

```

#### 🛠️ Usage

```python
jumpcloud.workday_import.authorize(
    workday_id="workday_id_example",
    auth={
    },
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### workday_id: `str`

##### auth: [`AuthInput`](./jump_cloud_python_sdk/type/auth_input.py)


##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`AuthInputObject`](./jump_cloud_python_sdk/type/auth_input_object.py)
#### 🌐 Endpoint

`/workdays/{workday_id}/auth` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.workday_import.deauthorize`

Removes any and all authorization methods from the workday instance

##### Sample Request
```
curl -X DELETE https://console.jumpcloud.com/api/v2/workdays/{WorkDayID}/auth \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
jumpcloud.workday_import.deauthorize(
    workday_id="workday_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### workday_id: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🌐 Endpoint

`/workdays/{workday_id}/auth` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.workday_import.get`

This endpoint will return  all the available information about an instance of Workday.

#### Sample Request

```
curl -X GET https://console.jumpcloud.com/api/v2/workdays/ \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
get_response = jumpcloud.workday_import.get(
    id="id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`WorkdayOutput`](./jump_cloud_python_sdk/pydantic/workday_output.py)

#### 🌐 Endpoint

`/workdays/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.workday_import.import`

The endpoint allows you to create a Workday Import request.

#### Sample Request 
```
curl -X POST https://console.jumpcloud.com/api/v2/workdays/{WorkdayID}/import \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '[
	{
		"email":"{email}",
		"firstname":"{firstname}",
		"lastname":"{firstname}",
		"username":"{username}",
		"attributes":[
			{"name":"EmployeeID","value":"0000"},
			{"name":"WorkdayID","value":"name.name"}
			]
		
	}
]
```

#### 🛠️ Usage

```python
import_response = jumpcloud.workday_import.import(
    body=[
        {
        }
    ],
    workday_id="workday_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### workday_id: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

##### requestBody: [`BulkUsersCreateRequest`](./jump_cloud_python_sdk/type/bulk_users_create_request.py)

#### 🔄 Return

[`JobId`](./jump_cloud_python_sdk/pydantic/job_id.py)

#### 🌐 Endpoint

`/workdays/{workday_id}/import` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.workday_import.importresults`

This endpoint provides a list of job results from the workday import and will contain all imported data from Workday.

#### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/workdays/{WorkdayID}/import/{ImportJobID}/results \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
```

#### 🛠️ Usage

```python
importresults_response = jumpcloud.workday_import.importresults(
    id="id_example",
    job_id="job_id_example",
    limit=10,
    skip=0,
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

##### job_id: `str`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`WorkdaysImportresultsResponse`](./jump_cloud_python_sdk/pydantic/workdays_importresults_response.py)

#### 🌐 Endpoint

`/workdays/{id}/import/{job_id}/results` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.workday_import.list`

This endpoint will return  all the available information about all your instances of Workday.

##### Sample Request
```
curl -X GET https://console.jumpcloud.com/api/v2/workdays/ \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'
  ```

#### 🛠️ Usage

```python
list_response = jumpcloud.workday_import.list(
    fields=[],
    limit=10,
    skip=0,
    sort=[],
    filter=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### fields: List[`str`]

The comma separated fields included in the returned records. If omitted, the default list of fields will be returned. 

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### filter: List[`str`]

A filter to apply to the query.  **Filter structure**: `<field>:<operator>:<value>`.  **field** = Populate with a valid field from an endpoint response.  **operator** =  Supported operators are: eq, ne, gt, ge, lt, le, between, search, in. _Note: v1 operators differ from v2 operators._  **value** = Populate with the value you want to search for. Is case sensitive. Supports wild cards.  **EX:** `GET /api/v2/groups?filter=name:eq:Test+Group`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`WorkdaysListResponse`](./jump_cloud_python_sdk/pydantic/workdays_list_response.py)

#### 🌐 Endpoint

`/workdays` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.workday_import.post`

This endpoint allows you to create a new workday instance.

You must supply a username and password for `Basic Authentication` that is the same as your WorkDay Integrator System User.  Failure to provide these credentials  will result in the request being rejected.

Currently `O-Auth` isn't a supported authentication protocol for WorkDay, but will be in the future.

Currently, only one instance is allowed and it must be `Workday Import`.

#### Sample Request
```
curl -X POST https://console.jumpcloud.com/api/v2/workdays/ \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
    "name": "Workday2",
    "reportUrl":"https://workday.com/ccx/service/customreport2/gms/user/reportname?format=json",
    "auth": {
      "basic": {
        "username": "someDeveloper",
        "password": "notTheRealPassword"
      }
    }
  }'
```

#### 🛠️ Usage

```python
post_response = jumpcloud.workday_import.post(
    auth={
    },
    name="dolore tempor",
    report_url="est sit laboris",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### auth: [`AuthInput`](./jump_cloud_python_sdk/type/auth_input.py)


##### name: `str`

##### report_url: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`WorkdayInput`](./jump_cloud_python_sdk/type/workday_input.py)
#### 🔄 Return

[`WorkdayOutput`](./jump_cloud_python_sdk/pydantic/workday_output.py)

#### 🌐 Endpoint

`/workdays` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.workday_import.put`

This endpoint allows you to update the name and Custom Report URL for a Workday Instance.

Currently, the name can not be changed from the default of `Workday Import`.

##### Sample Request
```
curl -X PUT https://console.jumpcloud.com/api/v2/workdays/{WorkdayID} \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}' \
  -d '{
	"reportUrl":"{Report_URL}",
	"name":"{Name}"
}	'
```

#### 🛠️ Usage

```python
put_response = jumpcloud.workday_import.put(
    id="id_example",
    name="string_example",
    report_url="string_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### id: `str`

##### name: `str`

##### report_url: `str`

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### ⚙️ Request Body

[`WorkdayFields`](./jump_cloud_python_sdk/type/workday_fields.py)
#### 🔄 Return

[`WorkdayOutput`](./jump_cloud_python_sdk/pydantic/workday_output.py)

#### 🌐 Endpoint

`/workdays/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.workday_import.workers`

This endpoint will return all of the data in your WorkDay Custom Report that has been associated with your WorkDay Instance in JumpCloud.

##### Sample Request

```
curl -X GET https://console.jumpcloud.com/api/v2/workdays/{WorkDayID}/workers \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: {API_KEY}'


```

#### 🛠️ Usage

```python
workers_response = jumpcloud.workday_import.workers(
    workday_id="workday_id_example",
    limit=10,
    skip=0,
    sort=[],
    x_org_id="string_example",
)
```

#### ⚙️ Parameters

##### workday_id: `str`

##### limit: `int`

The number of records to return at once. Limited to 100.

##### skip: `int`

The offset into the records to return.

##### sort: List[`str`]

The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending. 

##### x_org_id: `str`

Organization identifier that can be obtained from console settings.

#### 🔄 Return

[`WorkdaysWorkersResponse`](./jump_cloud_python_sdk/pydantic/workdays_workers_response.py)

#### 🌐 Endpoint

`/workdays/{workday_id}/workers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `jumpcloud.fde.get_fde_key`

This endpoint will return the current (latest) fde key saved for a system.

#### 🛠️ Usage

```python
get_fde_key_response = jumpcloud.fde.get_fde_key(
    system_id="system_id_example",
    x_org_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### system_id: `str`<a id="system_id-str"></a>

##### x_org_id: `str`<a id="x_org_id-str"></a>

Organization identifier that can be obtained from console settings.

#### 🔄 Return<a id="🔄-return"></a>

[`Systemfdekey`](./jump_cloud_python_sdk/pydantic/systemfdekey.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/systems/{system_id}/fdekey` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---


## Author<a id="author"></a>
This Python package is automatically generated by [Konfig](https://konfigthis.com)
