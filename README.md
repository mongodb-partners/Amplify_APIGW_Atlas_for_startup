# Microservice Application with API Architecture for Startups

This is a reference architecture for API-based applications with AWS Amplify , MongoDB Atlas, APIGW, and Lambda

## [MongoDB Atlas](https://www.mongodb.com/atlas)

MongoDB Atlas is an all-purpose database having features like Document Model, Geo-spatial, TimeSeries, hybrid
deployment, and multi-cloud services.
It evolved as a "Developer Data Platform", intended to reduce the developer's workload on development and management of
the database environment.
It also provides a free tier to test out the application/database features.


## [AWS Amplify](https://aws.amazon.com/amplify/)

Amplify provides all the essentials for building full-stack web and mobile apps on AWS. Develop the frontend, incorporate features like authentication and storage, connect to real-time data sources, deploy, and scale to millions of users.

## [Amazon API Gateway](https://aws.amazon.com/api-gateway/)

Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor,
and secure APIs at any scale.

## [Amazon Cognito User pool](https://aws.amazon.com/pm/cognito)

Amazon Cognito User pool helps you to deliver frictionless customer identity and access management (CIAM) with a
cost-effective and customizable platform. Helps you to add security features such as adaptive authentication, support
compliance, and data residency requirements. It can scale to millions of users across devices with a fully managed,
high-performing, and reliable identity store.

## Reference Architecture

<img width="825" alt="image" src="https://github.com/mongodb-partners/Amplify_APIGW_Atlas_for_startup/assets/101570105/f3150d8d-001e-4c71-a8e7-f63dcc61d601">


## Sample output

<img width="1028" alt="image" src="https://github.com/mongodb-partners/Amplify_APIGW_Atlas_for_startup/assets/101570105/cf1ffe14-b46b-4fec-80cd-0080a3979840">

1.  ## Prerequisites

    This demo, instructions, scripts, and cloudformation template are designed to be run in `us-east-1`. With a few
    modifications, you can try it out in other regions as well. Make sure to change REGION_NAME in global_args.py if not
    using US-EAST-1

    - [Create a MongoDB Cloud account](https://www.mongodb.com/resources/products/platform/mongodb-atlas-tutorial#creating-a-mongodb-atlas-account) 
        
        
        Note: It is sufficient to setup only the MongoDB Cloud Account for now. During the course of this demo setup, we build the Project,Cluster and Database.


    - Create an [API Key in an Organization](https://www.mongodb.com/docs/atlas/configure-api-access/#create-an-api-key-in-an-organization) and grant project owner permission and open access (0.0.0.0/1) for this demo purpose. 

    Side Note: Please note this setting is not suitable for production environment and the access should be restricted based on your policies.

    - Get the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) Installed & Configured
    - Get the [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_install) Installed & Configured
    - Get the [AWS AMPLIFY](https://docs.amplify.aws/gen1/react/tools/cli/start/set-up-cli/) installed for ReactJS & Configured


    - Set up the Python virtual environment  

    - Python3 - `yum install -y python3`
    - Python Pip - `yum install -y python-pip`
    - Virtualenv - `pipx install virtualenv`

1.  ## Setting up the environment

    - Get the application code

      ```bash
      git clone https://github.com/mongodb-partners/Microservice_Application_with_MongoDBAtlas_AWSCDK_APIGW_Lambda.git
      cd aws_mongodb_sample_dir
      ```

1.  ## Prepare the dev environment to run AWS CDK

    We will use `cdk` to make our deployments easier. Let's go ahead and install the necessary components.
    Use the link to copy MongoDB Atlas Organization ID

    ```bash
    # You should have npm pre-installed
    # If you DONT have cdk installed
    npm install -g aws-cdk

    # Make sure you in root directory
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt

    cd aws_mongodb_sample
	pip install --target ./dependencies pymongo
	cd ..
    ```
    # Set Environment Variables

    Run the [AWS CloudFormation template](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import-new-stack.html) with the [profile-secret-role.yaml](https://github.com/mongodb-partners/Amplify_APIGW_Atlas_for_startup/blob/main/aws_mongodb_sample_dir/profile-secret-role.yaml) file. 
    
        1. This template creates a secreats in the AWS Secret Manager to store the following
        
        MonogDB Atlas Organization ID
        MongoDB Atlas Organization API credentials - Public Key and Private Key . Note this is created during the prerequisite.
        MongoDB Atlas Databse User Credentials - User Name and Password
        AWS Account ID

        2. The template also creates the role and permissions required to setup the MongoDB Atlas through AWS CDK

    Run the Python script mongodb_prep_setup.py to activate the Cloudformation registry - MongoDB (private) extensions with the appropriate role.


    set up the AWS environment variables

    ```bash       
    export AWS_ACCESS_KEY_ID="Enter the AWS Access Key"
    export AWS_SECRET_ACCESS_KEY="Enter the AWS Secret Access Key"
    export AWS_SESSION_TOKEN="Enter the AWS Session Token" 
     ```        

    Set up the Global parameter in [global_args.py](https://github.com/mongodb-partners/Amplify_APIGW_Atlas_for_startup/blob/main/aws_mongodb_sample_dir/global_args.py)


    Set up the AWS CDK Bootstrap and check the CDK stacks - **AwsMongodbAtlasCreateStack**  & **AwsMongodbSampleStack** - are listed.
    

    ```bash       
        cdk bootstrap
        cdk ls
     ``` 

1.  ## Deploying the application

    Let us walk through each of the stacks,

    - **Stack: AwsMongodbAtlasCreateStack**

        This stack will setup the MongoDB Projects, Cluster and Database. It will also setup the user access and network access to the database.
        
        **Side Note:** For this demo purpose the network access is set to 0.0.0.0/0. This is not recommended for production environments.

          
    - **Stack: AwsMongodbSampleStack**

      This stack will create

      a)    Secret for storing ATLAS DB URI

      b)    Cognito User Pool for API Authentication

      c)    Lambda function that will create a database , insert dummy data and return document count

      d)    API Gateway backed by the lambda function created above


      ```bash
      cdk deploy --all
      ```

After successfully deploying the stack, Check the `Outputs` section of the stack to verify all the resource are created successfully.


## **Setup the Cognito user to check the access to the API Gateway Endpoint**

Navigate to the Cognito user pool and copy the User Pool ID and Client ID (App Integration tab)  from the Cognito User pool

Open Cloud Shell and create a user with the command mentioned below

   	```aws cognito-idp admin-create-user --user-pool-id  <YOUR_USER_POOL_ID>  --username apigwtest```

Force the user login through a secured password.

    ```aws cognito-idp admin-set-user-password --user-pool-id <YOUR_USER_POOL_ID>  --username apigwtest  --password <PASSWORD> --permanent```

Replace the User Pool ID and Client ID copied in the above step and also replace the user name and password of the user
created above

 	```aws cognito-idp admin-initiate-auth --user-pool-id <YOUR_USER_POOL_ID> --client-id <CLIENT_ID>  --auth-flow ADMIN_NO_SRP_AUTH --auth-parameters USERNAME=apigwtest,PASSWORD=<PASSWORD>```

Copy the **Id Token** created from the above step and run the below command to test the API. Copy the API_GATEWAY_ENDPOINT
from the API Gateway console --> API Gateway: APIs: ApiGateway (xxxxxx) :Stages

 	curl --location --request GET 'https://<API_GATEWAY_ENDPOINT>.execute-api.us-east-1.amazonaws.com/dev' --header 'Content-Type: application/json' --header 'Authorization: <ID_TOKEN>'

## Creating the frontend application

Switch into the frontend project.

    cd aws_mongodb_sample/frontend

Add th URL you retrieved in the above test step to the TodoList.jsx script.

    const apiEndpoint = "https://XXXXXX.execute-api.us-east-1.amazonaws.com/dev/todos";

First, you need to initialize Amplify. You can keep the default settings for this.

    amplify init

Next, we need to add hosting to the project. Choose `Hosting with Amplify Console` and `Manual deployment`.

    amplify hosting add

Whenever you make changes:

    amplify push

Finally, we can publish the frontend.

    amplify publish

## **Clean up**

Use `cdk destroy --all` to clean up all the AWS CDK resources.

The Amplify backend and frontend needs to be cleaned up manually.


## Troubleshooting

Refer to [this link](https://github.com/mongodb/mongodbatlas-cloudformation-resources/tree/master#troubleshooting) to
resolve some common issues encountered when using AWS CloudFormation/CDK with MongoDB Atlas Resources.

## Useful commands

* `cdk ls`          lists all stacks in the app
* `cdk synth`       emits the synthesized CloudFormation template
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compares the deployed stack with the current state
* `cdk docs`        open CDK documentation

Enjoy!
