import time, sys
from threading import Thread
from multiprocessing import Queue
from utils.Terminal import Terminal
import functools


def waiting(pattern=None, color=None, speed=0.1, message=None):
    def decorator(f):
        def patterns():
            patterns = {
                'colored': ['🔴', '🟠', '🟡', '🟢', '🔵', '🟣', '🟤'],
                'monkey': ['🙈', '🙉', '🙊'],
                'age': ['👶', '🧒', '👧', '👩'],
                'earth': ['🌍', '🌏', '🌎'],
                'moon': ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'],
                'square': ['■', '□'],
                'clock': ['○', '◔', '◑', '◕', '●'],
                'squares': ['▞', '▛', '▚', '▟'],
                'triangle': ['▶', '▼', '◀', '▲'],
                'empty_triangle': ['▷', '▽', '◁', '△'],
                'return_block': [
                    '█          ',
                    ' █         ',
                    '  █        ',
                    '   █       ',
                    '    █      ',
                    '     █     ',
                    '      █    ',
                    '       █   ',
                    '        █  ',
                    '         █ ',
                    '          █',
                    '         █ ',
                    '        █  ',
                    '       █   ',
                    '      █    ',
                    '     █     ',
                    '    █      ',
                    '   █       ',
                    '  █        ',
                    ' █         ',
                ],
                'block': [
                    '█          ',
                    ' █         ',
                    '  █        ',
                    '   █       ',
                    '    █      ',
                    '     █     ',
                    '      █    ',
                    '       █   ',
                    '        █  ',
                    '         █ ',
                    '          █',
                ],
                'bar': [
                    '╱',
                    '─',
                    '╲',
                    '│',
                ],
                'dot': [
                    '᳃',
                    '●',
                ],
                'arrow': [
                    '           ',
                    '>          ',
                    '->         ',
                    '-->        ',
                    '--->       ',
                    ' --->      ',
                    '  --->     ',
                    '   --->    ',
                    '    --->   ',
                    '     --->  ',
                    '      ---> ',
                    '       --->',
                    '        ---',
                    '         --',
                    '          -',
                ],
                'return_arrow': [
                    '           ',
                    '>          ',
                    '->         ',
                    '-->        ',
                    '--->       ',
                    ' --->      ',
                    '  --->     ',
                    '   --->    ',
                    '    --->   ',
                    '     --->  ',
                    '      ---> ',
                    '       --->',
                    '        ---',
                    '         --',
                    '          -',
                    '          <',
                    '         <-',
                    '        <--',
                    '       <---',
                    '      <--- ',
                    '    <---   ',
                    '   <---    ',
                    '  <---     ',
                    ' <---      ',
                    '<---       ',
                    '---        ',
                    '--         ',
                    '-          ',
                ]
            }

            return patterns[pattern] if pattern is not None and pattern in patterns else patterns['return_arrow']

        def wrapped_f(q, *args, **kwargs):
            ret = f(*args, **kwargs)
            q.put(ret)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            q = Queue()

            # Position du pattern
            pos = 0

            t = Thread(target=wrapped_f, args=(q,) + args, kwargs=kwargs)
            t.start()
            t.result_queue = q

            # Récupérer le pattern choisi
            display = patterns()

            # Ajouter un message personnalisé
            msg = '0 sec.' if message is None else str(message)

            # Dessiner l'horloge
            sys.stdout.write(
                Terminal.Text.txt_yellow('[') +
                Terminal.Text.txt(display[pos], color) +
                Terminal.Text.txt_yellow('] ') +
                Terminal.Text.faint(msg) + "\r\n"
            )
            sys.stdout.flush()
            sys.stdout.write("\033[F")

            while t.is_alive():
                # Patienter un instant
                time.sleep(speed)
                # Passer à la position suivante
                pos += 1

                # Afficher la durée d'attente
                sec = int(pos * speed)

                # Ajouter un message personnalisé
                msg = str(sec) + ' sec.' if message is None else str(message)

                # Afficher la nouvelle position
                sys.stdout.write(u"\u001b[1000D" +
                                 Terminal.Text.txt_yellow('[') +
                                 Terminal.Text.txt(display[pos % len(display)], color) +
                                 Terminal.Text.txt_yellow('] ') +
                                 Terminal.Text.faint(msg) + "\r\n"
                                 )
                sys.stdout.flush()
                sys.stdout.write("\033[F")

            # Effacer l'horloge
            print()
            sys.stdout.write("\033[F")

            return t.result_queue.get()

        return wrapper

    return decorator
