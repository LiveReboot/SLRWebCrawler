# Logiciel Main
import sys

from api.ieee import Ieee
from api.neo import neo
from api.sciencedirect import Sciencedirect

from utils.Terminal import Terminal

if __name__ == '__main__':

    # Initialiser les moteurs de recherches
    sd = Sciencedirect()
    #ieee = Ieee()

    # Lancer le programme
    Terminal.title("Initialisation")

    total = 0

    # Pour tous les arguments
    for argvPosition in range(1, len(sys.argv)):

        # Query String : String à rechercher dans les moteurs
        qs = sys.argv[argvPosition]

        # Afficher
        Terminal.subtitle("Query string : " + qs)

        # Lancer la recherche dans les moteurs de recherche
        results = sd.list(qs)

        total += len(results)

    # Le processus est terminé
    sys.exit("Terminé : " + str(total) + " publication(s)")
