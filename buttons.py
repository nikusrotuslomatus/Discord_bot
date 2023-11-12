import settings
import discord
from  settings import *
from discord.ext import commands
from discord import app_commands

gamers=[]
flag= False
async def start_game():
    global films
    global gamers
    gamers = set(gamers)
    gamers = list(gamers)
    spy_index = int(randint(0, len(gamers)-1))
    i = randint(0, len(films))
    for j in range(len(gamers)):
        if gamers[j] is not None and j != spy_index:
            await gamers[j].send(f"Твой фильм\n{films[i]}")
        else:
            await gamers[j].send("Ты шпион")
    films.pop(i)

class SimpleView(discord.ui.View):
    foo: bool = None

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        await self.message.channel.send("Timedout")
        await self.disable_all_items()

    @discord.ui.button(label="Join",
                       style=discord.ButtonStyle.success)
    async def join_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        gamers.append(interaction.user)
        await interaction.user.send("Вы присоединились к игре")


    @discord.ui.button(label="Leave",
                       style=discord.ButtonStyle.red)
    async def leave_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        for i in gamers:
            if i == interaction.user:
                gamers.remove(interaction.user)
                await interaction.user.send("Вы покинули игру")
                await interaction.deferUpdate()
            else:
                await interaction.user.send("Вы не учавствуете в игре")
                await interaction.deferUpdate()

    @discord.ui.button(label="Start",
                       style=discord.ButtonStyle.blurple)
    async def start_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        await start_game()

    @discord.ui.button(label="Голосование",
                       style=discord.ButtonStyle.danger)
    async def spy(self, interaction: discord.Interaction, button: discord.ui.Button):
        for i in gamers:
           await interaction.response.send_message(i.avatar)


    async def clear_chat(ctx, count=1, answer=True):
        await ctx.channel.purge(limit=count + 1)


