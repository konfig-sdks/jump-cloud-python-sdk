import typing_extensions

from jump_cloud_python_sdk.apis.tags import TagValues
from jump_cloud_python_sdk.apis.tags.graph_api import GraphApi
from jump_cloud_python_sdk.apis.tags.providers_api import ProvidersApi
from jump_cloud_python_sdk.apis.tags.system_insights_api import SystemInsightsApi
from jump_cloud_python_sdk.apis.tags.user_groups_api import UserGroupsApi
from jump_cloud_python_sdk.apis.tags.managed_service_provider_api import ManagedServiceProviderApi
from jump_cloud_python_sdk.apis.tags.apple_mdm_api import AppleMDMApi
from jump_cloud_python_sdk.apis.tags.google_emm_api import GoogleEMMApi
from jump_cloud_python_sdk.apis.tags.policies_api import PoliciesApi
from jump_cloud_python_sdk.apis.tags.system_groups_api import SystemGroupsApi
from jump_cloud_python_sdk.apis.tags.users_api import UsersApi
from jump_cloud_python_sdk.apis.tags.g_suite_api import GSuiteApi
from jump_cloud_python_sdk.apis.tags.office365_api import Office365Api
from jump_cloud_python_sdk.apis.tags.active_directory_api import ActiveDirectoryApi
from jump_cloud_python_sdk.apis.tags.software_apps_api import SoftwareAppsApi
from jump_cloud_python_sdk.apis.tags.policy_groups_api import PolicyGroupsApi
from jump_cloud_python_sdk.apis.tags.user_group_associations_api import UserGroupAssociationsApi
from jump_cloud_python_sdk.apis.tags.systems_api import SystemsApi
from jump_cloud_python_sdk.apis.tags.applications_api import ApplicationsApi
from jump_cloud_python_sdk.apis.tags.bulk_job_requests_api import BulkJobRequestsApi
from jump_cloud_python_sdk.apis.tags.duo_api import DuoApi
from jump_cloud_python_sdk.apis.tags.workday_import_api import WorkdayImportApi
from jump_cloud_python_sdk.apis.tags.ldap_servers_api import LDAPServersApi
from jump_cloud_python_sdk.apis.tags.system_group_associations_api import SystemGroupAssociationsApi
from jump_cloud_python_sdk.apis.tags.commands_api import CommandsApi
from jump_cloud_python_sdk.apis.tags.ip_lists_api import IPListsApi
from jump_cloud_python_sdk.apis.tags.policy_group_templates_api import PolicyGroupTemplatesApi
from jump_cloud_python_sdk.apis.tags.authentication_policies_api import AuthenticationPoliciesApi
from jump_cloud_python_sdk.apis.tags.custom_emails_api import CustomEmailsApi
from jump_cloud_python_sdk.apis.tags.organizations_api import OrganizationsApi
from jump_cloud_python_sdk.apis.tags.samba_domains_api import SambaDomainsApi
from jump_cloud_python_sdk.apis.tags.administrators_api import AdministratorsApi
from jump_cloud_python_sdk.apis.tags.identity_providers_api import IdentityProvidersApi
from jump_cloud_python_sdk.apis.tags.ingresso_api import IngressoApi
from jump_cloud_python_sdk.apis.tags.policy_group_associations_api import PolicyGroupAssociationsApi
from jump_cloud_python_sdk.apis.tags.radius_servers_api import RADIUSServersApi
from jump_cloud_python_sdk.apis.tags.systems_organization_settings_api import SystemsOrganizationSettingsApi
from jump_cloud_python_sdk.apis.tags.policy_group_members_membership_api import PolicyGroupMembersMembershipApi
from jump_cloud_python_sdk.apis.tags.system_group_members_membership_api import SystemGroupMembersMembershipApi
from jump_cloud_python_sdk.apis.tags.user_group_members_membership_api import UserGroupMembersMembershipApi
from jump_cloud_python_sdk.apis.tags.g_suite_import_api import GSuiteImportApi
from jump_cloud_python_sdk.apis.tags.password_manager_api import PasswordManagerApi
from jump_cloud_python_sdk.apis.tags.policytemplates_api import PolicytemplatesApi
from jump_cloud_python_sdk.apis.tags.push_verification_api import PushVerificationApi
from jump_cloud_python_sdk.apis.tags.aggregated_policy_stats_api import AggregatedPolicyStatsApi
from jump_cloud_python_sdk.apis.tags.directories_api import DirectoriesApi
from jump_cloud_python_sdk.apis.tags.feature_trials_api import FeatureTrialsApi
from jump_cloud_python_sdk.apis.tags.groups_api import GroupsApi
from jump_cloud_python_sdk.apis.tags.image_api import ImageApi
from jump_cloud_python_sdk.apis.tags.logos_api import LogosApi
from jump_cloud_python_sdk.apis.tags.microsoft_mdm_api import MicrosoftMDMApi
from jump_cloud_python_sdk.apis.tags.office365_import_api import Office365ImportApi
from jump_cloud_python_sdk.apis.tags.scim_import_api import SCIMImportApi
from jump_cloud_python_sdk.apis.tags.subscriptions_api import SubscriptionsApi
from jump_cloud_python_sdk.apis.tags.fde_api import FdeApi
from jump_cloud_python_sdk.apis.tags.account_manager_calendar_api import AccountManagerCalendarApi
from jump_cloud_python_sdk.apis.tags.add_on_api import AddOnApi
from jump_cloud_python_sdk.apis.tags.apple_vpp_api import AppleVPPApi
from jump_cloud_python_sdk.apis.tags.command_templates_api import CommandTemplatesApi
from jump_cloud_python_sdk.apis.tags.countries_api import CountriesApi
from jump_cloud_python_sdk.apis.tags.devices_api import DevicesApi
from jump_cloud_python_sdk.apis.tags.directory_insights_api import DirectoryInsightsApi
from jump_cloud_python_sdk.apis.tags.durt_api import DurtApi
from jump_cloud_python_sdk.apis.tags.edge_api import EdgeApi
from jump_cloud_python_sdk.apis.tags.go_api import GoApi
from jump_cloud_python_sdk.apis.tags.knowledge_api import KnowledgeApi
from jump_cloud_python_sdk.apis.tags.partners_api import PartnersApi
from jump_cloud_python_sdk.apis.tags.pay_now_api import PayNowApi
from jump_cloud_python_sdk.apis.tags.plan_api import PlanApi
from jump_cloud_python_sdk.apis.tags.plan_feature_api import PlanFeatureApi
from jump_cloud_python_sdk.apis.tags.promos_api import PromosApi
from jump_cloud_python_sdk.apis.tags.push_api import PushApi
from jump_cloud_python_sdk.apis.tags.recommendations_api import RecommendationsApi
from jump_cloud_python_sdk.apis.tags.remote_assist_api import RemoteAssistApi
from jump_cloud_python_sdk.apis.tags.sso_api import SSOApi
from jump_cloud_python_sdk.apis.tags.software_catalog_api import SoftwareCatalogApi
from jump_cloud_python_sdk.apis.tags.subscription_component_api import SubscriptionComponentApi
from jump_cloud_python_sdk.apis.tags.subscription_data_api import SubscriptionDataApi
from jump_cloud_python_sdk.apis.tags.trial_feature_insights_api import TrialFeatureInsightsApi
from jump_cloud_python_sdk.apis.tags.web_authn_api import WebAuthnApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.GRAPH: GraphApi,
        TagValues.PROVIDERS: ProvidersApi,
        TagValues.SYSTEM_INSIGHTS: SystemInsightsApi,
        TagValues.USER_GROUPS: UserGroupsApi,
        TagValues.MANAGED_SERVICE_PROVIDER: ManagedServiceProviderApi,
        TagValues.APPLE_MDM: AppleMDMApi,
        TagValues.GOOGLE_EMM: GoogleEMMApi,
        TagValues.POLICIES: PoliciesApi,
        TagValues.SYSTEM_GROUPS: SystemGroupsApi,
        TagValues.USERS: UsersApi,
        TagValues.G_SUITE: GSuiteApi,
        TagValues.OFFICE_365: Office365Api,
        TagValues.ACTIVE_DIRECTORY: ActiveDirectoryApi,
        TagValues.SOFTWARE_APPS: SoftwareAppsApi,
        TagValues.POLICY_GROUPS: PolicyGroupsApi,
        TagValues.USER_GROUP_ASSOCIATIONS: UserGroupAssociationsApi,
        TagValues.SYSTEMS: SystemsApi,
        TagValues.APPLICATIONS: ApplicationsApi,
        TagValues.BULK_JOB_REQUESTS: BulkJobRequestsApi,
        TagValues.DUO: DuoApi,
        TagValues.WORKDAY_IMPORT: WorkdayImportApi,
        TagValues.LDAP_SERVERS: LDAPServersApi,
        TagValues.SYSTEM_GROUP_ASSOCIATIONS: SystemGroupAssociationsApi,
        TagValues.COMMANDS: CommandsApi,
        TagValues.IP_LISTS: IPListsApi,
        TagValues.POLICY_GROUP_TEMPLATES: PolicyGroupTemplatesApi,
        TagValues.AUTHENTICATION_POLICIES: AuthenticationPoliciesApi,
        TagValues.CUSTOM_EMAILS: CustomEmailsApi,
        TagValues.ORGANIZATIONS: OrganizationsApi,
        TagValues.SAMBA_DOMAINS: SambaDomainsApi,
        TagValues.ADMINISTRATORS: AdministratorsApi,
        TagValues.IDENTITY_PROVIDERS: IdentityProvidersApi,
        TagValues.INGRESSO: IngressoApi,
        TagValues.POLICY_GROUP_ASSOCIATIONS: PolicyGroupAssociationsApi,
        TagValues.RADIUS_SERVERS: RADIUSServersApi,
        TagValues.SYSTEMS_ORGANIZATION_SETTINGS: SystemsOrganizationSettingsApi,
        TagValues.POLICY_GROUP_MEMBERS__MEMBERSHIP: PolicyGroupMembersMembershipApi,
        TagValues.SYSTEM_GROUP_MEMBERS__MEMBERSHIP: SystemGroupMembersMembershipApi,
        TagValues.USER_GROUP_MEMBERS__MEMBERSHIP: UserGroupMembersMembershipApi,
        TagValues.G_SUITE_IMPORT: GSuiteImportApi,
        TagValues.PASSWORD_MANAGER: PasswordManagerApi,
        TagValues.POLICYTEMPLATES: PolicytemplatesApi,
        TagValues.PUSH_VERIFICATION: PushVerificationApi,
        TagValues.AGGREGATED_POLICY_STATS: AggregatedPolicyStatsApi,
        TagValues.DIRECTORIES: DirectoriesApi,
        TagValues.FEATURE_TRIALS: FeatureTrialsApi,
        TagValues.GROUPS: GroupsApi,
        TagValues.IMAGE: ImageApi,
        TagValues.LOGOS: LogosApi,
        TagValues.MICROSOFT_MDM: MicrosoftMDMApi,
        TagValues.OFFICE_365_IMPORT: Office365ImportApi,
        TagValues.SCIM_IMPORT: SCIMImportApi,
        TagValues.SUBSCRIPTIONS: SubscriptionsApi,
        TagValues.FDE: FdeApi,
        TagValues.ACCOUNT_MANAGER_CALENDAR: AccountManagerCalendarApi,
        TagValues.ADD_ON: AddOnApi,
        TagValues.APPLE_VPP: AppleVPPApi,
        TagValues.COMMAND_TEMPLATES: CommandTemplatesApi,
        TagValues.COUNTRIES: CountriesApi,
        TagValues.DEVICES: DevicesApi,
        TagValues.DIRECTORY_INSIGHTS: DirectoryInsightsApi,
        TagValues.DURT: DurtApi,
        TagValues.EDGE: EdgeApi,
        TagValues.GO: GoApi,
        TagValues.KNOWLEDGE: KnowledgeApi,
        TagValues.PARTNERS: PartnersApi,
        TagValues.PAY_NOW: PayNowApi,
        TagValues.PLAN: PlanApi,
        TagValues.PLAN_FEATURE: PlanFeatureApi,
        TagValues.PROMOS: PromosApi,
        TagValues.PUSH: PushApi,
        TagValues.RECOMMENDATIONS: RecommendationsApi,
        TagValues.REMOTE_ASSIST: RemoteAssistApi,
        TagValues.SSO: SSOApi,
        TagValues.SOFTWARE_CATALOG: SoftwareCatalogApi,
        TagValues.SUBSCRIPTION_COMPONENT: SubscriptionComponentApi,
        TagValues.SUBSCRIPTION_DATA: SubscriptionDataApi,
        TagValues.TRIAL_FEATURE_INSIGHTS: TrialFeatureInsightsApi,
        TagValues.WEB_AUTHN: WebAuthnApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.GRAPH: GraphApi,
        TagValues.PROVIDERS: ProvidersApi,
        TagValues.SYSTEM_INSIGHTS: SystemInsightsApi,
        TagValues.USER_GROUPS: UserGroupsApi,
        TagValues.MANAGED_SERVICE_PROVIDER: ManagedServiceProviderApi,
        TagValues.APPLE_MDM: AppleMDMApi,
        TagValues.GOOGLE_EMM: GoogleEMMApi,
        TagValues.POLICIES: PoliciesApi,
        TagValues.SYSTEM_GROUPS: SystemGroupsApi,
        TagValues.USERS: UsersApi,
        TagValues.G_SUITE: GSuiteApi,
        TagValues.OFFICE_365: Office365Api,
        TagValues.ACTIVE_DIRECTORY: ActiveDirectoryApi,
        TagValues.SOFTWARE_APPS: SoftwareAppsApi,
        TagValues.POLICY_GROUPS: PolicyGroupsApi,
        TagValues.USER_GROUP_ASSOCIATIONS: UserGroupAssociationsApi,
        TagValues.SYSTEMS: SystemsApi,
        TagValues.APPLICATIONS: ApplicationsApi,
        TagValues.BULK_JOB_REQUESTS: BulkJobRequestsApi,
        TagValues.DUO: DuoApi,
        TagValues.WORKDAY_IMPORT: WorkdayImportApi,
        TagValues.LDAP_SERVERS: LDAPServersApi,
        TagValues.SYSTEM_GROUP_ASSOCIATIONS: SystemGroupAssociationsApi,
        TagValues.COMMANDS: CommandsApi,
        TagValues.IP_LISTS: IPListsApi,
        TagValues.POLICY_GROUP_TEMPLATES: PolicyGroupTemplatesApi,
        TagValues.AUTHENTICATION_POLICIES: AuthenticationPoliciesApi,
        TagValues.CUSTOM_EMAILS: CustomEmailsApi,
        TagValues.ORGANIZATIONS: OrganizationsApi,
        TagValues.SAMBA_DOMAINS: SambaDomainsApi,
        TagValues.ADMINISTRATORS: AdministratorsApi,
        TagValues.IDENTITY_PROVIDERS: IdentityProvidersApi,
        TagValues.INGRESSO: IngressoApi,
        TagValues.POLICY_GROUP_ASSOCIATIONS: PolicyGroupAssociationsApi,
        TagValues.RADIUS_SERVERS: RADIUSServersApi,
        TagValues.SYSTEMS_ORGANIZATION_SETTINGS: SystemsOrganizationSettingsApi,
        TagValues.POLICY_GROUP_MEMBERS__MEMBERSHIP: PolicyGroupMembersMembershipApi,
        TagValues.SYSTEM_GROUP_MEMBERS__MEMBERSHIP: SystemGroupMembersMembershipApi,
        TagValues.USER_GROUP_MEMBERS__MEMBERSHIP: UserGroupMembersMembershipApi,
        TagValues.G_SUITE_IMPORT: GSuiteImportApi,
        TagValues.PASSWORD_MANAGER: PasswordManagerApi,
        TagValues.POLICYTEMPLATES: PolicytemplatesApi,
        TagValues.PUSH_VERIFICATION: PushVerificationApi,
        TagValues.AGGREGATED_POLICY_STATS: AggregatedPolicyStatsApi,
        TagValues.DIRECTORIES: DirectoriesApi,
        TagValues.FEATURE_TRIALS: FeatureTrialsApi,
        TagValues.GROUPS: GroupsApi,
        TagValues.IMAGE: ImageApi,
        TagValues.LOGOS: LogosApi,
        TagValues.MICROSOFT_MDM: MicrosoftMDMApi,
        TagValues.OFFICE_365_IMPORT: Office365ImportApi,
        TagValues.SCIM_IMPORT: SCIMImportApi,
        TagValues.SUBSCRIPTIONS: SubscriptionsApi,
        TagValues.FDE: FdeApi,
        TagValues.ACCOUNT_MANAGER_CALENDAR: AccountManagerCalendarApi,
        TagValues.ADD_ON: AddOnApi,
        TagValues.APPLE_VPP: AppleVPPApi,
        TagValues.COMMAND_TEMPLATES: CommandTemplatesApi,
        TagValues.COUNTRIES: CountriesApi,
        TagValues.DEVICES: DevicesApi,
        TagValues.DIRECTORY_INSIGHTS: DirectoryInsightsApi,
        TagValues.DURT: DurtApi,
        TagValues.EDGE: EdgeApi,
        TagValues.GO: GoApi,
        TagValues.KNOWLEDGE: KnowledgeApi,
        TagValues.PARTNERS: PartnersApi,
        TagValues.PAY_NOW: PayNowApi,
        TagValues.PLAN: PlanApi,
        TagValues.PLAN_FEATURE: PlanFeatureApi,
        TagValues.PROMOS: PromosApi,
        TagValues.PUSH: PushApi,
        TagValues.RECOMMENDATIONS: RecommendationsApi,
        TagValues.REMOTE_ASSIST: RemoteAssistApi,
        TagValues.SSO: SSOApi,
        TagValues.SOFTWARE_CATALOG: SoftwareCatalogApi,
        TagValues.SUBSCRIPTION_COMPONENT: SubscriptionComponentApi,
        TagValues.SUBSCRIPTION_DATA: SubscriptionDataApi,
        TagValues.TRIAL_FEATURE_INSIGHTS: TrialFeatureInsightsApi,
        TagValues.WEB_AUTHN: WebAuthnApi,
    }
)
