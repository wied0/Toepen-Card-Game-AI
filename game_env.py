import numpy as np
import random


class Rules:
    @staticmethod
    def suits(kleurbekend, cards):
        suits = np.array([])
        if not kleurbekend:
            return cards
        else:
            for card in cards:
                suits = np.append(suits, card.split(' ')[1])
            if kleurbekend in suits:
                index_suits = np.where(kleurbekend == suits)[0]
                return cards[index_suits]
            else:
                return cards

    @staticmethod
    def goed_kaart(set_van_kaarten, gespeelde_kaart):
        if gespeelde_kaart in set_van_kaarten:
            return True
        else:
            return False


class Player(Rules):
    def play_card(self, player, cards, kleur):
        cards = self.suits(kleur, cards)
        if not kleur:
            print(f"{player} je mag kleur bekennen")
            print(f"Je kaarten zijn {cards}")
            while True:
                card_played = input()
                _ = self.goed_kaart(cards, card_played)
                if _:
                    break
                else:
                    print("Deze kaart heb je niet.")
            return str(card_played).upper()

        if kleur:
            print(f"Je moet een schut leggen van {kleur}")
            print(f"{player} kies een kaart uit {cards}")
            card_played = input()
            return str(card_played).upper()


class GameEnv(Rules):
    set_of_cards = np.array([])
    best_to_worst = np.array([])
    point = 1

    def __init__(self, player_names):
        self.players = list(player_names)
        print("Getting combinations \n")
        self.combinations()
        print("Initializing players")
        self.initialize_players(player_names)

    def initialize_players(self, *player_names):
        player_names = player_names[0]
        for name in player_names:
            self.__setattr__(f"{name}", self.shuffle_deal())
            self.__setattr__(f"{name}_points", 1)
        return self

    def round(self):
        first_to_start = self.players[random.randint(0, 2)]
        max_num_rounds = 4
        ronde = 1
        while ronde < max_num_rounds:
            setattr('toep', False)
            kleur_bekennen = None
            _players = self.players.copy()
            kaarten_en_namen = {}
            self.toep(getattr(self, 'toep'), first_to_start)
            if not getattr(self, 'toep'):
                played_card = self.play_card(first_to_start,
                                             getattr(self, first_to_start),
                                             kleur_bekennen)
                kaarten_en_namen[first_to_start] = played_card
                self.remove_card(first_to_start, played_card)
                _players.remove(first_to_start)
                kleur_bekennen = played_card.split(" ")[1]


                for player in _players:
                    played_card = self.play_card(player,
                                                 getattr(self, player),
                                                 kleur_bekennen)
                    self.remove_card(player, played_card)


                    if played_card.split(' ')[1] == kleur_bekennen:
                        kaarten_en_namen[player] = played_card
                gespeelde_kaarten = kaarten_en_namen.values()
                index_ = np.array([], dtype=np.int8)
                for card in gespeelde_kaarten:
                    index_ = np.append(index_, self.index(card))
                winner = self.winner(index_, kaarten_en_namen)
                first_to_start = winner
                ronde += 1



    def remove_card(self, player, card_played):
        index = np.where(getattr(self, player) == card_played)
        setattr(self, player, np.delete(getattr(self, player), index))
        return self

    def toep(self, toep, player):
        if not toep:
            print("Wil je toepen?")
            toep = input('[y/n]: ')
            if toep == 'y':
                GameEnv.point += 1
                setattr(self, 'toep', True)
        elif toep:
            print("Wil je callen?")
            call = input('[y/n]: ')
            if call == 'y':
                setattr(self, f"{player}_points", getattr(self, f"{player}_points") + 1)
            elif call == 'n':
                setattr(self, f"{player}_points", getattr(self, f"{player}_points"))
                self.players.remove('player')
                return self
            else:
                print('Geen valide input')

    @staticmethod
    def winner(index_, cards_played):
        winner = np.array(list(cards_played.keys()))
        return winner[np.argmax(index_)]

    @staticmethod
    def index(card):
        value = card.split(' ')[0]
        #suit = card.split(' ')[1]
        numbers = np.array(["J", "Q", "K", "A", "7", "8", "9", "10"])
        return np.where(value == numbers)[0]

    @staticmethod
    def shuffle_deal():
        # TODO add shuffle index but return None
        deck_size = len(GameEnv.set_of_cards)
        index_cards = np.arange(deck_size)
        np.random.shuffle(index_cards)
        GameEnv.set_of_cards = GameEnv.set_of_cards[index_cards]
        hand_dealt = GameEnv.set_of_cards[:4]
        GameEnv.set_of_cards = np.delete(GameEnv.set_of_cards, np.s_[:4])
        return hand_dealt

    @classmethod
    def combinations(cls):
        suits = ["H", "D", "S", "C"]
        numbers = ["J", "Q", "K", "A", "7", "8", "9", "10"]
        cls.best_to_worst = np.append(cls.best_to_worst, numbers)
        for suit in suits:
            for number in numbers:
                cls.set_of_cards = np.append(cls.set_of_cards, number+" "+suit)
        return cls


def main():
    game_test = GameEnv(('Maren', 'Ruben', 'Jorden'))
    game_test.round()


if __name__ == '__main__':
    main()