from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lex as lex,
    RemovalPolicy,
)


class LexStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # role
        lex_role = iam.Role(
            self,
            "LexRole",
            assumed_by=iam.ServicePrincipal("lexv2.amazonaws.com"),
            description="Role for the lex bot",
        )

        lex_role.apply_removal_policy(RemovalPolicy.DESTROY)

        # Slot values
        lilies = lex.CfnBot.SlotTypeValueProperty(sample_value="lilies")
        roses = lex.CfnBot.SlotTypeValueProperty(sample_value="roses")
        tulips = lex.CfnBot.SlotTypeValueProperty(sample_value="tulips")

        # slot type
        flower_type = lex.CfnBot.SlotTypeProperty(
            name="FlowerTypes",
            description="the type of flowers",
            slot_type_values=[lilies, roses, tulips],
            value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                resolution_strategy="OriginalValue"
            ),
        )

        # localeProperty
        en_us_locale = lex.CfnBot.BotLocaleProperty(
            locale_id="en_US",
            nlu_confidence_threshold=0.4,
            description="English Locale",
            voice_settings=lex.CfnBot.VoiceSettingsProperty(voice_id="Ivy"),
            slot_types=[flower_type],
        )

        # Lex bot
        lex_bot = lex.CfnBot(
            self,
            "MyLexBot",
            data_privacy={"ChildDirected": False},
            idle_session_ttl_in_seconds=123,
            name="FirstLexBot",
            role_arn=lex_role.role_arn,
            auto_build_bot_locales=False,
            bot_locales=[],
        )

        lex_bot.apply_removal_policy(RemovalPolicy.DESTROY)
