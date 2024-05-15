import os
import sys
from typing import Annotated
from twitchio.ext import commands, routines, eventsub
from twitchio.ext.commands import Command
from tinydb import TinyDB, Query

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.character import Character


CHANNEL = "qqlapraline_"
DB_COMMANDS = "commands.json"
CHARACTER_DATA_PATH = "../data/character_data.json"


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token="hz59p0wmy1h0defv1d41akzcc8la5g",
            prefix="!",
            client_secret="ksmbqk5juc8ur0zwjvel0jro5s37lu",
            initial_channels=[CHANNEL],
        )
        self.db = TinyDB(DB_COMMANDS, indent=4)
        self.commands_dict = self.load_custom_commands()
        for command_name, response in self.commands_dict.items():
            self.add_custom_command(command_name, response)
        self.character = Character()

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")
        print(f"Chaine de {CHANNEL}")

    async def event_message(self, message):
        if message.author is None:
            return
        print(f"Received message: {message.content} from {message.author.name}")
        await super().event_message(message)

    async def send_message(self, ctx, message):
        await ctx.send(message)

    def add_custom_command(self, command_name, response):
        async def custom_command(ctx: commands.Context):
            response_format = response.format(user=ctx.author.name, message=ctx.message.content)
            await ctx.send(response_format)

        command_instance = Command(command_name, custom_command)
        self.add_command(command_instance)

    def load_custom_commands(self):
        all_commands = self.db.all()
        commands_dict = {
            command["name"]: command["response"] for command in all_commands
        }
        return commands_dict

    def save_custom_commands(self, command_name, response):
        self.db.insert({"name": command_name, "response": response})
        self.commands_dict[command_name] = response

    @commands.command(name="add")
    async def viewer_add_command(
        self, ctx: commands.Context, command_name: str, *, response: str
    ):
        self.save_custom_commands(command_name, response)
        self.add_custom_command(command_name, response)
        await ctx.send(f"commande ajouté avec succès")

    @commands.command(name="commands")
    async def list_commands(self, ctx: commands.Context):
        all_commands = self.db.all()
        command_name = [command["name"] for command in all_commands]
        await ctx.send(f"La liste des commandes :  {command_name}")

    @commands.command(name="!")
    async def custom_command(self, ctx: commands.Context, command_name: str):
        if command_name in self.commands_dict:
            response = self.commands_dict[command_name]
            await ctx.send(response)
        else:
            await ctx.send("la commande n'exite pas ")

    def create_custom_command(self, command_name):
        async def command_func(self, ctx: commands.Context):
            response = self.commands_dict.get(
                command_name, "Cette commande n'existe pas"
            )
            await ctx.send(response)

        return commands.command(name=command_name)(command_func)

    def inscription(self, player_name):
        print(player_name)
        character = Character()
        message = character.write_new_character(player_name)
        return message

    @commands.command(name="inscription")
    async def inscription_command(self, ctx: commands.Context):
        # Appel de la fonction d'inscription avec le nom du joueur
        message = self.inscription(ctx.author.name)
        await ctx.send(message)

    @commands.command(name="my")
    async def see_character(self, ctx: commands.Context):

        player_name = ctx.author.name
        data = self.character.get_character_data(player_name)
        if data:
            await ctx.send(f"Statistiques de {player_name}:"
                            f"Level {data['level']}, Attack {data['attack']}, "
                            f"Defense {data['defense']}, Social {data['social']}, "
                            f"Style {data['style']}")
        else:
            await ctx.send("Tu n'as pas de perso")
        


bot = Bot()

bot.run()
