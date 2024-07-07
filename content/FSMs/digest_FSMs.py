# Define a StatesGroup for the DigestFSM finite state machine
from aiogram.fsm.state import State, StatesGroup


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
