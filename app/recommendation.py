# coding: utf-8

# All the recommandation logic and algorithms goes here

from random import choice

from app.User import User
import sys
import numpy as np
from sklearn.cluster import KMeans
class Recommendation:

    def __init__(self, movielens):

        # Dictionary of movies
        # The structure of a movie is the following:
        #     * id (which is the movie number, you can access to the movie with "self.movies[movie_id]")
        #     * title
        #     * release_date (year when the movie first aired)
        #     * adventure (=1 if the movie is about an adventure, =0 otherwise)
        #     * drama (=1 if the movie is about a drama, =0 otherwise)
        #     * ... (the list of genres)
        self.movies = movielens.movies

        # List of ratings
        # The structure of a rating is the following:
        #     * movie (with the movie number)
        #     * user (with the user number)
        #     * is_appreciated (in the case of simplified rating, whether or not the user liked the movie)
        #     * score (in the case of rating, the score given by the user)
        self.ratings = movielens.simplified_ratings

        # This is the set of users in the training set
        self.test_users = {}

        # Launch the process of ratings
        self.process_ratings_to_users()
        self.genres = []
        for movie in self.movies.values():
            self.genres.append(self.calculGenre(movie))
        self.genres = np.array(self.genres)

        self.cluster = KMeans(10)
        self.cluster.fit(self.genres)
        reload(sys)
        sys.setdefaultencoding('utf8')

    @staticmethod
    def calculGenre(movie):
        vecteurGenre = [movie.unknown,
        movie.action,
        movie.adventure,
        movie.animation,
        movie.children,
        movie.comedy,
        movie.crime,
        movie.documentary,
        movie.drama,
        movie.fantasy,
        movie.film_noir,
        movie.horror,
        movie.musical,
        movie.mystery,
        movie.romance,
        movie.sci_fi,
        movie.thriller,
        movie.war,
        movie.western]
        return vecteurGenre

    # To process ratings, users associated to ratings are created and every rating is then stored in its user
    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating.user)
            movie = self.movies[rating.movie]
            if hasattr(rating, 'is_appreciated'):
                if rating.is_appreciated:
                    user.good_ratings.append(movie)
                else:
                    user.bad_ratings.append(movie)
            if hasattr(rating, 'score'):
                user.ratings[movie.id] = rating.score

    # Register a user if it does not exist and return it
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Display the recommendation for a user
    def make_recommendation(self, user):
        #movie = choice(list(self.movies.values())).title
        #print(self.test_users)
        similarities = self.compute_all_similarities(user)
        otherUserMaxs = []
        for i in range(5):
            otherUserMaxs.append(choice(list(self.test_users.values())))
        simMax = similarities[self.miniMaxUsers(otherUserMaxs, similarities)]
        for otherUser in similarities:
            sim = similarities[otherUser]
            if simMax < sim:
                aTej = self.miniMaxUsers(otherUserMaxs, similarities)
                otherUserMaxs.remove(aTej)
                otherUserMaxs.append(otherUser)
                simMax = similarities[self.miniMaxUsers(otherUserMaxs, similarities)]
        titles = []
        for userMax in otherUserMaxs:
            movies = userMax.good_ratings
            for movie in movies:
                if movie.title not in titles:
                    titles.append(movie.title)
        return "Vos recommandations : " + ", ".join(titles)

    def miniMaxUsers(self, maxUsers, similarities):
        userMin = 0
        simMin = 10000
        for userBIS in maxUsers:
            currentSim = similarities[userBIS]
            if currentSim < simMin:
                userMin = userBIS
                simMin = similarities[userBIS]
        return userMin


    # Compute the similarity between two users
    @staticmethod
    def get_similarity(user_a, user_b):
        similarity = 0
        for movie in user_a.good_ratings:
            if movie in user_b.good_ratings:
                similarity += 1
            elif movie in user_b.bad_ratings:
                similarity -= 1
        for movie in user_a.bad_ratings:
            if movie in user_b.bad_ratings:
                similarity += 1
            elif movie in user_b.good_ratings:
                similarity -= 1
        norm = Recommendation.get_user_norm(user_a)*Recommendation.get_user_norm(user_b)
        return similarity/norm

    # Compute the similarity between a user and all the users in the data set
    def compute_all_similarities(self, user):
        all_similarities = {}
        for other_user in self.test_users.values():
            all_similarities[other_user]= self.get_similarity(user, other_user)
        return all_similarities

    @staticmethod
    def get_best_movies_from_users(users):
        return []

    @staticmethod
    def get_user_appreciated_movies(user):
        return []

    @staticmethod
    def get_user_norm(user):
        return len(user.good_ratings) + len(user.bad_ratings) + len(user.neutral_ratings)

    # Return a vector with the normalised ratings of a user
    @staticmethod
    def get_normalised_cluster_notations(user):
        return []
