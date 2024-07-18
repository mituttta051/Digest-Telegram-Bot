# A file that will contain message, command and callback handlers from digest branch

# Import downloaded packages
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from content.keyboards.digest_keyboards import supported_period_inline_keyboard

# Import project files
from content.FSMs.digest_FSMs import DigestFSM
from content.handlers.general_handlers import bot_start
import content.keyboards.general_keyboards as gk
import content.keyboards.digest_keyboards as dk
from resources.locales.buttons import buttons
from utils.LLMUtils import generate_summary
from utils.botUtils import get_messages_in_days, get_channels_with_permissions
from resources.locales.translation_dictionary import localise

digest_router = Router()


@digest_router.message(F.text.in_(buttons["digest_create"]))
async def bot_digest(message: Message, state: FSMContext) -> None:
    """
        Asynchronous function to handle the "Create digest" message and initiate the digest creation process.

        This function is triggered when a user sends a message with the text "Create digest". It sets the state to
        `DigestFSM.choose_channel` to prompt the user to choose a channel for the digest. It then retrieves a list of
        channels with permissions for the chat and sends a message with a keyboard to choose a channel.

        Args:
            message (aiogram.types.Message): The incoming message object containing the text "Create digest".
            state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.

        See:
            `utils.database.Utils.get_channels_with_permissions`: function that fetch a list of channels that the user has permission to use for the digest
        """
    # Set the state to choose a channel for the digest
    await state.set_state(DigestFSM.choose_channel)

    # Get a list of channels with permissions for the chat
    channels = await get_channels_with_permissions(message.chat.id)

    # Send a message with a keyboard to choose a channel
    await message.answer(await localise("Choose a channel", state),
                         reply_markup=await gk.channels_keyboard(channels, state))


@digest_router.callback_query(F.data == "back", DigestFSM.choose_channel)
async def digest_back_to_main(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(await localise("You return back", state))
    # Clear the state to reset the FSM
    # await state.clear()

    # Start the bot from the main menu
    await bot_start(callback.message, state)


@digest_router.callback_query(DigestFSM.choose_channel)
async def choose_period(callback: CallbackQuery, state: FSMContext) -> None:
    """
        Asynchronous function to handle callback queries when the state is `DigestFSM.choose_channel`.

        This function is triggered when a user selects a channel via a callback query while in the `choose_channel` state.
        It acknowledges the channel selection, updates the state data to include the chosen channel, and transitions
        the state to `DigestFSM.choose_period`. It then sends a message with an inline keyboard to choose a digest period.

        Args:
            callback (aiogram.types.CallbackQuery): The callback query object containing the data of the selected channel.
            state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.
        """
    # Acknowledge the channel selection (Todo: Replace placeholder text with actual channel title)
    await callback.answer(await localise('You chose channel', state))

    # Update the state data with the selected channel
    await state.update_data(channel=callback.data)

    # Set the state to choose a period for the digest
    await state.set_state(DigestFSM.choose_period)

    # Send a message with an inline keyboard to choose a digest period
    await callback.message.answer(text=await localise("Choose a digest period", state),
                                  reply_markup=await dk.supported_period_inline_keyboard(state))


@digest_router.callback_query(F.data == "back", DigestFSM.choose_period)
async def digest_back_to_choose_channel(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(await localise("You return back", state))
    # Clear the state to reset the FSM
    # await state.clear()

    # return bot to the choose channel
    await bot_digest(callback.message, state)


@digest_router.message(F.text.regexp(r'^\d+$'))
async def handle_custom_period(message: Message, state: FSMContext) -> None:
    if await state.get_state() == DigestFSM.choose_period.state:
        period = int(message.text)
        await set_custom_period(message, state)

@digest_router.message(F.text.in_(buttons["choose_custom_period"]))
async def custom_period_handler(message: Message, state: FSMContext) -> None:
    """
    Asynchronous function to handle the "Choose Custom Period" message button press.

    This function is triggered when a user selects the "Choose Custom Period" button. It sets the state to
    `DigestFSM.choose_custom_period` to prompt the user to input a custom period for the digest.

    Args:
        message (aiogram.types.Message): The incoming message object containing the "Choose Custom Period" button press.
        state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.
    """
    # Set the state to choose a custom period for the digest
    await state.set_state(DigestFSM.choose_custom_period)

    # Prompt the user to input a custom period for the digest
    await message.answer(await localise("Please enter a custom period", state))

# Handler for custom period input
@digest_router.message(DigestFSM.choose_custom_period)
async def set_custom_period(message: Message, state: FSMContext) -> None:
    try:
        custom_period = int(message.text)
        await message.answer(await localise("Custom period set to", state) + message.text + await localise("days", state))
        await state.update_data(period=message.text)

        # Set the state to generate the digest
        await state.set_state(DigestFSM.digest)
        data = await state.get_data()

        # Notify user that the digest is being prepared
        await message.answer(text=await localise("Digest is preparing...", state))

        # Get messages within the specified period
        messages = get_messages_in_days(data['channel'], data['period'])

        user_message = await message.answer(text="...")

        if len(messages) == 0:
            digest = await localise("Nothing has been posted since the bot was added", state)
        else:
            digest = await generate_summary(messages, data['channel'], user_message)

        # Send the digest with an inline keyboard for further actions
        await user_message.edit_text(text=digest, reply_markup=await dk.digest_inline_keyboard(state))
    except:
        await message.answer(await localise("You write incorrect number", state))
        await state.set_state(DigestFSM.choose_period)

        await message.answer(text=await localise("Choose a digest period", state),
                             reply_markup=await dk.supported_period_inline_keyboard(state))


# Handler for return back button
@digest_router.callback_query(F.data == "back", DigestFSM.choose_custom_period)
async def return_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer(await localise("You return back", state))
    await state.set_state(DigestFSM.choose_period)

    await callback.message.answer(text=await localise("Choose a digest period", state),
                                  reply_markup=await dk.supported_period_inline_keyboard(state))


@digest_router.callback_query(DigestFSM.choose_period)
async def digest_generate(callback: CallbackQuery, state: FSMContext) -> None:
    """
        Asynchronous function to generate a digest based on the chosen period.

        This function is triggered when a user selects a period via a callback query while in the `choose_period` state.
        It acknowledges the period selection, updates the state data to include the chosen period, and transitions
        the state to `DigestFSM.digest`. It then retrieves messages from the specified channel within the chosen period
        and generates a digest summary. If no messages are found, a default message is returned.

        Args:
            callback (aiogram.types.CallbackQuery): The callback query object with selected period data.
            state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.

        See:
            `utils.databaseUtils.get_messages_in_days`: function that fetch messages from the channel within the specified period.

            `utils.LLMUtils.generate_summary`: function that creates a digest from the messages.
        """
    # Acknowledge period selection
    await callback.answer(await localise("You chose period", state))

    # Store selected period in state data
    await state.update_data(period=callback.data)

    # Set the state to generate the digest
    await state.set_state(DigestFSM.digest)
    data = await state.get_data()

    # Notify user that the digest is being prepared
    await callback.message.answer(text=await localise("Digest is preparing...", state))

    # Get messages within the specified period
    messages = get_messages_in_days(data['channel'], data['period'])

    user_message = await callback.message.answer(text="...")

    if len(messages) == 0:
        digest = await localise("Nothing has been posted since the bot was added", state)
    else:
        digest = await generate_summary(messages, data['channel'], user_message)

    # Send the digest with an inline keyboard for further actions
    await user_message.edit_text(text=digest, reply_markup=await dk.digest_inline_keyboard(state))


@digest_router.callback_query(F.data == "digest_approve", DigestFSM.digest)
async def digest_approve(callback: CallbackQuery, state: FSMContext) -> None:
    """
        Callback function for handling the approval of a digest message.

        This function is triggered when a callback query with the data "digest_approve" is received.
        It posts the digest message to a selected channel and handles any exceptions that occur during the process.

        Parameters:
            callback (CallbackQuery): The callback query that triggered the function.
            state (FSMContext): The current state of the finite state machine.

        Returns:
            None
        """
    # Acknowledge the callback with a message
    await callback.answer(await localise('You chose "✅Approve"', state))

    # Edit the current message text and display an "Approve" button
    await callback.message.edit_text(text=callback.message.html_text,
                                     reply_markup=gk.one_button_keyboard("inline", await localise("✅Approve", state)))

    # Retrieve the stored state data
    data = await state.get_data()
    channel_id = data['channel']  # Extract the channel ID from the state data
    digest_text = callback.message.html_text  # Get the digest text from the callback message

    try:
        # Post the digest to the selected channel
        await callback.bot.send_message(chat_id=channel_id, text=digest_text)
        await callback.message.answer(await localise("🥳Digest posted successfully!", state))
    except Exception as e:
        # Handle any exceptions that occur during the message posting
        await callback.message.answer(f"Failed to post digest: {e}")

    # Clear the state to reset the FSM
    # await state.clear()

    # Start the bot from the main menu
    await bot_start(callback.message, state)


@digest_router.callback_query(F.data == "digest_edit")
async def digest_edit(callback: CallbackQuery, state: FSMContext) -> None:
    """
        Asynchronous function to handle the "Edit" callback query for the digest.

        This function is triggered when a user selects the "Edit" option via a callback query. It acknowledges the edit
        selection, stores the initial text of the digest, and edits the message to remove inline buttons. It then prompts
        the user to write their own version of the digest and provides an inline button to cancel editing. The state is
        transitioned to `DigestFSM.edit_text` to indicate that the user is editing the digest text.

        Args:
            callback (aiogram.types.CallbackQuery): The callback query object with the "digest_edit" data.
            state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.

        See:
            `content.keyboards.general_keyboards.one_button_keyboard`: function that creates a single-button keyboard of the specified type with the specified name.

            `content.keyboards.general_keyboards.make_inline_keyboard`: function that accepts inline buttons and forms a keyboard from them
        """
    # Acknowledge the edit selection
    await callback.answer(await localise('You chose "Edit"', state))

    # Store the initial text of the digest
    await state.update_data(initial_text=callback.message.html_text)

    # Edit the message to remove inline buttons
    await callback.message.edit_text(text=callback.message.html_text,
                                     reply_markup=gk.one_button_keyboard("inline", await localise("✏️Edit", state)))

    # Prompt user to write their own version and provide a cancel button
    await callback.message.answer(await localise("Write your own version and send it here", state),
                                  reply_markup=gk.make_inline_keyboard(
                                      dk.InlineKeyboardButton(text=await localise("❌Cancel editing", state),
                                                              callback_data="cancel_editing")))

    # Set the state to edit the text of the digest
    await state.set_state(DigestFSM.edit_text)


@digest_router.callback_query(F.data == "cancel_editing")
async def cancel_editing(callback: CallbackQuery, state: FSMContext) -> None:
    """
        Asynchronous function to handle the "Cancel editing" callback query.

        This function is triggered when a user selects the "Cancel editing" option via a callback query. It silently
        acknowledges the cancellation, restores the initial text of the digest, and removes the editing prompt. The state
        is then transitioned back to `DigestFSM.digest` to indicate that the editing session is over.

        Args:
            callback (aiogram.types.CallbackQuery): The callback query object with the "cancel_editing" data.
            state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.

        See:
            `content.keyboards.general_keyboards.one_button_keyboard`: function that creates a single-button keyboard of the specified type with the specified name.
        """
    # Acknowledge the cancellation
    await callback.answer()

    # Restore the initial text and remove the editing prompt
    await callback.message.edit_text(text=callback.message.html_text,
                                     reply_markup=gk.one_button_keyboard("inline",
                                                                         await localise("❌Cancel editing", state))

                                     )
    # Retrieve the initial text from the state data
    data = await state.get_data()
    initial_text = data['initial_text']

    # Set the state back to digest
    await state.set_state(DigestFSM.digest)

    # Send the initial text with the digest inline keyboard
    await callback.message.answer(text=initial_text, reply_markup=await dk.digest_inline_keyboard(state))


@digest_router.message(DigestFSM.edit_text)
async def edit_digest(message: Message, state: FSMContext) -> None:
    """
        Asynchronous function to handle edited digest text messages.

        This function is triggered when a user sends a message while in the `DigestFSM.edit_text` state. It transitions
        the state to `DigestFSM.digest` and sends the edited text back to the user with an inline keyboard for further
        actions.

        Args:
            message (aiogram.types.Message): The incoming message containing the edited digest text.
            state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.
        """
    # Set the state to digest
    await state.set_state(DigestFSM.digest)

    # Send the edited text with the digest inline keyboard
    await message.answer(text=message.html_text, reply_markup=await dk.digest_inline_keyboard(state))


@digest_router.callback_query(F.data == "digest_cancel", DigestFSM.digest)
async def digest_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    """
        Asynchronous function to handle the "Cancel" callback query for the digest.

        This function is triggered when a user selects the "Cancel" option via a callback query while in the `DigestFSM.digest` state.
        It acknowledges the cancellation, edits the message to remove inline buttons, and clears the state to return the user to the
        main menu.

        Args:
            callback (aiogram.types.CallbackQuery): The callback query object with the "digest_cancel" data.
            state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.

        See:
            `content.keyboards.general_keyboards.one_button_keyboard`: function that creates a single-button keyboard of the specified type with the specified name.

            `content.handlers.general_handlers.bot_start`: function that prints greeting message and calls the main menu keyboard
        """
    # Acknowledge the cancellation selection
    await callback.answer(await localise('You chose "❌Cancel"', state))

    # Edit the message to remove inline buttons
    await callback.message.edit_text(text=callback.message.html_text,
                                     reply_markup=gk.one_button_keyboard("inline", await localise("❌Cancel", state)))

    # Clear the state to reset the FSM
    # await state.clear()

    # Start the bot from the main menu
    await bot_start(callback.message, state)


@digest_router.callback_query(F.data == "digest_regenerate", DigestFSM.digest)
async def digest_regenerate(callback: CallbackQuery, state: FSMContext) -> None:
    """
        Asynchronous function to regenerate the digest based on the user's "Regenerate" selection.

        This function is triggered when a user selects the "Regenerate" option via a callback query while in the `DigestFSM.digest` state.
        It acknowledges the regeneration request, retrieves the latest messages within the specified period, and generates a new
        digest summary. If no new messages are found, a default message is returned. The message is then edited to display the new
        digest with an inline keyboard for further actions.

        Args:
            callback (aiogram.types.CallbackQuery): The callback query object with the "digest_regenerate" data.
            state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.

        See:
            `utils.botUtils.get_messages_in_days`: function that gets from database a list of messages from specific channel for a specified period

            `utils.LLMUtils.generate_summary`: function that create a digest from the messages.
        """
    # Acknowledge the regeneration selection
    await callback.answer('You chose "Regenerate"')

    await callback.message.answer(text=await localise("Digest is preparing...", state))

    # Retrieve the state data
    data = await state.get_data()

    # Get the latest messages within the specified period
    messages = get_messages_in_days(data['channel'], data['period'])

    user_message = await callback.message.answer(text="...")

    # Generate the digest summary
    if len(messages) == 0:
        digest = await localise("Nothing has been posted since the bot was added", state)
    else:
        digest = await generate_summary(messages, data['channel'], user_message)

    # Edit the message to display the new digest with the digest inline keyboard
    await user_message.edit_text(text=digest, reply_markup=await dk.digest_inline_keyboard(state))


@digest_router.callback_query(F.data == "empty-data")
async def empty_data_callback(callback: CallbackQuery) -> None:
    """
        Asynchronous function to handle callback queries with "empty-data" as the data.

        This function is a placeholder for handling callback queries with empty data. It silently acknowledges the callback
        without taking any further action.

        Args:
            callback (aiogram.types.CallbackQuery): The callback query object with the "empty-data" data.
        """
    # Acknowledge the callback without sending a message
    await callback.answer()
