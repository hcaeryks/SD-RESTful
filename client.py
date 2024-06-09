import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests, sv_ttk

BASE_URL = "http://127.0.0.1:5000"

def fetch_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return []

def post_data(endpoint, data):
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to create record: {e}")
        return None

def put_data(endpoint, data):
    try:
        response = requests.put(f"{BASE_URL}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to update record: {e}")
        return None

def delete_data(endpoint):
    try:
        response = requests.delete(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to delete record: {e}")
        return None

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Database Client")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        self.folder_tab = FolderTab(notebook)
        self.artist_tab = ArtistTab(notebook)
        self.song_tab = SongTab(notebook)

        notebook.add(self.folder_tab, text="Folders")
        notebook.add(self.artist_tab, text="Artists")
        notebook.add(self.song_tab, text="Songs")

class FolderTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.fetch_and_display()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("Number", "Title", "Theme", "Slogan"), show="headings")
        self.tree.heading("Number", text="Number")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Theme", text="Theme")
        self.tree.heading("Slogan", text="Slogan")
        self.tree.pack(fill='both', expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', expand=True)

        ttk.Button(btn_frame, text="Refresh", command=self.fetch_and_display).pack(side='left')
        ttk.Button(btn_frame, text="Add", command=self.add_folder).pack(side='left')
        ttk.Button(btn_frame, text="Update", command=self.update_folder).pack(side='left')
        ttk.Button(btn_frame, text="Delete", command=self.delete_folder).pack(side='left')

    def fetch_and_display(self):
        self.tree.delete(*self.tree.get_children())
        folders = fetch_data("folders")
        for folder in folders:
            self.tree.insert("", "end", values=(folder['number'], folder['title'], folder['theme'], folder['slogan']))

    def add_folder(self):
        data = {
            "number": simpledialog.askinteger("Input", "Number"),
            "title": simpledialog.askstring("Input", "Title"),
            "theme": simpledialog.askstring("Input", "Theme"),
            "slogan": simpledialog.askstring("Input", "Slogan"),
        }
        if data["number"] and data["title"]:
            result = post_data("folders", data)
            if result:
                messagebox.showinfo("Success", "Folder created successfully")
                self.fetch_and_display()

    def update_folder(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No folder selected")
            return

        item = self.tree.item(selected_item)
        folder_number = item["values"][0]
        data = {
            "title": simpledialog.askstring("Input", "Title", initialvalue=item["values"][1]),
            "theme": simpledialog.askstring("Input", "Theme", initialvalue=item["values"][2]),
            "slogan": simpledialog.askstring("Input", "Slogan", initialvalue=item["values"][3]),
        }
        result = put_data(f"folders/{folder_number}", data)
        if result:
            messagebox.showinfo("Success", "Folder updated successfully")
            self.fetch_and_display()

    def delete_folder(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No folder selected")
            return

        item = self.tree.item(selected_item)
        folder_number = item["values"][0]
        result = delete_data(f"folders/{folder_number}")
        if result:
            messagebox.showinfo("Success", "Folder deleted successfully")
            self.fetch_and_display()

class ArtistTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.fetch_and_display()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Pseudonym"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Pseudonym", text="Pseudonym")
        self.tree.pack(fill='both', expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', expand=True)

        ttk.Button(btn_frame, text="Refresh", command=self.fetch_and_display).pack(side='left')
        ttk.Button(btn_frame, text="Add", command=self.add_artist).pack(side='left')
        ttk.Button(btn_frame, text="Update", command=self.update_artist).pack(side='left')
        ttk.Button(btn_frame, text="Delete", command=self.delete_artist).pack(side='left')

    def fetch_and_display(self):
        self.tree.delete(*self.tree.get_children())
        artists = fetch_data("artists")
        for artist in artists:
            self.tree.insert("", "end", values=(artist['id'], artist['name'], artist['pseudonym']))

    def add_artist(self):
        data = {
            "name": simpledialog.askstring("Input", "Name"),
            "pseudonym": simpledialog.askstring("Input", "Pseudonym"),
        }
        if data["name"]:
            result = post_data("artists", data)
            if result:
                messagebox.showinfo("Success", "Artist created successfully")
                self.fetch_and_display()

    def update_artist(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No artist selected")
            return

        item = self.tree.item(selected_item)
        artist_id = item["values"][0]
        data = {
            "name": simpledialog.askstring("Input", "Name", initialvalue=item["values"][1]),
            "pseudonym": simpledialog.askstring("Input", "Pseudonym", initialvalue=item["values"][2]),
        }
        result = put_data(f"artists/{artist_id}", data)
        if result:
            messagebox.showinfo("Success", "Artist updated successfully")
            self.fetch_and_display()

    def delete_artist(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No artist selected")
            return

        item = self.tree.item(selected_item)
        artist_id = item["values"][0]
        result = delete_data(f"artists/{artist_id}")
        if result:
            messagebox.showinfo("Success", "Artist deleted successfully")
            self.fetch_and_display()

class SongTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.fetch_and_display()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "BPM", "Length", "Genre", "Artist", "Folder", "LN", "DiffN", "DiffH", "DiffA", "DiffL"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("BPM", text="BPM")
        self.tree.heading("Length", text="Length")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Artist", text="Artist")
        self.tree.heading("Folder", text="Folder")
        self.tree.heading("LN", text="LN")
        self.tree.heading("DiffN", text="DiffN")
        self.tree.heading("DiffH", text="DiffH")
        self.tree.heading("DiffA", text="DiffA")
        self.tree.heading("DiffL", text="DiffL")
        self.tree.pack(fill='both', expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', expand=True)

        ttk.Button(btn_frame, text="Refresh", command=self.fetch_and_display).pack(side='left')
        ttk.Button(btn_frame, text="Add", command=self.add_song).pack(side='left')
        ttk.Button(btn_frame, text="Update", command=self.update_song).pack(side='left')
        ttk.Button(btn_frame, text="Delete", command=self.delete_song).pack(side='left')

    def fetch_and_display(self):
        self.tree.delete(*self.tree.get_children())
        songs = fetch_data("songs")
        for song in songs:
            self.tree.insert("", "end", values=(song['id'], song['title'], song['bpm'], song['length'], song['genre'], song['artist'], song['folder'], song['ln'], song['diffN'], song['diffH'], song['diffA'], song['diffL']))

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
        if data["title"] and data["artist"] and data["folder"]:
            result = post_data("songs", data)
            if result:
                messagebox.showinfo("Success", "Song created successfully")
                self.fetch_and_display()

    def update_song(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No song selected")
            return

        item = self.tree.item(selected_item)
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
        result = put_data(f"songs/{song_id}", data)
        if result:
            messagebox.showinfo("Success", "Song updated successfully")
            self.fetch_and_display()

    def delete_song(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No song selected")
            return

        item = self.tree.item(selected_item)
        song_id = item["values"][0]
        result = delete_data(f"songs/{song_id}")
        if result:
            messagebox.showinfo("Success", "Song deleted successfully")
            self.fetch_and_display()

if __name__ == "__main__":
    app = Application()
    sv_ttk.set_theme("dark")
    app.mainloop()
