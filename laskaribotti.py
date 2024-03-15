# zulip-run-bot laskaribotti.py --config-file zuliprc.txt

queue = []
queue_uid = []

class LaskariHandler:
    def usage(self) -> str:
        return """
        Kaikki viestin lähettävät laitetaan jonoon.

        Jos viesti on komento, niin jonoon ei laiteta.
        Sallitut komennot ovat:

        - !aloita: lähetä käyttöohjeet kanavalle.
        - !seuraava: poista jonon ensimmäinen ja kerro poistettavan nimi.
        - !jono: printtaa jono.
        """

    def handle_message(self, message, bot_handler):
        sender = message['sender_full_name']
        uid = message['sender_id']
        full_content = message['full_content']
        if full_content[0] == '!':
            if full_content == '!aloita':
                bot_handler.send_message(dict(
                    type='stream',
                    to='etälaskarit',
                    subject='Tervetuloa etälaskareihin',
                    content='Moi! Ylläpidän autettavien jonoa. Jos tarvitset apua, niin pääset jonoon lähettämällä minulle vapaamuotoisen viestin. Paina nimeäni ja valitse "Send direct message". Vapaa assari auttaa sinua tuota pikaa!'
                ))
                bot_handler.send_message(dict(
                    type='stream',
                    to='assarit',
                    subject='Jonotilanne',
                    content='Moi! Ylläpidän autettavien jonoa. Saat seuraavan autettavan nimen lähettämällä minulle yksityisviestin: !seuraava'
                ))
                return
            elif full_content == '!seuraava':
                if len(queue) == 0:
                    bot_handler.send_reply(message, "Jono on tyhjä!")
                    return
                bot_handler.send_reply(message, "Seuraava autettava: @**{}**".format(queue[0]))
                bot_handler.send_message(dict(
                    type='stream',
                    to='assarit',
                    subject='Jonotilanne',
                    content='@**{}** auttaa käyttäjää @**{}**. Jonon pituus: {}'.format(sender,
                                                                                        queue[0],
                                                                                        len(queue) - 1)
                ))
                bot_handler.send_message(dict(
                    type='private',
                    to=[queue_uid[0]],
                    content='@**{}** auttaa sinua hetken kuluttua. Et ole enää jonossa, pääset uudestaan jonoon lähettämällä minulle vapaamuotoisen viestin.'.format(sender,                                                                                                    queue[0],                                                                                                  len(queue) - 1)
                ))
                del queue[0]
                del queue_uid[0]
                return
            elif full_content == '!jono':
                bot_handler.send_reply(message, str(queue))
                return
            bot_handler.send_reply(message, "Komentoa ei tunnistettu.")
            return
        elif sender in queue:
            bot_handler.send_reply(message, "Olet jo jonossa. Paikkasi jonossa: {}.".format(queue.index(sender) + 1))
            return
        # add to queue
        queue.append(sender)
        queue_uid.append(uid)
        bot_handler.send_reply(message, "Sinut on lisätty jonoon. Assari ottaa sinuun pian yhteyttä. Voit miettiä jo valmiiksi lähetätkö kysymyksestäsi esimerkiksi kuvan. Zulipissa voi kirjoittaa matemaattisia kaavoja LaTeXilla. Voit kirjoittaa LaTeXia esimerkiksi Abitin kaavaeditorin avulla (https://math-demo.abitti.fi) ja liittää sen Zulipiin. Voit myös liittää kuvakaappauksia. Paikkasi jonossa: {}.".format(len(queue)))
        bot_handler.send_message(dict(
            type='stream',
            to='assarit',
            subject='Jonotilanne',
            content='@**{}** liittyi jonoon. Jonon pituus: {}'.format(sender,
                                                                      len(queue))
        ))


handler_class = LaskariHandler
