from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import os
import pygame
from PyQt5.QtCore import QTimer

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class SupportTab(QWidget):
    def __init__(self, get_resource_path):
        super().__init__()
        layout = QVBoxLayout()
        image_path = get_resource_path("resources/mouse.png")
        support_pixmap = QPixmap(image_path)
        image_label = ClickableLabel()
        image_label.setPixmap(support_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)
        support_text = QLabel("Need help?\nContact me at:\nviktortornborg@hotmail.com")
        support_text.setAlignment(Qt.AlignCenter)
        support_text.setStyleSheet("color: #cccccc; font-size: 16px;")
        layout.addWidget(support_text)
        self.setLayout(layout)

        # Initialize pygame mixer
        pygame.mixer.init()
        wav_path = get_resource_path("resources/wootRat_song.wav")
        abs_wav_path = os.path.abspath(wav_path)
        self.is_playing = False
        self.image_label = image_label
        self.stopped_pixmap = support_pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.playing_pixmap = QPixmap(get_resource_path("resources/rat.png")).scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(self.stopped_pixmap)

        def play_or_stop_sound():
            if not self.is_playing:
                print("Image clicked, starting playback:", abs_wav_path)
                pygame.mixer.music.load(abs_wav_path)
                pygame.mixer.music.play()
                self.is_playing = True
                self.image_label.setPixmap(self.playing_pixmap)
            else:
                print("Image clicked, stopping playback.")
                pygame.mixer.music.stop()
                self.is_playing = False
                self.image_label.setPixmap(self.stopped_pixmap)

        image_label.clicked.connect(play_or_stop_sound)

        # Optionally, reset image when song ends
        def on_music_end():
            if self.is_playing and not pygame.mixer.music.get_busy():
                self.is_playing = False
                self.image_label.setPixmap(self.stopped_pixmap)
        # Timer to check if music ended
        self.music_timer = QTimer(self)
        self.music_timer.timeout.connect(on_music_end)
        self.music_timer.start(500)