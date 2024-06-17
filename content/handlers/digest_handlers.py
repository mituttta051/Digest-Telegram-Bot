# A file that will contain message, command and callback handlers from digest branch

# Import downloaded packages
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# Import project files
from content.handlers.general_handlers import bot_start
import content.keyboards.general_keyboards as gk
import content.keyboards.digest_keyboards as dk
from utils.LLMUtils import generate_summary
from utils.botUtils import get_messages_in_days, get_channels_with_permissions

digest_router = Router()


# Define a StatesGroup for the DigestFSM finite state machine
class DigestFSM(StatesGroup):
    """
    A class representing the finite state machine for managing the digest functionality.

    This class defines the states that the finite state machine can be in, which are used to track the user's progress
    through the digest creation process.

    States:
        choose_channel (aiogram.fsm.state.State): The state where the user is prompted to choose a channel for the digest.
        choose_period (aiogram.fsm.state.StateState): The state where the user is prompted to choose the period for the digest.
        digest (aiogram.fsm.state.StateState): The state where the digest is being generated or displayed.
        edit_text (aiogram.fsm.state.StateState): The state where the user is prompted to edit the text of the digest.
    """
    # State for choosing a channel for the digest
    choose_channel = State()

    # State for choosing the period for the digest
    choose_period = State()

    # State for the digest itself
    digest = State()

    # State for editing the text of the digest
    edit_text = State()


@digest_router.message(F.text == "Create digest")
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
    await message.answer("Choose a channel", reply_markup=dk.channels_keyboard(channels))


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
    await callback.answer(f'You chose channel')

    # Update the state data with the selected channel
    await state.update_data(channel=callback.data)

    # Set the state to choose a period for the digest
    await state.set_state(DigestFSM.choose_period)

    # Send a message with an inline keyboard to choose a digest period
    await callback.message.answer(text="Choose a digest period", reply_markup=dk.supported_period_inline_keyboard)


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
    await callback.answer("You chose period")

    # Store selected period in state data
    await state.update_data(period=callback.data)

    # Set the state to generate the digest
    await state.set_state(DigestFSM.digest)
    data = await state.get_data()

    # Notify user that the digest is being prepared
    await callback.message.answer(text="Digest is preparing...")

    # Get messages within the specified period
    messages = get_messages_in_days(data['channel'], data['period'])
    if len(messages) == 0:
        digest = "No posts have been posted since the bot was added"
    else:
        digest = await generate_summary(messages)

    # Send the digest with an inline keyboard for further actions
    await callback.message.answer(text=digest, reply_markup=dk.digest_inline_keyboard)


@digest_router.callback_query(F.data == "digest_approve", DigestFSM.digest)
async def digest_approve(callback: CallbackQuery, state: FSMContext) -> None:
    """
        Asynchronous function to handle the "Approve" callback query for the digest.

        This function is triggered when a user selects the "Approve" option via a callback query while in the `DigestFSM.digest` state.
        It acknowledges the approval, edits the message to remove inline buttons, and prepares to post the digest to the channel.
        After handling the approval, it returns the user to the main menu and clears the state.

        Args:
            callback (aiogram.types.CallbackQuery): The callback query object with the "digest_approve" data.
            state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.

        See:
            `content.handlers.general_handlers.bot_start`: function that prints greeting message and calls the main menu keyboard
        """
    # Acknowledge the approval selection
    await callback.answer('You chose "Approve"')

    # Edit the message to remove inline buttons
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=gk.one_button_keyboard("inline", "Approve"))

    # Channel posting actions (Todo: Implement channel posting logic)

    # Send a message to return to the main menu
    await callback.message.answer("Return back to main menu")

    # Clear the state to reset the FSM
    await state.clear()

    # Start the bot from the main menu
    await bot_start(callback.message)


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
    await callback.answer('You chose "Edit"')

    # Store the initial text of the digest
    await state.update_data(initial_text=callback.message.text)

    # Edit the message to remove inline buttons
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=gk.one_button_keyboard("inline", "Edit"))

    # Prompt user to write their own version and provide a cancel button
    await callback.message.answer("Write your own version",
                                  reply_markup=gk.make_inline_keyboard(dk.cancel_editing_inline_button))

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
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=gk.one_button_keyboard("inline", "Cancel editing"))

    # Retrieve the initial text from the state data
    data = await state.get_data()
    initial_text = data['initial_text']

    # Set the state back to digest
    await state.set_state(DigestFSM.digest)

    # Send the initial text with the digest inline keyboard
    await callback.message.answer(text=initial_text, reply_markup=dk.digest_inline_keyboard)


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
    await message.answer(text=message.text, reply_markup=dk.digest_inline_keyboard)


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
    await callback.answer('You chose "Cancel"')

    # Edit the message to remove inline buttons
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=gk.one_button_keyboard("inline", "Cancel"))

    # Clear the state to reset the FSM
    await state.clear()

    # Start the bot from the main menu
    await bot_start(callback.message)


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

    # Retrieve the state data
    data = await state.get_data()

    # Get the latest messages within the specified period
    messages = get_messages_in_days(data['channel'], data['period'])

    # Generate the digest summary
    if len(messages) == 0:
        digest = "No posts have been posted since the bot was added"
    else:
        digest = await generate_summary(messages)

    # Edit the message to display the new digest with the digest inline keyboard
    await callback.message.edit_text(text=digest, reply_markup=dk.digest_inline_keyboard)


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
