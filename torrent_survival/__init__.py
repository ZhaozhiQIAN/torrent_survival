import peewee

# database = connect('mysql://root:Windows9@localhost/FB')
database = peewee.MySQLDatabase(host='localhost', user='root', passwd='Windows9', database='FB', charset='utf8')
def before_request_handler():
    database.connect()

def after_request_handler():
    database.close()


class Torrent(peewee.Model):
    #  record_id = peewee.IntegerField(unique=True)
    torr_name = peewee.CharField()
    category = peewee.CharField()
    releaser = peewee.CharField()
    file_size = peewee.FloatField()
    seed_num = peewee.IntegerField()
    download_num = peewee.IntegerField()
    complete_num = peewee.IntegerField()
    release_time = peewee.DateTimeField()
    grab_time = peewee.DateTimeField()

    class Meta:
        database = database

#  database.connect()
#  database.create_tables([Torrent, ])