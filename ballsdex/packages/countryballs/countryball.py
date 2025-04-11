import logging
import random
import string
from datetime import datetime

import discord

from ballsdex.core.models import Ball, Special, balls
from ballsdex.packages.countryballs.components import CatchView
from ballsdex.settings import settings

log = logging.getLogger("ballsdex.packages.countryballs")

spwnmsglist = ["A wild cat appeared!", "One fierce feline approached!", "I wonder when bluenights cheap bcdex clone releases.", "zzZzZz- Oh, a silly cat appeared!", "shoutout to benektelse!", "This cat is judging you.", "hi", "Chat, is this cat real?", "This cat wonders if it's in a spawn rave...", "this is not awakened bahamut", "Catch me before i depart!!", "This cat has a 50% chance to be a shiny.", "Consider trying out Icondex!", "This message could be your advertisement!", "Legends say Shinytacotime is still working on Mina...", "say :3 NOW", "This cat is homeless. Give it a home!", "Join the official BCDEX server!", "This cat asked Gabril to NOT be given to Öfen.", "This is a certified cool dudes spawn message", "We can all agree that MattShea is a nice guy!", "You got a Shigong? Give it to snek.", "Hortas is probably the coolest guy in the community", "Gambling soon...", "You better not be farming..", "This cat is so silly", "Do you still remember AFK?", "Do you still remember öland?", "Do you still remember Pachi?", "BCEDEXs fate was unfortunate, but inevitable.", "Maybe this has a rare special? You never know.", "mfw cat spawned", "Unfortunate how theres so little Uber OGs active..", "What are you talking about? I never added a moth.", "Zenith owns the first ever Labyrinth special!", "Dont be a cheetah!", "Shoutout to everyone playing BCDEX! <3", "This cat is looking for Athani", "This cat is looking for Lamia", "This cat is looking for Öfen", "This cat is looking for Gabril", "This cat is looking for Koolnoob", "This cat is looking for Hortas", "This cat is looking for MrMan", "This cat is looking for Zenith", "Do not trust Evilnoob, he might be evil.", "Qotd? Never heard of that word.", "Go play the battle cats now!", "Will anyone ever get a full completion?"]

class CountryBall:
    def __init__(self, model: Ball):
        self.name = model.country
        self.model = model
        self.algo: str | None = None
        self.message: discord.Message = discord.utils.MISSING
        self.caught = False
        self.time = datetime.now()
        self.special: Special | None = None
        self.atk_bonus: int | None = None
        self.hp_bonus: int | None = None

    @classmethod
    async def get_random(cls):
        countryballs = list(filter(lambda m: m.enabled, balls.values()))
        if not countryballs:
            raise RuntimeError("No ball to spawn")
        rarities = [x.rarity for x in countryballs]
        cb = random.choices(population=countryballs, weights=rarities, k=1)[0]
        return cls(cb)

    async def spawn(self, channel: discord.TextChannel) -> bool:
        """
        Spawn a countryball in a channel.

        Parameters
        ----------
        channel: discord.TextChannel
            The channel where to spawn the countryball. Must have permission to send messages
            and upload files as a bot (not through interactions).

        Returns
        -------
        bool
            `True` if the operation succeeded, otherwise `False`. An error will be displayed
            in the logs if that's the case.
        """

        def generate_random_name():
            source = string.ascii_uppercase + string.ascii_lowercase + string.ascii_letters
            return "".join(random.choices(source, k=15))

        extension = self.model.wild_card.split(".")[-1]
        file_location = "./admin_panel/media/" + self.model.wild_card
        file_name = f"nt_{generate_random_name()}.{extension}"
        try:
            permissions = channel.permissions_for(channel.guild.me)
            if permissions.attach_files and permissions.send_messages:
                self.message = await channel.send((random.choice(spwnmsglist)),
                    view=CatchView(self),
                    file=discord.File(file_location, filename=file_name),
                )
                return True
            else:
                log.error("Missing permission to spawn ball in channel %s.", channel)
        except discord.Forbidden:
            log.error(f"Missing permission to spawn ball in channel {channel}.")
        except discord.HTTPException:
            log.error("Failed to spawn ball", exc_info=True)
        return False
