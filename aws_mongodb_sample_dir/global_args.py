class GlobalArgs():
    """
    Helper to define global statics
    """

    OWNER = "AWS_STARTUP_ACTIVATE_DEMO"
    ENVIRONMENT = "production"
    REPO_NAME = "AWS_STARTUP_ACTIVATE_DEMO"
    SOURCE_INFO = f"https://"
    VERSION = "2023_07_11"
    SUPPORT_EMAIL = ["", ]

    #AWS PARAMETERS
    SECRET_NAME ="cfn/atlas/profile/default"
    
    # MONGODB_URL: MongoDB Atlas AWS CDK will create a MongoDB Cluster and will pass newly created mongodb url to AWS Glue job stack.
    # MONGODB_USER/MONGODB_PASSWORD: For MongoDB username and password, we are directly setting it in mongodb stack and glue_job stack.
    
    DATABASE_NAME = "apigw_lambda_atlas"
    AUTH_DATABASE_NAME = "admin"
    REGION_NAME = "US_EAST_1"
    AWS_REGION = "us-east-1"
    IP_ADDRESS = "0.0.0.0/1" # Use for development or testing purposes only
    IP_COMMENT = "AWS APIGW + Lambda calling MongoDB Atlas Demo"
    PROFILE = "default"

    INSTANCE_SIZE = "M0"
    EBS_VOLUME_TYPE = "STANDARD"
    BACKING_PROVIDER_NAME = "AWS"

      # Tag details
    TAG_OWNER = "owner"
    TAG_PURPOSE = "API Gateway demo with Lambda and Atlas"
    TAG_EXPIRE_ON = "2024-01-01"