from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox

class KeyMappingTab(QWidget):
    def __init__(self, settings, direction_labels, all_keys, keycodes):
        super().__init__()
        layout = QVBoxLayout()
        self.key_mapping_dropdowns = {}
        for label in direction_labels:
            dropdown_label = QLabel(label)
            dropdown = QComboBox()
            dropdown.addItems(all_keys)
            saved_key = settings.get(label)
            if saved_key is not None:
                if isinstance(saved_key, int):
                    key_name = next((k for k, v in keycodes.items() if v == saved_key), all_keys[0])
                else:
                    key_name = saved_key
            else:
                key_name = all_keys[0]
            dropdown.setCurrentText(key_name)
            self.key_mapping_dropdowns[label] = dropdown
            layout.addWidget(dropdown_label)
            layout.addWidget(dropdown)
        self.setLayout(layout)