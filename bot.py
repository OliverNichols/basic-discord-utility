import datetime, discord, os
from discord.ext import commands

from modules.cogs import extensions
from modules.ext import funcs

class MH_Bot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix = '.',
            case_insensitive = True,
            intents=intents
        )

        self.remove_command('help')

        for extension in extensions:
            self.load_extension(f'modules.cogs.{extension}')

        self.before_invoke(self.before)

    def get_formatting(self, ctx, command_name):
        command = self.get_command(command_name)
        return "Usage: **`{}`**".format(f"{ctx.prefix}{command_name} {command.signature}".rstrip()).replace('_', ' ')

    async def on_ready(self):
        self.started_at = datetime.datetime.now()

    async def before(self, ctx):
        await ctx.trigger_typing()
    
    async def on_command_error(self, ctx, error):

        emoji_id = 731202371815866428
        
        if isinstance(error, commands.errors.CommandOnCooldown): 
            message = ' '.join([*str(error).split(' ')[:-1], funcs.format_seconds(float(str(error).split(' ')[-1][:-1]))])
            emoji_id = 857698973015605278

        elif isinstance(error, (commands.errors.BadArgument, commands.errors.MissingRequiredArgument)): 
            message = self.get_formatting(ctx, ctx.command.name)
            ctx.command.reset_cooldown(ctx)

        else: 
            message = "An unhandled exception occurred"
            ctx.command.reset_cooldown(ctx)
                    
        await ctx.send(f"{self.get_emoji(emoji_id)} {message}.", delete_after=10)

bot = MH_Bot()

if __name__ == '__main__':
    bot.run(os.getenv('bot_token'))
