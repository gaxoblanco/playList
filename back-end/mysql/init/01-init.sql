-- Crear tabla de bandas
CREATE TABLE IF NOT EXISTS band_spotify (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_spotify VARCHAR(30) NOT NULL UNIQUE,
    names VARCHAR(100) NOT NULL,
    img_url VARCHAR(255),
    popularidad INT,
    date_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_up TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Crear tabla de géneros
CREATE TABLE IF NOT EXISTS genre_spotify (
    id INT AUTO_INCREMENT PRIMARY KEY,
    names VARCHAR(50) NOT NULL UNIQUE
);

-- Crear tabla de relación muchos a muchos entre band y géneros
CREATE TABLE IF NOT EXISTS band_genre_spotify (
    id INT AUTO_INCREMENT PRIMARY KEY,
    band_id INT NOT NULL,
    genre_id INT NOT NULL,
    FOREIGN KEY (band_id) REFERENCES band_spotify(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre_spotify(id) ON DELETE CASCADE,
    UNIQUE KEY band_genre_unique (band_id, genre_id)
);

-- Insertar algunos géneros predeterminados
INSERT IGNORE INTO genre_spotify (names) VALUES 
('rock en español'),
('latin rock'),
('mexican rock'),
('latin pop'),
('pop'),
('rock'),
('electronic'),
('hip hop'),
('jazz'),
('classical');