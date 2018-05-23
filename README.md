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

### savegame file format

See the [Switchbrew wiki](http://switchbrew.org/index.php?title=Savegames) for
documentation on the savegame format.

### Command format

sg-goggles savegame-file-path [operation] [wildcard] [-outpath path]

### Operations

The utility supports the following operations:

1. dir - output to the console a list of the save files
2. cat - output to the console the contents of the save files
3. cp - copy the contents of the save files to the outpath or current directory

All operations take an optional wildcard parameter, for performing the
operation only on those save files that match the wildcard.
