from aws_cdk import (Stack,CfnOutput,Fn, aws_cloudformation as cfn, aws_iam as iam)

from constructs import Construct



from awscdk_resources_mongodbatlas import (AdvancedRegionConfig, AdvancedReplicationSpec, DatabaseUserProps,
                                           Specs, AccessListDefinition, IpAccessListProps,
                                           ProjectProps, ClusterProps, AtlasBasic,
                                           AdvancedRegionConfigProviderName)
from global_args import GlobalArgs
import boto3
import json
import base64
import importlib.util
import sys

# Validate if required modules are installed
required_modules = ['aws_cdk.aws_iam', 'aws_cdk.aws_cloudformation']
missing_modules = [module for module in required_modules if importlib.util.find_spec(module) is None]

if missing_modules:
    for module in missing_modules:
        print(f"Error: Module '{module}' not found. Please install the required modules using 'pip install {module}'")
    sys.exit(1)



def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name = GlobalArgs.AWS_REGION

    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    return json.loads(secret)

secret_name = GlobalArgs.SECRET_NAME
secrets = get_secret(secret_name)

secrets_username = secrets["MONGODBUSER"]
secrets_password = secrets["MONGODBPASSWORD"]
secrets_org_id = secrets["ATLASORGID"]
secrets_account_id = secrets["AWSACCOUNTID"]


class AwsMongodbAtlasCreateStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    org_id_var =  secrets_org_id
    region_var =  GlobalArgs.REGION_NAME
    profile_name_var = GlobalArgs.PROFILE
    ip_addr_var = GlobalArgs.IP_ADDRESS
    ip_comment_var = GlobalArgs.IP_COMMENT
    instanceSize = GlobalArgs.INSTANCE_SIZE
    ebsVolumeType = GlobalArgs.EBS_VOLUME_TYPE
    backingProviderName = GlobalArgs.BACKING_PROVIDER_NAME
    username = secrets_username
    password = secrets_password


#     # Define IAM Role for Atlas execution
#     atlas_execution_role = iam.Role(
#             self, "AtlasExecutionRole",
#             assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
#             description="Role for MongoDB Atlas execution",
#             role_name="atlas_execution_role"
#         )

# # Activate CloudFormation registry for private extension "MongoDB-Atlas-Cluster"
#     cfn.CfnTypeActivation(
#             self, "MongoDBAtlasClusterActivation",
#             product_name="MongoDB-Atlas-Cluster",
#             provisioning_artifact_id="2.1.0",  # Adjust the version as necessary
#             service_role=atlas_execution_role.role_arn
#       )

    region_configs_var = [
            AdvancedRegionConfig(analytics_specs=Specs(node_count=1, instance_size=instanceSize, ebs_volume_type=ebsVolumeType),
                                 electable_specs=Specs(node_count=3, instance_size=instanceSize, ebs_volume_type=ebsVolumeType),
                                 priority=7,
                                 provider_name=AdvancedRegionConfigProviderName.TENANT,
                                 backing_provider_name=backingProviderName,
                                 region_name=''.join(region_var))]
    replication_specs_var = [AdvancedReplicationSpec(advanced_region_configs=region_configs_var, num_shards=1)]

    access_list_defs_var = [AccessListDefinition(ip_address=''.join(ip_addr_var), comment=''.join(ip_comment_var))]

    self.atlas_basic_l3 = AtlasBasic(self, "AtlasBasic-py-l3",
                                    cluster_props=ClusterProps(
                                        replication_specs = replication_specs_var,
                                        name="aws-activate-startup-cluster"
                                    ),
                                    db_user_props=DatabaseUserProps(
                                        database_name=GlobalArgs.AUTH_DATABASE_NAME, 
                                        username=username,
                                        password=password
                                    ),
                                    project_props=ProjectProps(
                                        org_id = ''.join(org_id_var),
                                        name="aws-activate-startup-project"

                                    ),
                                    ip_access_list_props=IpAccessListProps(
                                        access_list = access_list_defs_var
                                    ),
                                    profile=''.join(profile_name_var)
                                )
    
    serveraddress = self.atlas_basic_l3.m_cluster.connection_strings.standard_srv
    
    CfnOutput(self,
                  f"serveradd",
                  description=f"Server Address",
                  value=self.atlas_basic_l3.m_cluster.connection_strings.standard_srv)
    
    self.clusteraddress = Fn.select(2, Fn.split('/', serveraddress))
                  
    self.Atlas_URI = f"mongodb+srv://" + username + ":" + password + "@" + self.clusteraddress
        
    # properties to share with other stacks
    @property
    def get_connection_string_srv(self):
        return self.Atlas_URI

    


