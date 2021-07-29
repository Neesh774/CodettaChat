import random

R_EATING = "I don't like eating anything because I'm a bot obviously!"
R_ADVICE = "If I were you, I would go to the internet and type exactly what you wrote there!"
R_CREATOR = "I was created by Kanishq Kancharla for the GenCyber Agent academy in 2021! He's very cheesy 😏"
R_DISCORD_BOT = 'I dunno man, if you like Discord bots, I think you should check out my creators Discord bot at https://github.com/Neesh774/Beano.'

def unknown():
    response = ["Could you please re-phrase that? ",
                "...",
                "I don't understand.",
                "Excuse me?",
                "Please try asking or saying something else.",
                "What does that mean?"][
        random.randrange(4)]
    return response