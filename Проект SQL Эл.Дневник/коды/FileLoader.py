from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class FileOpen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Рекомендации")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # Только для чтения
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        self.load_file()

    def load_file(self):
        with open("recomend.txt", 'r', encoding='utf-8') as f:
            content = f.read()
            self.text_edit.setText(content)
