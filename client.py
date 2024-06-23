import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import sv_ttk
import json

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Database Client")

        self.create_widgets()
        self.fetch_and_display_songs()
        self.fetch_and_display_artists()
        self.fetch_and_display_folders()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.song_frame = ttk.Frame(self.notebook)
        self.artist_frame = ttk.Frame(self.notebook)
        self.folder_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.song_frame, text="Songs")
        self.notebook.add(self.artist_frame, text="Artists")
        self.notebook.add(self.folder_frame, text="Folders")

        self.create_song_tab()
        self.create_artist_tab()
        self.create_folder_tab()

    def create_song_tab(self):
        self.tree_songs = ttk.Treeview(self.song_frame, columns=("ID", "Title", "BPM", "Length", "Genre", "Artist", "Folder", "LN", "DiffN", "DiffH", "DiffA", "DiffL"), show="headings")
        for col in self.tree_songs["columns"]:
            self.tree_songs.heading(col, text=col)
        self.tree_songs.pack(fill=tk.BOTH, expand=True)

        song_button_frame = ttk.Frame(self.song_frame)
        song_button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(song_button_frame, text="Add Song", command=self.add_song).pack(side=tk.LEFT, padx=5)
        ttk.Button(song_button_frame, text="Edit Song", command=self.edit_song).pack(side=tk.LEFT, padx=5)
        ttk.Button(song_button_frame, text="Delete Song", command=self.delete_song).pack(side=tk.LEFT, padx=5)
        ttk.Button(song_button_frame, text="Search Songs", command=self.search_songs).pack(side=tk.LEFT, padx=5)

    def create_artist_tab(self):
        self.tree_artists = ttk.Treeview(self.artist_frame, columns=("ID", "Name", "Pseudonym"), show="headings")
        for col in self.tree_artists["columns"]:
            self.tree_artists.heading(col, text=col)
        self.tree_artists.pack(fill=tk.BOTH, expand=True)

        artist_button_frame = ttk.Frame(self.artist_frame)
        artist_button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(artist_button_frame, text="Add Artist", command=self.add_artist).pack(side=tk.LEFT, padx=5)
        ttk.Button(artist_button_frame, text="Edit Artist", command=self.edit_artist).pack(side=tk.LEFT, padx=5)
        ttk.Button(artist_button_frame, text="Delete Artist", command=self.delete_artist).pack(side=tk.LEFT, padx=5)
        ttk.Button(artist_button_frame, text="Search Artists", command=self.search_artists).pack(side=tk.LEFT, padx=5)

    def create_folder_tab(self):
        self.tree_folders = ttk.Treeview(self.folder_frame, columns=("Number", "Title", "Theme", "Slogan"), show="headings")
        for col in self.tree_folders["columns"]:
            self.tree_folders.heading(col, text=col)
        self.tree_folders.pack(fill=tk.BOTH, expand=True)

        folder_button_frame = ttk.Frame(self.folder_frame)
        folder_button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(folder_button_frame, text="Add Folder", command=self.add_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(folder_button_frame, text="Edit Folder", command=self.edit_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(folder_button_frame, text="Delete Folder", command=self.delete_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(folder_button_frame, text="Search Folders", command=self.search_folders).pack(side=tk.LEFT, padx=5)

    def fetch_and_display_songs(self):
        response = requests.get("http://localhost:5000/songs")
        if response.status_code == 200:
            data = response.json()
            self.tree_songs.delete(*self.tree_songs.get_children())
            for song in data:
                self.tree_songs.insert("", tk.END, values=(song["id"], song["title"], song["bpm"], song["length"], song["genre"], song["artist"], song["folder"], song["ln"], song["diffN"], song["diffH"], song["diffA"], song["diffL"]))

    def fetch_and_display_artists(self):
        response = requests.get("http://localhost:5000/artists")
        if response.status_code == 200:
            data = response.json()
            self.tree_artists.delete(*self.tree_artists.get_children())
            for artist in data:
                self.tree_artists.insert("", tk.END, values=(artist["id"], artist["name"], artist["pseudonym"]))

    def fetch_and_display_folders(self):
        response = requests.get("http://localhost:5000/folders")
        if response.status_code == 200:
            data = response.json()
            self.tree_folders.delete(*self.tree_folders.get_children())
            for folder in data:
                self.tree_folders.insert("", tk.END, values=(folder["number"], folder["title"], folder["theme"], folder["slogan"]))

    def add_song(self):
        data = {
            "title": simpledialog.askstring("Input", "Title"),
            "bpm": simpledialog.askinteger("Input", "BPM"),
            "length": simpledialog.askinteger("Input", "Length"),
            "genre": simpledialog.askstring("Input", "Genre"),
            "artist": simpledialog.askinteger("Input", "Artist ID"),
            "folder": simpledialog.askinteger("Input", "Folder Number"),
            "ln": simpledialog.askinteger("Input", "LN"),
            "diffN": simpledialog.askinteger("Input", "DiffN"),
            "diffH": simpledialog.askinteger("Input", "DiffH"),
            "diffA": simpledialog.askinteger("Input", "DiffA"),
            "diffL": simpledialog.askinteger("Input", "DiffL"),
        }
        response = requests.post("http://localhost:5000/songs", json=data)
        if response.status_code == 201:
            messagebox.showinfo("Success", response.json()["message"])
            self.fetch_and_display_songs()

    def edit_song(self):
        selected_item = self.tree_songs.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No song selected")
            return

        item = self.tree_songs.item(selected_item)
        song_id = item["values"][0]
        data = {
            "title": simpledialog.askstring("Input", "Title", initialvalue=item["values"][1]),
            "bpm": simpledialog.askinteger("Input", "BPM", initialvalue=item["values"][2]),
            "length": simpledialog.askinteger("Input", "Length", initialvalue=item["values"][3]),
            "genre": simpledialog.askstring("Input", "Genre", initialvalue=item["values"][4]),
            "artist": simpledialog.askinteger("Input", "Artist ID", initialvalue=item["values"][5]),
            "folder": simpledialog.askinteger("Input", "Folder Number", initialvalue=item["values"][6]),
            "ln": simpledialog.askinteger("Input", "LN", initialvalue=item["values"][7]),
            "diffN": simpledialog.askinteger("Input", "DiffN", initialvalue=item["values"][8]),
            "diffH": simpledialog.askinteger("Input", "DiffH", initialvalue=item["values"][9]),
            "diffA": simpledialog.askinteger("Input", "DiffA", initialvalue=item["values"][10]),
            "diffL": simpledialog.askinteger("Input", "DiffL", initialvalue=item["values"][11]),
        }
        response = requests.put(f"http://localhost:5000/songs/{song_id}", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Success", response.json()["message"])
            self.fetch_and_display_songs()
        else:
            messagebox.showinfo("error", response.json()["message"])

    def delete_song(self):
        selected_item = self.tree_songs.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No song selected")
            return

        item = self.tree_songs.item(selected_item)
        song_id = item["values"][0]
        response = requests.delete(f"http://localhost:5000/songs/{song_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", response.json()["message"])
            self.fetch_and_display_songs()
        else:
            messagebox.showinfo("error", response.json()["message"])

    def add_artist(self):
        data = {
            "name": simpledialog.askstring("Input", "Name"),
            "pseudonym": simpledialog.askstring("Input", "Pseudonym"),
        }
        response = requests.post("http://localhost:5000/artists", json=data)
        if response.status_code == 201:
            messagebox.showinfo("Success", response.json()["message"])
            self.fetch_and_display_artists()

    def edit_artist(self):
        selected_item = self.tree_artists.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No artist selected")
            return

        item = self.tree_artists.item(selected_item)
        artist_id = item["values"][0]
        data = {
            "name": simpledialog.askstring("Input", "Name", initialvalue=item["values"][1]),
            "pseudonym": simpledialog.askstring("Input", "Pseudonym", initialvalue=item["values"][2]),
        }
        response = requests.put(f"http://localhost:5000/artists/{artist_id}", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Success", response.json()["message"])
            self.fetch_and_display_artists()
        else:
            messagebox.showinfo("error", response.json()["message"])

    def delete_artist(self):
        selected_item = self.tree_artists.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No artist selected")
            return

        item = self.tree_artists.item(selected_item)
        artist_id = item["values"][0]
        response = requests.delete(f"http://localhost:5000/artists/{artist_id}")
        if response.status_code == 200:
            messagebox.showinfo("message", response.json()["message"])
            self.fetch_and_display_artists()
        else:
            messagebox.showinfo("error", response.json()["message"])

    def add_folder(self):
        data = {
            "number": simpledialog.askinteger("Input", "Number"),
            "title": simpledialog.askstring("Input", "Title"),
            "theme": simpledialog.askstring("Input", "Theme"),
            "slogan": simpledialog.askstring("Input", "Slogan"),
        }
        response = requests.post("http://localhost:5000/folders", json=data)
        if response.status_code == 201:
            messagebox.showinfo("Success", response.json()["message"])
            self.fetch_and_display_folders()

    def edit_folder(self):
        selected_item = self.tree_folders.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No folder selected")
            return

        item = self.tree_folders.item(selected_item)
        folder_id = item["values"][0]
        data = {
            "number": simpledialog.askinteger("Input", "Number", initialvalue=item["values"][0]),
            "title": simpledialog.askstring("Input", "Title", initialvalue=item["values"][1]),
            "theme": simpledialog.askstring("Input", "Theme", initialvalue=item["values"][2]),
            "slogan": simpledialog.askstring("Input", "Slogan", initialvalue=item["values"][3]),
        }
        response = requests.put(f"http://localhost:5000/folders/{folder_id}", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Success", response.json()["message"])
            self.fetch_and_display_folders()
        else:
            messagebox.showinfo("error", response.json()["message"])

    def delete_folder(self):
        selected_item = self.tree_folders.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No folder selected")
            return

        item = self.tree_folders.item(selected_item)
        folder_id = item["values"][0]
        response = requests.delete(f"http://localhost:5000/folders/{folder_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", response.json()["message"])
            self.fetch_and_display_folders()
        else:
            messagebox.showinfo("error", response.json()["message"])

    def search_songs(self):
        self.create_search_window(
            {
                "title": tk.StringVar(),
                "bpm": tk.StringVar(),
                "length": tk.StringVar(),
                "genre": tk.StringVar(),
                "artist": tk.StringVar(),
                "folder": tk.StringVar(),
                "ln": tk.StringVar(),
                "diffN": tk.StringVar(),
                "diffH": tk.StringVar(),
                "diffA": tk.StringVar(),
                "diffL": tk.StringVar(),
            },
            "Search Songs",
            self.perform_search_songs
        )

    def search_artists(self):
        self.create_search_window(
            {
                "name": tk.StringVar(),
                "pseudonym": tk.StringVar(),
            },
            "Search Artists",
            self.perform_search_artists
        )

    def search_folders(self):
        self.create_search_window(
            {
                "number": tk.StringVar(),
                "title": tk.StringVar(),
                "theme": tk.StringVar(),
                "slogan": tk.StringVar(),
            },
            "Search Folders",
            self.perform_search_folders
        )

    def create_search_window(self, params, title, search_func):
        search_window = tk.Toplevel(self)
        search_window.title(title)

        for idx, (key, var) in enumerate(params.items()):
            ttk.Label(search_window, text=key.capitalize()).grid(row=idx, column=0, padx=5, pady=5)
            ttk.Entry(search_window, textvariable=var).grid(row=idx, column=1, padx=5, pady=5)

        ttk.Button(search_window, text="Search", command=lambda: search_func(params, search_window)).grid(row=len(params), column=0, columnspan=2, pady=10)

    def perform_search_songs(self, params, window):
        query_params = {key: var.get() for key, var in params.items() if var.get()}
        response = requests.get("http://localhost:5000/songs", params=query_params)
        if response.status_code == 200:
            data = response.json()
            self.tree_songs.delete(*self.tree_songs.get_children())
            for song in data:
                self.tree_songs.insert("", tk.END, values=(song["id"], song["title"], song["bpm"], song["length"], song["genre"], song["artist"], song["folder"], song["ln"], song["diffN"], song["diffH"], song["diffA"], song["diffL"]))
            window.destroy()

    def perform_search_artists(self, params, window):
        query_params = {key: var.get() for key, var in params.items() if var.get()}
        response = requests.get("http://localhost:5000/artists", params=query_params)
        if response.status_code == 200:
            data = response.json()
            self.tree_artists.delete(*self.tree_artists.get_children())
            for artist in data:
                self.tree_artists.insert("", tk.END, values=(artist["id"], artist["name"], artist["pseudonym"]))
            window.destroy()

    def perform_search_folders(self, params, window):
        query_params = {key: var.get() for key, var in params.items() if var.get()}
        response = requests.get("http://localhost:5000/folders", params=query_params)
        if response.status_code == 200:
            data = response.json()
            self.tree_folders.delete(*self.tree_folders.get_children())
            for folder in data:
                self.tree_folders.insert("", tk.END, values=(folder["number"], folder["title"], folder["theme"], folder["slogan"]))
            window.destroy()

if __name__ == "__main__":
    app = Application()
    sv_ttk.set_theme("dark")
    app.mainloop()
