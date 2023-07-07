# 
# Tiramisu Discord Bot
# --------------------
# Mod Applications
# 
import nextcord
from nextcord.ext import menus
import random

from libs import utility, modals, buttons, moderation
from libs.database import Database

class QuestionModal(nextcord.ui.Modal):
    def __init__(self, question: str, callback, responses: dict, question_index: int, timeout=300, min_length = 2, max_length = 300, *args, **kwargs):
        """ Modal for mod application questions """
        super().__init__(f'Create an Application', timeout=timeout)
        self.ext_callback = callback

        # Components
        self.input = nextcord.ui.TextInput(
            label = question,
            min_length = min_length,
            max_length = max_length,
            custom_id = f'tiramisu:{random.randint(1000,9999)}',
            #style = nextcord.TextInputStyle.short,
            *args, **kwargs
        )
        self.add_item(self.input)

        self.question = question
        self.responses = responses
        self.question_index = question_index

    async def callback(self, interaction: nextcord.Interaction):
        await self.ext_callback(interaction, question_index=(self.question_index + 1), responses=self.responses|{self.question: self.input.value}, )

class ContinueConfirmation(menus.ButtonMenu):
    def __init__(self, callback, text: str = '**Continue?**',*args, **kwargs):
        """ Use a button to confirm continuing Questions
        This is a workaround-- because you cannot respond to a modal with another modal """
        super().__init__(disable_buttons_after=True)

        self.text = text
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    async def send_initial_message(self, ctx, channel):
        return await channel.send(self.text, view=self)

    @nextcord.ui.button(label='Answer')
    async def on_button_press(self, button, interaction):
        try:
            self.kwargs['confirmed'] = True
            await self.callback(interaction, *self.args, **self.kwargs)
        except KeyError:
            await self.callback(interaction, *self.args, **self.kwargs, confirmed=True)
        self.stop()


async def create(interaction: nextcord.Interaction, answers: dict = None):
    """ Create an Application """
    db = Database(interaction.guild, reason='Applications, creating application')
    try:
        channel = interaction.guild.get_channel(int(db.fetch('application_channel')))
        if channel == None:
            raise ValueError
    except ValueError:
        await interaction.send(f'Applications are not enabled!\n*To enable them, have and admin set the `application_channel` setting to an appropriate channel.*')
        return

    application_number = db.fetch('application_int')
    if application_number == 'none':
        application_number = 0
    elif application_number.isdigit():
        application_number = int(application_number)
    else:
        application_number = 0
    application_number += 1
    db.set('application_int', str(application_number))
    

    try:
        mention_staff = interaction.guild.get_role(int(db.fetch('staff_role')))
        if mention_staff == None:
            raise ValueError
        mention_staff = f'||{mention_staff.mention}||\n'
    except:
        mention_staff = ''

    thread = await channel.create_thread(name=f'Application #{application_number}', type = nextcord.ChannelType.private_thread, 
        reason=f'Created Application # {application_number} for {interaction.user.name}.')
    if answers == None:
        answer_text = ''
    else:
        answer_text = '\n'
        for question in answers:
            answer_text += f'**{question}:** {answers[question]}\n'

    init = await thread.send(f'**{thread.name}** opened by {interaction.user.mention}\n{mention_staff}{answer_text}\nTo close this application, use the `/application close` slash command.\n\
To add people to the application, simply **@mention** them.')
    await init.pin(reason = 'Initial application message')
    
    await interaction.send(f'*Application Opened in {thread.mention}*')

    db.close()

async def answer_and_create(interaction: nextcord.Interaction, question_index: int = 0, responses: dict = {}, confirmed: bool = False):
    db = Database(interaction.guild, reason='Applications, fetch questions')
    application_questions = db.fetch('application_questions')
    default_questions = [ # Questions cannot be greater than 45 characters
        'Have you moderated a community before?',
        'What is your experience resolving confilicts?',
        'Why are you a good fit for the position?',
        'Why do you want to moderate this server?'
    ]
    if application_questions == 'none':
        questions = default_questions
    else:
        questions_unchecked = application_questions.split(';')
        if questions_unchecked[0] == application_questions:
            questions = default_questions
        else:
            questions = []
            for question in questions_unchecked:
                if len(question) > 45:
                    questions.append(f'{question[0:40]}...')
                else:
                    questions.append(question)

    
    if question_index > (len(questions) - 1):
        await create(interaction, answers=responses)
    elif confirmed:
        await interaction.response.send_modal(QuestionModal(questions[question_index], answer_and_create, responses, question_index))
    else:
        await ContinueConfirmation(answer_and_create, text=f'**Answer the next question? ({question_index + 1}/{len(questions)})**',
            question_index = question_index, responses = responses).start(ctx=None, interaction=interaction, ephemeral=True)



async def is_application(thread: nextcord.Thread or nextcord.Channel, debug: bool = False):
    """ Check if a Thread is a Application
    Returns: bool """
    if debug:
        def negative(reason):
            return False, reason
        def affirmative():
            return True, None
    else:
        def negative(reason):
            return False
        def affirmative():
            return True
    
    if thread.type != nextcord.ChannelType.private_thread:
        return negative('Not a private thread')
    
    db = Database(thread.guild, reason='Applications, checking if thread is application')

    application_channel = db.fetch('application_channel')
    if not application_channel.isdigit():
        return negative('`application_channel` is not set')
    elif int(application_channel) != thread.parent_id:
        return negative('Not a child of `application_channel`.')

    number = thread.name.replace("Application #", "")
    if number.isdigit(): # Check if name is 'Thread #0' etc.
        if not db.fetch('application_int').isdigit():
            return negative('`application_int` is not set! (no applications have been made)')
        if not int(number) <= int(db.fetch('application_int')):
            return negative('Thread number in name is higher than expected')
    else:
        return negative(f'Not named as a thread should be')
    
    return affirmative()

async def get_applicant(thread: nextcord.Thread):
    """ Get the User who created this Application
    This is done by iterating though history near thread creation time (to get the bot's initial message),
     and returning the first user mentioned.
    NOTE: This does NOT check if this thread is an application. """
    
    history = await thread.history(limit=10, around=thread.created_at).flatten()
    for message in history:
        first = message # After
    
    return message.mentions[0]
    
async def close(interaction: nextcord.Interaction):
    """ Close an Application """
    db = Database(interaction.guild, reason='Applications, close application')

    if not await is_application(interaction.channel):
        await interaction.send(f'Run this command in the application you wish to close.', ephemeral=True)
        return
    thread = interaction.channel # interaction is discarded upon response
    user = interaction.user
    await interaction.response.defer()  

    creator = await get_applicant(thread)
    await interaction.send(f'**🎟️ Application Closed.**')
    await thread.edit(name=f'{thread.name} [Closed]', archived=True, locked=True)
    await creator.send(f'Your application, {thread.name} has been closed. You can view it here: {thread.mention}.')
    await moderation.modlog(interaction.guild, '🎟️ Application Closed', interaction.user, creator, additional = {'Thread':thread.mention})

async def accept(interaction: nextcord.Interaction):
    """ Accept an Application and give user the `staff_role`"""
    db = Database(interaction.guild, reason='Applications, accept application')
    
    if interaction.user.id in db.fetch('admins'):
        if not await is_application(interaction.channel):
            await interaction.send('Run this command in the application you wish to accept.', ephemeral=True)
            return

        try:
            staff_role = interaction.guild.get_role(int(db.fetch('staff_role')))
            if staff_role == None:
                raise ValueError
        except ValueError:
            await interaction.send('The `staff_role` setting must be set to use this command.', ephemeral=True)
            return

        thread = interaction.channel
        user = interaction.user
        await interaction.response.defer()

        creator = await get_applicant(thread)
        await interaction.send(f'**✅ Application Accepted!**')
        await thread.edit(name=f'{thread.name} [Closed]', archived=True, locked=True)
        await creator.send(f'**Welcome to the {thread.guild.name} Staff Team**\nYour application, {thread.name} has been accepted!. You can view it here: {thread.mention}.')
        await creator.add_roles(staff_role)
        await moderation.modlog(interaction.guild, '✅ Application Accepted', interaction.user, creator, additional = {'Thread':thread.mention})


    else:
        with open('config/config.yml', 'r') as file:
            cfg = yaml.load(file, Loader=yaml.FullLoader)
        await interaction.send(cfg['messages']['noperm'], ephemeral=True)
