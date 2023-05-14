import asyncio, os, keyboard, random


# custom game over exception
class GameOver(Exception):
    pass


# setup settings
size = 30
tail = [(int(size), int(size / 2)), (int(size) + 1, int(size / 2))]
direction = 'right'
apple_coords = (random.randint(2, size * 2 - 1), random.randint(2, size - 2))
score = 0


# drawing func
async def draw():
    while True:
        os.system('clear')

        # drawing field
        print((size * 2 + 1) * '#')
        for i in range(size - 2):
            line = list(size * '  ')
            line[-1] = '#'

            # drawing tail
            for x in tail:
                if i == x[1]:
                    line[x[0]] = '#'
            # drawing apple
            if i == apple_coords[1]:
                line[apple_coords[0]] = '*'

            print('#' + ''.join(line))

        print((size * 2 + 1) * '#')

        # drawing score
        print(f'Score:{score}')
        await asyncio.sleep(0.01)


async def move_polling():
    global direction
    global apple_coords
    global score

    while True:
        # move polling
        tail.pop(-1)
        if direction == 'up':
            tail.insert(0, (tail[0][0], tail[0][1] - 1))
        if direction == 'right':
            tail.insert(0, (tail[0][0] + 1, tail[0][1]))
        if direction == 'left':
            tail.insert(0, (tail[0][0] - 1, tail[0][1]))
        if direction == 'down':
            tail.insert(0, (tail[0][0], tail[0][1] + 1))

        # apple eat polling
        if tail[0][0] == apple_coords[0] and tail[0][1] == apple_coords[1]:
            tail.append((size, size))
            apple_coords = (random.randint(2, size * 2 - 1), random.randint(2, size - 2))
            score += 100

        await asyncio.sleep(0.1)


async def keyboard_polling():
    global direction
    while True:
        if keyboard.is_pressed('w') and direction != 'down':
            direction = 'up'
        if keyboard.is_pressed('d') and direction != 'left':
            direction = 'right'
        if keyboard.is_pressed('a') and direction != 'right':
            direction = 'left'
        if keyboard.is_pressed('s') and direction != 'up':
            direction = 'down'

        await asyncio.sleep(0.01)


async def game_over():
    while True:
        # wall dead
        if tail[0][0] >= (size * 2) - 1 or tail[0][0] <= -1 or tail[0][1] >= size - 2 or tail[0][1] <= -1:
            raise GameOver
        # tail dead
        if tail.count(tail[0]) > 1:
            raise GameOver

        await asyncio.sleep(0.01)


async def main():
    # set up tasks
    draw_task = asyncio.create_task(draw())
    move_polling_task = asyncio.create_task(move_polling())
    game_over_task = asyncio.create_task(game_over())
    keyboard_polling_task = asyncio.create_task(keyboard_polling())
    # run game
    await asyncio.gather(draw_task, keyboard_polling_task, move_polling_task, game_over_task)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except GameOver:
        pass
    finally:
        # game end actions
        os.system('clear')
        print('GameOver!')
        print(f'Final score: {score}')