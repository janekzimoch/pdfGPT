from aws_cdk import App
from fastapi_fargate_stack import FastApiFargateStack

app = App()
FastApiFargateStack(app, "FastApiFargateStack")
app.synth()
