from tkinter import *
import random
from PIL import Image, ImageTk
from tkinter import messagebox


def stand():
    Game.is_standing = True
    Game.player_total = 0
    Game.dealer_total = 0
    display_second_dealer_card()

    for score in Game.dealer_score:
        Game.dealer_total += score

    for score in Game.player_score:
        Game.player_total += score

    Game.deal_button.config(state='disabled')
    Game.stand_button.config(state='disabled')

    if Game.dealer_total >= 17:
        if Game.dealer_total > 21:
            for card_num, card in enumerate(Game.dealer_score):
                if card == 11:
                    Game.dealer_score[card_num] = 1
                    Game.dealer_total = 0
                    for score in Game.dealer_score:
                        Game.dealer_total += score
                    if Game.dealer_total > 21:
                        Game.blackjack_status['player'] = 'bust'
            display_second_dealer_card()
            messagebox.showinfo('Player Wins!', f'Player: {Game.player_total}  Dealer: {Game.dealer_total}')
        elif Game.dealer_total == Game.player_total:
            display_second_dealer_card()
            messagebox.showinfo('Push', f'Player: {Game.player_total}  Dealer: {Game.dealer_total}')
        elif Game.dealer_total > Game.player_total:
            display_second_dealer_card()
            messagebox.showinfo('Dealer Wins!', f'Player: {Game.player_total}  Dealer: {Game.dealer_total}')
        else:
            display_second_dealer_card()
            messagebox.showinfo('Player wins!', f'Player: {Game.player_total}  Dealer: {Game.dealer_total}')

    else:
        dealer_hit()
        stand()


def display_second_dealer_card():
    dealer_image2 = resize_cards(f'cards/{Game.dealer[1]}.png')
    Game.dealer_label_2.image = dealer_image2
    Game.dealer_label_2.config(image=dealer_image2)


def blackjack_shuffle(player):
    Game.is_standing = False
    Game.player_total = 0
    Game.dealer_total = 0

    if player == "dealer":
        if len(Game.dealer_score) == 2:
            if sum(Game.dealer_score) == 21:
                Game.blackjack_status['dealer'] = 'yes'

    if player == "player":
        if len(Game.player_score) == 2:
            if sum(Game.player_score) == 21:
                Game.blackjack_status['player'] = 'yes'

        else:
            Game.player_total = sum(Game.player_score)
            if Game.player_total == 21:
                Game.blackjack_status["player"] = 'yes'
            elif Game.player_total > 21:
                for card_num, card in enumerate(Game.player_score):
                    if card == 11:
                        Game.player_score[card_num] = 1
                        Game.player_total = 0
                        for score in Game.player_score:
                            Game.player_total += score
                        if Game.player_total > 21:
                            Game.blackjack_status['player'] = 'bust'

                else:
                    if Game.player_total == 21:
                        Game.blackjack_status['player'] = 'yes'
                    if Game.player_total > 21:
                        Game.blackjack_status['player'] = 'bust'

    if len(Game.dealer_score) == 2 and len(Game.player_score) == 2:
        if Game.blackjack_status['dealer'] == 'yes' and Game.blackjack_status['player'] == 'yes':
            display_second_dealer_card()
            messagebox.showinfo('Push!', 'It is a tie!')
            Game.deal_button.config(state='disabled')
            Game.stand_button.config(state='disabled')

        elif Game.blackjack_status['dealer'] == 'yes':
            display_second_dealer_card()
            messagebox.showinfo('Dealer Wins!', f'Player: {Game.player_total}  Dealer: {Game.dealer_total}')
            Game.deal_button.config(state='disabled')
            Game.stand_button.config(state='disabled')

        elif Game.blackjack_status['player'] == 'yes':
            display_second_dealer_card()
            messagebox.showinfo('Player wins!', f'Player: {Game.player_total}  Dealer: {Game.dealer_total}')
            Game.deal_button.config(state="disabled")
            Game.stand_button.config(state="disabled")
    else:
        if Game.blackjack_status['dealer'] == 'yes' and Game.blackjack_status['player'] == 'yes':
            display_second_dealer_card()
            messagebox.showinfo('Push!', 'It is a tie!')
            Game.deal_button.config(state='disabled')
            Game.stand_button.config(state='disabled')

        elif Game.blackjack_status['dealer'] == 'yes':
            display_second_dealer_card()
            messagebox.showinfo('Dealer Wins!', 'Blackjack!')
            Game.deal_button.config(state='disabled')
            Game.stand_button.config(state='disabled')

        elif Game.blackjack_status['player'] == 'yes':
            display_second_dealer_card()
            messagebox.showinfo('Player wins!', "BlackJack!")
            Game.deal_button.config(state="disabled")
            Game.stand_button.config(state="disabled")

    if Game.blackjack_status['player'] == 'bust':
        display_second_dealer_card()
        messagebox.showinfo('Player busts!', f"Player Loses! {Game.player_total}")
        Game.deal_button.config(state="disabled")
        Game.stand_button.config(state="disabled")


# Resize Cards
def resize_cards(card):
    card_image = Image.open(card)
    resized_image = card_image.resize((150, 218))
    our_card_image = ImageTk.PhotoImage(resized_image)

    return our_card_image


# Shuffle the cards
def shuffle():
    Game.player_total = 0
    Game.dealer_total = 0

    Game.blackjack_status = {'dealer': 'no', 'player': 'no'}

    Game.deal_button.config(state="normal")
    Game.stand_button.config(state="normal")

    Game.dealer_label_1.config(image='')
    Game.dealer_label_2.config(image='')
    Game.dealer_label_3.config(image='')
    Game.dealer_label_4.config(image='')
    Game.dealer_label_5.config(image='')

    Game.player_label_1.config(image='')
    Game.player_label_2.config(image='')
    Game.player_label_3.config(image='')
    Game.player_label_4.config(image='')
    Game.player_label_5.config(image='')

    suits = ['diamonds', 'clubs', 'hearts', 'spades']
    values = (range(2, 15))

    Game.deck = []

    for suit in suits:
        for value in values:
            Game.deck.append(f'{value}_of_{suit}')

    Game.dealer = []
    Game.player = []
    Game.dealer_score = []
    Game.player_score = []
    Game.dealer_spot = 0
    Game.player_spot = 0

    dealer_hit()
    dealer_hit(not Game.is_standing)
    player_hit()
    player_hit()

    Game.root.title(f'Blackjack - {len(Game.deck)} cards left')


def dealer_hit(should_obfuscate=False):
    if Game.dealer_spot < 5:
        try:
            dealer_card = random.choice(Game.deck)
            Game.deck.remove(dealer_card)
            Game.dealer.append(dealer_card)
            display_card = dealer_card if not should_obfuscate else 'card_back_black'

            dcard = int(dealer_card.split("_", 1)[0])
            if dcard == 14:
                Game.dealer_score.append(11)
            elif dcard == 11 or dcard == 12 or dcard == 13:
                Game.dealer_score.append(10)
            else:
                Game.dealer_score.append(dcard)

            if Game.dealer_spot == 0:
                dealer_image1 = resize_cards(f'cards/{display_card}.png')
                Game.dealer_label_1.image = dealer_image1
                Game.dealer_label_1.config(image=dealer_image1)
            elif Game.dealer_spot == 1:
                dealer_image2 = resize_cards(f'cards/{display_card}.png')
                Game.dealer_label_2.image = dealer_image2
                Game.dealer_label_2.config(image=dealer_image2)
            elif Game.dealer_spot == 2:
                dealer_image3 = resize_cards(f'cards/{display_card}.png')
                Game.dealer_label_3.image = dealer_image3
                Game.dealer_label_3.config(image=dealer_image3)
            elif Game.dealer_spot == 3:
                dealer_image4 = resize_cards(f'cards/{display_card}.png')
                Game.dealer_label_4.image = dealer_image4
                Game.dealer_label_4.config(image=dealer_image4)
            elif Game.dealer_spot == 4:
                dealer_image5 = resize_cards(f'cards/{display_card}.png')
                Game.dealer_label_5.image = dealer_image5
                Game.dealer_label_5.config(image=dealer_image5)

            Game.dealer_spot += 1

            Game.root.title(f'Blackjack - {len(Game.deck)} cards left')
        except:
            Game.root.title(f'Blackjack - No cards in deck')

        blackjack_shuffle("dealer")


def player_hit():
    if Game.player_spot < 5:
        try:
            player_card = random.choice(Game.deck)
            Game.deck.remove(player_card)
            Game.player.append(player_card)

            pcard = int(player_card.split("_", 1)[0])
            if pcard == 14:
                Game.player_score.append(11)
            elif pcard == 11 or pcard == 12 or pcard == 13:
                Game.player_score.append(10)
            else:
                Game.player_score.append(pcard)

            if Game.player_spot == 0:
                player_image1 = resize_cards(f'cards/{player_card}.png')
                Game.player_label_1.image = player_image1
                Game.player_label_1.config(image=player_image1)
            elif Game.player_spot == 1:
                player_image2 = resize_cards(f'cards/{player_card}.png')
                Game.player_label_2.image = player_image2
                Game.player_label_2.config(image=player_image2)
            elif Game.player_spot == 2:
                player_image3 = resize_cards(f'cards/{player_card}.png')
                Game.player_label_3.image = player_image3
                Game.player_label_3.config(image=player_image3)
            elif Game.player_spot == 3:
                player_image4 = resize_cards(f'cards/{player_card}.png')
                Game.player_label_4.image = player_image4
                Game.player_label_4.config(image=player_image4)
            elif Game.player_spot == 4:
                player_image5 = resize_cards(f'cards/{player_card}.png')
                Game.player_label_5.image = player_image5
                Game.player_label_5.config(image=player_image5)

            Game.player_spot += 1

            Game.root.title(f'Blackjack - {len(Game.deck)} cards left')
        except:
            Game.root.title(f'Blackjack - No cards in deck')

        blackjack_shuffle("player")


def main():
    Game.root.title('Blackjack by Erica')
    Game.root.geometry('1200x800')
    Game.root.configure(background='light blue')
    Game.my_frame.pack(pady=20)
    Game.dealer_frame.pack(padx=20, ipadx=20)
    Game.player_frame.pack(ipadx=20, pady=10)
    Game.dealer_label_1.grid(row=0, column=0, pady=20, padx=20)
    Game.dealer_label_2.grid(row=0, column=1, pady=20, padx=20)
    Game.dealer_label_3.grid(row=0, column=2, pady=20, padx=20)
    Game.dealer_label_4.grid(row=0, column=3, pady=20, padx=20)
    Game.dealer_label_5.grid(row=0, column=4, pady=20, padx=20)
    Game.player_label_1.grid(row=0, column=0, pady=20, padx=20)
    Game.player_label_2.grid(row=0, column=1, pady=20, padx=20)
    Game.player_label_3.grid(row=0, column=2, pady=20, padx=20)
    Game.player_label_4.grid(row=0, column=3, pady=20, padx=20)
    Game.player_label_5.grid(row=0, column=4, pady=20, padx=20)
    Game.button_frame.pack(pady=20)
    Game.shuffle_button.grid(row=0, column=0)
    Game.deal_button.grid(row=0, column=1, padx=10)
    Game.stand_button.grid(row=0, column=2)

    shuffle()
    Game.root.mainloop()


class Game:
    dealer = []
    player = []
    dealer_spot = 0
    player_spot = 0
    player_total = 0
    dealer_total = 0
    player_score = []
    dealer_score = []
    is_standing = False
    blackjack_status = {}
    deck = []
    root = Tk()
    my_frame = Frame(root, bg='light blue')
    dealer_frame = LabelFrame(my_frame, text='Dealer', bd=0)
    player_frame = LabelFrame(my_frame, text='Player', bd=0)
    dealer_label_1 = Label(dealer_frame, text='')
    dealer_label_2 = Label(dealer_frame, text='')
    dealer_label_3 = Label(dealer_frame, text='')
    dealer_label_4 = Label(dealer_frame, text='')
    dealer_label_5 = Label(dealer_frame, text='')
    player_label_1 = Label(player_frame, text='')
    player_label_2 = Label(player_frame, text='')
    player_label_3 = Label(player_frame, text='')
    player_label_4 = Label(player_frame, text='')
    player_label_5 = Label(player_frame, text='')
    button_frame = Frame(root, bg='light blue')
    shuffle_button = Button(button_frame, text='Shuffle Deck', font=('Comic', 16), command=shuffle)
    deal_button = Button(button_frame, text='Hit', font=('Comic', 16), command=player_hit)
    stand_button = Button(button_frame, text='Stand', font=('Comic', 16), command=stand)


if __name__ == '__main__':
    main()
