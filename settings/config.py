from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
HOST = env.str("HOST")
DATABASE_NAME = env.str("DATABASE_NAME")
PORT = env.int('PORT') or 5000
GROUP_ID = env.int('GROUP_ID')
