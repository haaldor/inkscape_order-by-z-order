#!/usr/bin/env python3
#
# License: GPL2
# Copyright Alan "Haaldor" Błaszczyński
# https://github.com/Haaldor/inkscape-distributebyzorder
#
import inkex
import math
from inkex.transforms import Transform
from inkex.transforms import BoundingBox
from inkex.styles import Style

NULL_TRANSFORM = Transform([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])


class DistributeByZOrder(inkex.EffectExtension):
    def __init__(self):
        super(DistributeByZOrder, self).__init__()

    def effect(self):
        ### I would love to do the following and allow just selecting multiple elements, but I don't know how to sort "selected" by z-order. Maybe something to do for the future.
        # if self.svg.selected and len(self.svg.selected)>1
        #     self.distribute_by_z_order(self.svg.selected)
        if self.svg.selected and len(self.svg.selected)==1 and self.svg.selected[0].tag == inkex.addNS('g', 'svg'):
            self.distribute_by_z_order(list(reversed(self.svg.selected[0].getchildren())))
        else:
            inkex.utils.errormsg(f'You need to select exactly one group!')
            inkex.utils.debug(len(self.svg.selected))
            inkex.utils.debug(self.svg.selected[0].tag)

    def distribute_by_z_order(self, nodes):
        # This function takes in group of nodes (that should be sorted by z-order and have 2+ elements) and moves 2nd element to the right of the 1st element. Than it removes 1st element from the list and recursively executes itself for the now-reduced list of elements.
        init_transform = Transform(nodes[1].get("transform", [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]))
        
        # This here is a hack that helps the bounding box function calculate bounding box properly (for some reason it gives absolutely unhinged numbers without this line). I hate such hacks but with such awful docs that we have, we do what we gotta do.
        # This still doesn't work perfectly and the elements sometimes overlap each others, but they are sorted well enough for Align and Distribute grid system to do it's job properly, so I don't give a shit anymore.
        nodes[1].set("transform", Transform([[init_transform.a, 0.0, 0.0], [0.0, init_transform.d, 0.0]]))
        
        bbox0 = nodes[0].bounding_box() # Docs say that we should execute this function like this: BoundingBox(nodes[0]) # but this doesn't work. 
        bbox1 = nodes[1].bounding_box()

        #inkex.utils.debug(f"Element 0 right: {bbox0.right}")
        #inkex.utils.debug(f"Element 1 left: {bbox1.left}")
        
        # Move 2nd element from the list to the right of the 1st element from the list, centered vertically.
        nodes[1].set("transform", Transform([[1.0, 0.0, bbox0.right-bbox1.left], [0.0, 1.0, bbox0.center_y-bbox1.center_y]]).add_scale(init_transform.a, init_transform.d))

        # Remove first element, so the just-moved element will now be reference element for the next element after it.
        nodes.pop(0)

        if(len(nodes)>1):
          # If there are 2+ elements left in the group that weren't transformed, we recursively transform them.
          self.distribute_by_z_order(nodes)
        
        # At this point all elements should be stacked one next to another starting from the 1st element from given list.

if __name__ == '__main__':
    DistributeByZOrder().run()
