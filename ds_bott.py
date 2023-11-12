from settings import *
import buttons

gamers = buttons.gamers


# когда добавится playlist нужно проверить обработку в функции repeat и play_music
# to do сделай обработку доп сообщений
# добавить гиперссылку для current song отчета
class _youtube:
    def __init__(self, ctx=None):
        self.ctx = ctx
        self.playlist = [ ]

    async def create_connection(self):
        global vc
        voice_channel = None
        try:
            voice_channel = self.ctx.message.author.voice.channel
        except:
            await self.ctx.channel.send("Не знаю куда подключаться")
            return None
        try:
            vc = await voice_channel.connect()
        except:
            # await self.ctx.channel.send("Что то пошло не так(")
            print("error_voice_channel_connect")
        return vc

    async def _create_place_in_playlist(self, ctx):
        global mas_playlist
        mas_playlist.append({
            "is_playing": False,
            "guild": ctx.author.guild,
            "tracks": [ ]
        })

    async def add_song_to_playlist(self, song, ctx):
        global mas_playlist
        tmp_flag = False
        if len(mas_playlist) == 0:
            await self._create_place_in_playlist(ctx)
            mas_playlist[ 0 ][ "tracks" ] = [ song ]
        else:
            for i in mas_playlist:
                if i[ "guild" ] == ctx.author.guild:
                    temporary_mas_for_tracks = i[ "tracks" ]
                    temporary_mas_for_tracks.append(song)
                    i[ "tracks" ] = temporary_mas_for_tracks
                    tmp_flag = True
            if not tmp_flag:
                await self._create_place_in_playlist(ctx)
                mas_playlist[ -1 ][ "track" ] = list(song)


@client.command(name="play_music", aliases=[ "play" ])
async def play_music(ctx, arg):
    global vc
    global mas_playlist
    new_class = _youtube()
    new_class.ctx = ctx
    try:
        vc = await new_class.create_connection()
    except:
        return
    if vc == None:
        return
    await new_class.add_song_to_playlist(arg, ctx)
    i = await find_my_playlist(ctx)
    if i[ "is_playing" ] == False:
        await play_playlist(ctx)


async def play_playlist(ctx):
    global vc
    tmp_playlist = None
    for i in range(len(mas_playlist)):
        if mas_playlist[ i ][ "guild" ] == ctx.author.guild:
            if len(mas_playlist[ i ][ "tracks" ]) != 0:
                tmp_playlist = mas_playlist[ i ][ "tracks" ]
                mas_playlist[ i ][ "tracks" ] = mas_playlist[ i ][ "tracks" ][ 1: ]
                mas_playlist[ i ][ "is_playing" ] = True

            else:
                await ctx.channel.send("Я закончил проигрывать музыку")
                mas_playlist[ i ][ "is_playing" ] = False
                await vc.disconnect()
                return

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(tmp_playlist[ 0 ], download=False)
    URL = info[ 'formats' ][ 0 ][ 'url' ]
    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source=URL, **FFMPEG_OPTIONS))
    # await clear_chat(ctx,1,False)
    await ctx.channel.send("По просьбе " + str(ctx.author.mention) + " играет: " + str(info[ 'title' ]))
    while vc.is_playing():
        i = await find_my_playlist(ctx)
        if i[ "is_playing" ] == False:
            return
        await sleep(10)
    await play_playlist(ctx)


@client.command(name="testb", aliases=[ "button" ])
async def button(ctx):
    view = buttons.SimpleView(timeout=50)

    # button = discord.ui.Button(label="Click me")
    # view.add_item(button)

    message = await ctx.send(view=view)
    view.message = message

    await view.wait()


@client.command(name="disconnect_from_channel", aliases=[ "stop" ])
async def disconnect_from_channel(ctx):
    global mas_playlist
    for i in range(len(mas_playlist)):
        if mas_playlist[ i ][ "guild" ] == ctx.author.guild:
            mas_playlist[ i ][ "tracks" ] = [ ]
    await ctx.voice_client.disconnect()


async def find_my_playlist(ctx):
    global mas_playlist
    for i in mas_playlist:
        if i[ "guild" ] == ctx.author.guild:
            return i


@client.command(name="connect_to_user_channel", aliases=[ "join" ])
async def connect_to_user_channel(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()
        await ctx.send("Я вошел")


@client.event
async def on_guild_join(guild):
    pass


def del_cmd_str(stroke: str):
    str = stroke
    str = str.replace(prefix, '')
    global command_list
    for i in command_list:
        str = str.replace(i, '')
    if str[ 0 ] == " ":
        str = str.replace(' ', '', 1)

    return (str)


# доделать и закинуть в файл, а то треш-------------------------------------------------------------------------
@client.command(name="help_menu", aliases=[ "help" ])
async def help_menu(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title="Навигация по командам", colour=discord.Colour.from_rgb(139, 0, 0))
    # emb.set_image(url="https://citaty.info/files/quote-pictures/574462-saga-o-vinlande-vinland-saga.png")
    emb.set_thumbnail(url=client.user.avatar_url)
    emb.set_footer(text="Thanks you for using bot",
                   icon_url="https://tengyart.ru/wp-content/uploads/2019/07/Tors-vinland-saga-anime.jpg")
    emb.add_field(name='{}cls'.format(prefix), value="Очистка n сообщений чата")
    emb.add_field(name='{}fuck'.format(prefix), value="Буллинг Оли(только для мужиков)")
    emb.add_field(name='{}story'.format(prefix),
                  value="Узнай сколько сообщений отправил на сервер(Аккуратно, долго работает)")
    emb.add_field(name='{}date'.format(prefix), value="Узнай, когда ты создал свой дискорд аккаунт")
    emb.add_field(name='{} + who/кто/кого'.format(prefix), value="Выбор случайного человека")
    emb.add_field(name='{}help'.format(prefix), value="Вызов этой таблицы")
    emb.add_field(name='{}play'.format(prefix), value="+ youtube URL")
    await ctx.send(embed=emb)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command(name='date_of_account', aliases=[ 'date' ])
async def date_of_account(ctx):
    if ctx.author == client.user:
        return
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(str(ctx.author.mention)
                           + "\nДата создания твоего аккаунта:"
                           + "\n" + str(ctx.author.created_at))


@client.command(name='bulling', aliases=[ 'fuck' ])
async def bulling(ctx):
    global flag_for_bulling_olya
    if ctx.author.discriminator != olyas_tag:
        if flag_for_bulling_olya == False:
            await ctx.channel.send("Режим буллинга женщин включен")
            flag_for_bulling_olya = True
        else:
            flag_for_bulling_olya = False
            await ctx.channel.send("Режим буллинга женщин выключен")


@client.command(name="count_of_messages", aliases=[ "story" ])
async def count_of_messages(ctx):
    counter = 0
    text_channels = ctx.guild.text_channels
    async with ctx.channel.typing():
        for text_channel in text_channels:
            async for mess in text_channel.history(limit=2000):
                if mess.author == ctx.author:
                    counter += 1
        await ctx.channel.send(counter)
        return


@client.command(name="clear_chat", aliases=[ "cls" ])
@commands.has_permissions(administrator=True)
async def clear_chat(ctx, count=10, answer=True):
    strategy = ("у" * (int(count) % 10 == 1)) + ("и" * (int(count) % 10 in [ 2, 3, 4 ]))
    await ctx.channel.purge(limit=count + 1)
    if answer:
        await ctx.send(f"{ctx.author.mention}успешно удалил {count} строк{strategy}")


@client.command(name="spam_chat", aliases=[ "spam" ])
@commands.has_permissions(administrator=True)
async def spam_chat(ctx, count=10):
    count = min(count, 60)
    for i in range(count):
        await asyncio.sleep(rn.random() / 2)
        try:
            await ctx.send(''.join([ chr(rn.randint(4000, 5000)) for i in range(rn.randint(4, 13)) ]))
        except:
            await ctx.send("1")


@client.command(name="random_man", aliases=[ "who" ])
async def random_man(ctx, stroke=""):
    member_list = ctx.guild.members
    current_member = member_list[ rn.randint(0, len(member_list)) ]
    if stroke == "":
        await ctx.channel.send(
            f"Я уверен, что{current_member.mention}{del_cmd_str(ctx.message.content) * (len(stroke) != 0)}")
    else:
        await ctx.channel.send(f"Я уверен, что{current_member.mention}{del_cmd_str(stroke)}")


@client.command(name="test_command", aliases=[ "test" ])
async def test_command(ctx):
    # global last_played_song_arg
    # last_played_song_arg += 1
    # print(last_played_song_arg)
    # await ctx.channel.send(ctx.message.author.id)
    # sasha = client.get_user(int(ctx.message.author.id))
    # for user in client.users:
    #  user.get(ctx.message.author.id).send("someMessage")
    await ctx.message.author.send("hui")


@client.command(name="send_list_of_films", aliases=[ "sendl" ])
async def send_list_of_films(ctx):
    with open("moviesdoneright.txt", "rb") as file:
        await ctx.message.author.send("Вот список доступных для игры фильмов:",
                                      file=discord.File(file, "moviesdoneright.txt"))


@client.command(name="add_word", aliases=[ "add" ])
@commands.has_permissions(administrator=True)
async def add_word(ctx):
    with open("moviesdoneright.txt", "a", encoding="utf-8") as file:
        if (not _find_find_word_in_list(ctx.message.content)):
            file.write("\n")
            file.write(ctx.message.content[ 5: ])
            await ctx.channel.send("Done")
        else:
            await ctx.channel.send(
                f"Такой фильм:{del_cmd_str(ctx.message.content)}: не был добавлен, проверьте результат с помощью -sendl")


# Затестить повторения _________________________________________________________________________________________________
@client.command(name="add_all_word", aliases=[ "add_all" ])
@commands.has_permissions(administrator=True)
async def add_all_word(ctx):
    with open("moviesdoneright.txt", "a", encoding="utf-8") as file:
        msg_films = del_cmd_str(ctx.message.content).split(',')
        black_list = str()
        for i in msg_films:
            if not _find_find_word_in_list(i):
                file.write("\n")
                file.write(i)
            else:
                black_list += i + " "
        if len(black_list) == 0:
            await ctx.channel.send("Done")
        else:
            await  ctx.channel.send(
                f"Список фильмов которые не были добавлены:{black_list} проверьте результат с помощью -sendl")


def _find_find_word_in_list(str):
    try:
        with open("moviesdoneright.txt", "r", encoding="utf-8") as file:
            str = del_cmd_str(str.replace(' ', '')).lower()
            repeats = 0
            for i in file:
                tmp = i.replace(' ', '').lower()
                if tmp == str or tmp in str or str in tmp or len(tmp) > 30:
                    return 1
            if len(str) >= 10 and i[ :(len(i) / 2 + 2) ] in str[ :(len(str) / 2 + 2) ] or str[
                                                                                          :(len(str) / 2 + 2) ] in i[ :(
                    len(i) / 2 + 2) ]:
                return 1

            return 0
    except:
        pass


@client.event
async def on_message(ctx):
    global flag_for_bulling_olya
    if ctx.author == client.user:
        return
    stroke = ctx.content.lower()
    guild = ctx.guild
    if flag_for_bulling_olya:
        if str(ctx.author.discriminator) == olyas_tag and ctx.content != prefix + "fuck":
            await ctx.channel.send("Молчать женщина")
    if stroke.startswith(prefix + "кто") or stroke.startswith(prefix + "кого"):
        await random_man(ctx, stroke)

    # супер важная строка,которая отдает приоритет выполнения функциям с декоратором command
    await client.process_commands(ctx)


"""@client.listen("play_music")
async def _test_listen (ctx):
    await ctx.channel.send("123")
    print("123")"""

client.run(TOKEN)
