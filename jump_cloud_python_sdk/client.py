# coding: utf-8
"""
    JumpCloud API

    # Overview  JumpCloud's V2 API. This set of endpoints allows JumpCloud customers to manage objects, groupings and mappings and interact with the JumpCloud Graph.  ## API Best Practices  Read the linked Help Article below for guidance on retrying failed requests to JumpCloud's REST API, as well as best practices for structuring subsequent retry requests. Customizing retry mechanisms based on these recommendations will increase the reliability and dependability of your API calls.  Covered topics include: 1. Important Considerations 2. Supported HTTP Request Methods 3. Response codes 4. API Key rotation 5. Paginating 6. Error handling 7. Retry rates  [JumpCloud Help Center - API Best Practices](https://support.jumpcloud.com/support/s/article/JumpCloud-API-Best-Practices)  # Directory Objects  This API offers the ability to interact with some of our core features; otherwise known as Directory Objects. The Directory Objects are:  * Commands * Policies * Policy Groups * Applications * Systems * Users * User Groups * System Groups * Radius Servers * Directories: Office 365, LDAP,G-Suite, Active Directory * Duo accounts and applications.  The Directory Object is an important concept to understand in order to successfully use JumpCloud API.  ## JumpCloud Graph  We've also introduced the concept of the JumpCloud Graph along with  Directory Objects. The Graph is a powerful aspect of our platform which will enable you to associate objects with each other, or establish membership for certain objects to become members of other objects.  Specific `GET` endpoints will allow you to traverse the JumpCloud Graph to return all indirect and directly bound objects in your organization.  | ![alt text](https://s3.amazonaws.com/jumpcloud-kb/Knowledge+Base+Photos/API+Docs/jumpcloud_graph.png \"JumpCloud Graph Model Example\") | |:--:| | **This diagram highlights our association and membership model as it relates to Directory Objects.** |  # API Key  ## Access Your API Key  To locate your API Key:  1. Log into the [JumpCloud Admin Console](https://console.jumpcloud.com/). 2. Go to the username drop down located in the top-right of the Console. 3. Retrieve your API key from API Settings.  ## API Key Considerations  This API key is associated to the currently logged in administrator. Other admins will have different API keys.  **WARNING** Please keep this API key secret, as it grants full access to any data accessible via your JumpCloud console account.  You can also reset your API key in the same location in the JumpCloud Admin Console.  ## Recycling or Resetting Your API Key  In order to revoke access with the current API key, simply reset your API key. This will render all calls using the previous API key inaccessible.  Your API key will be passed in as a header with the header name \"x-api-key\".  ```bash curl -H \"x-api-key: [YOUR_API_KEY_HERE]\" \"https://console.jumpcloud.com/api/v2/systemgroups\" ```  # System Context  * [Introduction](https://docs.jumpcloud.com) * [Supported endpoints](https://docs.jumpcloud.com) * [Response codes](https://docs.jumpcloud.com) * [Authentication](https://docs.jumpcloud.com) * [Additional examples](https://docs.jumpcloud.com) * [Third party](https://docs.jumpcloud.com)  ## Introduction  JumpCloud System Context Authorization is an alternative way to authenticate with a subset of JumpCloud's REST APIs. Using this method, a system can manage its information and resource associations, allowing modern auto provisioning environments to scale as needed.  **Notes:**   * The following documentation applies to Linux Operating Systems only.  * Systems that have been automatically enrolled using Apple's Device Enrollment Program (DEP) or systems enrolled using the User Portal install are not eligible to use the System Context API to prevent unauthorized access to system groups and resources. If a script that utilizes the System Context API is invoked on a system enrolled in this way, it will display an error.  ## Supported Endpoints  JumpCloud System Context Authorization can be used in conjunction with Systems endpoints found in the V1 API and certain System Group endpoints found in the v2 API.  * A system may fetch, alter, and delete metadata about itself, including manipulating a system's Group and Systemuser associations,   * `/api/systems/{system_id}` | [`GET`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_get) [`PUT`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_put) * A system may delete itself from your JumpCloud organization   * `/api/systems/{system_id}` | [`DELETE`](https://docs.jumpcloud.com/api/1.0/index.html#operation/systems_delete) * A system may fetch its direct resource associations under v2 (Groups)   * `/api/v2/systems/{system_id}/memberof` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemGroupMembership)   * `/api/v2/systems/{system_id}/associations` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemAssociationsList)   * `/api/v2/systems/{system_id}/users` | [`GET`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemTraverseUser) * A system may alter its direct resource associations under v2 (Groups)   * `/api/v2/systems/{system_id}/associations` | [`POST`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemAssociationsPost) * A system may alter its System Group associations   * `/api/v2/systemgroups/{group_id}/members` | [`POST`](https://docs.jumpcloud.com/api/2.0/index.html#operation/graph_systemGroupMembersPost)     * _NOTE_ If a system attempts to alter the system group membership of a different system the request will be rejected  ## Response Codes  If endpoints other than those described above are called using the System Context API, the server will return a `401` response.  ## Authentication  To allow for secure access to our APIs, you must authenticate each API request. JumpCloud System Context Authorization uses [HTTP Signatures](https://tools.ietf.org/html/draft-cavage-http-signatures-00) to authenticate API requests. The HTTP Signatures sent with each request are similar to the signatures used by the Amazon Web Services REST API. To help with the request-signing process, we have provided an [example bash script](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/shell/SigningExample.sh). This example API request simply requests the entire system record. You must be root, or have permissions to access the contents of the `/opt/jc` directory to generate a signature.  Here is a breakdown of the example script with explanations.  First, the script extracts the systemKey from the JSON formatted `/opt/jc/jcagent.conf` file.  ```bash #!/bin/bash conf=\"`cat /opt/jc/jcagent.conf`\" regex=\"systemKey\\\":\\\"(\\w+)\\\"\"  if [[ $conf =~ $regex ]] ; then   systemKey=\"${BASH_REMATCH[1]}\" fi ```  Then, the script retrieves the current date in the correct format.  ```bash now=`date -u \"+%a, %d %h %Y %H:%M:%S GMT\"`; ```  Next, we build a signing string to demonstrate the expected signature format. The signed string must consist of the [request-line](https://tools.ietf.org/html/rfc2616#page-35) and the date header, separated by a newline character.  ```bash signstr=\"GET /api/systems/${systemKey} HTTP/1.1\\ndate: ${now}\" ```  The next step is to calculate and apply the signature. This is a two-step process:  1. Create a signature from the signing string using the JumpCloud Agent private key: ``printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key`` 2. Then Base64-encode the signature string and trim off the newline characters: ``| openssl enc -e -a | tr -d '\\n'``  The combined steps above result in:  ```bash signature=`printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key | openssl enc -e -a | tr -d '\\n'` ; ```  Finally, we make sure the API call sending the signature has the same Authorization and Date header values, HTTP method, and URL that were used in the signing string.  ```bash curl -iq \\   -H \"Accept: application/json\" \\   -H \"Content-Type: application/json\" \\   -H \"Date: ${now}\" \\   -H \"Authorization: Signature keyId=\\\"system/${systemKey}\\\",headers=\\\"request-line date\\\",algorithm=\\\"rsa-sha256\\\",signature=\\\"${signature}\\\"\" \\   --url https://console.jumpcloud.com/api/systems/${systemKey} ```  ### Input Data  All PUT and POST methods should use the HTTP Content-Type header with a value of 'application/json'. PUT methods are used for updating a record. POST methods are used to create a record.  The following example demonstrates how to update the `displayName` of the system.  ```bash signstr=\"PUT /api/systems/${systemKey} HTTP/1.1\\ndate: ${now}\" signature=`printf \"$signstr\" | openssl dgst -sha256 -sign /opt/jc/client.key | openssl enc -e -a | tr -d '\\n'` ;  curl -iq \\   -d \"{\\\"displayName\\\" : \\\"updated-system-name-1\\\"}\" \\   -X \"PUT\" \\   -H \"Content-Type: application/json\" \\   -H \"Accept: application/json\" \\   -H \"Date: ${now}\" \\   -H \"Authorization: Signature keyId=\\\"system/${systemKey}\\\",headers=\\\"request-line date\\\",algorithm=\\\"rsa-sha256\\\",signature=\\\"${signature}\\\"\" \\   --url https://console.jumpcloud.com/api/systems/${systemKey} ```  ### Output Data  All results will be formatted as JSON.  Here is an abbreviated example of response output:  ```json {   \"_id\": \"625ee96f52e144993e000015\",   \"agentServer\": \"lappy386\",   \"agentVersion\": \"0.9.42\",   \"arch\": \"x86_64\",   \"connectionKey\": \"127.0.0.1_51812\",   \"displayName\": \"ubuntu-1204\",   \"firstContact\": \"2013-10-16T19:30:55.611Z\",   \"hostname\": \"ubuntu-1204\"   ... ```  ## Additional Examples  ### Signing Authentication Example  This example demonstrates how to make an authenticated request to fetch the JumpCloud record for this system.  [SigningExample.sh](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/shell/SigningExample.sh)  ### Shutdown Hook  This example demonstrates how to make an authenticated request on system shutdown. Using an init.d script registered at run level 0, you can call the System Context API as the system is shutting down.  [Instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) is an example of an init.d script that only runs at system shutdown.  After customizing the [instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) script, you should install it on the system(s) running the JumpCloud agent.  1. Copy the modified [instance-shutdown-initd](https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd) to `/etc/init.d/instance-shutdown`. 2. On Ubuntu systems, run `update-rc.d instance-shutdown defaults`. On RedHat/CentOS systems, run `chkconfig --add instance-shutdown`.  ## Third Party  ### Chef Cookbooks  [https://github.com/nshenry03/jumpcloud](https://github.com/nshenry03/jumpcloud)  [https://github.com/cjs226/jumpcloud](https://github.com/cjs226/jumpcloud)  # Multi-Tenant Portal Headers  Multi-Tenant Organization API Headers are available for JumpCloud Admins to use when making API requests from Organizations that have multiple managed organizations.  The `x-org-id` is a required header for all multi-tenant admins when making API requests to JumpCloud. This header will define to which organization you would like to make the request.  **NOTE** Single Tenant Admins do not need to provide this header when making an API request.  ## Header Value  `x-org-id`  ## API Response Codes  * `400` Malformed ID. * `400` x-org-id and Organization path ID do not match. * `401` ID not included for multi-tenant admin * `403` ID included on unsupported route. * `404` Organization ID Not Found.  ```bash curl -X GET https://console.jumpcloud.com/api/v2/directories \\   -H 'accept: application/json' \\   -H 'content-type: application/json' \\   -H 'x-api-key: {API_KEY}' \\   -H 'x-org-id: {ORG_ID}'  ```  ## To Obtain an Individual Organization ID via the UI  As a prerequisite, your Primary Organization will need to be setup for Multi-Tenancy. This provides access to the Multi-Tenant Organization Admin Portal.  1. Log into JumpCloud [Admin Console](https://console.jumpcloud.com). If you are a multi-tenant Admin, you will automatically be routed to the Multi-Tenant Admin Portal. 2. From the Multi-Tenant Portal's primary navigation bar, select the Organization you'd like to access. 3. You will automatically be routed to that Organization's Admin Console. 4. Go to Settings in the sub-tenant's primary navigation. 5. You can obtain your Organization ID below your Organization's Contact Information on the Settings page.  ## To Obtain All Organization IDs via the API  * You can make an API request to this endpoint using the API key of your Primary Organization.  `https://console.jumpcloud.com/api/organizations/` This will return all your managed organizations.  ```bash curl -X GET \\   https://console.jumpcloud.com/api/organizations/ \\   -H 'Accept: application/json' \\   -H 'Content-Type: application/json' \\   -H 'x-api-key: {API_KEY}' ```  # SDKs  You can find language specific SDKs that can help you kickstart your Integration with JumpCloud in the following GitHub repositories:  * [Python](https://github.com/TheJumpCloud/jcapi-python) * [Go](https://github.com/TheJumpCloud/jcapi-go) * [Ruby](https://github.com/TheJumpCloud/jcapi-ruby) * [Java](https://github.com/TheJumpCloud/jcapi-java) 

    The version of the OpenAPI document: 2.0
    Contact: support@jumpcloud.com
    Created by: https://support.jumpcloud.com/support/s/
"""

import typing
import inspect
from datetime import date, datetime
from jump_cloud_python_sdk.client_custom import ClientCustom
from jump_cloud_python_sdk.configuration import Configuration
from jump_cloud_python_sdk.api_client import ApiClient
from jump_cloud_python_sdk.type_util import copy_signature
from jump_cloud_python_sdk.apis.tags.active_directory_api import ActiveDirectoryApi
from jump_cloud_python_sdk.apis.tags.administrators_api import AdministratorsApi
from jump_cloud_python_sdk.apis.tags.aggregated_policy_stats_api import AggregatedPolicyStatsApi
from jump_cloud_python_sdk.apis.tags.apple_mdm_api import AppleMDMApi
from jump_cloud_python_sdk.apis.tags.applications_api import ApplicationsApi
from jump_cloud_python_sdk.apis.tags.authentication_policies_api import AuthenticationPoliciesApi
from jump_cloud_python_sdk.apis.tags.bulk_job_requests_api import BulkJobRequestsApi
from jump_cloud_python_sdk.apis.tags.commands_api import CommandsApi
from jump_cloud_python_sdk.apis.tags.custom_emails_api import CustomEmailsApi
from jump_cloud_python_sdk.apis.tags.directories_api import DirectoriesApi
from jump_cloud_python_sdk.apis.tags.duo_api import DuoApi
from jump_cloud_python_sdk.apis.tags.feature_trials_api import FeatureTrialsApi
from jump_cloud_python_sdk.apis.tags.g_suite_api import GSuiteApi
from jump_cloud_python_sdk.apis.tags.g_suite_import_api import GSuiteImportApi
from jump_cloud_python_sdk.apis.tags.google_emm_api import GoogleEMMApi
from jump_cloud_python_sdk.apis.tags.graph_api import GraphApi
from jump_cloud_python_sdk.apis.tags.groups_api import GroupsApi
from jump_cloud_python_sdk.apis.tags.ip_lists_api import IPListsApi
from jump_cloud_python_sdk.apis.tags.identity_providers_api import IdentityProvidersApi
from jump_cloud_python_sdk.apis.tags.image_api import ImageApi
from jump_cloud_python_sdk.apis.tags.ingresso_api import IngressoApi
from jump_cloud_python_sdk.apis.tags.ldap_servers_api import LDAPServersApi
from jump_cloud_python_sdk.apis.tags.logos_api import LogosApi
from jump_cloud_python_sdk.apis.tags.managed_service_provider_api import ManagedServiceProviderApi
from jump_cloud_python_sdk.apis.tags.microsoft_mdm_api import MicrosoftMDMApi
from jump_cloud_python_sdk.apis.tags.office365_api import Office365Api
from jump_cloud_python_sdk.apis.tags.office365_import_api import Office365ImportApi
from jump_cloud_python_sdk.apis.tags.organizations_api import OrganizationsApi
from jump_cloud_python_sdk.apis.tags.password_manager_api import PasswordManagerApi
from jump_cloud_python_sdk.apis.tags.policies_api import PoliciesApi
from jump_cloud_python_sdk.apis.tags.policy_group_associations_api import PolicyGroupAssociationsApi
from jump_cloud_python_sdk.apis.tags.policy_group_members_membership_api import PolicyGroupMembersMembershipApi
from jump_cloud_python_sdk.apis.tags.policy_group_templates_api import PolicyGroupTemplatesApi
from jump_cloud_python_sdk.apis.tags.policy_groups_api import PolicyGroupsApi
from jump_cloud_python_sdk.apis.tags.policytemplates_api import PolicytemplatesApi
from jump_cloud_python_sdk.apis.tags.providers_api import ProvidersApi
from jump_cloud_python_sdk.apis.tags.push_verification_api import PushVerificationApi
from jump_cloud_python_sdk.apis.tags.radius_servers_api import RADIUSServersApi
from jump_cloud_python_sdk.apis.tags.scim_import_api import SCIMImportApi
from jump_cloud_python_sdk.apis.tags.samba_domains_api import SambaDomainsApi
from jump_cloud_python_sdk.apis.tags.software_apps_api import SoftwareAppsApi
from jump_cloud_python_sdk.apis.tags.subscriptions_api import SubscriptionsApi
from jump_cloud_python_sdk.apis.tags.system_group_associations_api import SystemGroupAssociationsApi
from jump_cloud_python_sdk.apis.tags.system_group_members_membership_api import SystemGroupMembersMembershipApi
from jump_cloud_python_sdk.apis.tags.system_groups_api import SystemGroupsApi
from jump_cloud_python_sdk.apis.tags.system_insights_api import SystemInsightsApi
from jump_cloud_python_sdk.apis.tags.systems_api import SystemsApi
from jump_cloud_python_sdk.apis.tags.systems_organization_settings_api import SystemsOrganizationSettingsApi
from jump_cloud_python_sdk.apis.tags.user_group_associations_api import UserGroupAssociationsApi
from jump_cloud_python_sdk.apis.tags.user_group_members_membership_api import UserGroupMembersMembershipApi
from jump_cloud_python_sdk.apis.tags.user_groups_api import UserGroupsApi
from jump_cloud_python_sdk.apis.tags.users_api import UsersApi
from jump_cloud_python_sdk.apis.tags.workday_import_api import WorkdayImportApi
from jump_cloud_python_sdk.apis.tags.fde_api import FdeApi



class JumpCloud(ClientCustom):

    def __init__(self, configuration: typing.Union[Configuration, None] = None, **kwargs):
        super().__init__(configuration, **kwargs)
        if (len(kwargs) > 0):
            configuration = Configuration(**kwargs)
        if (configuration is None):
            raise Exception("configuration is required")
        api_client = ApiClient(configuration)
        self.active_directory: ActiveDirectoryApi = ActiveDirectoryApi(api_client)
        self.administrators: AdministratorsApi = AdministratorsApi(api_client)
        self.aggregated_policy_stats: AggregatedPolicyStatsApi = AggregatedPolicyStatsApi(api_client)
        self.apple_mdm: AppleMDMApi = AppleMDMApi(api_client)
        self.applications: ApplicationsApi = ApplicationsApi(api_client)
        self.authentication_policies: AuthenticationPoliciesApi = AuthenticationPoliciesApi(api_client)
        self.bulk_job_requests: BulkJobRequestsApi = BulkJobRequestsApi(api_client)
        self.commands: CommandsApi = CommandsApi(api_client)
        self.custom_emails: CustomEmailsApi = CustomEmailsApi(api_client)
        self.directories: DirectoriesApi = DirectoriesApi(api_client)
        self.duo: DuoApi = DuoApi(api_client)
        self.feature_trials: FeatureTrialsApi = FeatureTrialsApi(api_client)
        self.g_suite: GSuiteApi = GSuiteApi(api_client)
        self.g_suite_import: GSuiteImportApi = GSuiteImportApi(api_client)
        self.google_emm: GoogleEMMApi = GoogleEMMApi(api_client)
        self.graph: GraphApi = GraphApi(api_client)
        self.groups: GroupsApi = GroupsApi(api_client)
        self.ip_lists: IPListsApi = IPListsApi(api_client)
        self.identity_providers: IdentityProvidersApi = IdentityProvidersApi(api_client)
        self.image: ImageApi = ImageApi(api_client)
        self.ingresso: IngressoApi = IngressoApi(api_client)
        self.ldap_servers: LDAPServersApi = LDAPServersApi(api_client)
        self.logos: LogosApi = LogosApi(api_client)
        self.managed_service_provider: ManagedServiceProviderApi = ManagedServiceProviderApi(api_client)
        self.microsoft_mdm: MicrosoftMDMApi = MicrosoftMDMApi(api_client)
        self.office_365: Office365Api = Office365Api(api_client)
        self.office_365_import: Office365ImportApi = Office365ImportApi(api_client)
        self.organizations: OrganizationsApi = OrganizationsApi(api_client)
        self.password_manager: PasswordManagerApi = PasswordManagerApi(api_client)
        self.policies: PoliciesApi = PoliciesApi(api_client)
        self.policy_group_associations: PolicyGroupAssociationsApi = PolicyGroupAssociationsApi(api_client)
        self.policy_group_members_&amp;_membership: PolicyGroupMembersMembershipApi = PolicyGroupMembersMembershipApi(api_client)
        self.policy_group_templates: PolicyGroupTemplatesApi = PolicyGroupTemplatesApi(api_client)
        self.policy_groups: PolicyGroupsApi = PolicyGroupsApi(api_client)
        self.policytemplates: PolicytemplatesApi = PolicytemplatesApi(api_client)
        self.providers: ProvidersApi = ProvidersApi(api_client)
        self.push_verification: PushVerificationApi = PushVerificationApi(api_client)
        self.radius_servers: RADIUSServersApi = RADIUSServersApi(api_client)
        self.scim_import: SCIMImportApi = SCIMImportApi(api_client)
        self.samba_domains: SambaDomainsApi = SambaDomainsApi(api_client)
        self.software_apps: SoftwareAppsApi = SoftwareAppsApi(api_client)
        self.subscriptions: SubscriptionsApi = SubscriptionsApi(api_client)
        self.system_group_associations: SystemGroupAssociationsApi = SystemGroupAssociationsApi(api_client)
        self.system_group_members_&amp;_membership: SystemGroupMembersMembershipApi = SystemGroupMembersMembershipApi(api_client)
        self.system_groups: SystemGroupsApi = SystemGroupsApi(api_client)
        self.system_insights: SystemInsightsApi = SystemInsightsApi(api_client)
        self.systems: SystemsApi = SystemsApi(api_client)
        self.systems_organization_settings: SystemsOrganizationSettingsApi = SystemsOrganizationSettingsApi(api_client)
        self.user_group_associations: UserGroupAssociationsApi = UserGroupAssociationsApi(api_client)
        self.user_group_members_&amp;_membership: UserGroupMembersMembershipApi = UserGroupMembersMembershipApi(api_client)
        self.user_groups: UserGroupsApi = UserGroupsApi(api_client)
        self.users: UsersApi = UsersApi(api_client)
        self.workday_import: WorkdayImportApi = WorkdayImportApi(api_client)
        self.fde: FdeApi = FdeApi(api_client)
