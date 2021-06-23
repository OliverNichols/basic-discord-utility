import datetime, os
from discord.ext import commands

from modules.cogs import extensions

class MH_Bot(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix = ';',
            case_insensitive = True,
            chunk_guilds_at_startup = False
        )

        self.remove_command('help')

        for extension in extensions:
            self.load_extension(f'modules.cogs.{extension}')

        self.before_invoke(self.before)

    async def on_ready(self):
        self.started_at = datetime.datetime.now()

    async def before(self, ctx):
        await ctx.trigger_typing()

bot = MH_Bot()

if __name__ == '__main__':
    bot.run(os.getenv('mh_bot_token'))
