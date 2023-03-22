import os

from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_dynamodb as dynamodb,
)



from omegaconf import OmegaConf
from constructs import Construct


conf_parameters = OmegaConf.load("config/config.yaml")

class AutoEipRoute53BindingKarpenterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


         # create a DynamoDB table, with Parition key as EIP, DNS name and allocation_id(), and distributed_status
        table = dynamodb.Table(
            self, conf_parameters['dynamodb']['table'],
            partition_key=dynamodb.Attribute(
                name="EIP",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        ) 

         # create an IAM role for the Lambda function
        fn_role = iam.Role(
            self, "test_role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )

        # Please do modify it for your production environments
        fn_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))


        # create a Lambda function to handle the event, need pass Host_zone_id, EIP tagging, EC2 tag
        binding_fn = lambda_.Function(
            self, "MyFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="lambda_logic.lambda_handler",
            code=lambda_.Code.from_asset(os.path.join("./lambda/")),
            role=fn_role,
            environment={
                "eip_tags": conf_parameters['lambda']['eip_tag']['team'],
                "ec2_tags": conf_parameters['lambda']['ec2_tag']['team'],
                "host_zone_id": conf_parameters['route53']['host_zone_id'],
                "table_name": table.table_name,
                "suffix": conf_parameters['route53']['suffix']
            },
            timeout=Duration.seconds(60)
                    
        )

    
        
        # catch the instance running states via eventbridge default bus
        rule = events.Rule(
                self, "karpenter_detection",
                description="Trigger when an EC2 instance state changes",
                event_pattern=events.EventPattern(
                    source=["aws.ec2"],
                    detail_type=["EC2 Instance State-change Notification"],
                    detail={
                        "state": ["running"]
                    },
                ),
        )

        rule.add_target(targets.LambdaFunction(binding_fn))

        
        
        
