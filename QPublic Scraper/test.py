import pyperclip

brand_names = """
Sony Music
Eminem
Mac Miller
Playboi Carti
Good
Drake Waterfowl
UMGD
50 Cent
Tyler, the Creator
Juice Wrld
Nas
Post Malone
Jay Z
A Tribe Called Quest
Outkast
Universal Music Group
WEA CORP
Queen
Fleetwood Mac
Metallica
Van Halen
Boston
Rolling Stones
Led Zeppelin
Ozzy Osbourne
ACDC
Guns N' Roses
Rage Against The Machine
Jimi Hendrix
Pearl Jam
Journey
BTS
Taylor Swift
Lana Del Rey
Kelly Clarkson
PID
Newbourne Media
Michael Jackson
Arista
Abba
P!nk
Justin Bieber
Shawn Mendes
Evanescence
Backstreet Boys
Luke Bryan
Blake Shelton
Chris Stapleton
Alan Jackson
Alabama Crimson Tide
Josh Turner
Kane Brown
Tim McGraw
Walker Hayes
Carrie Underwood
Kenny Chesney
George Jones
Randy Travis
Shania Twain
Sonoma
Warner Classics
Andrea Bocelli
Susan Boyle
Luciano Pavarotti
Telarc
Naxos Records
Vinyl
Denon
Frank Sinatra
Chandos
Adele
Maximum Games
Walmeck
Tinksky
Almencla
Gymax
GLFSIL
Monoprice
AKG
STARTIST
CMGB
Fanzey
Ktaxon
Linyer
MERIGLARE
Novashion
Toma
Turtle Beach
Beexcellent
SteelSeries
Gtheos
Microsoft
KontrolFreek
PlayStation
WD
RUNMUS
RIG
PDP
PowerA
SPBPQY
""".strip()

# add index to each line
brand_names = brand_names.splitlines()
for i in range(len(brand_names)):
    brand_names[i] = str(i+1) + ". " + brand_names[i]

brand_names = "\n".join(brand_names)

prompt = f"""
These are the names of brands and I want their website URL:
NOTE: make PSV format and Have Brand NAME|URL These are listed on Walmart but I want their original Site if It is not available then Put NA

{brand_names}

I need all
"""

pyperclip.copy(prompt)
