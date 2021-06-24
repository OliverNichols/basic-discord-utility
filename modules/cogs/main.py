import datetime, discord, gspread, traceback
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

from ..ext import constants, funcs

class Main(commands.Cog):

    document_name = "Fast wins calculation"
    sheet_number = 1

    cell_refs = {
        'NA': 'BA3',
        'EU': 'BA4'
    }

    def __init__(self, bot):
        self.bot = bot

        scope = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)

        self.google_client = gspread.authorize(creds)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def get(self, ctx, *, na_or_eu:funcs.value_in(['na','eu'])):
        "Ping all players that have not yet participated in today's CW from a specific region."

        region = na_or_eu
        
        sheet = self.google_client.open(self.document_name).worksheets()[self.sheet_number-1]
        cell = self.cell_refs[region.upper()]

        try: 
            data = sheet.get(cell)[0][0]
            
            for ping in filter(None, data.split(', ')):
                name = ping.split('#')[0][1:]

                member = discord.utils.get(ctx.guild.members, name=name)
                if member: data = data.replace(ping, member.mention)
            
        except IndexError: data = f"No data found on sheet {self.sheet_number}, cell {cell}."
        
        await ctx.send(f"**Remaining Players from {region.upper()}:** {data}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx):
        "Reload the bot's modules - currently can only be used by the owner."
        try:
            for extension in tuple(self.bot.extensions):
                self.bot.reload_extension(extension)

            await ctx.send("Successfully reloaded.", delete_after=5)

        except Exception:
            traceback.print_exc()

            await ctx.send("Failed to reload.", delete_after=5)

    @commands.command()
    async def ping(self, ctx):
        "Check the bot's latency and up-time."
        if funcs.isdigit(self.bot.latency): latency = int(self.bot.latency*1000)
        else: latency = 0

        if hasattr(self.bot, 'started_at'): up_time = (datetime.datetime.now()-self.bot.started_at).total_seconds()
        else: up_time = 0
        
        embed = discord.Embed(color=constants.green, title="Pong! :ping_pong:", description=f"**Latency:** {latency}ms | **Up-time:** {funcs.format_seconds(up_time)}")

        if not up_time: 
            embed.color = constants.orange
            if not up_time: embed.set_footer(text=f"The bot is currently still coming online.")
        elif latency > 200: embed.color = constants.red

        response = await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, *, command_name:str.lower=None):
        "Check brief information about the bot and its commands."
        embed = discord.Embed(color=constants.blue, title="Help")

        if command_name:
            command = self.bot.get_command(command_name)

            if command:
                embed.description = '\n'.join(filter(None, [
                    command.callback.__doc__,
                    self.bot.get_formatting(ctx, command.name)
                ]))

            else:
                embed = discord.Embed(color=constants.red, description="Command not found.", delete_after=5)

        else:
            embed.add_field(
                name = "**Description**",
                value = "A basic Discord bot created by Ollie for some utility functions related to clan wars.",
                inline = False
            )

            embed.add_field(
                name = "**Commands**",
                value = ', '.join(map("`{}`".format, filter(lambda x:not x.hidden, self.bot.commands)))
            )


        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Main(bot))

def teardown(bot):
    bot.remove_cog('Main')