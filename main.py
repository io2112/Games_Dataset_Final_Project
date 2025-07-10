import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt

# create database
conn = sqlite3.connect("games.db")
cursor = conn.cursor()

# make table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        genre TEXT,
        release_year INTEGER,
        publisher TEXT,
        rating REAL
    )
""")
conn.commit()

class GameApp(QMainWindow):
    def __init__(self):
        super().__init__()
        #load every widget from qt designer file
        loadUi("FinalProjectGui.ui", self)
        
        #connect buttons
        self.addButton.clicked.connect(self.add_game)
        self.deleteButton.clicked.connect(self.delete_game)
        self.updateButton.clicked.connect(self.update_game)
        self.searchInput.returnPressed.connect(self.search_game)
        self.applyFilters.clicked.connect(self.apply_filters)
        self.showChart.clicked.connect(self.show_stats)

        #show all games when program starts
        self.show_all_games()

    #pop-up message
    def show_message(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec_()
    
    def show_all_games(self):
        cursor.execute("SELECT title, genre, release_year, publisher, rating FROM games")
        games = cursor.fetchall()
        
        self.tableWidget.setRowCount(0)     #clears old rows
        for i, game in enumerate(games):
            self.tableWidget.insertRow(i)
            for j, data in enumerate(game):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data)))
    
    def add_game(self):
        title = self.titleInput.text()
        if title == "":
            self.show_message("Please enter a title!")
            return
        
        genre = self.genreInput.currentText()
        year = self.yearInput.value()
        publisher = self.publiserInput.text()
        rating = self.ratingInput.value()
        
        cursor.execute("INSERT INTO games (title, genre, release_year, publisher, rating) VALUES (?,?,?,?,?)", 
                      (title, genre, year, publisher, rating))
        conn.commit()
        
        self.show_message("Game added!")
        self.show_all_games()
    
    def delete_game(self):
        title = self.titleInput.text()
        if title == "":
            self.show_message("Please enter a title to delete!")
            return
        
        cursor.execute("DELETE FROM games WHERE title = ?", (title,))
        conn.commit()
        
        self.show_message("Game deleted!")
        self.show_all_games()
    
    def update_game(self):
        title = self.titleInput.text()
        if title == "":
            self.show_message("Please enter a title to update!")
            return
        
        rating = self.ratingInput.value()
        cursor.execute("UPDATE games SET rating = ? WHERE title = ?", (rating, title))
        conn.commit()
        
        self.show_message("Rating updated!")
        self.show_all_games()
    
    def search_game(self):
        search_text = self.searchInput.text()
        cursor.execute("SELECT title, genre, release_year, publisher, rating FROM games WHERE title LIKE ?", 
                      ("%" + search_text + "%",))
        games = cursor.fetchall()
        
        self.tableWidget.setRowCount(0)
        for i, game in enumerate(games):
            self.tableWidget.insertRow(i)
            for j, data in enumerate(game):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data)))
    
    def apply_filters(self):
        genre = self.filterGenre.currentText()
        year = self.filterYear.value()
        rating = self.filterRating.value()
        
        query = "SELECT title, genre, release_year, publisher, rating FROM games WHERE 1=1"
        params = []
        
        if genre != "All":
            query = query + " AND genre = ?"
            params.append(genre)
        
        if year > 0:
            query = query + " AND release_year = ?"
            params.append(year)
        
        if rating > 0:
            query = query + " AND rating >= ?"
            params.append(rating)
        
        cursor.execute(query, params)
        games = cursor.fetchall()
        
        self.tableWidget.setRowCount(0)
        for i, game in enumerate(games):
            self.tableWidget.insertRow(i)
            for j, data in enumerate(game):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data)))

    def show_stats(self):
        cursor.execute("SELECT genre, AVG(rating) FROM games GROUP BY genre")
        data = cursor.fetchall()

        if len(data) == 0:
            self.show_message("No data!")
            return

        genres = []
        ratings = []
        for row in data:
            genres.append(row[0])
            ratings.append(row[1])

        plt.bar(genres, ratings)
        plt.title("Average Rating by Genre")
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameApp()
    window.setWindowTitle("Game Database")
    window.show()
    sys.exit(app.exec_())
