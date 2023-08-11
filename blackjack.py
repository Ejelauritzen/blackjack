from tkinter import *
import random
from PIL import Image, ImageTk
from tkinter import messagebox

root = Tk()
root.title('Blackjack by Erica')
root.geometry('1200x800')
root.configure(background='light blue')


def stand():
    global dealer, player_total, dealer_total, player_score, dealer_score, is_standing

    is_standing = True
    player_total = 0
    dealer_total = 0
    display_second_dealer_card()

    for score in dealer_score:
        dealer_total += score

    for score in player_score:
        player_total += score

    deal_button.config(state='disabled')
    stand_button.config(state='disabled')


    if dealer_total >= 17:
        if dealer_total > 21:
            for card_num, card in enumerate(dealer_score):
                if card == 11:
                    dealer_score[card_num] = 1
                    dealer_total = 0
                    for score in dealer_score:
                        dealer_total += score
                    if dealer_total > 21:
                        blackjack_status['player'] = 'bust'
            display_second_dealer_card()
            messagebox.showinfo('Player Wins!', f'Player: {player_total}  Dealer: {dealer_total}')
        elif dealer_total == player_total:
            display_second_dealer_card()
            messagebox.showinfo('Push', f'Player: {player_total}  Dealer: {dealer_total}')
        elif dealer_total > player_total:
            display_second_dealer_card()
            messagebox.showinfo('Dealer Wins!', f'Player: {player_total}  Dealer: {dealer_total}')
        else:
            display_second_dealer_card()
            messagebox.showinfo('Player wins!', f'Player: {player_total}  Dealer: {dealer_total}')

    else:
        dealer_hit()
        stand()


def display_second_dealer_card():
    dealer_image2 = resize_cards(f'PNG-cards-1.3/{dealer[1]}.png')
    dealer_label_2.config(image=dealer_image2)

def blackjack_shuffle(player):
    global player_total, dealer_total, player_score, is_standing

    is_standing = False
    player_total = 0
    dealer_total = 0

    if player == "dealer":
        if len(dealer_score) == 2:
            if sum(dealer_score) == 21:
                blackjack_status['dealer'] = 'yes'

    if player == "player":
        if len(player_score) == 2:
            if sum(player_score) == 21:
                blackjack_status['player'] = 'yes'

        else:
            player_total = sum(player_score)
            if player_total == 21:
                blackjack_status["player"] = 'yes'
            elif player_total > 21:
                for card_num, card in enumerate(player_score):
                    if card == 11:
                        player_score[card_num] = 1
                        player_total = 0
                        for score in player_score:
                            player_total += score
                        if player_total > 21:
                            blackjack_status['player'] = 'bust'

                else:
                    if player_total == 21:
                        blackjack_status['player'] = 'yes'
                    if player_total > 21:
                        blackjack_status['player'] = 'bust'

    if len(dealer_score) == 2 and len(player_score) == 2:
        if blackjack_status['dealer'] == 'yes' and blackjack_status['player'] == 'yes':

            display_second_dealer_card()
            messagebox.showinfo('Push!', 'It is a tie!')
            deal_button.config(state='disabled')
            stand_button.config(state='disabled')

        elif blackjack_status['dealer'] == 'yes':
            display_second_dealer_card()
            messagebox.showinfo('Dealer Wins!', f'Player: {player_total}  Dealer: {dealer_total}')
            deal_button.config(state='disabled')
            stand_button.config(state='disabled')

        elif blackjack_status['player'] == 'yes':
            display_second_dealer_card()
            messagebox.showinfo('Player wins!', f'Player: {player_total}  Dealer: {dealer_total}')
            deal_button.config(state="disabled")
            stand_button.config(state="disabled")
    else:
        if blackjack_status['dealer'] == 'yes' and blackjack_status['player'] == 'yes':
            display_second_dealer_card()
            messagebox.showinfo('Push!', 'It is a tie!')
            deal_button.config(state='disabled')
            stand_button.config(state='disabled')

        elif blackjack_status['dealer'] == 'yes':
            display_second_dealer_card()
            messagebox.showinfo('Dealer Wins!', 'Blackjack!')
            deal_button.config(state='disabled')
            stand_button.config(state='disabled')

        elif blackjack_status['player'] == 'yes':
            display_second_dealer_card()
            messagebox.showinfo('Player wins!', "BlackJack!")
            deal_button.config(state="disabled")
            stand_button.config(state="disabled")

    if blackjack_status['player'] == 'bust':
        display_second_dealer_card()
        messagebox.showinfo('Player busts!', f"Player Loses! {player_total}")

        deal_button.config(state="disabled")
        stand_button.config(state="disabled")


# Resize Cards
def resize_cards(card):
    card_image = Image.open(card)

    resized_image = card_image.resize((150, 218))

    global our_card_image
    our_card_image = ImageTk.PhotoImage(resized_image)

    return our_card_image


# Shuffle the cards
def shuffle():
    global blackjack_status, player_total, dealer_total, is_standing
    player_total = 0
    dealer_total = 0

    blackjack_status = {'dealer': 'no', 'player': 'no'}

    deal_button.config(state="normal")
    stand_button.config(state="normal")

    dealer_label_1.config(image='')
    dealer_label_2.config(image='')
    dealer_label_3.config(image='')
    dealer_label_4.config(image='')
    dealer_label_5.config(image='')

    player_label_1.config(image='')
    player_label_2.config(image='')
    player_label_3.config(image='')
    player_label_4.config(image='')
    player_label_5.config(image='')

    suits = ['diamonds', 'clubs', 'hearts', 'spades']
    values = (range(2, 15))

    global deck
    deck = []

    for suit in suits:
        for value in values:
            deck.append(f'{value}_of_{suit}')

    global dealer, player, dealer_spot, player_spot, dealer_score, player_score
    dealer = []
    player = []
    dealer_score = []
    player_score = []
    dealer_spot = 0
    player_spot = 0

    dealer_hit()
    dealer_hit(not is_standing)
    player_hit()
    player_hit()

    root.title(f'Blackjack - {len(deck)} cards left')


def dealer_hit(should_obfuscate=False):
    global dealer_spot
    if dealer_spot < 5:
        try:
            dealer_card = random.choice(deck)
            deck.remove(dealer_card)
            dealer.append(dealer_card)
            display_card = dealer_card if not should_obfuscate else 'card_back_black'

            dcard = int(dealer_card.split("_", 1)[0])
            if dcard == 14:
                dealer_score.append(11)
            elif dcard == 11 or dcard == 12 or dcard == 13:
                dealer_score.append(10)
            else:
                dealer_score.append(dcard)

            global dealer_image1, dealer_image2, dealer_image3, dealer_image4, dealer_image5

            if dealer_spot == 0:
                dealer_image1 = resize_cards(f'PNG-cards-1.3/{display_card}.png')
                dealer_label_1.config(image=dealer_image1)
                dealer_spot += 1
            elif dealer_spot == 1:
                dealer_image2 = resize_cards(f'PNG-cards-1.3/{display_card}.png')
                dealer_label_2.config(image=dealer_image2)
                dealer_spot += 1
            elif dealer_spot == 2:
                dealer_image3 = resize_cards(f'PNG-cards-1.3/{display_card}.png')
                dealer_label_3.config(image=dealer_image3)
                dealer_spot += 1
            elif dealer_spot == 3:
                dealer_image4 = resize_cards(f'PNG-cards-1.3/{display_card}.png')
                dealer_label_4.config(image=dealer_image4)
                dealer_spot += 1
            elif dealer_spot == 4:
                dealer_image5 = resize_cards(f'PNG-cards-1.3/{display_card}.png')
                dealer_label_5.config(image=dealer_image5)
                dealer_spot += 1

            root.title(f'Blackjack - {len(deck)} cards left')
        except:
            root.title(f'Blackjack - No cards in deck')

        blackjack_shuffle("dealer")


def player_hit():
    global player_spot
    if player_spot < 5:
        try:
            player_card = random.choice(deck)
            deck.remove(player_card)
            player.append(player_card)

            pcard = int(player_card.split("_", 1)[0])
            if pcard == 14:
                player_score.append(11)
            elif pcard == 11 or pcard == 12 or pcard == 13:
                player_score.append(10)
            else:
                player_score.append(pcard)

            global player_image1, player_image2, player_image3, player_image4, player_image5

            if player_spot == 0:
                player_image1 = resize_cards(f'PNG-cards-1.3/{player_card}.png')
                player_label_1.config(image=player_image1)
                player_spot += 1
            elif player_spot == 1:
                player_image2 = resize_cards(f'PNG-cards-1.3/{player_card}.png')
                player_label_2.config(image=player_image2)
                player_spot += 1
            elif player_spot == 2:
                player_image3 = resize_cards(f'PNG-cards-1.3/{player_card}.png')
                player_label_3.config(image=player_image3)
                player_spot += 1
            elif player_spot == 3:
                player_image4 = resize_cards(f'PNG-cards-1.3/{player_card}.png')
                player_label_4.config(image=player_image4)
                player_spot += 1
            elif player_spot == 4:
                player_image5 = resize_cards(f'PNG-cards-1.3/{player_card}.png')
                player_label_5.config(image=player_image5)
                player_spot += 1

            root.title(f'Blackjack - {len(deck)} cards left')
        except:
            root.title(f'Blackjack - No cards in deck')

        blackjack_shuffle("player")


def deal_cards():
    try:
        card = random.choice(deck)
        deck.remove(card)
        dealer.append(card)
        global dealer_image
        dealer_image = resize_cards(f'PNG-cards-1.3/{card}.png')
        dealer_label.config(image=dealer_image)

        card = random.choice(deck)
        deck.remove(card)
        player.append(card)
        global player_image
        player_image = resize_cards(f'PNG-cards-1.3/{card}.png')
        player_label.config(image=player_image)

        root.title(f'Blackjack - {len(deck)} cards left')

    except:
        root.title(f'Blackjack - No cards in deck')


my_frame = Frame(root, bg='light blue')
my_frame.pack(pady=20)

# Create frames for cards
dealer_frame = LabelFrame(my_frame, text='Dealer', bd=0)
dealer_frame.pack(padx=20, ipadx=20)

player_frame = LabelFrame(my_frame, text='Player', bd=0)
player_frame.pack(ipadx=20, pady=10)

# Put cards in frames
dealer_label_1 = Label(dealer_frame, text='')
dealer_label_1.grid(row=0, column=0, pady=20, padx=20)

dealer_label_2 = Label(dealer_frame, text='')
dealer_label_2.grid(row=0, column=1, pady=20, padx=20)

dealer_label_3 = Label(dealer_frame, text='')
dealer_label_3.grid(row=0, column=2, pady=20, padx=20)

dealer_label_4 = Label(dealer_frame, text='')
dealer_label_4.grid(row=0, column=3, pady=20, padx=20)

dealer_label_5 = Label(dealer_frame, text='')
dealer_label_5.grid(row=0, column=4, pady=20, padx=20)

player_label_1 = Label(player_frame, text='')
player_label_1.grid(row=0, column=0, pady=20, padx=20)

player_label_2 = Label(player_frame, text='')
player_label_2.grid(row=0, column=1, pady=20, padx=20)

player_label_3 = Label(player_frame, text='')
player_label_3.grid(row=0, column=2, pady=20, padx=20)

player_label_4 = Label(player_frame, text='')
player_label_4.grid(row=0, column=3, pady=20, padx=20)

player_label_5 = Label(player_frame, text='')
player_label_5.grid(row=0, column=4, pady=20, padx=20)

# Create buttons
button_frame = Frame(root, bg='light blue')
button_frame.pack(pady=20)

shuffle_button = Button(button_frame, text='Shuffle Deck', font=('Comic', 16), command=shuffle)
shuffle_button.grid(row=0, column=0)

deal_button = Button(button_frame, text='Hit', font=('Comic', 16), command=player_hit)
deal_button.grid(row=0, column=1, padx=10)

stand_button = Button(button_frame, text='Stand', font=('Comic', 16), command=stand)
stand_button.grid(row=0, column=2)

shuffle()

root.mainloop()
