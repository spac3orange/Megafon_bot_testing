import sqlite3 as sq
from data.config import logger
import datetime
from typing import List, Dict, Union, Tuple

@logger.catch()
async def db_start() -> None:
    """
    Initializes the connection to the database and creates the table if it does not exist.
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id INTEGER, sub_until TEXT, combinations TEXT, "
                "notifications_days TEXT, notification_time TEXT, regions TEXT)")
    db.commit()
    logger.info('connected to database')


@logger.catch()
async def db_check_user(user_id: int) -> bool:
    """
    Check if a user with the specified user_id exists in the database.
    Args:
        user_id (int): The user ID to check.
    Returns:
        bool: True if the user is not found, False otherwise.
    """
    global db, cur
    db = sq.connect('user_base.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM profile WHERE user_id = ?", (user_id,))
    user_data = cur.fetchone()
    if user_data is None:
        return True
    else:
        return False


@logger.catch()
async def db_add_user(user_id: int, sub_until=None) -> None:
    """
    Add a new user with the specified user_id to the database.
    Args:
        user_id (int): The user ID to add.
        sub_until (Optional[str], optional): Subscription expiration date (if any). Defaults to None.
    Returns:
        None
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("SELECT user_id FROM profile WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    if result is not None:
        logger.warning(f"User with ID {user_id} already exists")
        return
    cur.execute("INSERT INTO profile(user_id, sub_until) VALUES (?, ?)", (user_id, sub_until))
    db.commit()
    logger.info(f"User with ID {user_id} added to database")


@logger.catch()
async def db_remove_user(user_id: int) -> None:
    """
    Remove a user with the specified user_id from the database.
    Args:
        user_id (int): The user ID to remove.
    Returns:
        None
    """
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("DELETE FROM profile WHERE user_id = ?", (user_id,))
    db.commit()


@logger.catch()
async def db_get_users() -> List[int]:
    """
    Retrieve a list of all user_ids from the database.
    Returns:
        List[int]: A list of user IDs.
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("SELECT user_id FROM profile")
    user_ids = [row[0] for row in cur.fetchall()]
    db.close()
    return user_ids


@logger.catch()
async def db_get_users_full() -> List[Dict[str, Union[int, str]]]:
    """
    Retrieve a list of all users from the database as a list of dictionaries.
    Each dictionary contains keys: 'user_id', 'sub_until', and 'combinations'.
    Returns:
        List[Dict[str, Union[int, str]]]: A list of dictionaries representing users.
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("SELECT user_id, sub_until, combinations FROM profile")
    users = []
    for row in cur.fetchall():
        user = {
            'user_id': row[0],
            'sub_until': row[1],
            'combinations': row[2]
        }
        users.append(user)
    db.close()
    return users


@logger.catch()
async def db_add_combination(user_id: int, combination: str) -> None:
    """
    Add a combination for the user with the specified user_id to the database.
    Args:
        user_id (int): The user ID for which to add the combination.
        combination (str): The combination to add.
    Returns:
        None
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("SELECT user_id FROM profile WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    if result is None:
        logger.warning(f"Пользователь с ID {user_id} не найден в базе данных")
        return
    cur.execute("SELECT combinations FROM profile WHERE user_id = ?", (user_id,))
    current_combinations = cur.fetchone()[0]
    if current_combinations is not None:

        new_combinations = current_combinations + "," + combination
    else:
        new_combinations = combination
    cur.execute("UPDATE profile SET combinations = ? WHERE user_id = ?", (new_combinations, user_id))
    logger.info(f"Комбинация '{combination}' добавлена для пользователя {user_id}")
    db.commit()


@logger.catch()
async def db_get_user_combinations(user_id: int) -> List[str]:
    """
    Retrieve all combination groups for the user with the specified user_id from the corresponding table.
    Args:
        user_id (int): The user ID for which to retrieve combination groups.
    Returns:
        List[str]: A list of combination groups for the specified user.
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()

    table_name = f"user_{user_id}"
    cur.execute(f"SELECT comb_group FROM {table_name}")
    combination_groups = [row[0] for row in cur.fetchall()]

    db.close()
    logger.info(f"Extracting combination groups for user {user_id} from table {table_name}")
    return combination_groups


async def db_remove_combination_group(user_id: int, combination_indices: List[int]) -> None:
    """
    Remove combination groups at the specified indices for the given user.
    Args:
        user_id (int): The user ID for which to remove the combination groups.
        combination_indices (List[int]): The indices of the combination groups to remove (1-based).
    Returns:
        None
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    table_name = f"user_{user_id}"
    cur.execute(f"SELECT comb_group FROM {table_name}")
    combination_groups = [row[0] for row in cur.fetchall()]
    combination_groups = [comb_group for index, comb_group in enumerate(combination_groups, start=1) if index not in combination_indices]
    cur.execute(f"DELETE FROM {table_name}")
    for comb_group in combination_groups:
        cur.execute(f"INSERT INTO {table_name} (comb_group) VALUES (?)", (comb_group,))
    db.commit()
    logger.info(f"Combination groups at indices {combination_indices} removed for user {user_id}")
    db.close()

@logger.catch()
async def get_all_combinations_list() -> List[Dict[str, Union[int, List[str]]]]:
    """
    Returns a list of dictionaries containing user IDs and their corresponding combinations.
    """
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("SELECT user_id, combinations FROM profile")
    user_combinations_list = []
    for row in cur.fetchall():
        user_id = row[0]
        combinations_str = row[1]
        combinations = combinations_str.split(',')
        user_combinations = {
            'user_id': user_id,
            'combinations': combinations
        }
        user_combinations_list.append(user_combinations)
    db.close()
    logger.info('Retrieved user combinations from the database')
    return user_combinations_list


@logger.catch()
async def db_set_notification_settings(user_id: int, notification_days: str, notification_time: str) -> None:
    """
    Write the user's notification settings to the database.
    Args:
        user_id (int): The user ID for which to set the notification settings.
        notification_days (str): The days on which to send notifications (as a comma-separated string).
        notification_time (str): The time at which to send notifications (in HH:MM format, 24-hour).
    Returns:
        None
    """
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("UPDATE profile SET notifications_days = ?, notification_time = ? WHERE user_id = ?",
                (notification_days, notification_time, user_id))
    db.commit()
    db.close()
    logger.info(f"Notification settings updated for user {user_id}")


@logger.catch()
async def db_get_notification_settings(user_id: int) -> Tuple[str, str]:
    """
    Retrieves the notification settings from the database for the specified user ID.
    Returns a tuple containing the notification days and notification time.
    """
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("SELECT notifications_days, notification_time FROM profile WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    db.close()

    if result is not None:
        notification_days = result[0]
        notification_time = result[1]
        logger.info(f"Retrieved notification settings for user {user_id}")
        return notification_days, notification_time
    else:
        logger.warning(f"No notification settings found for user {user_id}")
        return 'None', 'None'


@logger.catch()
async def get_users_with_matching_date() -> List[int]:
    """
       Retrieve user IDs with subscription expiration dates matching the current date.

       Returns:
           List[int]: A list of user IDs with matching expiration dates.
    """
    current_date = datetime.date.today().strftime("%d-%m-%Y")

    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("SELECT user_id FROM profile WHERE sub_until = ?",
                (current_date,))
    user_ids = [row[0] for row in cur.fetchall()]
    db.close()

    return user_ids


@logger.catch()
async def db_remove_notifications() -> None:
    """
    Remove notification_days and notification_time for all users in the database.
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("UPDATE profile SET notifications_days = NULL, notification_time = NULL")
    db.commit()
    logger.info('Removed notification_days and notification_time for all users')


@logger.catch()
async def db_add_user_regions(user_id: int, regions: str) -> None:
    """
    Add regions for a user with the specified user_id to the database.
    Args:
        user_id (int): The user ID to add regions for.
        regions (str): Comma-separated string of regions to add.
    Returns:
        None
    """
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("SELECT user_id, regions FROM profile WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    if result is None:
        logger.warning(f"User with ID {user_id} does not exist")
        return
    existing_regions = result[1]  # Get the existing regions from the database
    if existing_regions:
        updated_regions = f"{existing_regions}, {regions}"
    else:
        updated_regions = regions
    cur.execute("UPDATE profile SET regions = ? WHERE user_id = ?", (updated_regions, user_id))
    db.commit()
    logger.info(f"Regions '{regions}' added for user with ID {user_id}")


@logger.catch()
async def db_get_user_regions(user_id: int) -> str:
    """
    Retrieve regions for a user with the specified user_id from the database.
    Args:
        user_id (int): The user ID to retrieve regions for.
    Returns:
        str: Comma-separated string of regions for the user.
    """
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("SELECT regions FROM profile WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    if result is None:
        logger.warning(f"User with ID {user_id} does not exist")
        return ''
    regions = result[0]
    db.close()
    return regions


@logger.catch()
async def db_remove_user_regions(user_id: int, regions_to_remove: List[int]) -> None:
    """
    Remove specified regions for a user with the specified user_id from the database.
    Args:
        user_id (int): The user ID to remove regions for.
        regions_to_remove (List[int]): List of region numbers to remove.
    Returns:
        None
    """
    if "all" in regions_to_remove:
        regions_to_remove = ["all"]  # Заменяем "all" на список с одним элементом "all"
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    cur.execute("SELECT user_id, regions FROM profile WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    if result is None:
        logger.warning(f"User with ID {user_id} does not exist")
        return
    existing_regions = result[1]  # Получаем текущие регионы из базы данных
    if existing_regions:
        if "all" in regions_to_remove:
            updated_regions = ""  # Очищаем регионы, если есть "all" в списке
        else:
            existing_region_list = [int(region) for region in existing_regions.split(",")]
            # Удаляем указанные регионы из текущего списка
            updated_region_list = [region for region in existing_region_list if region not in regions_to_remove]
            updated_regions = ", ".join(map(str, updated_region_list))
    else:
        logger.warning(f"User with ID {user_id} has no regions to remove")
        return
    cur.execute("UPDATE profile SET regions = ? WHERE user_id = ?", (updated_regions, user_id))
    db.commit()
    logger.info(f"Regions {regions_to_remove} removed for user with ID {user_id}")


@logger.catch()
async def db_add_comb_group(user_id: int, comb_group: str) -> None:
    """
    Add a combination group to the table with the same name as the user_id.
    Args:
        user_id (int): The user ID to add the combination group for.
        comb_group (str): The combination group to add.
    Returns:
        None
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    # Проверяем наличие таблицы для пользователя
    table_name = f"user_{user_id}"
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cur.fetchone()
    if result is None:
        # Создаем таблицу для пользователя с дополнительным столбцом active
        cur.execute(f"CREATE TABLE {table_name} (comb_group TEXT, active BOOLEAN DEFAULT FALSE)")
        db.commit()
        logger.info(f"Table '{table_name}' created")
    # Добавляем данные в таблицу пользователя
    cur.execute(f"INSERT INTO {table_name} (comb_group) VALUES (?)", (comb_group,))
    db.commit()
    logger.info(f"Combination group '{comb_group}' added for user with ID {user_id}")
    db.close()

@logger.catch()
async def db_get_comb_groups(user_id: int) -> List[str]:
    """
    Get a list of all combination groups from the table with the same name as the user_id.
    Args:
        user_id (int): The user ID to get the combination groups for.
    Returns:
        List[str]: A list of combination groups.
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    # Проверяем наличие таблицы для пользователя
    table_name = f"user_{user_id}"
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cur.fetchone()
    if result is None:
        logger.warning(f"Table '{table_name}' does not exist for user with ID {user_id}")
        db.close()
        return []

    # Получаем все группы комбинаций из таблицы пользователя
    cur.execute(f"SELECT comb_group FROM {table_name}")
    combination_groups = [row[0] for row in cur.fetchall()]

    db.close()
    return combination_groups


@logger.catch()
async def db_add_combinations_to_group(user_id: int, group_index: int, combinations: str) -> None:
    """
    Add combinations to a specific group in the user's table.
    Args:
        user_id (int): The user ID.
        group_index (int): The index of the group.
        combinations (str): The combinations to add.
    Returns:
        None
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    # Проверяем наличие таблицы для пользователя
    table_name = f"user_{user_id}"
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cur.fetchone()
    if result is None:
        logger.warning(f"Table '{table_name}' does not exist for user with ID {user_id}")
        db.close()
        return

    # Обновляем группу комбинаций в таблице пользователя
    cur.execute(f"SELECT comb_group FROM {table_name} WHERE rowid=?", (group_index,))
    result = cur.fetchone()
    if result is None:
        logger.warning(f"Group with index {group_index} does not exist for user with ID {user_id}")
        db.close()
        return

    existing_comb_group = result[0]
    if existing_comb_group:
        comb_group = f"{existing_comb_group}, {combinations}"
    else:
        comb_group = combinations

    cur.execute(f"UPDATE {table_name} SET comb_group=? WHERE rowid=?", (comb_group, group_index))
    db.commit()
    logger.info(f"Combinations '{combinations}' added to group with index {group_index} for user with ID {user_id}")

    db.close()


@logger.catch()
async def db_remove_combinations_from_group(user_id: int, group_index: int, combinations: str) -> None:
    """
    Remove combinations from a specific group in the user's table.
    Args:
        user_id (int): The user ID.
        group_index (int): The index of the group.
        combinations (str): The combinations to remove.
    Returns:
        None
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    # Проверяем наличие таблицы для пользователя
    table_name = f"user_{user_id}"
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cur.fetchone()
    if result is None:
        logger.warning(f"Table '{table_name}' does not exist for user with ID {user_id}")
        db.close()
        return

    # Получаем текущую группу комбинаций из таблицы пользователя
    cur.execute(f"SELECT comb_group FROM {table_name} WHERE rowid=?", (group_index,))
    result = cur.fetchone()
    if result is None:
        logger.warning(f"Group with index {group_index} does not exist for user with ID {user_id}")
        db.close()
        return

    existing_comb_group = result[0]
    if existing_comb_group:
        # Разделяем текущую группу комбинаций на отдельные комбинации
        current_combinations = existing_comb_group.split(", ")
        # Разделяем комбинации, которые нужно удалить
        combinations_to_remove = combinations.split(", ")
        # Удаляем указанные комбинации из текущих комбинаций
        updated_combinations = [comb for comb in current_combinations if comb not in combinations_to_remove]
        # Обновляем группу комбинаций в таблице пользователя
        updated_comb_group = ", ".join(updated_combinations)
        cur.execute(f"UPDATE {table_name} SET comb_group=? WHERE rowid=?", (updated_comb_group, group_index))
        db.commit()
        logger.info(f"Combinations '{combinations}' removed from group with index {group_index} for user with ID {user_id}")
    else:
        logger.warning(f"No combinations exist in group with index {group_index} for user with ID {user_id}")

    db.close()


@logger.catch()
async def db_update_comb_group_status(user_id: int, group_indexes: List[int]) -> None:
    """
    Update the 'active' column in the table for the specified user_id and group_indexes.
    Args:
        user_id (int): The user ID.
        group_indexes (List[int]): The list of group indexes to update.
    Returns:
        None
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    table_name = f"user_{user_id}"
    # Получаем все записи в таблице
    cur.execute(f"SELECT rowid FROM {table_name}")
    all_rows = cur.fetchall()
    # Обновляем статусы групп комбинаций в таблице
    for row in all_rows:
        row_id = row[0]
        if row_id in group_indexes:
            cur.execute(f"UPDATE {table_name} SET active = TRUE WHERE rowid = ?", (row_id,))
        else:
            cur.execute(f"UPDATE {table_name} SET active = FALSE WHERE rowid = ?", (row_id,))
    db.commit()
    logger.info(f"Combination group statuses updated for user with ID {user_id}")
    db.close()


@logger.catch()
async def db_get_active_combinations(user_id: int) -> List[str]:
    """
    Get all active combinations from the user's table.
    Args:
        user_id (int): The user ID.
    Returns:
        List[str]: The list of active combinations.
    """
    global db, cur
    db = sq.connect('database/user_base.db')
    cur = db.cursor()
    table_name = f"user_{user_id}"
    # Проверяем наличие таблицы для пользователя
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cur.fetchone()
    if result is None:
        logger.warning(f"Table '{table_name}' does not exist for user with ID {user_id}")
        db.close()
        return []
    # Получаем все активные комбинации из таблицы
    cur.execute(f"SELECT comb_group FROM {table_name} WHERE active = TRUE")
    results = cur.fetchall()
    active_combinations = [result[0] for result in results] if results else []
    db.close()
    return active_combinations