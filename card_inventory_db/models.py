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

from elixir import Entity, Field, using_options, using_table_options
from elixir import Integer, UnicodeText, BLOB, Enum
from elixir import ManyToOne, OneToMany, OneToOne


class Card(Entity):
    scanned_image = OneToOne('ScannedImage')
    box = ManyToOne('Box')
    box_index = Field(Integer)
    card_id = Field(UnicodeText)
    notes = Field(UnicodeText)

    using_options(tablename='cards')
    using_table_options(schema='inventory')

class Box(Entity):
    name = Field(UnicodeText)
    collection = ManyToOne('Collection')
    collection_index = Field(Integer)

    cards = OneToMany('Card')

    using_options(tablename='boxes')
    using_table_options(schema='inventory')

class Collection(Entity):
    name = Field(UnicodeText)

    using_options(tablename='collections')
    using_table_options(schema='inventory')

class ScannedImage(Entity):
        #this is listed as ManyToOne, though there will only ever be
        #a single scanned image per card
    card = ManyToOne('models.Card')
    status = Field(Enum(
        'unprocessed',
        'candidate_match',
        'confident_match'),
        index = True)
    scan_png = Field(BLOB)

    using_options(tablename='scanned_images')
    using_table_options(schema='scanned_images')
