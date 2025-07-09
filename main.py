### game_app.py
import sqlite3

conn = sqlite3.connect("games.db")
cursor = conn.cursor()

def show_all_games():
    cursor.execute("SELECT title, genre, release_year, publisher, rating FROM games LIMIT 10")
    games = cursor.fetchall()

    print("\nAll Games:")
    for game in games:
        title = game[0] or "Unknown Title"
        genre = game[1] or "Unknown Genre"
        year = game[2] or "Unknown Year"
        publisher = game[3] or "Unknown Publisher"
        rating = game[4] or "Unknown Rating"

        print("Title:", title)
        print("Genre:", genre)
        print("Release Year:", year)
        print("Publisher:", publisher)
        print("Rating:", rating)
        print("------")

def search_by_title():
    keyword = input("Enter part of the title: ")
    cursor.execute("SELECT * FROM games WHERE title LIKE ?", ('%' + keyword + '%',))
    results = cursor.fetchall()

    if results:
        for game in results:
            print(game)
    else:
        print("No game found with that title.")

def add_game():
    print("\nEnter new game details:")
    title = input("Title: ")
    genre = input("Genre: ")
    year = input("Release Year: ")
    publisher = input("Publisher: ")
    rating = input("Rating (e.g. 8.5): ")

    if not year.isdigit() or not rating.replace('.', '', 1).isdigit():
        print("Please enter valid numbers for year and rating.")
        return

    cursor.execute("""
        INSERT INTO games (title, genre, release_year, publisher, rating)
        VALUES (?, ?, ?, ?, ?)""", (title, genre, int(year), publisher, float(rating)))
    conn.commit()
    print("Game added successfully.")

def delete_game():
    title = input("Enter the title of the game to delete: ")
    cursor.execute("SELECT * FROM games WHERE title = ?", (title,))
    result = cursor.fetchone()

    if result:
        cursor.execute("DELETE FROM games WHERE title = ?", (title,))
        conn.commit()
        print("Game deleted successfully.")
    else:
        print("Game not found.")

def update_game():
    title = input("Enter the title of the game to update: ")
    cursor.execute("SELECT * FROM games WHERE title = ?", (title,))
    result = cursor.fetchone()

    if result:
        new_rating = input("Enter new rating: ")
        if new_rating.replace('.', '', 1).isdigit():
            cursor.execute("UPDATE games SET rating = ? WHERE title = ?", (float(new_rating), title))
            conn.commit()
            print("Rating updated successfully.")
        else:
            print("Invalid rating value.")
    else:
        print("Game not found.")

def filter_by_year():
    year = input("Enter release year: ")
    if not year.isdigit():
        print("Invalid year.")
        return
    cursor.execute("SELECT * FROM games WHERE release_year = ?", (int(year),))
    results = cursor.fetchall()
    if results:
        for game in results:
            print(game)
    else:
        print("No games found for that year.")

def filter_by_genre():
    genre = input("Enter genre: ")
    cursor.execute("SELECT * FROM games WHERE genre = ?", (genre,))
    results = cursor.fetchall()
    if results:
        for game in results:
            print(game)
    else:
        print("No games found for that genre.")

def filter_by_rating():
    rating = input("Enter minimum rating: ")
    if not rating.replace('.', '', 1).isdigit():
        print("Invalid rating.")
        return
    cursor.execute("SELECT * FROM games WHERE rating >= ?", (float(rating),))
    results = cursor.fetchall()
    if results:
        for game in results:
            print(game)
    else:
        print("No games found above that rating.")

# Example usage:
if __name__ == "__main__":
    while True:
        print("\nVideo Game Database")
        print("1. Show all games")
        print("2. Search by title")
        print("3. Add new game")
        print("4. Delete a game")
        print("5. Update game rating")
        print("6. Filter by release year")
        print("7. Filter by genre")
        print("8. Filter by rating")
        print("9. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            show_all_games()
        elif choice == '2':
            search_by_title()
        elif choice == '3':
            add_game()
        elif choice == '4':
            delete_game()
        elif choice == '5':
            update_game()
        elif choice == '6':
            filter_by_year()
        elif choice == '7':
            filter_by_genre()
        elif choice == '8':
            filter_by_rating()
        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
