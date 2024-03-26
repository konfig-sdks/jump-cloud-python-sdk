operation_parameter_map = {
    '/activedirectories/{activedirectory_id}/associations-GET': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories/{activedirectory_id}/associations-POST': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories/{activedirectory_id}/users-GET': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/activedirectories/{activedirectory_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/activedirectories/{activedirectory_id}/agents/{agent_id}-DELETE': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'agent_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories/{activedirectory_id}/agents/{agent_id}-GET': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'agent_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories/{activedirectory_id}/agents-GET': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories/{activedirectory_id}/agents-POST': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'agentType'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories/{id}-PATCH': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'domain'
            },
            {
                'name': 'id'
            },
            {
                'name': 'primaryAgent'
            },
            {
                'name': 'useCase'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories-POST': {
        'parameters': [
            {
                'name': 'domain'
            },
            {
                'name': 'id'
            },
            {
                'name': 'primaryAgent'
            },
            {
                'name': 'useCase'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/administrators/{id}/organizationlinks-POST': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'organization'
            },
        ]
    },
    '/administrators/{id}/organizationlinks-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/organizations/{id}/administratorlinks-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/administrators/{administrator_id}/organizationlinks/{id}-DELETE': {
        'parameters': [
            {
                'name': 'administrator_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/systems/{systemObjectId}/aggregated-policy-stats-GET': {
        'parameters': [
            {
                'name': 'systemObjectId'
            },
            {
                'name': 'organizationObjectId'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/csr-GET': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/devices/{device_id}-DELETE': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'device_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/depkey-GET': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/devices/{device_id}/clearActivationLock-POST': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'device_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/devices/{device_id}/osUpdateStatus-POST': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'device_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/devices/{device_id}/refreshActivationLockInformation-POST': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'device_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/devices/{device_id}/scheduleOSUpdate-POST': {
        'parameters': [
            {
                'name': 'install_action'
            },
            {
                'name': 'product_key'
            },
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'device_id'
            },
            {
                'name': 'max_user_deferrals'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/devices/{device_id}/erase-POST': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'device_id'
            },
            {
                'name': 'pin'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/devices-GET': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-total-count'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/devices/{device_id}/lock-POST': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'device_id'
            },
            {
                'name': 'pin'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/devices/{device_id}/restart-POST': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'device_id'
            },
            {
                'name': 'kextPaths'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/devices/{device_id}/shutdown-POST': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'device_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/enrollmentprofiles/{id}-GET': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/enrollmentprofiles-GET': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/devices/{device_id}-GET': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'device_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/applemdms/{id}-PUT': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'ades'
            },
            {
                'name': 'allowMobileUserEnrollment'
            },
            {
                'name': 'appleCertCreatorAppleID'
            },
            {
                'name': 'appleSignedCert'
            },
            {
                'name': 'defaultIosUserEnrollmentDeviceGroupID'
            },
            {
                'name': 'defaultSystemGroupID'
            },
            {
                'name': 'dep'
            },
            {
                'name': 'encryptedDepServerToken'
            },
            {
                'name': 'name'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applemdms/{apple_mdm_id}/refreshdepdevices-POST': {
        'parameters': [
            {
                'name': 'apple_mdm_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applications/{application_id}/associations-GET': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applications/{application_id}/associations-POST': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applications/{application_id}/users-GET': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/applications/{application_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/applications/{application_id}/import/jobs-POST': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'allowUserReactivation'
            },
            {
                'name': 'operations'
            },
            {
                'name': 'queryString'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applications/{application_id}/logo-DELETE': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applications/{application_id}-GET': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applications/{application_id}/logo-POST': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'image'
            },
        ]
    },
    '/applications/{application_id}/import/users-GET': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'query'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'sortOrder'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/authn/policies/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/authn/policies/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/authn/policies-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'x-total-count'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/authn/policies/{id}-PATCH': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'description'
            },
            {
                'name': 'conditions'
            },
            {
                'name': 'disabled'
            },
            {
                'name': 'effect'
            },
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/authn/policies-POST': {
        'parameters': [
            {
                'name': 'description'
            },
            {
                'name': 'conditions'
            },
            {
                'name': 'disabled'
            },
            {
                'name': 'effect'
            },
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/bulk/user/expires-POST': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/bulk/userstates-POST': {
        'parameters': [
            {
                'name': 'start_date'
            },
            {
                'name': 'state'
            },
            {
                'name': 'user_ids'
            },
            {
                'name': 'activation_email_override'
            },
            {
                'name': 'send_activation_emails'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/bulk/userstates/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/bulk/userstates/eventlist/next-GET': {
        'parameters': [
            {
                'name': 'users'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/bulk/userstates-GET': {
        'parameters': [
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'userid'
            },
        ]
    },
    '/bulk/user/unlocks-POST': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/bulk/users-POST': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'creation-source'
            },
        ]
    },
    '/bulk/users/{job_id}/results-GET': {
        'parameters': [
            {
                'name': 'job_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/bulk/users-PATCH': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/commandqueue/{workflow_instance_id}-DELETE': {
        'parameters': [
            {
                'name': 'workflow_instance_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/commands/{command_id}/associations-GET': {
        'parameters': [
            {
                'name': 'command_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/commands/{command_id}/associations-POST': {
        'parameters': [
            {
                'name': 'command_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/commands/{command_id}/systems-GET': {
        'parameters': [
            {
                'name': 'command_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/commands/{command_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'command_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/queuedcommand/workflows-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'search'
            },
        ]
    },
    '/customemails-POST': {
        'parameters': [
            {
                'name': 'subject'
            },
            {
                'name': 'type'
            },
            {
                'name': 'title'
            },
            {
                'name': 'body'
            },
            {
                'name': 'button'
            },
            {
                'name': 'header'
            },
            {
                'name': 'id'
            },
            {
                'name': 'nextStepContactInfo'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/customemails/{custom_email_type}-DELETE': {
        'parameters': [
            {
                'name': 'custom_email_type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/customemail/templates-GET': {
        'parameters': [
        ]
    },
    '/customemails/{custom_email_type}-GET': {
        'parameters': [
            {
                'name': 'custom_email_type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/customemails/{custom_email_type}-PUT': {
        'parameters': [
            {
                'name': 'subject'
            },
            {
                'name': 'type'
            },
            {
                'name': 'custom_email_type'
            },
            {
                'name': 'title'
            },
            {
                'name': 'body'
            },
            {
                'name': 'button'
            },
            {
                'name': 'header'
            },
            {
                'name': 'id'
            },
            {
                'name': 'nextStepContactInfo'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/directories-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/duo/accounts/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/duo/accounts/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/duo/accounts-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/duo/accounts-POST': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/duo/accounts/{account_id}/applications/{application_id}-DELETE': {
        'parameters': [
            {
                'name': 'account_id'
            },
            {
                'name': 'application_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/duo/accounts/{account_id}/applications/{application_id}-GET': {
        'parameters': [
            {
                'name': 'account_id'
            },
            {
                'name': 'application_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/duo/accounts/{account_id}/applications-GET': {
        'parameters': [
            {
                'name': 'account_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/duo/accounts/{account_id}/applications-POST': {
        'parameters': [
            {
                'name': 'apiHost'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'name'
            },
            {
                'name': 'secretKey'
            },
            {
                'name': 'account_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/duo/accounts/{account_id}/applications/{application_id}-PUT': {
        'parameters': [
            {
                'name': 'apiHost'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'name'
            },
            {
                'name': 'account_id'
            },
            {
                'name': 'application_id'
            },
            {
                'name': 'secretKey'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/featureTrials/{feature_code}-GET': {
        'parameters': [
            {
                'name': 'feature_code'
            },
        ]
    },
    '/gsuites/{gsuite_id}/domains-POST': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'domain'
            },
        ]
    },
    '/gsuites/{gsuite_id}/domains-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/gsuites/{gsuite_id}/domains/{domainId}-DELETE': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'domainId'
            },
        ]
    },
    '/gsuites/{gsuite_id}/associations-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/gsuites/{gsuite_id}/associations-POST': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/gsuites/{gsuite_id}/translationrules/{id}-DELETE': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/gsuites/{gsuite_id}/translationrules/{id}-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/gsuites/{gsuite_id}/translationrules-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/gsuites/{gsuite_id}/translationrules-POST': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'builtIn'
            },
            {
                'name': 'direction'
            },
        ]
    },
    '/gsuites/{gsuite_id}/users-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/gsuites/{gsuite_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/gsuites/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/gsuites/{gsuite_id}/import/jumpcloudusers-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'maxResults'
            },
            {
                'name': 'orderBy'
            },
            {
                'name': 'pageToken'
            },
            {
                'name': 'query'
            },
            {
                'name': 'sortOrder'
            },
        ]
    },
    '/gsuites/{gsuite_id}/import/users-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'maxResults'
            },
            {
                'name': 'orderBy'
            },
            {
                'name': 'pageToken'
            },
            {
                'name': 'query'
            },
            {
                'name': 'sortOrder'
            },
        ]
    },
    '/gsuites/{id}-PATCH': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'defaultDomain'
            },
            {
                'name': 'groupsEnabled'
            },
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'userLockoutAction'
            },
            {
                'name': 'userPasswordExpirationAction'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/gsuites/{gsuite_id}/import/jumpcloudusers-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'maxResults'
            },
            {
                'name': 'orderBy'
            },
            {
                'name': 'pageToken'
            },
            {
                'name': 'query'
            },
            {
                'name': 'sortOrder'
            },
        ]
    },
    '/gsuites/{gsuite_id}/import/users-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'maxResults'
            },
            {
                'name': 'orderBy'
            },
            {
                'name': 'pageToken'
            },
            {
                'name': 'query'
            },
            {
                'name': 'sortOrder'
            },
        ]
    },
    '/google-emm/signup-urls-POST': {
        'parameters': [
        ]
    },
    '/google-emm/enrollment-tokens-POST': {
        'parameters': [
            {
                'name': 'allowPersonalUsage'
            },
            {
                'name': 'createdWhere'
            },
            {
                'name': 'displayName'
            },
            {
                'name': 'duration'
            },
            {
                'name': 'enrollmentType'
            },
            {
                'name': 'enterpriseObjectId'
            },
            {
                'name': 'oneTimeOnly'
            },
            {
                'name': 'provisioningExtras'
            },
            {
                'name': 'userObjectId'
            },
            {
                'name': 'zeroTouch'
            },
        ]
    },
    '/google-emm/enterprises-POST': {
        'parameters': [
            {
                'name': 'enrollmentToken'
            },
            {
                'name': 'signupUrlName'
            },
        ]
    },
    '/google-emm/enterprises/{enterpriseObjectId}/enrollment-tokens-POST': {
        'parameters': [
            {
                'name': 'enterpriseObjectId'
            },
            {
                'name': 'allowPersonalUsage'
            },
            {
                'name': 'createdWhere'
            },
            {
                'name': 'displayName'
            },
            {
                'name': 'duration'
            },
            {
                'name': 'enrollmentType'
            },
            {
                'name': 'oneTimeOnly'
            },
            {
                'name': 'provisioningExtras'
            },
            {
                'name': 'userObjectId'
            },
            {
                'name': 'zeroTouch'
            },
        ]
    },
    '/google-emm/web-tokens-POST': {
        'parameters': [
            {
                'name': 'enterpriseObjectId'
            },
            {
                'name': 'iframeFeature'
            },
            {
                'name': 'parentFrameUrl'
            },
        ]
    },
    '/google-emm/enterprises/{enterpriseId}/enrollment-tokens/{tokenId}-DELETE': {
        'parameters': [
            {
                'name': 'enterpriseId'
            },
            {
                'name': 'tokenId'
            },
        ]
    },
    '/google-emm/enterprises/{enterpriseId}-DELETE': {
        'parameters': [
            {
                'name': 'enterpriseId'
            },
        ]
    },
    '/google-emm/devices/{deviceId}/erase-device-POST': {
        'parameters': [
            {
                'name': 'deviceId'
            },
        ]
    },
    '/google-emm/enterprises/{enterpriseId}/connection-status-GET': {
        'parameters': [
            {
                'name': 'enterpriseId'
            },
        ]
    },
    '/google-emm/devices/{deviceId}-GET': {
        'parameters': [
            {
                'name': 'deviceId'
            },
        ]
    },
    '/google-emm/devices/{deviceId}/policy_results-GET': {
        'parameters': [
            {
                'name': 'deviceId'
            },
        ]
    },
    '/google-emm/enterprises/{enterpriseObjectId}/devices-GET': {
        'parameters': [
            {
                'name': 'enterpriseObjectId'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/google-emm/enterprises/{enterpriseObjectId}/enrollment-tokens-GET': {
        'parameters': [
            {
                'name': 'enterpriseObjectId'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/google-emm/enterprises-GET': {
        'parameters': [
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/google-emm/devices/{deviceId}/lock-POST': {
        'parameters': [
            {
                'name': 'deviceId'
            },
        ]
    },
    '/google-emm/enterprises/{enterpriseId}-PATCH': {
        'parameters': [
            {
                'name': 'enterpriseId'
            },
            {
                'name': 'allowDeviceEnrollment'
            },
            {
                'name': 'deviceGroupId'
            },
        ]
    },
    '/google-emm/devices/{deviceId}/reboot-POST': {
        'parameters': [
            {
                'name': 'deviceId'
            },
        ]
    },
    '/google-emm/devices/{deviceId}/resetpassword-POST': {
        'parameters': [
            {
                'name': 'deviceId'
            },
            {
                'name': 'flags'
            },
            {
                'name': 'newPassword'
            },
        ]
    },
    '/activedirectories/{activedirectory_id}/associations-GET': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories/{activedirectory_id}/associations-POST': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/activedirectories/{activedirectory_id}/users-GET': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/activedirectories/{activedirectory_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'activedirectory_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/applications/{application_id}/associations-GET': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applications/{application_id}/associations-POST': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/applications/{application_id}/users-GET': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/applications/{application_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/commands/{command_id}/associations-GET': {
        'parameters': [
            {
                'name': 'command_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/commands/{command_id}/associations-POST': {
        'parameters': [
            {
                'name': 'command_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/commands/{command_id}/systems-GET': {
        'parameters': [
            {
                'name': 'command_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/commands/{command_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'command_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/gsuites/{gsuite_id}/associations-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/gsuites/{gsuite_id}/associations-POST': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/gsuites/{gsuite_id}/users-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/gsuites/{gsuite_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'gsuite_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/identity-provider/policies/{idp_routing_policy_id}/associations-GET': {
        'parameters': [
            {
                'name': 'idp_routing_policy_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/identity-provider/policies/{idp_routing_policy_id}/associations-POST': {
        'parameters': [
            {
                'name': 'idp_routing_policy_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/identity-provider/policies/{idp_routing_policy_id}/associations/users-GET': {
        'parameters': [
            {
                'name': 'idp_routing_policy_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/identity-provider/policies/{idp_routing_policy_id}/associations/usergroups-GET': {
        'parameters': [
            {
                'name': 'idp_routing_policy_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/associations-GET': {
        'parameters': [
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/associations-POST': {
        'parameters': [
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/users-GET': {
        'parameters': [
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/office365s/{office365_id}/associations-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/office365s/{office365_id}/associations-POST': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/office365s/{office365_id}/users-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/office365s/{office365_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policies/{policy_id}/associations-GET': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policies/{policy_id}/associations-POST': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/associations-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/associations-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/members-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/members-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/membership-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/systems-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policygroups/{group_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policies/{policy_id}/memberof-GET': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policies/{policy_id}/systems-GET': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policies/{policy_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/radiusservers/{radiusserver_id}/associations-GET': {
        'parameters': [
            {
                'name': 'radiusserver_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/radiusservers/{radiusserver_id}/associations-POST': {
        'parameters': [
            {
                'name': 'radiusserver_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/radiusservers/{radiusserver_id}/users-GET': {
        'parameters': [
            {
                'name': 'radiusserver_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/radiusservers/{radiusserver_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'radiusserver_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/softwareapps/{software_app_id}/associations-GET': {
        'parameters': [
            {
                'name': 'software_app_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/softwareapps/{software_app_id}/associations-POST': {
        'parameters': [
            {
                'name': 'software_app_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/softwareapps/{software_app_id}/systems-GET': {
        'parameters': [
            {
                'name': 'software_app_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/softwareapps/{software_app_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'software_app_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systems/{system_id}/associations-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systems/{system_id}/associations-POST': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/associations-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/associations-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/members-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/members-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/membership-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/commands-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'details'
            },
        ]
    },
    '/systemgroups/{group_id}/policies-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systemgroups/{group_id}/policygroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systemgroups/{group_id}/users-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systemgroups/{group_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systems/{system_id}/memberof-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systems/{system_id}/commands-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'details'
            },
        ]
    },
    '/systems/{system_id}/policies-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systems/{system_id}/policygroups-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systems/{system_id}/users-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systems/{system_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systems/{system_id}/policystatuses-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/users/{user_id}/associations-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/users/{user_id}/associations-POST': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/associations-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/associations-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/members-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/members-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/membership-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/activedirectories-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/applications-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/directories-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/gsuites-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/ldapservers-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/office365s-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/radiusservers-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/systems-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/memberof-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/users/{user_id}/activedirectories-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/users/{user_id}/applications-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/directories-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/gsuites-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/ldapservers-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/office365s-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/radiusservers-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/systems-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/groups-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'x-unfiltered-total-count'
            },
        ]
    },
    '/iplists/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/iplists/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/iplists-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'x-total-count'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/iplists/{id}-PATCH': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'description'
            },
            {
                'name': 'ips'
            },
            {
                'name': 'name'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/iplists-POST': {
        'parameters': [
            {
                'name': 'description'
            },
            {
                'name': 'ips'
            },
            {
                'name': 'name'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/iplists/{id}-PUT': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'description'
            },
            {
                'name': 'ips'
            },
            {
                'name': 'name'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/identity-provider/policies/{idp_routing_policy_id}/associations-GET': {
        'parameters': [
            {
                'name': 'idp_routing_policy_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/identity-provider/policies/{idp_routing_policy_id}/associations-POST': {
        'parameters': [
            {
                'name': 'idp_routing_policy_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/identity-provider/policies/{idp_routing_policy_id}/associations/users-GET': {
        'parameters': [
            {
                'name': 'idp_routing_policy_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/identity-provider/policies/{idp_routing_policy_id}/associations/usergroups-GET': {
        'parameters': [
            {
                'name': 'idp_routing_policy_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/applications/{application_id}/logo-DELETE': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/accessrequests-POST': {
        'parameters': [
            {
                'name': 'operationId'
            },
            {
                'name': 'additionalAttributes'
            },
            {
                'name': 'applicationIntId'
            },
            {
                'name': 'expiry'
            },
            {
                'name': 'organizationObjectId'
            },
            {
                'name': 'remarks'
            },
            {
                'name': 'requestorId'
            },
            {
                'name': 'resourceId'
            },
            {
                'name': 'resourceType'
            },
        ]
    },
    '/accessrequests/{accessId}-GET': {
        'parameters': [
            {
                'name': 'accessId'
            },
        ]
    },
    '/accessrequests/{accessId}/revoke-POST': {
        'parameters': [
            {
                'name': 'accessId'
            },
        ]
    },
    '/accessrequests/{accessId}-PUT': {
        'parameters': [
            {
                'name': 'accessId'
            },
            {
                'name': 'additionalAttributes'
            },
            {
                'name': 'expiry'
            },
            {
                'name': 'organizationObjectId'
            },
            {
                'name': 'remarks'
            },
        ]
    },
    '/ldapservers/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/associations-GET': {
        'parameters': [
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/associations-POST': {
        'parameters': [
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/users-GET': {
        'parameters': [
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/ldapservers-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/ldapservers/{id}-PATCH': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'userLockoutAction'
            },
            {
                'name': 'userPasswordExpirationAction'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/logos/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/cases/metadata-GET': {
        'parameters': [
        ]
    },
    '/administrators/{id}/organizationlinks-POST': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'organization'
            },
        ]
    },
    '/providers/{provider_id}/organizations-POST': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'maxSystemUsers'
            },
            {
                'name': 'name'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates/{id}-DELETE': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates/{id}-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/providers/{provider_id}/configuredpolicytemplates/{id}-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/providers/{provider_id}-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'fields'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/providers/{provider_id}/administrators-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'sortIgnoreCase'
            },
        ]
    },
    '/administrators/{id}/organizationlinks-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/organizations/{id}/administratorlinks-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/providers/{provider_id}/configuredpolicytemplates-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates/{id}/members-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/providers/{provider_id}/organizations-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'sortIgnoreCase'
            },
        ]
    },
    '/providers/{provider_id}/administrators-POST': {
        'parameters': [
            {
                'name': 'email'
            },
            {
                'name': 'provider_id'
            },
            {
                'name': 'apiKeyAllowed'
            },
            {
                'name': 'bindNoOrgs'
            },
            {
                'name': 'enableMultiFactor'
            },
            {
                'name': 'firstname'
            },
            {
                'name': 'lastname'
            },
            {
                'name': 'role'
            },
            {
                'name': 'roleName'
            },
        ]
    },
    '/providers/{provider_id}/cases-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/administrators/{administrator_id}/organizationlinks/{id}-DELETE': {
        'parameters': [
            {
                'name': 'administrator_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/providers/{provider_id}/invoices/{ID}-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'ID'
            },
        ]
    },
    '/providers/{provider_id}/invoices-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/providers/{provider_id}/organizations/{id}-PUT': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'maxSystemUsers'
            },
            {
                'name': 'name'
            },
        ]
    },
    '/microsoft-mdm/configuration-files-POST': {
        'parameters': [
        ]
    },
    '/office365s/{office365_id}/domains/{domain_id}-DELETE': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'domain_id'
            },
        ]
    },
    '/office365s/{office365_id}-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/office365s/{office365_id}/domains-POST': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'domain'
            },
        ]
    },
    '/office365s/{office365_id}/domains-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/office365s/{office365_id}/import/users-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'ConsistencyLevel'
            },
            {
                'name': 'top'
            },
            {
                'name': 'skipToken'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'search'
            },
            {
                'name': 'orderby'
            },
            {
                'name': 'count'
            },
        ]
    },
    '/office365s/{office365_id}/associations-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/office365s/{office365_id}/associations-POST': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/office365s/{office365_id}/translationrules/{id}-DELETE': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/office365s/{office365_id}/translationrules/{id}-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/office365s/{office365_id}/translationrules-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/office365s/{office365_id}/translationrules-POST': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'builtIn'
            },
            {
                'name': 'direction'
            },
        ]
    },
    '/office365s/{office365_id}/users-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/office365s/{office365_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/office365s/{office365_id}-PATCH': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'defaultDomain'
            },
            {
                'name': 'groupsEnabled'
            },
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'userLockoutAction'
            },
            {
                'name': 'userPasswordExpirationAction'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/office365s/{office365_id}/import/users-GET': {
        'parameters': [
            {
                'name': 'office365_id'
            },
            {
                'name': 'ConsistencyLevel'
            },
            {
                'name': 'top'
            },
            {
                'name': 'skipToken'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'search'
            },
            {
                'name': 'orderby'
            },
            {
                'name': 'count'
            },
        ]
    },
    '/administrators/{id}/organizationlinks-POST': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'organization'
            },
        ]
    },
    '/administrators/{id}/organizationlinks-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/organizations/{id}/administratorlinks-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/organizations/cases-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/administrators/{administrator_id}/organizationlinks/{id}-DELETE': {
        'parameters': [
            {
                'name': 'administrator_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/passwordmanager/devices/{UUID}-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/passwordmanager/devices-GET': {
        'parameters': [
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policies/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policies/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policyresults/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policytemplates/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policies-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policies/{policy_id}/policyresults-GET': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/policytemplates-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policyresults-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/policies/{policy_id}/policystatuses-GET': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policies/{policy_id}/associations-GET': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policies/{policy_id}/associations-POST': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policies/{policy_id}/memberof-GET': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policies/{policy_id}/systems-GET': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policies/{policy_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'policy_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policies-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'template'
            },
            {
                'name': 'notes'
            },
            {
                'name': 'values'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policies/{id}-PUT': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'id'
            },
            {
                'name': 'notes'
            },
            {
                'name': 'values'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systems/{system_id}/policystatuses-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/associations-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/associations-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/systems-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policygroups/{group_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policygroups/{group_id}/members-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/members-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/membership-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates/{id}-DELETE': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates/{id}-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/providers/{provider_id}/configuredpolicytemplates/{id}-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/providers/{provider_id}/configuredpolicytemplates-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates/{id}/members-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policygroups-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/associations-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/associations-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/members-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/members-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/membership-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policygroups/{group_id}/systems-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policygroups/{group_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/policygroups/{id}-PUT': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policytemplates/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/policytemplates-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/cases/metadata-GET': {
        'parameters': [
        ]
    },
    '/providers/{provider_id}/integrations/autotask-POST': {
        'parameters': [
            {
                'name': 'secret'
            },
            {
                'name': 'username'
            },
            {
                'name': 'provider_id'
            },
        ]
    },
    '/providers/{provider_id}/integrations/connectwise-POST': {
        'parameters': [
            {
                'name': 'companyId'
            },
            {
                'name': 'privateKey'
            },
            {
                'name': 'publicKey'
            },
            {
                'name': 'url'
            },
            {
                'name': 'provider_id'
            },
        ]
    },
    '/providers/{provider_id}/integrations/syncro-POST': {
        'parameters': [
            {
                'name': 'apiToken'
            },
            {
                'name': 'subdomain'
            },
            {
                'name': 'provider_id'
            },
        ]
    },
    '/providers/{provider_id}/organizations-POST': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'maxSystemUsers'
            },
            {
                'name': 'name'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates/{id}-DELETE': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/integrations/autotask/{UUID}-DELETE': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/integrations/connectwise/{UUID}-DELETE': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/integrations/syncro/{UUID}-DELETE': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates/{id}-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/integrations/autotask/{UUID}-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/integrations/connectwise/{UUID}-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/integrations/syncro/{UUID}-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/providers/{provider_id}/configuredpolicytemplates/{id}-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/providers/{provider_id}/billing/contract-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
        ]
    },
    '/providers/{provider_id}/billing/details-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
        ]
    },
    '/providers/{provider_id}-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'fields'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/providers/{provider_id}/administrators-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'sortIgnoreCase'
            },
        ]
    },
    '/providers/{provider_id}/configuredpolicytemplates-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/providers/{provider_id}/policygrouptemplates/{id}/members-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/providers/{provider_id}/organizations-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'sortIgnoreCase'
            },
        ]
    },
    '/integrations/autotask/{UUID}/mappings-PATCH': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'data'
            },
        ]
    },
    '/integrations/connectwise/{UUID}/mappings-PATCH': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'data'
            },
        ]
    },
    '/integrations/syncro/{UUID}/mappings-PATCH': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'data'
            },
        ]
    },
    '/integrations/autotask/{UUID}/settings-PATCH': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'automaticTicketing'
            },
            {
                'name': 'companyTypeIds'
            },
        ]
    },
    '/integrations/connectwise/{UUID}/settings-PATCH': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'automaticTicketing'
            },
            {
                'name': 'companyTypeIds'
            },
        ]
    },
    '/integrations/syncro/{UUID}/settings-PATCH': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'automaticTicketing'
            },
        ]
    },
    '/providers/{provider_id}/administrators-POST': {
        'parameters': [
            {
                'name': 'email'
            },
            {
                'name': 'provider_id'
            },
            {
                'name': 'apiKeyAllowed'
            },
            {
                'name': 'bindNoOrgs'
            },
            {
                'name': 'enableMultiFactor'
            },
            {
                'name': 'firstname'
            },
            {
                'name': 'lastname'
            },
            {
                'name': 'role'
            },
            {
                'name': 'roleName'
            },
        ]
    },
    '/providers/{provider_id}/cases-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/providers/{provider_id}/administrators/{id}-DELETE': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/integrations/connectwise/{UUID}/agreements/{agreement_ID}/additions-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'agreement_ID'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/integrations/connectwise/{UUID}/agreements-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/providers/{provider_id}/integrations/ticketing/alerts-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
        ]
    },
    '/providers/{provider_id}/integrations/autotask/alerts/configuration/options-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
        ]
    },
    '/providers/{provider_id}/integrations/connectwise/alerts/configuration/options-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
        ]
    },
    '/providers/{provider_id}/integrations/syncro/alerts/configuration/options-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
        ]
    },
    '/providers/{provider_id}/integrations/autotask/alerts/configuration-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
        ]
    },
    '/providers/{provider_id}/integrations/connectwise/alerts/configuration-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
        ]
    },
    '/providers/{provider_id}/integrations/syncro/alerts/configuration-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
        ]
    },
    '/integrations/syncro/{UUID}/billing_mapping_configuration_options-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/integrations/autotask/{UUID}/companies-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/integrations/connectwise/{UUID}/companies-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/integrations/syncro/{UUID}/companies-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/integrations/autotask/{UUID}/companytypes-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/integrations/connectwise/{UUID}/companytypes-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/integrations/autotask/{UUID}/contracts-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/integrations/autotask/{UUID}/contracts/fields-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/providers/{provider_id}/integrations-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/providers/{provider_id}/invoices/{ID}-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'ID'
            },
        ]
    },
    '/providers/{provider_id}/invoices-GET': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/integrations/autotask/{UUID}/mappings-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/integrations/connectwise/{UUID}/mappings-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/integrations/syncro/{UUID}/mappings-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/integrations/autotask/{UUID}/contracts/services-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/integrations/autotask/{UUID}/settings-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/integrations/connectwise/{UUID}/settings-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/integrations/syncro/{UUID}/settings-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
        ]
    },
    '/integrations/{integration_type}/{UUID}/errors-GET': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'integration_type'
            },
        ]
    },
    '/providers/{provider_id}/integrations/autotask/alerts/{alert_UUID}/configuration-PUT': {
        'parameters': [
            {
                'name': 'destination'
            },
            {
                'name': 'dueDays'
            },
            {
                'name': 'priority'
            },
            {
                'name': 'shouldCreateTickets'
            },
            {
                'name': 'status'
            },
            {
                'name': 'provider_id'
            },
            {
                'name': 'alert_UUID'
            },
            {
                'name': 'queue'
            },
            {
                'name': 'resource'
            },
            {
                'name': 'source'
            },
        ]
    },
    '/providers/{provider_id}/integrations/connectwise/alerts/{alert_UUID}/configuration-PUT': {
        'parameters': [
            {
                'name': 'shouldCreateTickets'
            },
            {
                'name': 'provider_id'
            },
            {
                'name': 'alert_UUID'
            },
            {
                'name': 'dueDays'
            },
            {
                'name': 'priority'
            },
            {
                'name': 'source'
            },
        ]
    },
    '/providers/{provider_id}/integrations/syncro/alerts/{alert_UUID}/configuration-PUT': {
        'parameters': [
            {
                'name': 'problemType'
            },
            {
                'name': 'shouldCreateTickets'
            },
            {
                'name': 'provider_id'
            },
            {
                'name': 'alert_UUID'
            },
            {
                'name': 'dueDays'
            },
            {
                'name': 'priority'
            },
            {
                'name': 'status'
            },
            {
                'name': 'userId'
            },
            {
                'name': 'username'
            },
        ]
    },
    '/integrations/autotask/{UUID}-PATCH': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'secret'
            },
            {
                'name': 'username'
            },
        ]
    },
    '/integrations/connectwise/{UUID}-PATCH': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'companyId'
            },
            {
                'name': 'privateKey'
            },
            {
                'name': 'publicKey'
            },
            {
                'name': 'url'
            },
        ]
    },
    '/integrations/syncro/{UUID}-PATCH': {
        'parameters': [
            {
                'name': 'UUID'
            },
            {
                'name': 'apiToken'
            },
            {
                'name': 'subdomain'
            },
        ]
    },
    '/providers/{provider_id}/organizations/{id}-PUT': {
        'parameters': [
            {
                'name': 'provider_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'maxSystemUsers'
            },
            {
                'name': 'name'
            },
        ]
    },
    '/pushendpoints/verifications/{verificationId}-GET': {
        'parameters': [
            {
                'name': 'verificationId'
            },
        ]
    },
    '/users/{userId}/pushendpoints/{pushEndpointId}/verify-POST': {
        'parameters': [
            {
                'name': 'userId'
            },
            {
                'name': 'pushEndpointId'
            },
            {
                'name': 'message'
            },
        ]
    },
    '/radiusservers/{radiusserver_id}/associations-GET': {
        'parameters': [
            {
                'name': 'radiusserver_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/radiusservers/{radiusserver_id}/associations-POST': {
        'parameters': [
            {
                'name': 'radiusserver_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/radiusservers/{radiusserver_id}/users-GET': {
        'parameters': [
            {
                'name': 'radiusserver_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/radiusservers/{radiusserver_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'radiusserver_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/applications/{application_id}/import/users-GET': {
        'parameters': [
            {
                'name': 'application_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'query'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'sortOrder'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/sambadomains/{id}-DELETE': {
        'parameters': [
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/sambadomains/{id}-GET': {
        'parameters': [
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/sambadomains-GET': {
        'parameters': [
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/sambadomains-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'sid'
            },
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/ldapservers/{ldapserver_id}/sambadomains/{id}-PUT': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'sid'
            },
            {
                'name': 'ldapserver_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/softwareapps/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/softwareapps/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/softwareapps-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/softwareapps/{software_app_id}/statuses-GET': {
        'parameters': [
            {
                'name': 'software_app_id'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/softwareapps-POST': {
        'parameters': [
            {
                'name': 'displayName'
            },
            {
                'name': 'id'
            },
            {
                'name': 'settings'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/softwareapps/{software_app_id}/reclaim-licenses-POST': {
        'parameters': [
            {
                'name': 'software_app_id'
            },
        ]
    },
    '/softwareapps/{software_app_id}/retry-installation-POST': {
        'parameters': [
            {
                'name': 'software_app_id'
            },
        ]
    },
    '/softwareapps/{software_app_id}/associations-GET': {
        'parameters': [
            {
                'name': 'software_app_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/softwareapps/{software_app_id}/associations-POST': {
        'parameters': [
            {
                'name': 'software_app_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/softwareapps/{software_app_id}/systems-GET': {
        'parameters': [
            {
                'name': 'software_app_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/softwareapps/{software_app_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'software_app_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/softwareapps/{id}-PUT': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'displayName'
            },
            {
                'name': 'id'
            },
            {
                'name': 'settings'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/softwareapps/validate-POST': {
        'parameters': [
            {
                'name': 'url'
            },
        ]
    },
    '/subscriptions-GET': {
        'parameters': [
        ]
    },
    '/systemgroups/{group_id}/associations-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/associations-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/commands-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'details'
            },
        ]
    },
    '/systemgroups/{group_id}/policies-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systemgroups/{group_id}/policygroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systemgroups/{group_id}/users-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systemgroups/{group_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systemgroups/{group_id}/members-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/members-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/membership-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/suggestions-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'object_ids'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'description'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'email'
            },
            {
                'name': 'memberQuery'
            },
            {
                'name': 'memberQueryExemptions'
            },
            {
                'name': 'memberSuggestionsNotify'
            },
            {
                'name': 'membershipMethod'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/suggestions-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/systemgroups/{group_id}/associations-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/associations-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/members-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/members-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/membership-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{group_id}/policies-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systemgroups/{group_id}/policygroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systemgroups/{group_id}/users-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systemgroups/{group_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systemgroups/{id}-PUT': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'id'
            },
            {
                'name': 'description'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'email'
            },
            {
                'name': 'memberQuery'
            },
            {
                'name': 'memberQueryExemptions'
            },
            {
                'name': 'memberSuggestionsNotify'
            },
            {
                'name': 'membershipMethod'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systemgroups/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systeminsights/chassis_info-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/disk_info-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/ie_extensions-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/kernel_info-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/os_version-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/sip_config-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/system_info-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/tpm_info-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/user_groups-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/alf-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/alf_exceptions-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/alf_explicit_auths-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/appcompat_shims-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/apps-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/authorized_keys-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/azure_instance_metadata-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/azure_instance_tags-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/battery-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/bitlocker_info-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/browser_plugins-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/certificates-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/chrome_extensions-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/connectivity-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/crashes-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/cups_destinations-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/disk_encryption-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/dns_resolvers-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/etc_hosts-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/firefox_addons-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/groups-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/interface_addresses-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/interface_details-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/launchd-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/linux_packages-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/logged_in_users-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/logical_drives-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/managed_policies-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/mounts-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/patches-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/programs-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/python_packages-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/safari_extensions-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/scheduled_tasks-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/secureboot-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/services-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/shadow-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/shared_folders-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/shared_resources-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/sharing_preferences-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/startup_items-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/system_controls-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/uptime-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/usb_devices-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/userassist-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/user_ssh_keys-GET': {
        'parameters': [
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/users-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/wifi_networks-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/wifi_status-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/windows_security_center-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systeminsights/windows_security_products-GET': {
        'parameters': [
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/systems/{system_id}/fdekey-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systems/{system_id}/softwareappstatuses-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/systems/{system_id}/associations-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systems/{system_id}/associations-POST': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systems/{system_id}/memberof-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systems/{system_id}/commands-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'details'
            },
        ]
    },
    '/systems/{system_id}/policies-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systems/{system_id}/policygroups-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systems/{system_id}/users-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/systems/{system_id}/usergroups-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'Date'
            },
            {
                'name': 'Authorization'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/devices/settings/defaultpasswordsync-GET': {
        'parameters': [
            {
                'name': 'organizationObjectId'
            },
        ]
    },
    '/devices/settings/signinwithjumpcloud-GET': {
        'parameters': [
            {
                'name': 'organizationObjectId'
            },
        ]
    },
    '/devices/settings/defaultpasswordsync-PUT': {
        'parameters': [
            {
                'name': 'enabled'
            },
            {
                'name': 'organizationObjectId'
            },
        ]
    },
    '/devices/settings/signinwithjumpcloud-PUT': {
        'parameters': [
            {
                'name': 'organizationObjectId'
            },
            {
                'name': 'settings'
            },
        ]
    },
    '/usergroups/{group_id}/associations-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/associations-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/activedirectories-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/applications-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/directories-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/gsuites-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/ldapservers-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/office365s-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/radiusservers-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/systems-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/members-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/members-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/membership-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/suggestions-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'user_ids'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'description'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'email'
            },
            {
                'name': 'memberQuery'
            },
            {
                'name': 'memberQueryExemptions'
            },
            {
                'name': 'memberSuggestionsNotify'
            },
            {
                'name': 'membershipMethod'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/suggestions-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/usergroups-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{id}-PUT': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'id'
            },
            {
                'name': 'description'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'email'
            },
            {
                'name': 'memberQuery'
            },
            {
                'name': 'memberQueryExemptions'
            },
            {
                'name': 'memberSuggestionsNotify'
            },
            {
                'name': 'membershipMethod'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/associations-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/associations-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/members-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/members-POST': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/membership-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/usergroups/{group_id}/activedirectories-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/applications-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/directories-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/gsuites-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/ldapservers-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/office365s-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/radiusservers-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/systems-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/usergroups/{group_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'group_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/pushendpoints/{push_endpoint_id}-DELETE': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'push_endpoint_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/users/{user_id}/pushendpoints/{push_endpoint_id}-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'push_endpoint_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/users/{user_id}/pushendpoints-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/users/{user_id}/pushendpoints/{push_endpoint_id}-PATCH': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'push_endpoint_id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'state'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/users/{user_id}/associations-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'targets'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/users/{user_id}/associations-POST': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'id'
            },
            {
                'name': 'op'
            },
            {
                'name': 'attributes'
            },
            {
                'name': 'type'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/users/{user_id}/memberof-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/users/{user_id}/activedirectories-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
        ]
    },
    '/users/{user_id}/applications-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/directories-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/gsuites-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/ldapservers-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/office365s-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/radiusservers-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/systems-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/users/{user_id}/systemgroups-GET': {
        'parameters': [
            {
                'name': 'user_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'x-org-id'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/workdays/{workday_id}/auth-POST': {
        'parameters': [
            {
                'name': 'workday_id'
            },
            {
                'name': 'auth'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/workdays/{workday_id}/auth-DELETE': {
        'parameters': [
            {
                'name': 'workday_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/workdays/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/workdays/{workday_id}/import-POST': {
        'parameters': [
            {
                'name': 'workday_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/workdays/{id}/import/{job_id}/results-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'job_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/workdays-GET': {
        'parameters': [
            {
                'name': 'fields'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/workdays-POST': {
        'parameters': [
            {
                'name': 'auth'
            },
            {
                'name': 'name'
            },
            {
                'name': 'reportUrl'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/workdays/{id}-PUT': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'name'
            },
            {
                'name': 'reportUrl'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/workdays/{workday_id}/workers-GET': {
        'parameters': [
            {
                'name': 'workday_id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'skip'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
    '/systems/{system_id}/fdekey-GET': {
        'parameters': [
            {
                'name': 'system_id'
            },
            {
                'name': 'x-org-id'
            },
        ]
    },
};