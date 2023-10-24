from aiogram.fsm.state import StatesGroup, State


class UserAddState(StatesGroup):
    user_id = State()
    subscribe_period = State()
    update_db = State()


class UserRemoveState(StatesGroup):
    user_id = State()
    update_db = State()


class AddMaskState(StatesGroup):
    input_combination = State()
    update_db = State()


class RemoveCombState(StatesGroup):
    remove_comb = State()
    update_db = State()


class EditNotifState(StatesGroup):
    days = State()
    time = State()
    update_database = State()


class AddSubState(StatesGroup):
    days = State()


class AddRegState(StatesGroup):
    input_regs = State()


class EditCombGroupsState(StatesGroup):
    edit_index = State()
    select_operation = State()
    add_to_group = State()
    remove_from_group = State()


class SetActiveGroups(StatesGroup):
    groups = State()


class DelRegState(StatesGroup):
    del_reg = State()