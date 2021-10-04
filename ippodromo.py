def ippodromo(update: Update, context: CallbackContext):

    # da una lista di cavalli predeterminati, scegline n a caso e dammi la lista di questi cavalli, che useremo per gareggiare.
    def genera_cavalli(n, cavalli_esistenti):
        lista_cavalli = []
        cavalli_disponibili = cavalli_esistenti.copy()
        for i in range(n):
            random.shuffle(cavalli_disponibili)
            cavallo = cavalli_disponibili.pop()
            nome = cavallo['name']
            emoji = cavallo['emoji']
            speed_min = cavallo['speed_min']
            speed_max = cavallo['speed_max']
            randomness = cavallo['randomness']
            corse_fatte = cavallo['corse_fatte']
            corse_vinte = cavallo['corse_vinte']
            generazione = cavallo['generazione']
            lista_cavalli.append([i + 1, nome, emoji, speed_min, speed_max, randomness, corse_fatte, corse_vinte, generazione])

        return lista_cavalli

    # data l'emoji, la posizione e la larghezza, crea una riga orizzontale col cavallo che va verso sx
    def make_row(width, emoji, pos, status):
        # spacer = "\_"
        spacer = "_"
        if status == 250:  # Addormentato
            emoji_cavallo = "😴"
        elif status == 200:  # superboost
            emoji_cavallo = "🚀"
        elif status == 350:  # infortunio
            emoji_cavallo = "🤕"
        elif status == 300:  # boost
            emoji_cavallo = "🏍"
        elif status == 450:  # inciampa
            emoji_cavallo = "😖"
        elif status == 300:  # salta
            emoji_cavallo = "🦄"
        elif status == 666:  # fofofinish
            emoji_cavallo = "🐴"
        else:
            emoji_cavallo = "🏇"
        row = []
        rounded_pos = math.floor(pos + 2)
        if rounded_pos >= width + 2:
            rounded_pos = width + 2
            emoji_cavallo = "🏁"
        row.append(emoji)
        # row.append("\|")
        if status == 666:
            row.append("_")
        else:
            row.append("|")
        for i in range(width):
            row.append(spacer)
        # row.append("\|")
        row.append("|")
        row.insert(rounded_pos, emoji_cavallo)
        row.reverse()
        return row

    # data una lista di cavalli (da cui prendere l'emoji e l'ordine) e una lista di posizioni, disegna l'intera gara
    def make_box(width, horse_set: list, horse_pos: list):
        box = []
        for n in range(len(horse_set)):
            row = make_row(width, horse_set[n][2], horse_pos[n][1], horse_pos[n][4])
            box.append(row)
        return box

    # da una lista di posizioni, una lista di cavalli, computa quello che accade e ritorna la lista di posizioni aggiornate e, se qualcuno ha finito, l'ordine di vittoria.
    def move_horses(horse_pos, horse_set, eventi, step):
        speed_min = 3
        speed_max = 4
        randomness = 5
        for n in range(len(horse_set)):

            # horse_pos[n][0] -> corsia
            # horse_pos[n][1] -> posizione
            # horse_pos[n][2] -> nome
            # horse_pos[n][3] -> è ancora in gara? (bool)
            # horse_pos[n][4] -> status (100 = regolare, 200 = infortunio grave, 300 = dopato)
            # horse_pos[n][5] -> ha oltrepassato il traguardo?
            # horse_pos[n][6] -> ha vinto? unused

            if horse_pos[n][5] is False:   # Se è ancora in gara:



                if random.random() < (horse_set[n][randomness] / 50):  # evento megararo

                    if random.random() < 0.5:  # evento cattivo
                        horse_pos[n][4] = 250  # addormentato
                        horse_pos[n][3] = False  # non è più in gara
                        horse_pos[n][5] = True  # ha finito la gara
                        eventi += f"[{step}] {horse_pos[n][2]} si è addormentato... \n"
                        continue  # vai al prossimo cavallo

                    else:  # evento buono
                        eventi += f"[{step}] {horse_pos[n][2]} corre fortissimo e velocissimo!\n"
                        horse_pos[n][4] = 200  # supermegaboost


                elif random.random() < (horse_set[n][randomness] / 20):  # evento raro

                    if random.random() < 0.5:  # evento cattivo
                        horse_pos[n][4] = 350  # infortunato
                        eventi += f"[{step}] {horse_pos[n][2]} si è infortunato!\n"

                    else:  # evento buono
                        horse_pos[n][4] = 300  # dopato
                        horse_set[n][randomness] += 0.05
                        horse_set[n][randomness] = round(horse_set[n][randomness], 2)
                        eventi += f"[{step}] {horse_pos[n][2]} corre fortissimo!\n"


                elif random.random() < (horse_set[n][randomness] / 10):  # evento comune
                    if random.random() < 0.5:  # evento cattivo
                        horse_pos[n][4] = 450  # rallentamento
                        eventi += f"[{step}] {horse_pos[n][2]} inciampa!\n"

                    else:  # evento buono
                        horse_pos[n][4] = 400  # boost
                        eventi += f"[{step}] {horse_pos[n][2]} salta in avanti!\n"

                if horse_pos[n][4] == 200:  # superboost
                    jump = random.uniform(horse_set[n][speed_min], horse_set[n][speed_max]) * 2.5
                    horse_pos[n][1] += jump
                    horse_pos[n][1] = round(horse_pos[n][1], 2)

                elif horse_pos[n][4] == 300:  # boost
                    jump = random.uniform(horse_set[n][speed_min], horse_set[n][speed_max]) * 1.5
                    horse_pos[n][1] += jump
                    horse_pos[n][1] = round(horse_pos[n][1], 2)

                elif horse_pos[n][4] == 350:  # infortunato
                    jump = random.uniform(horse_set[n][speed_min], horse_set[n][speed_max]) / 2
                    horse_pos[n][1] += jump
                    horse_pos[n][1] = round(horse_pos[n][1], 2)
                    # print(f"arrotondato {horse_pos[n][1]}")

                elif horse_pos[n][4] == 400:  # salta in avanti
                    jump = random.uniform(horse_set[n][speed_min], horse_set[n][speed_max]) * 2
                    horse_pos[n][1] += jump
                    horse_pos[n][1] = round(horse_pos[n][1], 2)
                    horse_pos[n][4] = 100

                elif horse_pos[n][4] == 450:  # inciampa, salta il turno
                    horse_pos[n][4] = 100

                else:  # non succede niente, avanti
                    jump = random.uniform(horse_set[n][speed_min], horse_set[n][speed_max])
                    horse_pos[n][1] += jump
                    horse_pos[n][1] = round(horse_pos[n][1], 2)

                if horse_pos[n][1] > 20:  # se è a 20+, ha finito la gara
                    horse_pos[n][5] = True  # ha finito la gara
                    # eventi += f"{horse_pos[n][2]} ha raggiunto il traguardo.\n"
                    continue  # vai al prossimo cavallo
        return horse_pos, eventi

    # aggiunge, dalla lista delle posizioni, alla lista dei vincitori i cavalli che hanno passato pos20. Se sono più di uno, randomizza chi vince.
    def add_winners(horse_pos, winners, eventi, step):
        wins = []

        if not winners:  # IL VINCITORE
            for horse in horse_pos: 
                if horse[1] > 20:  # se è oltre il traguardo
                    wins.append(horse[0])  # aggiungolo

            if len(wins) > 1:  # se ci sono più di un cavallo che ha vinto contemporaneamente a 'sto giro
                random.shuffle(wins)  # randomizziamo
                eventi += f"[{step}] 📸 WOW! Servirà il fotofinish!\n"

        else:
            for horse in horse_pos: 
                if horse[1] > 20: 
                    if horse[0] not in winners:  # se è oltre il traguardo
                        wins.append(horse[0])  # aggiungolo

            if len(wins) > 1:  # se ci sono più di un cavallo che ha vinto contemporaneamente a 'sto giro
                random.shuffle(wins)  # randomizziamo

        for n in wins:
            winners.append(n)

        return winners, eventi

    # apporta modifiche alla lista cavalli permanente dopo ogni gara, applicando bonus/malus e invecchiamento. Resetta i cavalli vecchi, lenti e pazzi.
    def aggiorna_cavalli(horse_pos, winners, cavalli_morti, horse_set, cavalli_esistenti, messaggio):
        # print("dalla funzione", cavalli_esistenti)
        for cavallo in cavalli_esistenti:
            if winners:
                if cavallo['name'] == horse_pos[winners[0]][2]:  # il vincitore
                    n = cavalli_esistenti.index(cavallo)
                    if cavalli_esistenti[n]['speed_min'] < 3:
                        cavalli_esistenti[n]['speed_min'] += 0.1
                        cavalli_esistenti[n]['speed_min'] = round(cavalli_esistenti[n]['speed_min'], 2)
                        cavalli_esistenti[n]['speed_max'] += 0.1
                        cavalli_esistenti[n]['speed_max'] = round(cavalli_esistenti[n]['speed_max'], 2)

                        cavalli_esistenti[n]['randomness'] += 0.03
                        cavalli_esistenti[n]['randomness'] = round(cavalli_esistenti[n]['randomness'], 2)
                    cavalli_esistenti[n]['corse_vinte'] += 1

            for i in cavalli_morti:
                if cavallo['name'] == horse_pos[i][2]:  # i morti
                    n = cavalli_esistenti.index(cavallo)
                    if cavalli_esistenti[n]['speed_min'] > 0.8:
                        cavalli_esistenti[n]['speed_min'] -= 0.1
                        cavalli_esistenti[n]['speed_max'] -= 0.1
                        # cavalli_esistenti[n]['randomness'] -= 0.05
                        # cavalli_esistenti[n]['randomness'] = round(cavalli_esistenti[n]['randomness'], 2)
                        cavalli_esistenti[n]['speed_min'] = round(cavalli_esistenti[n]['speed_min'], 2)
                        cavalli_esistenti[n]['speed_max'] = round(cavalli_esistenti[n]['speed_max'], 2)

            for i in horse_pos:  # tutti i cavalli che hanno gareggiato
                if cavallo['name'] == i[2]:  
                    n = cavalli_esistenti.index(cavallo)
                    cavalli_esistenti[n]['corse_fatte'] += 1
                    if cavalli_esistenti[n]['corse_fatte'] > random.randint(70, 90):
                        # il cavallo è vecchio ed è morto. ne serve uno nuovo
                        messaggio += f"Oh no! {cavallo['name']} è morto di vecchiaia! Dopo soltanto {cavalli_esistenti[n]['corse_fatte']} corse fatte.\n"
                        cavalli_esistenti[n]['speed_min'] = round(random.uniform(1.0, 1.5), 2)
                        cavalli_esistenti[n]['speed_max'] = round(random.uniform(2.0, 3.0), 2)
                        cavalli_esistenti[n]['randomness'] = round(random.uniform(0, 0.25), 2)
                        cavalli_esistenti[n]['corse_fatte'] = 0
                        cavalli_esistenti[n]['corse_vinte'] = 0
                        cavalli_esistenti[n]['generazione'] += 1
                        continue

                    if cavalli_esistenti[n]['randomness'] > 0.65:  # lo uccidiamo perché impazzisce
                        messaggio += f"Oh no! {cavallo['name']} è stato abbattuto perché è impazzito! Dopo soltanto {cavalli_esistenti[n]['corse_fatte']} corse fatte.\n"
                        cavalli_esistenti[n]['speed_min'] = round(random.uniform(1.0, 1.5), 2)
                        cavalli_esistenti[n]['speed_max'] = round(random.uniform(2.0, 3.0), 2)
                        cavalli_esistenti[n]['randomness'] = round(random.uniform(0, 0.25), 2)
                        cavalli_esistenti[n]['corse_fatte'] = 0
                        cavalli_esistenti[n]['corse_vinte'] = 0
                        cavalli_esistenti[n]['generazione'] += 1
                        continue

                    if cavalli_esistenti[n]['speed_min'] + cavalli_esistenti[n]['speed_max'] < 2.5:  # lo abbattiamo perché troppo lento e ce ne prendiamo uno nuovo 
                        messaggio += f"Oh no! {cavallo['name']} è stato abbattuto perché troppo lento! Dopo soltanto {cavalli_esistenti[n]['corse_fatte']} corse fatte.\n"
                        cavalli_esistenti[n]['speed_min'] = round(random.uniform(1.0, 1.5), 2)
                        cavalli_esistenti[n]['speed_max'] = round(random.uniform(2.0, 3.0), 2)
                        cavalli_esistenti[n]['randomness'] = round(random.uniform(0, 0.25), 2)
                        cavalli_esistenti[n]['corse_fatte'] = 0
                        cavalli_esistenti[n]['corse_vinte'] = 0
                        cavalli_esistenti[n]['generazione'] += 1

                    else:  # si invecchia baby!

                        if cavalli_esistenti[n]['corse_fatte'] < 30:
                            cavalli_esistenti[n]['speed_min'] += 0  # è giovane, niente malus di invecchiamento

                        elif cavalli_esistenti[n]['corse_fatte'] < 60:
                            cavalli_esistenti[n]['speed_min'] -= 0.1   # è adulto, malus di invecchiamento
                            cavalli_esistenti[n]['speed_max'] -= 0.1   # è adulto, malus di invecchiamento

                        else:
                            cavalli_esistenti[n]['speed_min'] -= 0.2   # è vecchio, letteralmente deve morire
                            cavalli_esistenti[n]['speed_max'] -= 0.1   # è adulto, malus di invecchiamento

                        cavalli_esistenti[n]['speed_min'] = round(cavalli_esistenti[n]['speed_min'], 2)
                        cavalli_esistenti[n]['speed_max'] = round(cavalli_esistenti[n]['speed_max'], 2)

        return cavalli_esistenti, messaggio

    # simula n gare con i cavalli estratti e restituisce un indice con il numero delle vittorie per ogni cavallo
    def simula_corse(horse_pos: list, horse_set: list, n):
        sim_winners = {}
        for i in range(len(horse_set)):
            sim_winners[i] = 0

        for gara in range(n):
            sim_horse_pos = deepcopy(horse_pos)
            sim_horse_set = deepcopy(horse_set)
            # print("stati iniziali")
            # print(sim_horse_pos)
            # print(sim_horse_set)

            gara_winners = []
            sim_eventi = ""
            sim_race_finished = False
            # print("gara n", gara)
            # print(horse_pos)
            # print(horse_set)
            sim_step = 0
            while sim_race_finished is False:

                sim_step += 1

                # Actual Computation
                sim_horse_pos, sim_eventi = move_horses(sim_horse_pos, sim_horse_set, sim_eventi, sim_step)
                gara_winners, sim_eventi = add_winners(sim_horse_pos, gara_winners, sim_eventi, sim_step)
                # print(sim_horse_pos)
                # print(gara_winners)

                # Ending Condition, someone has won
                if gara_winners:
                    # gara winners is already shuffled in add_winners if there's more than 1 winner
                    sim_winners[gara_winners[0]] += 1
                    sim_race_finished = True
                # Ending condition, everyone is dead
                elif all(not horse[3] for horse in sim_horse_pos):
                    sim_race_finished = True

            # print("finita!")
            # print(sim_horse_pos)
            # print(gara_winners)
            # print(f"gara numero {gara}: vincitore {sim_horse_set[gara_winners[0]][1]}")

        return sim_winners

    # Controlli pre-gara
    # if update.effective_user.id not in config.ADMINS:
    #     update.message.reply_text(f"Per adesso no, scusa.")
    #     return

    if "gara_in_corso" not in context.bot_data:
        context.bot_data["gara_in_corso"] = False

    if has_played_recently(context, "ippodromo", 60):
        update.message.reply_text("Riprova tra un minuto.")
        return

    elif context.bot_data["gara_in_corso"] is True:
        update.message.reply_text(f"C'è gia una gara in corso.")
        return
    else:
        context.user_data["ippodromo"] = time.time()


    # Inizio routine
    context.bot_data["gara_in_corso"] = True
    bot = Bot(config.BOT_TOKEN)
    print(f'{get_now()} [deep_pink3]{update.effective_user.username}[/deep_pink3] in [yellow1]{update.message.chat.title[:10]}[/yellow1] ({str(update.message.chat.id)[4:]}) avvia una gara!')
    transcript = f"{get_now()} TRASCRIZIONE GARA:\n\n"

    cavalli_esistenti = [
        {'name': 'Potato', 'emoji': '🥔', 'speed_min': 1.13, 'speed_max': 2.15, 'randomness': 0.11, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Gargiulo', 'emoji': '👮', 'speed_min': 1.28, 'speed_max': 2.48, 'randomness': 0.18, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Disabile', 'emoji': '♿', 'speed_min': 1.3, 'speed_max': 2.83, 'randomness': 0.18, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Redneck', 'emoji': '🪕', 'speed_min': 1.41, 'speed_max': 2.48, 'randomness': 0.19, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Talebano', 'emoji': '👳', 'speed_min': 1.22, 'speed_max': 2.41, 'randomness': 0.13, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Fatina', 'emoji': '🧚', 'speed_min': 1.29, 'speed_max': 2.18, 'randomness': 0.14, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'SanGennaro', 'emoji': '🩸', 'speed_min': 1.32, 'speed_max': 2.13, 'randomness': 0.06, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Karaoke', 'emoji': '🎤', 'speed_min': 1.2, 'speed_max': 2.76, 'randomness': 0.08, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Cuore Nero', 'emoji': '🖤', 'speed_min': 1.08, 'speed_max': 2.48, 'randomness': 0.13, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'King', 'emoji': '🤴🏼', 'speed_min': 1.03, 'speed_max': 2.40, 'randomness': 0.17, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Pungolo', 'emoji': '🤺', 'speed_min': 1.42, 'speed_max': 2.79, 'randomness': 0.14, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Bomba', 'emoji': '🧕🏾', 'speed_min': 1.44, 'speed_max': 2.9, 'randomness': 0.01, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'AltPolizia', 'emoji': '🤚🏻', 'speed_min': 1.08, 'speed_max': 3, 'randomness': 0.06, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Rizla', 'emoji': '🚬', 'speed_min': 1.31, 'speed_max': 2.8, 'randomness': 0.20, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Maometto', 'emoji': '👳🏿', 'speed_min': 1.26, 'speed_max': 3, 'randomness': 0.21, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Cronometro', 'emoji': '⏲️', 'speed_min': 1.32, 'speed_max': 2.1, 'randomness': 0.22, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Teslo', 'emoji': '🔋', 'speed_min': 1.14, 'speed_max': 2, 'randomness': 0.16, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Salva', 'emoji': '💾', 'speed_min': 1.48, 'speed_max': 2.9, 'randomness': 0.13, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Dago', 'emoji': '🗡️', 'speed_min': 1.17, 'speed_max': 2.01, 'randomness': 0.16, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Covid', 'emoji': '💉', 'speed_min': 1.22, 'speed_max': 2.41, 'randomness': 0.14, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Mortimer', 'emoji': '⚰️', 'speed_min': 1.47, 'speed_max': 2.12, 'randomness': 0.18, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Moai', 'emoji': '🗿', 'speed_min': 1.09, 'speed_max': 2.77, 'randomness': 0.25, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0},
        {'name': 'Lollipop', 'emoji': '🍭', 'speed_min': 1.43, 'speed_max': 2.31, 'randomness': 0.21, 'corse_fatte': 0, 'corse_vinte': 0, 'generazione': 0}
    ]

    if 'cavalli_esistenti' not in context.bot_data:
        context.bot_data['cavalli_esistenti'] = cavalli_esistenti
    else:
        cavalli_esistenti = context.bot_data['cavalli_esistenti']

    # Estrazione cavalli dal roster e preparazione griglia di partenza 
    horse_set = genera_cavalli(6, cavalli_esistenti)
    horse_pos = []
    winners = []

    for n in range(len(horse_set)):
        horse_pos.append([n, 0.00, horse_set[n][1], True, 100, False, False])
    race_finished = False

    # Simulazione di n gare per gli odds:
    sim_results = simula_corse(horse_pos, horse_set, 100)
    sim_odds_list = []

    # Preparazione messaggio pre-gara e compilazione odds
    message_lista_cavalli = "Si preparino i cavalli:\n"
    for n in range(len(horse_set)):

        if sim_results[n] == 0:
            sim_odd = 101
            # print(sim_odd)
        else:
            sim_odd = round(100 / sim_results[n], 2)
        if sim_odd > 2:
            sim_odd = math.trunc(sim_odd)
        sim_odds_list.append([horse_set[n][0], horse_set[n][1], sim_odd])

        message_lista_cavalli += f"{horse_set[n][2]} {horse_set[n][1]} {int_to_roman(horse_set[n][8]+1)}\t(odds: {sim_odd})\n"

    if "odds_list" not in context.bot_data:
        context.bot_data["odds_list"] = sim_odds_list
    context.bot_data["odds_list"] = sim_odds_list

    transcript += f"{message_lista_cavalli}\n"
    transcript += f"Le scommesse sono aperte! Avete un minuto per scommettere sul cavallo vincitore.\nUsate il comando /s o /scommetti <ammontare> <NomeCavallo>.\nLa somma vinta è le'ammontare moltiplicato per gli odds del cavallo.\n"

    bot.send_message(update.message.chat.id, message_lista_cavalli)
    bot.send_message(update.message.chat.id, "Le scommesse sono aperte! Avete un minuto per scommettere sul cavallo vincitore.\nUsate il comando /s o  /scommetti <ammontare> <NomeCavallo>.\nLa somma vinta è l'ammontare moltiplicato per gli odds del cavallo.")

    # Apertura scommesse
    if 'scommesse_aperte' not in context.bot_data:
        context.bot_data['scommesse_aperte'] = True
    context.bot_data['scommesse_aperte'] = True

    time.sleep(60)
    # time.sleep(4)

    # Chiusura scommesse
    context.bot_data['scommesse_aperte'] = False
    context.bot_data["odds_list"] = []
    transcript += f"SCOMMESSE CHIUSE! La gara inizierà fra dieci secondi!\n"
    lista_scommesse = ""

    for scommessa in context.bot_data["scommesse_ippodromo"]:
        user_id = scommessa[1]
        nickname = bot.get_chat_member(update.effective_chat.id, user_id).user.first_name
        name = scommessa[2]
        puntata = scommessa[3]
        odd = scommessa[4]
        vincita = scommessa[5]
        lista_scommesse += f"\n{nickname} ha scommesso ŧ{puntata} su {name.capitalize()} ({odd})\n"


    transcript += f"{lista_scommesse}\n"
    bot.send_message(update.message.chat.id, "SCOMMESSE CHIUSE! La gara inizierà fra dieci secondi!")

    time.sleep(10)

    # Inizio Gara
    message_gara = "3... 2... 1... VIA!"

    gara = bot.send_message(update.message.chat.id, message_gara)
    transcript += f"{message_gara}\n"
    eventi = ""
    gara_id = gara.message_id

    # Loop della gara
    i = 0  # Step Counter
    while race_finished is False:
        i += 1

        # Ending Condition
        if all(horse[5] for horse in horse_pos):  # Non gareggia più nessuno
            race_finished = True
            break

        if winners:  # c'è un vincitore
            race_finished = True
            break

        # Actual Computation
        horse_pos, eventi = move_horses(horse_pos, horse_set, eventi, i)
        winners, eventi = add_winners(horse_pos, winners, eventi, i)

        # Display the box
        box = make_box(20, horse_set, horse_pos)
        edited_message_gara = ""
        for row in box:
            edited_message_gara += "".join(row) + "\n"

        if eventi != "":
            edited_message_gara += "\n"
            edited_message_gara += eventi


        try:
            bot.edit_message_text(f"{edited_message_gara}", update.message.chat.id, gara_id)
            transcript += f"{edited_message_gara}\n\n"
        except TelegramError:
            print("Errore nel mandare il messaggio")
        time.sleep(4)

    # Post Gara
    # Fotofinish

    if len(winners) > 1:

        winners_names = []
        for i in winners:
            winners_names.append(horse_set[i][1])
        winner = winners_names[0]
        random.shuffle(winners_names)

        # print(winners_names)
        # print(f"winner: {winner}")
        # print(horse_set)
        # print(horse_pos)

        finish_horse_set = []
        finish_horse_pos = []

        for horse in horse_pos:
            if horse[2] in winners_names:
                if horse[2] == winner:
                    horse.append("vincitore")
                else:
                    horse.append("perdente")
                horse[4] = 666
                horse[1] = 0
                finish_horse_pos.append(horse)

        for horse in horse_set:
            if horse[1] in winners_names:
                finish_horse_set.append(horse)


        # print(finish_horse_pos)
        # print(finish_horse_set)

        temp = list(zip(finish_horse_pos, finish_horse_set))
        random.shuffle(temp)
        finish_horse_pos, finish_horse_set = zip(*temp)

        message_fotofinish = bot.send_message(update.message.chat.id, "I giudici stanno controllando il fotofinish...")
        transcript += "I giudici stanno controllando il fotofinish...\n"
        fotofinish_id = message_fotofinish.message_id


        for i in range(4):  # 4 step
            box = make_box(3, finish_horse_set, finish_horse_pos)
            edited_finish_message = "📸 REPLAY:\n\n"
            for row in box:
                edited_finish_message += "".join(row) + "\n"

            for horse in finish_horse_pos:
                horse[1] += 1
            if i == 2:
                for horse in finish_horse_pos:
                    if horse[2] != winner:
                        horse[1] -= 1

            bot.edit_message_text(f"{edited_finish_message}", update.message.chat.id, fotofinish_id)
            transcript += f"{edited_finish_message}\n\n"
            time.sleep(3)




    message_classifica = "\n🥇 Vincitore 🥇\n"
    pos = 1
    if winners:
        n = winners[0]
        message_classifica += f"{horse_set[n][2]} {horse_set[n][1]} {int_to_roman(horse_set[n][8]+1)} {'🏍' if horse_pos[n][4] == 300 else ''}{'🚀' if horse_pos[n][4] == 200 else ''}{'🤕' if horse_pos[n][4] == 350 else ''}\n"
        pos += 1
    else:
        message_classifica += f"Nessuno! Ha vinto lo sport."
    bot.send_message(update.message.chat.id, message_classifica)
    transcript += f"{message_classifica}\n\n"

    # calcolo se ci sono e quali sono i cavalli che non hanno attraversato il traguardo (aka morti o altro)
    # cavalli_totali = set(range(len(horse_set)))
    # cavalli_arrivati = set(winners)
    # cavalli_morti = cavalli_totali.difference(cavalli_arrivati) 

    # if cavalli_morti:
    #     message_classifica_morti = "Non classificati:\n"
    #     for n in cavalli_morti:
    #         message_classifica_morti += f"[{pos}]{horse_set[n][2]} {horse_set[n][1]} {int_to_roman(horse_set[n][8]+1)} 😴\n"
    #         pos += 1

    #     bot.send_message(update.message.chat.id, message_classifica_morti)
    #     transcript += f"{message_classifica_morti}\n\n"

    # Aggiorno Statistiche cavalli
    cavalli_morti = set()
    messaggio_abbattuti = ""
    cavalli_esistenti, messaggio_abbattuti = aggiorna_cavalli(horse_pos, winners, cavalli_morti, horse_set, cavalli_esistenti, messaggio_abbattuti)
    if messaggio_abbattuti != "":
        bot.send_message(update.message.chat.id, messaggio_abbattuti)
        transcript += f"{messaggio_abbattuti}\n\n"
    for cavallo in cavalli_esistenti:
        if cavallo['corse_vinte'] != 0 and cavallo['corse_fatte'] != 0:
            cavallo['winrate'] = round(cavallo['corse_vinte'] / cavallo['corse_fatte'], 2)
        else:
            cavallo['winrate'] = 0

    # Pagamento Scommesse
    # [index, user_id, name, importo, odd, vincita]
    # [  0  ,    1   ,  2  ,    3   ,  4 ,    5   ]
    # [1, 456481297, 'king', 10, 16, 160],
    # [3, 456481297, 'schizzo', 20, 8, 160],
    # [5, 456481297, 'bomba', 5, 1.18, 6]
    # ] {horse_set[n][2]} {horse_set[n][1]
    id_cavallo_vincitore = winners[0]
    messaggio_vincitori_scommesse = ""
    for scommessa in context.bot_data["scommesse_ippodromo"]:
        if scommessa[0] == id_cavallo_vincitore:
            user_id = scommessa[1]
            nickname = bot.get_chat_member(update.effective_chat.id, user_id).user.first_name
            name = scommessa[2]
            puntata = scommessa[3]
            vincita = scommessa[5]
            jackpot = check_jackpot(context)
            if scommessa[6] == 1:  # scommessa jackpot
                bot.send_message(update.message.chat.id, f"{nickname} ha vinto il 💰 jackpot di ŧ{jackpot}! 🌟")
                edit_balance_others(jackpot, context.dispatcher, user_id)
                set_jackpot(0, context)
            messaggio_vincitori_scommesse += f"{nickname} ha vinto ŧ{vincita} puntando ŧ{puntata} su {name.capitalize()}!\n"
            edit_balance_others(vincita, context.dispatcher, user_id)
            if add_highest_wins(vincita, user_id, context) is True:
                bot.send_message(update.message.chat.id, "Wow una vincita da record!")
        else:
            if scommessa[6] == 1:  # scommessa jackpot
                jackpot = check_jackpot(context)
                nickname = bot.get_chat_member(update.effective_chat.id, user_id).user.first_name
                bot.send_message(update.message.chat.id, f"{nickname} ha perso l'occasione di vincere il jackpot di ŧ{jackpot}! Peccato!")
            edit_jackpot(math.floor(scommessa[3] / 6), context)
    if messaggio_vincitori_scommesse != "":
        messaggio_vincitori_scommesse += "Tutti gli altri hanno perso!"
    else:
        messaggio_vincitori_scommesse += "Nessuna scommessa vinta. Unico vincitore: lo sport."

    bot.send_message(update.message.chat.id, messaggio_vincitori_scommesse)
    transcript += f"{messaggio_vincitori_scommesse}\n\n"

    URL = "https://hastebin.com"
    response = requests.post(URL + "/documents", transcript.encode('utf-8'))
    r = json.loads(response.text)
    pastebin_url = f"{URL}/raw/{r['key']}"

    update.message.reply_html(f'Riassunto <a href="{pastebin_url}">qui</a>.', disable_web_page_preview=True, quote=False)

    context.bot_data["scommesse_ippodromo"] = []
    context.bot_data["gara_in_corso"] = False

    # TO HERE
    return

def scommetti(update: Update, context: CallbackContext):
    if update.effective_user.id in config.BANS:
        return
    if not (context.bot_data["gara_in_corso"] and context.bot_data['scommesse_aperte']):
        if not context.bot_data["gara_in_corso"]:
            update.message.reply_text("Non c'è nessuna gara in corso.")
            # print(context.bot_data["odds_list"])
        elif not context.bot_data['scommesse_aperte']:
            update.message.reply_text("Le scommesse sono chiuse!")
            # print(context.bot_data["odds_list"])
        return

    odds_list = context.bot_data["odds_list"]
    lista_nomi = []
    for cavallo in odds_list:
        lista_nomi.append(cavallo[1].lower())

    # [
    # [posizione, "nome", 1.1],
    # [posizione2, "nome2", 1.8]
    # ]

    if update.effective_user.id in config.BANS:
        return
    if not context.args: 
        # update.message.reply_text("coglione", quote=False)
        return

    try:
        ammontare = int(context.args[0])
        nome_cavallo = context.args[1].lower()
    except IndexError:
        update.message.reply_text("uso: /scommetti ammontare nomecavallo ", quote=False)
    except ValueError:
        update.message.reply_text("Non capisco la cifra", quote=False)
        return

    if nome_cavallo not in lista_nomi:
        update.message.reply_text("Questo cavallo non sta gareggiando", quote=False)
        return



    if ammontare < 1:
        update.message.reply_text("Coglione", quote=False)
        return

    else:
        if check_balance(context) >= ammontare:
            scommessa = ammontare
            if scommessa > 1000000:
                update.message.reply_text("Scommessa massima: ŧ1000000", quote=False)
                return
        else:
            update.message.reply_text(f"Hai soltanto ŧ{check_balance(context)}.", quote=False)
            return
    nome_cavallo = context.args[1].lower()
    user_id = update.effective_user.id
    indice = lista_nomi.index(nome_cavallo)
    odd = odds_list[indice][2]
    vincita = round(odd * scommessa)
    if "scommesse_ippodromo" not in context.bot_data:
        context.bot_data["scommesse_ippodromo"] = []
    # context.bot_data["scommesse_ippodromo"] = []
    if random.randint(1, 100) == 17:
        scommessa_jackpot = 1
    else:
        scommessa_jackpot = 0
    la_scommessa = [indice, user_id, nome_cavallo, scommessa, odd, vincita, scommessa_jackpot]
    for scommesse in context.bot_data["scommesse_ippodromo"]:
        if (nome_cavallo in scommesse) and (user_id in scommesse):
            update.message.reply_text(f"Hai già una scommessa per questo cavallo.")
            return
    else:
        context.bot_data["scommesse_ippodromo"].append(la_scommessa)
    edit_balance(-scommessa, context)
    # edit_jackpot(math.floor(scommessa / 10), context)
    print(f"{get_now()} [deep_pink3]{update.effective_user.username}[/deep_pink3] in [yellow1]{update.message.chat.title[:10]}[/yellow1] ({str(update.message.chat.id)[4:]}) scommette su un cavallo ({scommessa} su {nome_cavallo})")
    if scommessa_jackpot == 1:
        update.message.reply_text(f"[ŧ{check_balance(context)}] 🧾 Scommessa registrata: ŧ{scommessa} su {context.args[1]}\n🌟 SCOMMESSA JACKPOT 🌟 Se vinci, ti porti a casa anche il jackpot!! 💰")
    else:
        update.message.reply_text(f"[ŧ{check_balance(context)}] 🧾 Scommessa registrata: ŧ{scommessa} su {context.args[1]}")
    return

