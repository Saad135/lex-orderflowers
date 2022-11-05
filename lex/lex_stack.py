from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lex as lex,
)


class LexStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lex bot draft 1
        cfn_bot = lex.CfnBot(
            self,
            "MyLexBot",
            data_privacy={"ChildDirected": False},
            idle_session_ttl_in_seconds=123,
            name="FirstLexBot",
            role_arn="role_arn",
        )
