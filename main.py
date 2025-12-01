import kagglehub
import pandas as pd
import os
import networkx as nx

# Download latest version
# path = kagglehub.dataset_download("prajitdatta/movielens-100k-dataset")
path = "/Users/shivenpandya/.cache/kagglehub/datasets/prajitdatta/movielens-100k-dataset/versions/1"

print("Path to dataset files:", path)

# The actual data files are likely inside a 'ml-100k' subdirectory
data_dir = os.path.join(path, 'ml-100k')

# Check if the subdirectory exists, otherwise use the base path
if not os.path.exists(data_dir):
    data_dir = path

print(f"Data directory: {data_dir}")
print("Files in directory:", os.listdir(data_dir))

# Create a graph
movie_graph = nx.MultiDiGraph()

# Process genre data
genres = ['unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film_Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

for genre in genres:
    movie_graph.add_node(genre, type="genre")

# Process movie data

file_path = os.path.join(data_dir, 'u.item')

if os.path.exists(file_path):
    columns = ['movie_id', 'title', 'release_date', 'video_release_date', 'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film_Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    movies = pd.read_csv(file_path, sep='|', names=columns, encoding='latin-1')
else:
    raise Exception(f"File not found: {file_path}")

print("Following are the movies:")
for item in movies.iterrows():
    movie_info = item[1]
    genre_list = list(movie_info)[5:]
    genre_list = [genres[i] for i, genre in enumerate(genre_list) if genre == 1]
    movie_id = movie_info['movie_id']
    title = movie_info['title']
    release_date = movie_info['release_date']
    movie_graph.add_node(f"movie_{movie_id}", type="movie", title=title, release_date=release_date)
    for genre in genre_list:
        movie_graph.add_edge(f"movie_{movie_id}", genre, type="has_genre")

# Process user data

file_path = os.path.join(data_dir, 'u.user')

if os.path.exists(file_path):
    columns = ['user_id', 'age', 'gender', 'occupation', 'zip_code']
    users = pd.read_csv(file_path, sep='|', names=columns, encoding='latin-1')
else:
    raise Exception(f"File not found: {file_path}")

for user in users.iterrows():
    user_info = user[1]
    user_id = user_info['user_id']
    age = user_info['age']
    gender = user_info['gender']
    occupation = user_info['occupation']
    zip_code = user_info['zip_code']
    movie_graph.add_node(f"user_{user_id}", type="user", age=age, gender=gender, occupation=occupation, zip_code=zip_code)

# Process user ratings

file_path = os.path.join(data_dir, 'u.data')

if os.path.exists(file_path):
    columns = ['user_id', 'item_id', 'rating', 'timestamp']
    ratings = pd.read_csv(file_path, sep='\t', names=columns, encoding='latin-1')
else:
    raise Exception(f"File not found: {file_path}")

for rating in ratings.iterrows():
    rating_info = rating[1]
    user_id = rating_info['user_id']
    movie_id = rating_info['item_id']
    rating = rating_info['rating']
    timestamp = rating_info['timestamp']
    movie_graph.add_edge(f"user_{user_id}", f"movie_{movie_id}", type="RATED", rating=rating, timestamp=timestamp)

print("Number of nodes:", movie_graph.number_of_nodes())
print("Number of edges:", movie_graph.number_of_edges())

print([x for x in movie_graph.successors("user_42") if movie_graph["user_42"][x][0]["type"]=="RATED"])


