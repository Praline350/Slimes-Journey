def add_custom_command(self, command_name: str, response: str):
        async def custom_command(ctx):
            formatted_response = response.replace("{user}", ctx.author.name)
            await ctx.send(formatted_response)
        setattr(self, f'cmd_{command_name}', custom_command)
        
        self.command(name=command_name)(custom_command)
        # Enregistrez les commandes personnalisées dans le fichier JSON
        self.save_custom_commands()