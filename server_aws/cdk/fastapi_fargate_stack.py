from aws_cdk import Stack
import os
from aws_cdk import Stack, CfnOutput
from constructs import Construct
from dotenv import load_dotenv

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecs_patterns as ecs_patterns
import aws_cdk.aws_iam as iam


load_dotenv()

ECR_REGISTRY = os.environ["ECR_REGISTRY"]
PORT = os.environ["PORT"]
ROLE_ARN = os.environ["ROLE_ARN"]


class FastApiFargateStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # (i) Create VPC
        vpc = ec2.Vpc(self, "pdfgptVPC", max_azs=2)

        # (ii) Create Fargate Cluster
        ecs_cluster = ecs.Cluster(
            self,
            "pdfgptECSCluster",
            vpc=vpc,
        )

        role = iam.Role.from_role_arn(self, "CDKFargateECSTaskRole", ROLE_ARN)

        image = ecs.ContainerImage.from_registry(ECR_REGISTRY)

        task_definition = ecs.FargateTaskDefinition(
            scope=self,
            id="pdfgptCDKFargateECSTask",
            execution_role=role,
            task_role=role,
            cpu=512,
            memory_limit_mib=2048,
        )

        port_mapping = ecs.PortMapping(
            container_port=int(PORT), host_port=int(PORT))
        task_definition.add_container(
            id="CDKFargateContainer",
            image=image,
            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_ecs/LogDriver.html
            logging=ecs.LogDrivers.aws_logs(stream_prefix='pdfgpt_container'),
        ).add_port_mappings(port_mapping)

        ecs_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "pdfgptFastAPIService",
            cluster=ecs_cluster,
            cpu=512,
            memory_limit_mib=2048,
            desired_count=1,
            task_definition=task_definition,
        )

        CfnOutput(
            self,
            "pdfgptCDKFargateLoadBalancerDNS",
            value=ecs_service.load_balancer.load_balancer_dns_name,
        )
