from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox, QHBoxLayout
from utils.settings import VALUE_LABELS

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

        # Activation key option
        self.use_activation_key_checkbox = QCheckBox(VALUE_LABELS[8])
        self.use_activation_key_checkbox.setChecked(settings.get(VALUE_LABELS[8], False))
        layout.addWidget(self.use_activation_key_checkbox)

        activation_key_layout = QHBoxLayout()
        activation_key_label = QLabel(VALUE_LABELS[9])
        self.activation_key_dropdown = QComboBox()
        self.activation_key_dropdown.addItems(all_keys)
        saved_activation_key = settings.get(VALUE_LABELS[9])
        if saved_activation_key is not None:
            if isinstance(saved_activation_key, int):
                key_name = next((k for k, v in keycodes.items() if v == saved_activation_key), all_keys[0])
            else:
                key_name = saved_activation_key
            self.activation_key_dropdown.setCurrentText(key_name)
        else:
            self.activation_key_dropdown.setCurrentIndex(0)
        activation_key_layout.addWidget(activation_key_label)
        activation_key_layout.addWidget(self.activation_key_dropdown)
        layout.addLayout(activation_key_layout)

        # Enable/disable dropdown based on checkbox
        self.activation_key_dropdown.setEnabled(self.use_activation_key_checkbox.isChecked())
        self.use_activation_key_checkbox.stateChanged.connect(
            lambda state: self.activation_key_dropdown.setEnabled(state == 2)
        )

        self.setLayout(layout)