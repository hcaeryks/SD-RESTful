DROP TABLE IF EXISTS folder;
DROP TABLE IF EXISTS artist;
DROP TABLE IF EXISTS song;

CREATE TABLE folder (
    number INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    theme TEXT,
    slogan TEXT
);

CREATE TABLE artist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    pseudonym TEXT
);

CREATE TABLE song (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    bpm TEXT,
    length INTEGER,
    genre TEXT,
    artist INTEGER,
    folder INTEGER,
    ln BOOLEAN DEFAULT 0,
    diffN INTEGER,
    diffH INTEGER,
    diffA INTEGER,
    diffL INTEGER,
    FOREIGN KEY (artist) REFERENCES artist(id) ON DELETE SET NULL,
    FOREIGN KEY (folder) REFERENCES folder(number) ON DELETE CASCADE
);

INSERT INTO folder (number, title, theme, slogan) VALUES
(1, 'HEROIC VERSE', 'Heroic', 'Be a Hero!'),
(2, 'BISTROVER', 'Bistro', 'Bon Appétit!'),
(3, 'ROOTAGE', 'Cyber', 'Welcome to the Network'),
(4, 'CANNON BALLERS', 'Race', 'Start Your Engines!'),
(5, 'SINOBUZ', 'Ninja', 'Unleash Your Ninja Spirit');

INSERT INTO artist (id, name, pseudonym) VALUES
(1, 'Takayuki Ishikawa', 'dj TAKA'),
(2, 'Naoki Maeda', 'NAOKI'),
(3, 'Ryu☆', 'Ryu*'),
(4, 'Yoshitaka Nishimura', 'DJ YOSHITAKA'),
(5, 'Yoshihiro Tagawa', 'TAG');

INSERT INTO song (id, title, bpm, length, genre, artist, folder, ln, diffN, diffH, diffA, diffL) VALUES
(1, 'Everlasting Message', '145', 200, 'Trance', 1, 1, 0, 5, 8, 11, 0),
(2, 'Holygrail', '150', 180, 'Hard Dance', 1, 2, 1, 4, 7, 10, 0),
(3, 'FIRE FIRE', '150', 190, 'Hardcore', 2, 3, 0, 6, 9, 12, 0),
(4, 'AGEHA', '144', 195, 'Trance', 3, 4, 0, 5, 8, 11, 0),
(5, 'Gold Rush', '160', 175, 'Pop', 4, 5, 1, 4, 7, 10, 0),
(6, 'Love Is Eternity', '155', 185, 'Happy Hardcore', 3, 1, 0, 5, 8, 11, 0),
(7, 'Symbolic', '172', 190, 'Hard Trance', 2, 2, 1, 6, 9, 12, 0),
(8, 'Rising in the Sun', '158', 200, 'Pop Trance', 5, 3, 0, 5, 8, 11, 0),
(9, 'Sakura Storm', '180', 190, 'Japanese Pop', 4, 4, 1, 6, 9, 12, 0),
(10, 'Blue Rain', '140', 210, 'Drum & Bass', 5, 5, 0, 5, 8, 11, 0);

INSERT INTO song_artist (song_id, artist_id) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 3),
(5, 4),
(6, 3),
(7, 2),
(8, 5),
(9, 4),
(10, 5);
