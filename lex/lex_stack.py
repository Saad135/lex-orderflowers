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

        # Sample Utterances
        utterance_flowers_a = lex.CfnBot.SampleUtteranceProperty(
            utterance="I would like to pick up flowers"
        )
        utterance_flowers_b = lex.CfnBot.SampleUtteranceProperty(
            utterance="I would like to order some flowers"
        )

        # Message group
        flower_confirm_group = lex.CfnBot.MessageGroupProperty(
            message=lex.CfnBot.MessageProperty(
                plain_text_message="Okay, your {FlowerType} will be ready for pickup by {PickupTime} on {PickupDate}.  Does this sound okay?"
            )
        )

        # Prompt specification
        flowers_accept = lex.CfnBot.PromptSpecificationProperty(
            message_groups_list=[flower_confirm_group],
            max_retries=3,
            allow_interrupt=False,
        )

        # Declination message group
        flower_decline_group = lex.CfnBot.MessageGroupProperty(
            message=lex.CfnBot.MessageProperty(
                plain_text_message="Okay, I will not place your order."
            )
        )

        # Declination response
        decline_flowers = lex.CfnBot.ResponseSpecificationProperty(
            message_groups_list=[flower_decline_group], allow_interrupt=False
        )

        # lex intent confirmation
        confirm_flowers = lex.CfnBot.IntentConfirmationSettingProperty(
            prompt_specification=flowers_accept, declination_response=decline_flowers
        )

        # Slot Priorities
        pickup_date_priority = lex.CfnBot.SlotPriorityProperty(
            priority=2, slot_name="PickupDate"
        )

        flower_type_priority = lex.CfnBot.SlotPriorityProperty(
            priority=1, slot_name="FlowerType"
        )

        pickup_time_priority = lex.CfnBot.SlotPriorityProperty(
            priority=3, slot_name="PickupTime"
        )

        # Flower slot group list
        flower_slot_group = lex.CfnBot.MessageGroupProperty(
            message=lex.CfnBot.MessageProperty(
                plain_text_message="What type of flowers would you like to order?"
            )
        )

        # Flower slot Prompt specification
        flowers_slot_promt = lex.CfnBot.PromptSpecificationProperty(
            message_groups_list=[flower_slot_group],
            max_retries=3,
            allow_interrupt=False,
        )

        # value elicitation setting for flower type slot
        flower_value_elicit = lex.CfnBot.SlotValueElicitationSettingProperty(
            slot_constraint="Required", prompt_specification=flowers_slot_promt
        )

        # Flower Type Slot Property
        flower_type_slot = lex.CfnBot.SlotProperty(
            name="FlowerType",
            description="slot for the flower type",
            slot_type_name="FlowerType",
            value_elicitation_setting=flower_type_slot,
        )

        # lex intent
        order_flower_intent = lex.CfnBot.IntentProperty(
            name="OrderFlowers",
            description="Intent to order a bouquet of flowers for pickup",
            sample_utterances=[utterance_flowers_a, utterance_flowers_b],
            intent_confirmation_setting=confirm_flowers,
            slot_priorities=[
                pickup_date_priority,
                flower_type_priority,
                pickup_time_priority,
            ],
            slots=[flower_type_slot],
        )

        # localeProperty
        en_us_locale = lex.CfnBot.BotLocaleProperty(
            locale_id="en_US",
            nlu_confidence_threshold=0.4,
            description="English Locale",
            voice_settings=lex.CfnBot.VoiceSettingsProperty(voice_id="Ivy"),
            slot_types=[flower_type],
            intents=[order_flower_intent],
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
