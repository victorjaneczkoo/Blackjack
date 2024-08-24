import random
from colorama import Fore

class Card:
    def __init__(self, number=None):
        if number is not None:
            self.type = [Fore.BLACK + "♠", Fore.BLACK + "♣", Fore.RED + "♥", Fore.RED + "♦"][number // 13]
            self.number = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"][number % 13]
            self.value = self.number if self.number in [2, 3, 4, 5, 6, 7, 8, 9, 10] else 10 if self.number in ["Jack", "Queen", "King"] else 11
            return
        self.type = random.choice([Fore.BLACK + "♠", Fore.BLACK + "♣", Fore.RED + "♥", Fore.RED + "♦"])
        self.number = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"])
        self.value = self.number if self.number in [2, 3, 4, 5, 6, 7, 8, 9, 10] else 10 if self.number in ["Jack", "Queen", "King"] else 11
    
    def __str__(self):
        return f"{self.number} of {self.type + Fore.RESET}"
    
    def changeacevalue(self):
        if self.number == "Ace":
            self.value = 1


class Deck:
    def __init__(self):
        self.cards = [Card(x) for x in range(52)]
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self):
        return self.cards.pop()
    
    
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0
        self.aces = 0
    
    def draw(self, deck):
        card = deck.draw()
        self.hand.append(card)
        self.score += card.value
        if card.number == "Ace":
            self.aces += 1
    
    def showhand(self):
        print(f"\n\033[1m{self.name}'s hand:\033[22m")
        for card in self.hand:
            print(f"> {card}")
        print(f"< Score: {self.score}")
    
    def checkbust(self):
        while self.score > 21 and self.aces > 0:
            self.score -= 10
            self.aces -= 1
        if self.score > 21:
            return True
        return False
    
    def reset(self):
        self.hand = []
        self.score = 0
        self.aces = 0
        
        
class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")
    
    def showhand(self, showall=False):
        print(f"\n\033[1m{self.name}'s hand:\033[22m")
        if showall:
            for card in self.hand:
                print(f"  {card}")
            print(f"> Score: {self.score}\n")
        else:
            print(f"> {self.hand[0]}")
            print("> Hidden card")
            print(f"< Score: {self.hand[0].value} + ?")
    
    def play(self, deck):
        while self.score < 17:
            self.draw(deck)
            if self.checkbust():
                break
        self.showhand(showall=True)
        return self.score > 21
    
    def reset(self):
        self.hand = []
        self.score = 0
        self.aces = 0
        
        
def main():
    print("Welcome to Blackjack!")
    deck = Deck()
    player = Player(input("Enter your name: "))
    dealer = Dealer()
    
    while True:
        player.reset()
        dealer.reset()
        deck.shuffle()
        player.draw(deck)
        player.draw(deck)
        dealer.draw(deck)
        dealer.draw(deck)
        
        player.showhand()
        dealer.showhand()
        
        while input("\nDo you want to hit? (y/n): ").lower() == "y":
            player.draw(deck)
            player.showhand()
            if player.checkbust():
                print("You busted!\n")
                break
        
        if not player.checkbust():
            dealer.play(deck)
            if dealer.checkbust():
                print("Dealer busted!\n")
            else:
                if player.score > dealer.score:
                    print("You win!\n")
                elif player.score < dealer.score:
                    print("Dealer wins!\n")
                else:
                    print("It's a tie!\n")
        
        if input("Do you want to play again? (y/n): ").lower() != "y":
            break
        
    print("Thanks for playing!")
    

if __name__ == "__main__":
    main()
    