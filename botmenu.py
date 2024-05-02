import logging
import discord
from discord.ext import commands
from config import token

logging.basicConfig(level=logging.DEBUG)

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

class Select(discord.ui.Select):
    def __init__(self, ctx: commands.Context, options, placeholder="Sélectionnez une option"):
        self.ctx = ctx
        super().__init__(placeholder=placeholder, options=options)

    async def callback(self, interaction: discord.Interaction):
        try:
            selected_option = interaction.data['values'][0]
            await interaction.response.send_message(f"{selected_option} sélectionnée!", delete_after=3)
        except Exception as e:
            await interaction.response.send_message(f"Oups, une erreur s'est produite : {e}", ephemeral=True, delete_after=3)
            print(f"Error while handling interaction ({interaction.id}) : {e}")

class SelectView(discord.ui.View):
    def __init__(self, ctx: commands.Context, *, current_page=0):
        super().__init__()
        self.ctx = ctx
        self.current_page = current_page
        self.pages = [
            [
                discord.SelectOption(label="Option 1", emoji="😊", description="C'est la première option de la liste!")
            ],
            [
                discord.SelectOption(label="Option 2", emoji="😊", description="C'est la deuxième option de la liste!")
            ],
            [
                discord.SelectOption(label="Option 3", emoji="😊", description="C'est la troisième option de la liste!"),
                discord.SelectOption(label="Option 4", emoji="😊", description="C'est la quatrième option de la liste!")
            
            ]
        ]
        self.make_select()

    def make_select(self):
        self.clear_items()
        select = Select(self.ctx, self.pages[self.current_page], placeholder="Sélectionnez une option")
        self.add_item(select)

        if self.current_page > 0:
            prev_btn = discord.ui.Button(label="Page précédente", style=discord.ButtonStyle.secondary)
            prev_btn.callback = self.handle_previous_page
            self.add_item(prev_btn)

        if self.current_page < len(self.pages) - 1:
            next_btn = discord.ui.Button(label="Page suivante", style=discord.ButtonStyle.secondary)
            next_btn.callback = self.handle_next_page
            self.add_item(next_btn)

    async def handle_previous_page(self, interaction: discord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
        self.make_select()
        await interaction.response.edit_message(view=self)

    async def handle_next_page(self, interaction: discord.Interaction):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
        self.make_select()
        await interaction.response.edit_message(view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.ctx.author.id

@bot.event
async def on_ready() -> None:
    print('Je suis connecté !')

@bot.command()
async def menu(ctx):
    try:
        select_view = SelectView(ctx)
        message = await ctx.send("Menu!", view=select_view)
        select_view.children[0].message = message
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite lors de la création du menu : {e}")

bot.run(token)
