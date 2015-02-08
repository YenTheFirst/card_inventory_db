import models
import elixir

def setup_session(inventory_dbname = None, scanned_images_dbname = None):
        #create engine
    elixir.metadata.bind = 'sqlite://'
    b = elixir.metadata.bind
    if inventory_dbname is not None:
        b.execute("attach database ? as inventory", inventory_dbname)
    if scanned_images_dbname is not None:
        b.execute("attach database ? as scanned_images", scanned_images_dbname);
    elixir.setup_all()

