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

digest_router = Router()


class EditDigestFSM(StatesGroup):
    edit_text = State()


@digest_router.message(F.text == "Create digest")
async def bot_digest(message: Message):
    digest = "**There is some digest**"  # Digest creation method call
    await message.answer(text=digest, reply_markup=aiogram.types.ReplyKeyboardRemove())
    await message.edit_text(text=digest, reply_markup=dk.digest_inline_keyboard)


@digest_router.callback_query(F.data == "digest_approve")
async def digest_approve(callback: CallbackQuery):
    await callback.answer('You chose "Approve"')
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=gk.one_button_keyboard("inline", "Approve"))  # Remove inline buttons

    # Channel posting actions (?)

    await callback.message.answer("Return back to main menu")
    await bot_start(callback.message)


@digest_router.callback_query(F.data == "digest_edit")
async def digest_edit(callback: CallbackQuery, state: FSMContext):
    await callback.answer('You chose "Edit"')

    await state.update_data(initial_text=callback.message.text)

    await callback.message.edit_text(text=callback.message.text, reply_markup=gk.one_button_keyboard("inline", "Edit"))  # Remove inline buttons
    await callback.message.answer("Write your own version", reply_markup=gk.make_inline_keyboard(dk.cancel_editing_inline_button))

    await state.set_state(EditDigestFSM.edit_text)


@digest_router.callback_query(F.data == "cancel_editing")
async def cancel_editing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=gk.one_button_keyboard("inline", "Cancel editing"))

    data = await state.get_data()
    initial_text = data['initial_text']
    await state.clear()

    await callback.message.answer(text=initial_text, reply_markup=dk.digest_inline_keyboard)


@digest_router.message(EditDigestFSM.edit_text)
async def edit_digest(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(text=message.text, reply_markup=dk.digest_inline_keyboard)


@digest_router.callback_query(F.data == "digest_cancel")
async def digest_cancel(callback: CallbackQuery):
    await callback.answer('You chose "Cancel"')
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=gk.one_button_keyboard("inline", "Cancel"))  # Remove inline buttons
    await bot_start(callback.message)


@digest_router.callback_query(F.data == "digest_regenerate")
async def digest_regenerate(callback: CallbackQuery):
    await callback.answer('You chose "Regenerate"')

    digest = callback.message.text + ' ' + "Regenerated."  # Digest creation method call

    await callback.message.edit_text(text=digest, reply_markup=dk.digest_inline_keyboard)


@digest_router.callback_query(F.data == "empty-data")
async def empty_data_callback(callback: CallbackQuery):
    await callback.answer()
