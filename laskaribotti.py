# zulip-run-bot laskaribotti.py --config-file zuliprc.txt

queue = []

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
        full_content = message['full_content']
        if full_content[0] == '!':
            if full_content == '!aloita':
                bot_handler.send_message(dict(
                    type='stream',
                    to='etälaskarit',
                    subject='Tervetuloa etälaskareihin',
                    content='Jos tarvitset apua, niin pääset jonoon lähettämällä minulle viestin. Paina nimeäni ja valitse "Send direct message". Vapaa assari auttaa sinua tuota pikaa!'
                ))
                bot_handler.send_message(dict(
                    type='stream',
                    to='assarit',
                    subject='Jonotilanne',
                    content='Ylläpidän autettavien jonoa. Saat seuraavan autettavan nimen lähettämällä minulle viestin: !seuraava'
                ))
                return
            elif full_content == '!seuraava':
                if len(queue) == 0:
                    bot_handler.send_reply(message, "Jono on tyhjä.")
                    return
                bot_handler.send_reply(message, "Seuraava autettava: @**{}**".format(queue[0]))
                del queue[0]
                bot_handler.send_message(dict(
                    type='stream',
                    to='assarit',
                    subject='Jonotilanne',
                    content='Jonon pituus: {}'.format(len(queue))
                ))
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
        bot_handler.send_reply(message, "Sinut on lisätty jonoon. Paikkasi jonossa: {}.".format(len(queue)))
        bot_handler.send_message(dict(
            type='stream',
            to='assarit',
            subject='Jonotilanne',
            content='Jonon pituus: {}'.format(len(queue))
        ))


handler_class = LaskariHandler
