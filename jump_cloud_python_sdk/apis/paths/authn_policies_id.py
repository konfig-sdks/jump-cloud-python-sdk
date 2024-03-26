from jump_cloud_python_sdk.paths.authn_policies_id.get import ApiForget
from jump_cloud_python_sdk.paths.authn_policies_id.delete import ApiFordelete
from jump_cloud_python_sdk.paths.authn_policies_id.patch import ApiForpatch


class AuthnPoliciesId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
