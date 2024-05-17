import os
import sys
import threading
from dotenv import load_dotenv
from typing import Annotated
from twitchio.ext import commands, routines, eventsub
from twitchio.ext.commands.errors import CommandOnCooldown
from twitchio.ext.commands import Command
from tinydb import TinyDB, Query
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.character import Character
from models.event import Event, PassiveEvent, ActiveEvent


CHANNEL = "QQlaPraline_"
DB_COMMANDS = "commands.json"
CHARACTER_DATA_PATH = "../data/character_data.json"
load_dotenv()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token = os.getenv('TOKEN'),
            prefix="!",
            client_secret = os.getenv('CLIENT_SECRET'),
            initial_channels=[CHANNEL],
        )
        self.db = TinyDB(DB_COMMANDS, indent=4)
        self.commands_dict = self.load_custom_commands()
        for command_name, response in self.commands_dict.items():
            self.add_custom_command(command_name, response)
        self.character = Character()
        self.all_event = Event()
        self.passive_event = PassiveEvent()
        self.active_event = ActiveEvent()
        self.open = False
        self.open_choice = False
        


    async def on_commmand_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"Qu'un seul vote !")


    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")
        print(f"Chaine de {CHANNEL}")

    async def event_message(self, message):
        if message.author is None:
            return
        print(f"{message.author.name} : {message.content}")
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
        if not self.open:
            await ctx.send('Pas d evenement')
            return
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
            await ctx.send("Tu n'as pas encore de perso !")

    def progress(self):
        threading.Thread(target=self.start_timer).start()

    def start_timer(self):
        time.sleep(30)
        self.timer = True
        return self.timer
    
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.member)
    @commands.command(name="event")
    async def activate_event(self, ctx: commands.Context):
        state = self.active_event.get_state_event()
        if state == 0:
            event = self.active_event.get_activate_event()
            message = event['descritpion']
            choice = event['choice']
            await ctx.send(message)
            await ctx.send(choice)
            self.active_event.toggle_state_true()
        else:
            await ctx.send("Pas d'event actif !")
        
    @commands.cooldown(rate=1, per=180, bucket=commands.Bucket.member)
    @commands.command(name='1', aliases=('2', '3'))
    async def event_choice(self, ctx: commands.Context):
        state = self.active_event.get_state_event()
        if state == 1:
            user_choice = ctx.message.content.lstrip('!')
            self.active_event.incr_user_choice(user_choice)
            await ctx.send(f"{ctx.author.name} à voté ! ")
        else:
            await ctx.send("Aucun choix en cours")


if __name__ == "__main__":
    bot = Bot()
    bot.run()
