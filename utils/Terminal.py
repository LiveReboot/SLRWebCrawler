import datetime
import time, sys


class Terminal:
    # ====================
    # Liste des codes d'affichage
    # ====================

    class Code:

        # Effacer tout le formatage
        clear = "\033[0m"

        # Gras
        bold = "\033[1m"
        not_bold = "\033[22m"

        # Faint
        faint = "\033[2m"
        not_faint = "\033[22m"

        # Italic
        italic = "\033[3m"
        not_italic = "\033[23m"

        # Souligné
        underline = "\033[4m"
        not_underline = "\033[24m"

        # Blink
        blink = "\033[5m"
        not_blink = "\033[25m"

        # Inverse
        inverse = "\033[7m"
        not_inverse = "\033[27m"

        # Invisible
        invisible = "\033[8m"
        not_invisible = "\033[28m"

        # Crossed
        crossed = "\033[9m"
        not_crossed = "\033[29m"

        # Background
        bg_black = "\033[40m"
        bg_red = "\033[41m"
        bg_green = "\033[42m"
        bg_yellow = "\033[43m"
        bg_blue = "\033[44m"
        bg_magenta = "\033[45m"
        bg_cyan = "\033[46m"
        bg_white = "\033[47m"
        bg_default = "\033[49m"

        # Foreground
        txt_black = "\033[30m"
        txt_red = "\033[31m"
        txt_green = "\033[32m"
        txt_yellow = "\033[33m"
        txt_blue = "\033[34m"
        txt_magenta = "\033[35m"
        txt_cyan = "\033[36m"
        txt_white = "\033[37m"
        txt_default = "\033[39m"

    # ====================
    # Modification du texte
    # ====================

    class Text:

        @staticmethod
        def clear(text=""):
            return Terminal.Code.clear + text

        @staticmethod
        def bold(text=""):
            return Terminal.Code.bold + text + Terminal.Code.not_bold

        @staticmethod
        def b(text=""):
            return Terminal.Text.bold(text)

        @staticmethod
        def faint(text=""):
            return Terminal.Code.faint + text + Terminal.Code.not_faint

        @staticmethod
        def f(text=""):
            return Terminal.Text.faint(text)

        @staticmethod
        def italic(text=""):
            return Terminal.Code.italic + text + Terminal.Code.not_italic

        @staticmethod
        def i(text=""):
            return Terminal.Text.italic(text)

        @staticmethod
        def underline(text=""):
            return Terminal.Code.underline + text + Terminal.Code.not_underline

        @staticmethod
        def u(text=""):
            return Terminal.Text.underline(text)

        @staticmethod
        def blink(text=""):
            return Terminal.Code.blink + text + Terminal.Code.not_blink

        @staticmethod
        def inverse(text=""):
            return Terminal.Code.inverse + text + Terminal.Code.not_inverse

        @staticmethod
        def invisible(text=""):
            return Terminal.Code.invisible + text + Terminal.Code.not_invisible

        @staticmethod
        def crossed(text=""):
            return Terminal.Code.crossed + text + Terminal.Code.not_crossed

        # Couleur de fond
        # ----------------------------

        @staticmethod
        def bg_black(text=""):
            return Terminal.Code.bg_black + text + Terminal.Code.bg_default

        @staticmethod
        def bg_red(text=""):
            return Terminal.Code.bg_red + text + Terminal.Code.bg_default

        @staticmethod
        def bg_green(text=""):
            return Terminal.Code.bg_green + text + Terminal.Code.bg_default

        @staticmethod
        def bg_yellow(text=""):
            return Terminal.Code.bg_yellow + text + Terminal.Code.bg_default

        @staticmethod
        def bg_blue(text=""):
            return Terminal.Code.bg_blue + text + Terminal.Code.bg_default

        @staticmethod
        def bg_magenta(text=""):
            return Terminal.Code.bg_magenta + text + Terminal.Code.bg_default

        @staticmethod
        def bg_cyan(text=""):
            return Terminal.Code.bg_cyan + text + Terminal.Code.bg_default

        @staticmethod
        def bg_white(text=""):
            return Terminal.Code.bg_white + text + Terminal.Code.bg_default

        @staticmethod
        def bg_default(text=""):
            return Terminal.Code.bg_default + text

        @staticmethod
        def background(text="", color=""):

            colors = {
                "black": Terminal.Text.bg_black(text),
                "red": Terminal.Text.bg_red(text),
                "green": Terminal.Text.bg_green(text),
                "yellow": Terminal.Text.bg_yellow(text),
                "blue": Terminal.Text.bg_blue(text),
                "magenta": Terminal.Text.bg_magenta(text),
                "cyan": Terminal.Text.bg_cyan(text),
                "white": Terminal.Text.bg_white(text)
            }

            if color.lower() in colors:
                return colors[color.lower()]
            else:
                return Terminal.Text.bg_default(text),

        @staticmethod
        def bg(text="", color=""):
            return Terminal.Text.background(text, color)

        # Couleur de texte
        # ----------------------------

        @staticmethod
        def txt_black(text=""):
            return Terminal.Code.txt_black + text + Terminal.Code.txt_default

        @staticmethod
        def txt_red(text=""):
            return Terminal.Code.txt_red + text + Terminal.Code.txt_default

        @staticmethod
        def txt_green(text=""):
            return Terminal.Code.txt_green + text + Terminal.Code.txt_default

        @staticmethod
        def txt_yellow(text=""):
            return Terminal.Code.txt_yellow + text + Terminal.Code.txt_default

        @staticmethod
        def txt_blue(text=""):
            return Terminal.Code.txt_blue + text + Terminal.Code.txt_default

        @staticmethod
        def txt_magenta(text=""):
            return Terminal.Code.txt_magenta + text + Terminal.Code.txt_default

        @staticmethod
        def txt_cyan(text=""):
            return Terminal.Code.txt_cyan + text + Terminal.Code.txt_default

        @staticmethod
        def txt_white(text=""):
            return Terminal.Code.txt_white + text + Terminal.Code.txt_default

        @staticmethod
        def txt_default(text=""):
            return Terminal.Code.txt_default + text

        @staticmethod
        def text(text="", color=""):

            colors = {
                "black": Terminal.Text.txt_black(text),
                "red": Terminal.Text.txt_red(text),
                "green": Terminal.Text.txt_green(text),
                "yellow": Terminal.Text.txt_yellow(text),
                "blue": Terminal.Text.txt_blue(text),
                "magenta": Terminal.Text.txt_magenta(text),
                "cyan": Terminal.Text.txt_cyan(text),
                "white": Terminal.Text.txt_white(text)
            }

            if color.lower() in colors:
                return colors[color.lower()]
            else:
                return Terminal.Text.txt_default(text),

        @staticmethod
        def txt(text="", color=""):
            return Terminal.Text.text(text, color)

    # ====================
    # Messages
    # ====================

    @staticmethod
    def print(s, withDate=True):
        now = datetime.datetime.now()

        # Date
        dd = str(now.day) if now.day >= 10 else "0" + str(now.day)
        mm = str(now.month) if now.month >= 10 else "0" + str(now.month)
        yyyy = str(now.year)

        # Heure
        hh = str(now.hour) if now.hour >= 10 else "0" + str(now.hour)
        ii = str(now.minute) if now.minute >= 10 else "0" + str(now.minute)
        ss = str(now.second) if now.second >= 10 else "0" + str(now.second)

        # Récupérer la date et heure
        fulldate = dd + "/" + mm + "/" + yyyy
        fullhour = hh + ":" + ii + ":" + ss

        # Time
        timestamp = Terminal.Text.txt_blue(fulldate + " (" + fullhour + ")")

        # Afficher le message
        print(timestamp + " - " + s if withDate else s)

    @staticmethod
    def success(text="", title="Success : "):
        Terminal.print(Terminal.Text.txt_green(Terminal.Text.bold(title) + text))

    @staticmethod
    def warning(text="", title="Warning : "):
        Terminal.print(Terminal.Text.txt_yellow(Terminal.Text.bold(title) + text))

    @staticmethod
    def danger(text="", title="Danger : "):
        Terminal.print(Terminal.Text.txt_red(Terminal.Text.bold(title) + text))

    @staticmethod
    def info(text="", title="Info : "):
        Terminal.print(Terminal.Text.txt_blue(Terminal.Text.bold(title) + text))

    @staticmethod
    def error(text="", code=0, title="Error"):
        t = title + " #" + str(code) + " : "
        Terminal.print(Terminal.Text.txt_white(Terminal.Text.bg_red(Terminal.Text.bold(t) + text)))

    @staticmethod
    def loading(text="Chargement en cours", finish="Chargement terminé"):
        Terminal.print(Terminal.Text.bg_yellow(Terminal.Text.txt_white(" ~~ " + text + " ~~ ")))
        for i in range(0, 100):
            time.sleep(0.01)
            sys.stdout.write(u"\u001b[1000D" + str(i + 1) + "%")
            sys.stdout.flush()

        # Remonter à la ligne précédente
        sys.stdout.write("\033[F")

        # Effacer le message
        clean = ""
        for i in range(0, len(text) + 32):
            clean += " "

        print(clean)

        sys.stdout.write("\033[F")
        # Afficher un nouveau message
        Terminal.success(finish)

    @staticmethod
    def clear():
        print("\033c")

    @staticmethod
    def title(text, color="red"):

        char = "-"

        white = ""
        delimiter = ""

        size = len(str(text))

        for i in range(1, size + 5):
            delimiter += char
        for i in range(1, size + 3):
            white += " "

        print(
            Terminal.Text.text(delimiter, color) + "\r\n" +
            Terminal.Text.text(char + white + char, color) + "\r\n" +
            Terminal.Text.text(char + " " + str(text) + " " + char, color) + "\r\n" +
            Terminal.Text.text(char + white + char, color) + "\r\n" +
            Terminal.Text.text(delimiter, color)
        )

    @staticmethod
    def subtitle(text, color="blue"):
        print(Terminal.Text.text(Terminal.Text.bold("-> " + text), color))

    @staticmethod
    def subsubtitle(text, color="cyan"):
        print(Terminal.Text.text(Terminal.Text.italic("   + " + text), color))
