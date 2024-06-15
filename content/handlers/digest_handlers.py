# A file that will contain message, command and callback handlers from digest branch
# Import downloaded packages
import aiogram.types
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


class DigestFSM(StatesGroup):
    choose_channel = State()
    choose_period = State()
    digest = State()
    edit_text = State()


@digest_router.message(F.text == "Create digest")
async def bot_digest(message: Message, state: FSMContext):
    await state.set_state(DigestFSM.choose_channel)

    channels = await get_channels_with_permissions(message.chat.id)
    await message.answer("Choose a channel", reply_markup=dk.channels_keyboard(channels))


@digest_router.callback_query(DigestFSM.choose_channel)
async def choose_period(callback: CallbackQuery, state: FSMContext):
    await callback.answer(f'You chose channel')  # Todo: Get channel title

    await state.update_data(channel=callback.data)
    await state.set_state(DigestFSM.choose_period)

    await callback.message.answer(text="Choose a digest period", reply_markup=dk.supported_period_inline_keyboard)


@digest_router.callback_query(DigestFSM.choose_period)
async def digest_generate(callback: CallbackQuery, state: FSMContext):
    await callback.answer("You chose period")

    await state.update_data(period=callback.data)
    await state.set_state(DigestFSM.digest)
    data = await state.get_data()

    messages = get_messages_in_days(data['channel'], data['period'])

    if len(messages) == 0:
        digest = "No posts have been posted since the bot was added"
    else:
        digest = await generate_summary(messages)

    await callback.message.answer(text=digest, reply_markup=dk.digest_inline_keyboard)


@digest_router.callback_query(F.data == "digest_approve", DigestFSM.digest)
async def digest_approve(callback: CallbackQuery, state: FSMContext):
    await callback.answer('You chose "Approve"')
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=gk.one_button_keyboard("inline", "Approve"))  # Remove inline buttons

    # Channel posting actions (?)

    await callback.message.answer("Return back to main menu")
    await state.clear()
    await bot_start(callback.message)


@digest_router.callback_query(F.data == "digest_edit")
async def digest_edit(callback: CallbackQuery, state: FSMContext):
    await callback.answer('You chose "Edit"')

    await state.update_data(initial_text=callback.message.text)

    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=gk.one_button_keyboard("inline", "Edit"))  # Remove inline buttons
    await callback.message.answer("Write your own version",
                                  reply_markup=gk.make_inline_keyboard(dk.cancel_editing_inline_button))

    await state.set_state(DigestFSM.edit_text)


@digest_router.callback_query(F.data == "cancel_editing")
async def cancel_editing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=gk.one_button_keyboard("inline", "Cancel editing"))

    data = await state.get_data()
    initial_text = data['initial_text']
    await state.set_state(DigestFSM.digest)

    await callback.message.answer(text=initial_text, reply_markup=dk.digest_inline_keyboard)


@digest_router.message(DigestFSM.edit_text)
async def edit_digest(message: Message, state: FSMContext):
    await state.set_state(DigestFSM.digest)

    await message.answer(text=message.text, reply_markup=dk.digest_inline_keyboard)


@digest_router.callback_query(F.data == "digest_cancel", DigestFSM.digest)
async def digest_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer('You chose "Cancel"')
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=gk.one_button_keyboard("inline", "Cancel"))  # Remove inline buttons
    await state.clear()
    await bot_start(callback.message)


@digest_router.callback_query(F.data == "digest_regenerate", DigestFSM.digest)
async def digest_regenerate(callback: CallbackQuery, state: FSMContext):
    await callback.answer('You chose "Regenerate"')

    data = await state.get_data()

    messages = get_messages_in_days(data['channel'], data['period'])

    if len(messages) == 0:
        digest = "No posts have been posted since the bot was added"
    else:
        digest = await generate_summary(messages)

    await callback.message.edit_text(text=digest, reply_markup=dk.digest_inline_keyboard)


@digest_router.callback_query(F.data == "empty-data")
async def empty_data_callback(callback: CallbackQuery):
    await callback.answer()
