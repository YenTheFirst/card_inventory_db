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

import elixir
from setup_session import setup_session
import sys

def create_db(inventory_dbname, scanned_dbname):
    setup_session(inventory_dbname, scanned_dbname)
    elixir.create_all()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: utils.setup_db <inventory_dbname> <scanned_images_dbname>"
        sys.exit(1)
    create_db(sys.argv[1], sys.argv[2])
