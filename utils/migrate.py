"""
copyright 2013-2015 Talin Salway

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from setup_session import setup_session
import elixir
from models import Card, Box, Collection, ScannedImage
import old_models
import sys
import re

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "usage: migrate <old_db> <new_inv_db> <new_scan_db>"
        sys.exit(2)

    old_models.__metadata__.bind = 'sqlite:///%s' % sys.argv[1]
    setup_session(sys.argv[2], sys.argv[3])
    elixir.setup_all()

    #we'll create some default collections
    #'numbered_boxes' will contain any numbered boxes
    #'other_boxes' will contain non-numbered boxes
    #'decks' will contain any cards that are 'temporarily_out'
    numbered_boxes = Collection(name = "numbered_boxes")
    other_boxes = Collection(name = "other_boxes")
    decks = Collection(name = "decks")

    #we'll keep track of new boxes as we make them.
    boxes = {
        numbered_boxes: {},
        other_boxes: {},
        decks: {}
    }

    for old_card in old_models.InvCard.query.yield_per(100):
        #figure out what collection/box it goes in
        collection = other_boxes
        box_name = 'unknown'
        if old_card.inventory_status == 'permanently_gone':
            #for now, we won't try to save permanently gone cards.
            continue
        elif old_card.inventory_status == 'temporarily_out':
            collection = decks
            box_name = old_card.most_recent_log().reason
        elif old_card.box and old_card.inventory_status == 'present':
            if re.match("^\d+$", old_card.box):
                collection = numbered_boxes
            else:
                collection = other_boxes
            box_name = old_card.box

        #get or create the box

        if box_name not in boxes[collection]:
            collection_index = 0
            if collection == numbered_boxes:
                collection_index = int(box_name)
            else:
                collection_index = len(boxes[collection])
            boxes[collection][box_name] = Box(
                    name = box_name,
                    collection = collection,
                    collection_index = collection_index)
        box = boxes[collection][box_name]

        #create the new card & image.
        #for now, use set_name/card_name/card_name_downcased as the card_id
        #this should be similar to mtgjson's UID.

        #fill out any notes we might care about
        things_of_interest = []
        if old_card.language != 'english' and old_card.language is not None:
            things_of_interest.append(old_card.language)
        if old_card.is_foil:
            things_of_interest.append("foil")
        if old_card.condition is not None and old_card.condition != '' and old_card.condition != 'near_mint':
            things_of_interest.append("condition "+old_card.condition)

        card = Card(
                box = box,
                box_index = old_card.box_index,
                card_id = "%s/%s/%s" % (
                    old_card.set_name,
                    old_card.name,
                    unicode.lower(old_card.name)),
                notes = " ".join(things_of_interest))
        if old_card.recognition_status == 'scanned':
            status = 'unprocessed'
        elif old_card.recognition_status == 'candidate_match':
            status = 'candidate_match'
        elif old_card.recognition_status == 'incorrect_match':
            status = 'candidate_match'
        elif old_card.recognition_status == 'verified':
            status = 'confident_match'
        else:
            status = 'unprocessed'

        ScannedImage(
                card = card,
                status = status,
                scan_png = old_card.scan_png)

    elixir.session.commit()




