import imdb

class MovieData():
    # Create the object that will be used to access the IMDb's database.
    # By default access the web.
    imdb_access = imdb.IMDb()            
    
    def __init__(self):
        pass
    
    def get_movie_data(self, movie_id):
        return self.imdb_access.get_movie(movie_id)

    def search_movie_data (self, title):    
        return self.imdb_access.search_movie(title)        
    
    def get_person_data(self, person_id):
        return self.imdb_access.get_person(person_id)
        
    def update_movie_data(self, movie):
        self.imdb_access.update(movie)
