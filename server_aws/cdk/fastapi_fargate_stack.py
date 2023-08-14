from aws_cdk import Stack
import os
from aws_cdk import Stack, CfnOutput, Duration
from constructs import Construct
from dotenv import load_dotenv

import aws_cdk.aws_route53 as route53
import aws_cdk.aws_certificatemanager as acm
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecs_patterns as ecs_patterns
import aws_cdk.aws_iam as iam


load_dotenv()

ECR_REGISTRY = os.environ["ECR_REGISTRY"]
PORT = os.environ["PORT"]
ROLE_ARN = os.environ["ROLE_ARN"]
domainName = 'api.gptlegal.net'
projectName = 'pdfgpt'


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

        # zone = route53.HostedZone(self, "HostedZone",
        #                           zone_name=domainName
        #                           )

        cert = acm.Certificate(self, "Certificate",
                               domain_name=domainName,
                               validation=acm.CertificateValidation.from_dns()
                               )

        ecs_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "pdfgptFastAPIService",
            cluster=ecs_cluster,
            cpu=512,
            memory_limit_mib=2048,
            desired_count=1,
            public_load_balancer=True,
            certificate=cert,
            redirect_http=True,  # internet says this is recommended but i haven't tried
            task_definition=task_definition,
        )

        ecs_service.target_group.configure_health_check(
            path="/health", interval=Duration.minutes(2))

        CfnOutput(
            self,
            "pdfgptCDKFargateLoadBalancerDNS",
            value=ecs_service.load_balancer.load_balancer_dns_name,
        )


# CREATING CERTIFICATE

# clientPrefix = 'pdfgpt'
# domainName = 'gptlegal.net'
# // previously created route 53 hosted zone
# const zone = route53.HostedZone.fromLookup(this, `${clientPrefix}-zone`, {
#   domainName: props.domain,
# });

# // SSL certificate for the domain
# const cert = new certificatemanager.Certificate(
#   this,
#   "certificate",
#   {
#     domainName: "example.com",
#     validation: certificatemanager.CertificateValidation.fromDns(zone),
#   }
# );


# ENABLE HTTPS IN LOAD BALANCER

# fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
#     self,
#     f"{id}-service",
#     cluster=cluster,
#     desired_count=mincount,
#     public_load_balancer=True,
#     protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTPS,
#     domain_name=fdomainName,
#     domain_zone=zone,
#     redirect_http=True,
#     task_definition=task_definition
# )
# fargate_service.target_group.configure_health_check(path="/healthcheck", interval=60)
