INPUT = """Player 1:
25
37
35
16
9
26
17
5
47
32
11
43
40
15
7
19
36
20
50
3
21
34
44
18
22

Player 2:
12
1
27
41
4
39
13
29
38
2
33
28
10
6
24
31
42
8
23
45
46
48
49
30
14""".split("\n")


def make_list(values):
    head = [None, None]
    tail = head
    for value in values:
        tail[1] = [value, None]
        tail = tail[1]
    return head, tail


def get_list_length(head):
    n = 0
    while head[1]:
        n += 1
        head = head[1]
    return n


CHARS = "".join(chr(ord("A") + n) for n in range(0, 26)) + "".join(
    chr(ord("a") + n) for n in range(0, 26))


class Player:
    def __init__(self, name, cards):
        self.name = name
        self.head, self.tail = make_list(cards)
        self.card_count = get_list_length(self.head)

    def is_done(self):
        return self.head == self.tail

    def draw(self):
        if self.tail is self.head:
            return None
        card = self.head[1]
        self.head[1] = card[1]
        if self.tail is card:
            self.tail = self.head
        self.card_count -= 1
        return card[0]

    def add(self, card):
        self.tail[1] = [card, None]
        self.tail = self.tail[1]
        self.card_count += 1

    def cards(self):
        cards = []
        card = self.head[1]
        while card:
            cards.append(card[0])
            card = card[1]
        return cards

    def score(self):
        cards = self.cards()
        factor = len(cards)
        score = 0
        for card in cards:
            score += card * factor
            factor -= 1
        return score

    def deck_id(self):
        return str(self.name) + "".join(CHARS[c] for c in self.cards())


def play(player1, player2):
    while not player1.is_done() and not player2.is_done():
        card1, card2 = player1.draw(), player2.draw()
        if card1 > card2:
            player1.add(card1)
            player1.add(card2)
            yield f"Player 1 wins the round! {card1} vs {card2}"
        else:
            player2.add(card2)
            player2.add(card1)
            yield f"Player 2 wins the round! {card2} vs {card1}"


PLAYER1 = Player("1", (int(s) for s in INPUT[1:26]))
PLAYER2 = Player("2", (int(s) for s in INPUT[28:]))
for i, s in enumerate(play(PLAYER1, PLAYER2)):
    if i > 1000:
        break
    print(i, s)

print(PLAYER1.score())


def play2(player1, player2):
    play2.MAX_GAME_NO = 1000

    def recursive_play(player1, player2, game, known_outcomes):
        input_id = f"{player1.deck_id()}:{player2.deck_id()}"
        if input_id in known_outcomes:
            if game <= play2.MAX_GAME_NO:
                print(
                    f"Player {known_outcomes[input_id]} wins game {game}. Known outcome.")
                play2.MAX_GAME_NO = game
            return player1 if known_outcomes[
                                  input_id] == player1.name else player2
        known_deck_ids = set()
        rnd = 0
        while not player1.is_done() and not player2.is_done():
            deck_ids = f"{player1.deck_id()}:{player2.deck_id()}"
            if deck_ids in known_deck_ids:
                break
            known_deck_ids.add(deck_ids)
            card1, card2 = player1.draw(), player2.draw()
            if card1 <= player1.card_count and card2 <= player2.card_count:
                winner = recursive_play(Player(player1.name,
                                               player1.cards()[:card1]),
                                        Player(player2.name,
                                               player2.cards()[:card2]),
                                        game + 1,
                                        known_outcomes)
                winner = player1 if player1.name == winner.name else player2
            elif card1 > card2:
                winner = player1
            else:
                winner = player2
            winner.add(max(card1, card2))
            winner.add(min(card1, card2))
            rnd += 1
            if rnd > 100000:
                raise Exception("Too many rounds!!")

        winner = player2 if player1.is_done() else player1
        if game < 7:
            print(f"Player {winner.name} wins game {game} after {rnd} rounds! ({len(known_outcomes)})")
        known_outcomes[input_id] = winner.name
        return winner

    return recursive_play(player1, player2, 1, {})


PLAYER1 = Player("1", (int(s) for s in INPUT[1:26]))
PLAYER2 = Player("2", (int(s) for s in INPUT[28:]))
WINNER = play2(PLAYER1, PLAYER2)

print(WINNER.score())

print(WINNER.cards())
print(PLAYER1.cards())
print(PLAYER2.cards())
