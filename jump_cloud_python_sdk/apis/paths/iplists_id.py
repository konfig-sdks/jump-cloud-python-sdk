from jump_cloud_python_sdk.paths.iplists_id.get import ApiForget
from jump_cloud_python_sdk.paths.iplists_id.put import ApiForput
from jump_cloud_python_sdk.paths.iplists_id.delete import ApiFordelete
from jump_cloud_python_sdk.paths.iplists_id.patch import ApiForpatch


class IplistsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
