import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_movie_suggestions():
    selected_genre = genre_combobox.get()
    genre_link = 'https://www.imdb.com/search/title/?genres={}'.format(selected_genre)

    try:
        response = requests.get(genre_link)
    except requests.exceptions.RequestException as e:
        print(e)
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    movie_titles = []
    for movie in soup.find_all('div', class_='lister-item'):
        movie_titles.append(movie.h3.a.text)

    movie_suggestions_df = pd.DataFrame(movie_titles, columns=['Movie Title'])

    movie_suggestions_df = movie_suggestions_df.sort_values(by=['Movie Title'], ascending=True)

    movie_suggestions_list.delete(0, tk.END)

    for index, row in movie_suggestions_df.iterrows():
        movie_suggestions_list.insert(tk.END, row['Movie Title'])

root = tk.Tk()
root.title('Movie Suggestion App')
root.geometry('600x400')

frame = ttk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

genres = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Mystery", "Sci-Fi", "Thriller"]

genre_label = ttk.Label(frame, text='Select a genre:')
genre_label.grid(row=0, column=0, padx=5, pady=10)

genre_combobox = ttk.Combobox(frame, values=genres, width=40)
genre_combobox.grid(row=0, column=1, padx=5, pady=10)

submit_button = ttk.Button(frame, text='Submit', command=get_movie_suggestions)
submit_button.grid(row=0, column=2, padx=5, pady=10)

movie_suggestions_label = ttk.Label(frame, text='Suggested movies:')
movie_suggestions_label.grid(row=1, column=0, padx=5, pady=10)

movie_suggestions_list = tk.Listbox(frame, bg='lightgrey', fg='black', selectbackground='grey', width=50)
movie_suggestions_list.grid(row=1, column=1, padx=5, pady=10)

root.mainloop()
