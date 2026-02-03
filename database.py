import logging
import aiosqlite
import config


DB_NAME = 'quiz_bot.db'


async def create_table():
    """
    Initializes the database and creates the 'quiz_state' table if it doesn't already exist.
    """
    logging.info("Attempting to connect to the database and create tables...")
    try:
        async with aiosqlite.connect('quiz_bot.db') as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY, 
                question_index INTEGER, 
                last_score INTEGER DEFAULT 0
            )''')
            await db.commit()
        logging.info("Table 'quiz_state' has been successfully verified/created.")
    except Exception as e:
        logging.error(f"Database initialization error: {e}")


async def update_quiz_index(user_id, index):
    """
    Updates or inserts the current quiz question index for a specific user in the database.
    """
    logging.info(f"Attempting to update quiz index for user {user_id} to index {index}.")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR REPLACE INTO quiz_state (user_id, question_index, last_score) 
            VALUES (?, ?, COALESCE((SELECT last_score FROM quiz_state WHERE user_id = ?), 0))
        ''', (user_id, index, user_id))
        await db.commit()


async def get_quiz_index(user_id):
    """
    Fetches the current quiz question index for a specific user from the database.
    Returns the index if found, otherwise returns 0.
    """
    logging.info(f"Attempting to fetch quiz index for user {user_id}.")
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
                results = await cursor.fetchone()
                if results is not None:
                    logging.info(f"Found existing index {results[0]} for user {user_id}.")
                    return results[0]
                else:
                    logging.info(f"No existing index found for user {user_id}, returning default 0.")
                    return 0
    except Exception as e:
        logging.error(f"Failed to fetch quiz index for user {user_id}. Error: {e}")
        return 0


async def update_quiz_score(user_id, score):
    """
    Updates the current score (number of correct answers) for a specific user in the database.
    """
    logging.info(f"Updating score for user {user_id} to {score}.")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR REPLACE INTO quiz_state (user_id, last_score, question_index) 
            VALUES (?, ?, COALESCE((SELECT question_index FROM quiz_state WHERE user_id = ?), 0))
        ''', (user_id, score, user_id))
        await db.commit()


async def get_quiz_data(user_id):
    """
    Fetches both the current question index and the last score for a specific user.
    """
    logging.info(f"Fetching quiz state and score for user {user_id}.")
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index, last_score FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            return await cursor.fetchone()
        