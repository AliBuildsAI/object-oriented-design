from enum import Enum
from abc import ABC, abstractmethod
from typing import Union, List
import random


class Suit(Enum):
    CLUBS = 'clubs'
    DIAMONDS = 'diamonds'
    HEARTS = 'hearts'
    SPADES = 'spades'

class Card:
    def __init__(self, suit: Suit, value: int) -> None:
        self._suit = suit
        self._value = value

    @property
    def value(self) -> int:
        return self._value
    
    @property
    def suit(self) -> Suit:
        return self._suit
    
    def __repr__(self) -> str:
        return 'Card(suit={}, value={})'.format(self.suit, self.value)
    
class Deck:
    def __init__(self):
        self._cards = []
        for suit in Suit:
            for value in range(1, 14):
                self._cards.append(Card(suit, min(10, value)))
    
    def draw(self) -> Card:
        return self._cards.pop()
    
    def shuffle(self) -> None:
        for i in range(len(self._cards)):
            j = random.randint(0, len(self._cards) - 1)
            self._cards[i], self._cards[j] = self._cards[j], self._cards[i]


class Hand:
    def __init__(self):
        self._cards = []
        self._score = 0

    def add_card(self, card: Card) -> None:
        self._cards.append(card)
        self._score += card.value
        if card.value == 1 and self.score <= 11:
            self._score += 10
        # print('Score: {}'.format(self._score))

    @property
    def score(self) -> int:
        return self._score
    
    @property
    def cards(self) -> List[Card]:
        return self._cards

class Player(ABC):
    def __init__(self, hand: Hand) -> None:
        self._hand = hand

    @property
    def hand(self) -> Hand:
        return self._hand

    def clear_hand(self) -> None:
        self._hand = Hand()

    def add_card(self, card: Card) -> None:
        self._hand.add_card(card)

    @abstractmethod
    def make_move(self):
        pass
    

class CustomerPlayer(Player):
    def __init__(self, hand: Hand, balance: int):
        super().__init__(hand)
        self._balance = balance
        self.name = 'customer'

    @property
    def balance(self) -> Union[float, int]:
        return self._balance
    
    def place_bet(self, amount: Union[float, int]) -> Union[float, int]:
        if amount > self._balance:
            raise ValueError('Insufficient funds')
        self._balance -= amount
        return amount
    @property
    def balance(self) -> Union[float, int]:
        return self._balance
    
    def receive_winnings(self, amount: Union[float, int]) -> None:
        self._balance += amount
    
    def make_move(self) -> bool:
        if self.hand.score > 21:
            return False
        is_gonna_move = input('Draw a new card? [y/n]: ')
        return is_gonna_move.lower() == 'y'
    
class Dealer(Player):
    def __init__(self, hand: Hand):
        super().__init__(hand)
        self.name = 'dealer'
        self._target_score = 17
    @property
    def target_score(self) -> int:
        return self._target_score
    
    @target_score.setter
    def target_score(self, target_score: int) -> None:
        if isinstance(target_score, int) and target_score <= 21:
            self._target_score = target_score
        else:
            raise ValueError("input should be a positive integer smaller than 22.")
    
    def make_move(self) -> bool:
        return self._get_hand().score < self._target_score
    

class Game:
    def __init__(self, customer: CustomerPlayer, dealer: Dealer, deck: Deck) -> None:
        self._customer = customer
        self._dealer = dealer
        self._deck = deck

    def give_initial_cards(self):
        self._customer.hand.add_card(self._deck.draw())
        print(self._customer.hand.score)
        self._customer.hand.add_card(self._deck.draw())
        print(self._customer.hand.score)
        self._dealer.hand.add_card(self._deck.draw())
        print(self._dealer.hand.cards[0])
        self._dealer.hand.add_card(self._deck.draw())

    def give_card(self, player: Player):
        player.hand.add_card(self._deck.draw())
        if isinstance(player, CustomerPlayer):
            print(self._customer.hand.score)

    def play_round(self, bet_amount: Union[int, float]):
        self._customer.place_bet(bet_amount)
        self._deck.shuffle()

        self.give_initial_cards()

        while self._customer.make_move():
            self.give_card(self._customer)
            if self._customer.hand.score > 21:
                print('Player loses!')
                self.cleanup_round()
                return
        
        self._dealer.target_score = self._customer.hand.score

        while self._dealer.hand.score < self._customer.hand.score:
            self.give_card(self._dealer)
        print('final dealer score: ', self._dealer.hand.score)
        if self._dealer.hand.score > 22:
            self._customer.receive_winnings(bet_amount * 2)
            print('Player wins {}$'.format(bet_amount))
        elif self._dealer.hand.score > self._customer.hand.score:
            print('Player loses {}$'.format(bet_amount))
        else:
            self._customer.receive_winnings(bet_amount)
            print('Game ends with a draw!')
        self.cleanup_round()
    
    def cleanup_round(self):
        self._deck = Deck()
        self._customer.clear_hand()
        self._dealer.clear_hand()
        print('Player balance: ', self._customer.balance)


    def place_bet(self) -> Union[int, float]:
        while True:
            try:
                bet_amount = int(input('How much you want to bet? from 1$ to {}$'.format(self._customer.balance)))
                if self._customer.balance >= bet_amount >= 1 :
                    break
                else:
                    print('Please enter a valid bet amount from 1$ to {}$'.format(self._customer.balance))
            except:
                print('Please enter a valid bet amount from 1$ to {}$'.format(self._customer.balance))
        return bet_amount
    
    def play(self):
        while self._customer.balance:
            play_round = input('Do you want to play Blackjack? [y/n] ')
            if play_round.lower() == 'y':
                bet_amount = self.place_bet()
                self.play_round(bet_amount)
            elif play_round.lower() == 'n':
                break
            else:
                print('Invalid input. please only [y/n]')
        print("You can leave with {}".format(self._customer.balance))


player = CustomerPlayer(Hand(), 1000)
dealer = Dealer(Hand())

Game(player, dealer, Deck()).play()