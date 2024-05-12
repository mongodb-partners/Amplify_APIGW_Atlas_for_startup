
import boto3

# Create an IAM client
iam = boto3.client('iam')

# Call the list_roles operation
response = iam.list_roles()

# Filter for the role name matching 'aws-startup-activate' and get the ARN
role_arn = next((role['Arn'] for role in response['Roles'] if 'aws-startup-activate' in role['RoleName']), None)

# Create a CloudFormation client
cf = boto3.client('cloudformation')

# Define the types
types = ["MongoDB::Atlas::Cluster", "MongoDB::Atlas::DatabaseUser", "MongoDB::Atlas::Project", "MongoDB::Atlas::ProjectIpAccessList"]

# Call the list_types operation
response = cf.list_types(Visibility='PRIVATE', Type='RESOURCE')

# Iterate over the types in the response
for type_info in response['TypeSummaries']:
    # If the type is in your list
    if type_info['TypeName'] in types:
        # Get the TypeName and PublisherId
        type_name = type_info['TypeName']
        publisher_id = type_info['PublisherId']

        # Run the aws cloudformation activate-type command
        try:
            response = cf.activate_type(
                TypeName=type_name,
                ExecutionRoleArn=role_arn,
                Type='RESOURCE',
                PublisherId=publisher_id,
                AutoUpdate=True
            )
            print(f"Activated type: {type_name}")
        except Exception as e:
            print(f"Failed to activate type: {type_name}. Error: {e}")