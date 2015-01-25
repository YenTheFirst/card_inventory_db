This project describes a database for keeping inventory of a collection of collectible cards.

# Setup

from within the package, running `python -m utils.setup_db <inventory_filename> <scanned_images_filename>` will create the databases.

# Schema

This project uses two SQLite databases - one to hold scanned images of the cards, and one to hold the remainder of the inventory. The databases are split this way so that the main inventory table is small, lightweight, and quick to query, and so the inventory db can be transferred around quickly. Other projects using this module can choose to not load or use the scanned images db.

### scanned images DB

#### scanned\_images table

Each scanned image belongs to exactly one card.

- id - unique primary key
- card\_id - a reference to the card record
- status - a set of possible statuses this image could be in -
    - unprocessed - this image is in the database, and recorded in the inventory system, but nothing further is known
    - candidate\_match - an automated tool has proposed a recognition for this scanned image, but it needs verification.
    - confident\_match - this card is confidently recognized - either by an automated tool with high confidence, or humane verification
- scan\_png - BLOB, containing the png encoding of a scanned image

### inventory DB

#### cards table

This describes individual cards, including unique identifying information. Each card has exactly scanned\_image, and a location in exactly one box.

- id - unique primary key
- scanned\_image\_id - a reference to a single row in the scanned\_images db.
- box\_id - a reference to the box this card is in.
- box\_index - an integer describing where in the box this card is. Interperetation depends on the box, and is not currently defined.
- card\_id - a text field, uniquely describing which card this is. This can be used as a reference to a separate DB which describes the available cards for collection.
- notes - a text field, describing any notes about this particular card, such as mint status, misprinting, or other interesting statuses.

#### box table

This describes a box or other container that cards are kept in. Does not necessarily describe a literal box - could be a numbered box, a trade binder, a display case, or a deck. I call it a 'box' instead of a 'container', as 'box' is short and specific, and 'container' is vague, even though not all possible containers are literally boxes.

Each box is part of exactly one collection, and holds any number of cards.

- id - unique primary key
- name - human-readable name of this box.
- collection\_id - a reference to the collection this box is a part of.
- collection\_index - an integer describing the position of this box within the collection. Interperetation depends on the collection, is not currently defined, and may not be meaningful for all collections.

#### collection table

This describes a grouping of boxes that have similar function. Examples are - a set of trade binders, a large box of smaller numbered boxes, or a collection of decks.

Each collection has any number of boxes.

- id - unique primary key
- name - human readable name.


# Migrating from older inventory

This project grew out of the card\_scan project, and is a refinement of the inventory system used in there. The included utils.migrate tool can be used to convert an older inventory db to this new style.



# Licensing

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

