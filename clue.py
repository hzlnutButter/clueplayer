suspects = ["plum", "peacock", "green", "white", "mustard", "scarlet"]
rooms = ["observatory", "living room", "theatre", "spa", "patio", "kitchen", "dining room", "guest house", "hall"]
weapons = ["rope", "candlestick", "knife", "pistol", "bat", "dumbbell", "trophy", "poison", "axe"]

culprit_suspect = ""
culprit_room = ""
culprit_weapon = ""

players = []

class Player():
    registry = []
    def __init__(self, name, cards_per_player):
        self.registry.append(self)
        self.name = name.title()
        self.hand = []
        self.hand_length = cards_per_player
        self.possible_cards = []
        all_cards = suspects + rooms + weapons
        for item in all_cards:
            self.possible_cards.append(item)
    def __repr__(self):
        return self.name
    def list_hand(self):
        hand = self.name + " has:"
        for item in self.hand:
            hand += (" " + item + ",")
        print(hand.strip(","))
    def check_possible_cards(self):
        for item in self.possible_cards:
            if (item not in suspects) and (item not in rooms) and (item not in weapons):
                self.possible_cards.remove(item)
        if len(self.possible_cards) == (self.hand_length - len(self.hand)):
            for item in self.possible_cards:
                self.hand.append(item)
        if len(self.hand) == self.hand_length:
            self.possible_cards = []

    def add_cards(self, cards_str):
        cards = cards_str.lower().split(", ")
        for card in cards:
            self.hand.append(card)
            self.possible_cards.remove(card)
            if card in suspects:
                suspects.remove(card)
            elif card in rooms:
                rooms.remove(card)
            elif card in weapons:
                weapons.remove(card)
        self.check_possible_cards()
        self.list_hand()
    def remove_possible_card(self, card):
        self.possible_cards.remove(card)
        self.check_possible_cards()
        self.list_hand()
    def unknown_card_revealed(self, rumour_cards):
        rumour_cards_list = rumour_cards.lower().split(", ")
        possible_revealed_cards = []
        for item in rumour_cards_list:
            if item in self.possible_cards:
                possible_revealed_cards.append()
        if len(possible_revealed_cards) == 1:
            self.add_cards(rumour_cards_list)
            self.check_possible_cards
            self.list_hand
            
def update_stats(cards_in_pool):
    global suspects, rooms, weapons, culprit_suspect, culprit_room, culprit_weapon

    # check each possible location the card could exist
    for item in suspects:
        suspect_in_pool = True
        for player in Player.registry:
            if item in player.possible_cards:
                suspect_in_pool = False
                break
        if cards_in_pool > 0:
            suspect_in_pool = False
        if suspect_in_pool:
            culprit_suspect = item
            break
    for item in rooms:
        room_in_pool = True
        for player in Player.registry:
            if item in player.hand or item in player.possible_cards:
                room_in_pool = False
                break
        if cards_in_pool > 0:
            room_in_pool = False
        if room_in_pool:
            culprit_room = item
            break
    for item in weapons:
        weapon_in_pool = True
        for player in Player.registry:
            if item in player.hand or item in player.possible_cards:
                weapon_in_pool = False
                break
        if cards_in_pool > 0:
            weapon_in_pool = False
        if weapon_in_pool:
            culprit_weapon = item
            break
    
    # check if the suspects list is 1
    if len(suspects) == 1:
        culprit_suspect = suspects[0]
    if len(rooms) == 1:
        culprit_room = rooms[0]
    if len(weapons) == 1:
        culprit_weapon = weapons[0]
    
    if culprit_suspect:
        print(" ~ ~ " + culprit_suspect.upper() + " did it! ~ ~")
    if culprit_room:
        print(" ~ ~ It was in the " + culprit_room.upper() + "! ~ ~")
    if culprit_weapon:
        print(" ~ ~ It was done with the " + culprit_weapon.upper() + "! ~ ~")
    
    if not culprit_suspect:
        suspects_str = "Possible suspects:"
        for suspect in suspects:
            suspects_str += (" " + suspect + ",")
        print(suspects_str.strip(","))
    if not culprit_room:
        rooms_str = "Possible rooms:"
        for room in rooms:
            rooms_str += (" " + room + ",")
        print(rooms_str.strip(","))
    if not culprit_weapon:
        weapons_str = "Possible weapons:"
        for weapon in weapons:
            weapons_str += (" " + weapon + ",")
        print(weapons_str.strip(","))

# setup
num_cards = len(suspects) + len(rooms) + len(weapons)
num_players = int(input("How many players?\n > "))
cards_per_player = int((num_cards - 3) / num_players)
cards_in_pool = int((num_cards - 3) % num_players)
print(str(cards_per_player) + " cards per player and " + str(cards_in_pool) + " in the pool.")

me = Player("Jenna", cards_per_player)
players.append(me)
remaining_players = num_players - 1

my_hand = input("List your hand:\n > ")
me.add_cards(my_hand)

while remaining_players > 0:
    player_name = input("Next player: ")
    player = Player(player_name, cards_per_player)
    players.append(player)
    remaining_players = remaining_players - 1

# turns
while True:
    if cards_in_pool > 0:
        next_move = input("\nInput next move: get POOL cards, REMOVE possible card, add cards to PLAYER NAME, UNKNOWN card revealed\n > ").lower()
    else:
        next_move = input("\nInput next move: REMOVE possible card, add cards to PLAYER NAME, UNKNOWN card revealed\n > ").lower()
    if "pool" in next_move: # get pool cards
        pool_cards_input = input("Input pool cards:\n > ").lower()
        pool_cards = pool_cards_input.split(", ")
        for card in pool_cards:
            if card in suspects:
                suspects.remove(card)
            elif card in rooms:
                rooms.remove(card)
            elif card in weapons:
                weapons.remove(card)
        cards_in_pool = 0
    elif "remove" in next_move: # remove_possible_card
        which_players = input("From which players?\n > ").title()
        which_players_list = which_players.split(", ")
        which_card = input("Which card?\n > ").lower()
        for player in which_players_list:
            for player_class in Player.registry:
                if player_class.name == player:
                    player_class.remove_possible_card(which_card)
    elif "unknown" in next_move: # unknown_card_revealed
        player = input("Who was it revealed to?\n > ")
        rumour_cards = input("Which cards were involved in the rumour?\n > ")
        player.unknown_card_revealed(rumour_cards)
    for player in Player.registry: # add_cards
        if player.name.lower() in next_move:
            which_cards = input("Which cards would you like to add?\n > ")
            player.add_cards(which_cards)

    update_stats(cards_in_pool)
    
# intrigue cards = 8 are clocks (figure out probability)