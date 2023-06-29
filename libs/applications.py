# 
# Tiramisu Discord Bot
# --------------------
# Mod Applications
# 
import nextcord

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
            style = nextcord.TextInputStyle.paragraph,
            *args, **kwargs
        )
        self.add_item(self.input)

        self.question = question
        self.responses = responses
        self.question_index = question_index

    async def callback(self, interaction: nextcord.Interaction):
        await self.ext_callback(interaction, question_index=(self.question_index + 1), responses=self.responses|{self.question: self.input.value}, )

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

    if buttons:
        raise NotImplementedError
    else:
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

async def answer_and_create(interaction: nextcord.Interaction, question_index: int = 0, responses: dict = None):
    db = Database(interaction.guild, reason='Applications, fetch questions')
    application_questions = db.fetch('application_questions')
    default_questions = [
        'Have you moderated a community before?',
        'How much experience do you have resolving confilicts?',
        'Why do you think you would be a good fit for the position?',
        'Why do you want to be a moderator on this server?'
    ]
    if application_questions == 'none':
        questions = default_questions
    else:
        questions = application_questions.split(';')
        if questions[0] == application_questions:
            questions = default_questions
    
    if question_index > len(questions):
        await create(interaction, answers=responses)
    else:
        await interaction.response.send_modal(QuestionModal(questions[question_index], answer_and_create, responses, question_index))



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

    if not db.fetch('appliation').isdigit():
        return negative('`application_channel` is not set')
    elif int(db.fetch('application_channel')) != thread.parent_id:
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
