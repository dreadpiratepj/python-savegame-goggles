# python-savegame-goggles
A Python utility for retrieving save files from Nintendo Switch savegame archives

Long story short: while hacking my Breath of the Wild game saves, I messed up
and lost all of my Hero's Path data. Luckily I had made a backup of my Switch's
internal flash storage (a.k.a. NAND) before my mistake. But there is currently
no way to restore this backup without wiping off all the other changes I had
made to my game. There is a way to inject just the Hero's Path data, but I need
to retrieve the individual files from the NAND archive.

This utility is my attempt to solve this problem. I figure other people may
have a similar need, so I'm open sourcing this code in the hope others might
benefit from it. Opening it also invites other hackers to fork and make
contributions.
