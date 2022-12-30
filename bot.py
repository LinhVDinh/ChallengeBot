import datetime
import discord


# dictionaries to keep track of users
counters = {}       # counter for checkins
last_checkin = {}   # keep a record for last checkin
starter_date = datetime.date(2021,1,1)

async def send_message(message, user_message, is_private):      # on message sent
    # list the commands
    key_words = ['!help', '!challenge', '!checkin', '!leaderboard', '!quit']
    try:
        if user_message in key_words:               # checks if user input is valid
            user_id = str(message.author)           # converts name author name to a string
            current_date = datetime.date.today()    # today's date object
            # list of commands
            if user_message == '!help':
                help = '**Commands:** \n**!challenge** - Enter the challenge\n**!checkin** - Check in to challenge\n**!leaderboard** - Check out current leaderboard\n**!quit** - Drop out of challenge'
                await message.channel.send(help)
            # registers contestants to the challenge
            elif user_message == '!challenge':
                if user_id in counters:                                                         # if contestant's username is already in system
                    await message.channel.send(user_id + " is already registered.")             # send message to channel
                else:
                    newmsg = ('**' + user_id + '**' + " *has entered the challenge* ")          # if the contestant is a new challenger
                    counters[user_id] = 0                                                       # add user to dictionary
                    last_checkin[user_id] = starter_date                                        # add user last check in to dictionary
                    await message.channel.send(newmsg)                                          # send message to channel
            elif user_message == '!checkin':
                if user_id in counters:                                                         # if contestant's username is already in system
                    days_difference = current_date - last_checkin[user_id]                      # difference between last check in and today's date
                    if (days_difference.days) > 0:                                              # if last check in was at least 1 day ago
                        counters[user_id] += 1                                                  # increment counter
                        last_checkin[user_id] = current_date                                    # update last check in date
                        await message.channel.send('**' + user_id + '**' + f' your check in count is now {counters[user_id]}')      # send message
                    else:
                        await message.channel.send('Already checked in today.')                 # check in already happened
                else:
                    await message.channel.send('Challenger is not registered.')                 # the contestant cannot check in because username is not registered
            elif user_message == '!leaderboard':
                keys = list(counters.keys())                                                    # create list of user_ids
                values = list(counters.values())                                                # create list of values from user ids
                leaderboard = ''                                                                # blank string
                for contestants in range(0, len(keys)):                                         # loops to go through all user ids
                    if last_checkin[user_id] != starter_date:                                   # if check is updated, display check in, otherwise, display None
                        leaderboard += keys[contestants] + ':    ' + str(values[contestants]) + '    *Last check in:* **' + str(last_checkin[keys[contestants]]) + '**\n'
                    else:
                        leaderboard += keys[contestants] + ':    ' + str(values[contestants]) + '    *Last check in:* **None**\n'
                if len(leaderboard) == 0:
                    await message.channel.send('No contest!')                                   # display 'No contest' when there are no challengers
                else:
                    await message.channel.send('**Leaderboard:** \n' + leaderboard)
            elif user_message == '!quit':                                                       # delete the user from dictionary
                if user_id in counters:
                    del counters[user_id]
                    await message.channel.send('**' + user_id + '**' + ' *has dropped out of the challenge*')
                else:
                    await message.channel.send('Contestant was not registered.')                # unable to quit if not registered
    except Exception as e:                                                                      # errors
        print(e)

def run_discord_bot():
    TOKEN = 'MTA1NDg3ODA2MTU1Mzc5NTE0NQ.GLzEoi.B_6nY9oFszR0himlUS5y40QHQPSDgLmtgFwWCo'          # token for bot


    intents = discord.Intents.all()
    intents.message_content = True

    client = discord.Client(intents=intents)

    # standard discord
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if user_message[0] == '/':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    @client.event
    async def on_raw_reaction_add(payload):                                                     # when reaction on discord
        message_id = payload.message_id
        if message_id == 1057476734351589488:                                                   # select message id to track reactions
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            if payload.emoji.name == 'crzDoglove':                                              # if this emoji is selected
                role = discord.utils.get(guild.roles, name = 'Challenger')                      # select role challenger to save into role
            elif payload.emoji.name == 'heart':                                                 # if this emoji is selected
                role = discord.utils.get(guild.roles, name = 'Cat')                             # select role Cat to save into role


            if role is not None:                                                                # if there is a role saved
                member = await(await client.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)    # fetch member
                if member is not None:                                                          # if member exist
                    await member.add_roles(role)                                                # assign role to member
                    print("Done")                                                               # print done to verify
                else:
                    print("Member not found.")
            else:
                print("Role not found.")

    @client.event
    async def on_raw_reaction_remove(payload):                                                  # when reaction on discord
        message_id = payload.message_id
        if message_id == 1057476734351589488:                                                   # select message to track reactions
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            if payload.emoji.name == 'crzDoglove':                                              # if this emoji is selected
                role = discord.utils.get(guild.roles, name='Challenger')                        # select role challenger to save into role
            elif payload.emoji.name == 'heart':                                                 # if this emoji is selected
                role = discord.utils.get(guild.roles, name='Cat')                               # select role Cat to save into role


            if role is not None:                                                                # if there is a role saved
                member = await(await client.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)    # fetch member
                if member is not None:                                                          # if member exist
                    await member.remove_roles(role)                                             # assign role to member
                    print("Done")                                                               # print done to verify
                else:
                    print("Member not found.")
            else:
                print("Role not found.")


    client.run(TOKEN)