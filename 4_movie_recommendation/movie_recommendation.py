from typing import List, Dict, Optional
from enum import Enum


class MovieRating(Enum):
    NOT_SEEN = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class User:
    def __init__(self, user_id: int, name: str):
        self._user_id = user_id
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def user_id(self) -> int:
        return self._user_id


class Movie:
    def __init__(self, movie_id: int, movie_name: str):
        self._movie_id = movie_id
        self._movie_name = movie_name

    @property
    def movie_name(self) -> str:
        return self._movie_name

    @property
    def movie_id(self) -> int:
        return self._movie_id


class RatingsData:
    def __init__(self) -> None:
        self._user_movies = {}  # key: user_id, value: Set[Movie]
        self._movie_ratings = {}  # Map<movie_id, Map<User_id, rating>>
        self._movies = []
        self._users = []

    @property
    def user_movies(self):
        return self._user_movies
    
    @property
    def users(self) -> List[User]:
        return self._users
    
    @property
    def movie_ratings(self) -> Dict:
        return self._movie_ratings
    
    @property
    def movies(self) -> List[Movie]:
        return self._movies

    def add_rating(self, user: User, movie: Movie, rating: MovieRating) -> None:
        if user.user_id not in self._user_movies:
            self._user_movies[user.user_id] = set()
            self._users.append(user)
        self._user_movies[user.user_id].add(movie.movie_id)
        if movie.movie_id not in self._movie_ratings:
            self._movie_ratings[movie.movie_id] = {}
            self._movies.append(movie)
        self._movie_ratings[movie.movie_id][user.user_id] = rating

    def get_average_rating(self, movie_id: int) -> float:
        if movie_id not in self._movie_ratings:
            return MovieRating.NOT_SEEN.value
        average_rating = 0
        for rating in self._movie_ratings[movie_id].values():
            average_rating += rating.value
        average_rating /= len(self._movie_ratings[movie_id].values())
        return average_rating

class Recommender:
    def __init__(self, data: RatingsData):
        self._data = data

    def recommend_movie(self, user: User) -> Movie:
        if user.user_id in self._data.user_movies:
            return self._recommend_to_existing_user(user)
        else:
            return self._recommend_to_new_user(user)
    
    def _recommend_to_new_user(self, user: User) -> Optional[str]:
        "get the movie with the highest average rating"
        max_rating = -1
        recommended_movie = None
        for movie in self._data.movies:
            movie_rating = self._data.get_average_rating(movie.movie_id)
            if movie_rating > max_rating:
                max_rating = movie_rating
                recommended_movie = movie.movie_name
        return recommended_movie


    def _recommend_to_existing_user(self, user: User) -> Optional[str]:
        "find the user with the highest similarity, recommend their favorite movie that the user have not seen"
        similarity_score = float('inf')  # the lower, the better
        best_movie = None
        for other_user in self._data.users:
            if other_user == user:
                continue
            user_similarity_score = self._get_similarity_score(user, other_user)
            if user_similarity_score < similarity_score:
                similarity_score = user_similarity_score
                recommended_movie = self._recommend_unwatched_movie(user, other_user).movie_name
                best_movie = recommended_movie if recommended_movie else best_movie
        return best_movie

    def _get_similarity_score(self, user1: User, user2: User) -> float:
        both_seen_movies = self._data.user_movies[user1.user_id].intersection(self._data.user_movies[user2.user_id])
        if len(both_seen_movies) == 0:
            return float('inf')
        score = 0
        for i, movie in enumerate(both_seen_movies):
            score += abs(self._data.movie_ratings[movie][user1.user_id].value - self._data.movie_ratings[movie][user2.user_id].value)
        score /= (i+1)
        return score

    def _recommend_unwatched_movie(self, user: User, reviewer: User) -> Optional[Movie]:
        best_movie = None
        max_rating = -1
        for movie in self._data.movies:
            if movie.movie_id in self._data.user_movies[reviewer.user_id] and movie.movie_id not in self._data.user_movies[user.user_id]:
                rating = self._data.get_average_rating(movie.movie_id)
                if rating > max_rating:
                    max_rating = rating
                    best_movie = movie
        return best_movie
    
        
if __name__ == "__main__":
    user1 = User(1, 'User 1')
    user2 = User(2, 'User 2')
    user3 = User(3, 'User 3')

    movie1 = Movie(1, 'Batman Begins')
    movie2 = Movie(2, 'Liar Liar')
    movie3 = Movie(3, 'The Godfather')

    ratings = RatingsData()
    ratings.add_rating(user1, movie1, MovieRating.FIVE)
    ratings.add_rating(user1, movie2, MovieRating.TWO)
    ratings.add_rating(user2, movie2, MovieRating.TWO)
    ratings.add_rating(user2, movie3, MovieRating.FOUR)

    recommender = Recommender(ratings)

    print(recommender.recommend_movie(user1)) # The Godfather
    print(recommender.recommend_movie(user2)) # Batman Begins
    print(recommender.recommend_movie(user3)) # Batman Begins
