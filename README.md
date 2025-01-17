# Order by z-order extension for Inkscape
This extension takes selected singular group and distributes it's children next to one another, ordered by their z-order.
Initially intended use is to visually distribute elements that are stacked on top of each other (i.e. when importing multiple files) that are correctly ordered in layer visually, but if tried to distribute them using "Align and Distribute" tab they are totally shuffled.

This extension only does minimal work possible and is intended to have just "good enough" outcome that can be further worked with using "Align and Distribute" functionality.

#### *Notice: This extension will overwrite matrix transforms, although it will try to preserve the scale set by transform. Scalled elements may be not positioned perfectly.* 

Feel free to poke around my code and improve upon it. I tried to comment the code somewhat readably, but keep in mind this is just a single weeknight project.
