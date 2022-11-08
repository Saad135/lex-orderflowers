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

        # lilies sample values
        lilies_value = lex.CfnBot.SampleValueProperty(value="lilies")

        # Slot values: lolies
        lilies = lex.CfnBot.SlotTypeValueProperty(sample_value=lilies_value)

        # roses sample values
        roses_value = lex.CfnBot.SampleValueProperty(value="roses")

        # Slot values: lolies
        roses = lex.CfnBot.SlotTypeValueProperty(sample_value=roses_value)

        # tulips sample values
        tulips_value = lex.CfnBot.SampleValueProperty(value="tulips")

        # Slot values: tulips
        tulips = lex.CfnBot.SlotTypeValueProperty(sample_value=tulips_value)

        # slot type
        flower_type = lex.CfnBot.SlotTypeProperty(
            name="FlowerTypes",
            description="the type of flowers",
            slot_type_values=[lilies, roses, tulips],
            value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                resolution_strategy="ORIGINAL_VALUE"
            ),
        )

        # Sample Utterances
        utterance_flowers_a = lex.CfnBot.SampleUtteranceProperty(
            utterance="I would like to pick up flowers"
        )
        utterance_flowers_b = lex.CfnBot.SampleUtteranceProperty(
            utterance="I would like to order some flowers"
        )

        # flower confirm text message
        flower_confirm_message = lex.CfnBot.PlainTextMessageProperty(
            value="Okay, your {FlowerType} will be ready for pickup by {PickupTime} on {PickupDate}.  Does this sound okay?"
        )

        # Message group
        flower_confirm_group = lex.CfnBot.MessageGroupProperty(
            message=lex.CfnBot.MessageProperty(
                plain_text_message=flower_confirm_message
            )
        )

        # Prompt specification
        flowers_accept = lex.CfnBot.PromptSpecificationProperty(
            message_groups_list=[flower_confirm_group],
            max_retries=3,
            allow_interrupt=False,
        )

        # flower decline text message
        flower_decline_message = lex.CfnBot.PlainTextMessageProperty(
            value="Okay, I will not place your order."
        )

        # Declination message group
        flower_decline_group = lex.CfnBot.MessageGroupProperty(
            message=lex.CfnBot.MessageProperty(
                plain_text_message=flower_decline_message
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

        # FlowerType

        # flower slot message
        flower_slot_message = lex.CfnBot.PlainTextMessageProperty(
            value="What type of flowers would you like to order?"
        )

        # Flower slot group list
        flower_slot_group = lex.CfnBot.MessageGroupProperty(
            message=lex.CfnBot.MessageProperty(plain_text_message=flower_slot_message)
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
            slot_type_name="FlowerTypes",
            value_elicitation_setting=flower_value_elicit,
        )

        # PickupDate

        # PickupDate slot message
        pickup_date_slot_message = lex.CfnBot.PlainTextMessageProperty(
            value="What day do you want the {FlowerType} to be picked up?"
        )

        # PickupDate group list
        pickup_date_group = lex.CfnBot.MessageGroupProperty(
            message=lex.CfnBot.MessageProperty(
                plain_text_message=pickup_date_slot_message
            )
        )

        # PickupDate Prompt specification
        pickup_date_prompt = lex.CfnBot.PromptSpecificationProperty(
            message_groups_list=[pickup_date_group],
            max_retries=3,
            allow_interrupt=False,
        )

        # value elicitation setting for PickupDate
        pickup_date_elicit = lex.CfnBot.SlotValueElicitationSettingProperty(
            slot_constraint="Required", prompt_specification=pickup_date_prompt
        )

        # PickupDate Property
        pickup_date_slot = lex.CfnBot.SlotProperty(
            name="PickupDate",
            description="slot for the flower type",
            slot_type_name="AMAZON.Date",
            value_elicitation_setting=pickup_date_elicit,
        )

        # PickupTime

        # PickupTime slot message
        pickup_time_slot_message = lex.CfnBot.PlainTextMessageProperty(
            value="At what time do you want the {FlowerType} to be picked up?"
        )

        # PickupTime group list
        pickup_time_group = lex.CfnBot.MessageGroupProperty(
            message=lex.CfnBot.MessageProperty(
                plain_text_message=pickup_time_slot_message
            )
        )

        # PickupTime Prompt specification
        pickup_time_prompt = lex.CfnBot.PromptSpecificationProperty(
            message_groups_list=[pickup_time_group],
            max_retries=3,
            allow_interrupt=False,
        )

        # value elicitation setting for PickupTime
        pickup_time_elicit = lex.CfnBot.SlotValueElicitationSettingProperty(
            slot_constraint="Required", prompt_specification=pickup_time_prompt
        )

        # PickupTime Property
        pickup_time_slot = lex.CfnBot.SlotProperty(
            name="PickupTime",
            description="slot for the flower type",
            slot_type_name="AMAZON.Time",
            value_elicitation_setting=pickup_time_elicit,
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
            slots=[flower_type_slot, pickup_date_slot, pickup_time_slot],
        )

        # fallback intent
        fallback_intent = lex.CfnBot.IntentProperty(
            name="FallbackIntent",
            description="Default intent when no other intent matches",
            parent_intent_signature="AMAZON.FallbackIntent",
        )

        # localeProperty
        en_us_locale = lex.CfnBot.BotLocaleProperty(
            locale_id="en_US",
            nlu_confidence_threshold=0.4,
            description="English Locale",
            voice_settings=lex.CfnBot.VoiceSettingsProperty(voice_id="Ivy"),
            slot_types=[flower_type],
            intents=[order_flower_intent, fallback_intent],
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
            bot_locales=[en_us_locale],
        )

        lex_bot.apply_removal_policy(RemovalPolicy.DESTROY)

        # Bot version locale details
        lex_bot_locale_details = lex.CfnBotVersion.BotVersionLocaleDetailsProperty(
            source_bot_version="DRAFT"
        )

        # Bot version local specification
        lex_bot_locale_specs = lex.CfnBotVersion.BotVersionLocaleSpecificationProperty(
            locale_id="en_US", bot_version_locale_details=lex_bot_locale_details
        )

        # Bot Version
        lex_bot_version = lex.CfnBotVersion(
            self,
            id="MyLexBotVersion",
            bot_id=lex_bot.attr_id,
            bot_version_locale_specification=[lex_bot_locale_specs],
            description="OrderFlowers Version",
        )
