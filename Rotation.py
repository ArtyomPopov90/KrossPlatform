import random

def is_web():
    return "__BRYTHON__" in globals()

def write(message, end='\n'):
    if is_web():
        from browser import document
        console = document.getElementById('console')
        p = document.createElement('p')
        p.textContent = '> ' + message
        console.appendChild(p)
        console.scrollTop = console.scrollHeight
    else:
        print(message, end=end)


async def read():
    if is_web():
        from browser import document, aio
        inp = document.getElementById('input')
        while True:
            event = await aio.event(inp, 'keydown')
            if event.key == 'Enter':
                tmp = event.target.value
                event.target.value = ''
                write(tmp)
                return tmp
    else:
        return input()


def run(function):
    if is_web():
        from browser import aio
        aio.run(function())
    else:
        import asyncio
        asyncio.run(function())

def display_board(board):
    for i in range(0, 13, 4):
        print(board[i], board[i + 1], board[i + 2], board[i + 3])


async def main():
    write(" " * 26 + "ROTATE")
    write(" " * 20 + "CREATIVE COMPUTING")
    write(" " * 18 + "MORRISTOWN, NEW JERSEY\n\n\n")
    write("INSTRUCTIONS: ")
    a = await read()
    write("\n")
    if a[0] != "N":

        write("IN THIS GAME THE BOARD IS LAID OUT AS FOLLOWS:")
        board = [str(i) for i in range(1, 17)]
        display_board(board)
        write("BOARD POSITIONS ARE OCCUPIED RANDOMLY BY THE LETTERS A TO P.")
        write("THE OBJECT OF THE GAME IS TO ORDER THE LETTERS BY ROTATING")
        write("ANY FOUR LETTERS CLOCKWISE ONE POSITION. YOU SPECIFY THE")
        write("UPPER LEFT POSITION OF THE FOUR YOU WISH TO ROTATE, I.E.,")
        write("VALID MOVES ARE 1, 2, 3, 5, 6, 7, 9, 10 AND 11.")
        write("CONSEQUENTLY, IF THE BOARD LOOKED LIKE:")

        board = [chr(i + 64) for i in range(1, 17)]
        board[1] = 'C'
        board[2] = 'G'
        board[5] = 'B'
        board[6] = 'F'
        display_board(board)

        write("AND YOU ROTATED POSITION 2, THE BOARD WOULD BE:")

        for i in range(2, 7):
            board[i] = chr(i + 64)
        display_board(board)
        write("AND YOU WOULD WIN !\n")

        write("YOU ALSO GET ONE 'SPECIAL' MOVE PER GAME WHICH YOU MAY OR")
        write("MAY NOT NEED. THE SPECIAL MOVE ALLOWS YOU TO EXCHANGE")
        write("ANY TWO ADJACENT LETTERS IN A ROW. TO MAKE THIS MOVE,")
        write("INPUT A '-1' AS YOUR MOVE AND YOU WILL BE ASKED FOR THE")
        write("POSITIONS OF THE TWO LETTERS TO EXCHANGE. REMEMBER --")
        write("ONLY ONE SPECIAL MOVE PER GAME!\n")

        write("TO GIVE UP AT ANY TIME, TYPE '0'.\n")
        write("GOOD LUCK !\n")

    board = ['0'] * 16

    for i in range(16):
        while True:
            random_letter = chr(random.randint(65, 80))
            if random_letter not in board:
                board[i] = random_letter
                break

    m = 0
    s = 0
    write("HERE'S THE STARTING BOARD...")
    display_board(board)

    while True:
        write("POSITION TO ROTATE: ")
        i = await read()
        i = int(i)
        if i == 0:
            write("\n\n")
            main()
        elif i == -1:
            if s == 1:
                write("ONLY ONE SPECIAL MOVE PER GAME.")
                continue
            write("EXCHANGE WHICH TWO POSITIONS: ")
            inStr = await read()
            inStr = str(inStr)
            x, y = map(int, inStr.split())
            if x != y + 11 and x != y - 1:
                write("ILLEGAL. AGAIN...")
            else:
                s += 1
                board[x - 1], board[y - 1] = board[y - 1], board[x - 1]
                display_board(board)
        elif i == 4 or i == 8 or i > 12:
            write("ILLEGAL. AGAIN...")
        else:
            m += 1
            t = board[i - 1]
            board[i - 1], board[i + 3], board[i + 4], board[i] = board[i + 3], board[i + 4], board[i], t
            display_board(board)

        if "".join(board) == "ABCDEFGHIJKLMNOP":
            write(f"YOU ORDERED THE BOARD IN {m} MOVES.")
            write(chr(7))
            play_again = input("PLAY AGAIN (Y/N): ")
            if play_again.startswith("Y"):
                write("\n\n")
                main()
            else:
                write(f"YOU PLAYED {games_played} GAMES AND ORDERED THE BOARD IN AN AVERAGE")
                write(f"OF {moves_total / games_played} MOVES PER GAME.")
                break

games_played = 0
moves_total = 0
run(main)