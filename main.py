#!/usr/bin/env python3

import sys
import math
import logging
from os import path as os_path
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from PyQt6.QtGui import QDoubleValidator, QIcon, QPalette
from PyQt6.QtCore import Qt
from const import (
    BUTTONS,
    CALCULATION_CONFIG,
    ICON,
    INPUT_CONFIG,
    LICENSE,
    STYLE_SHEET,
    TITLE,
    TITLE_ABOUT,
)

BASE_DIR = os_path.dirname(os_path.abspath(__file__))


def _calculate_probability(z):
    try:
        probability = 1 / (1 + math.exp(-z)) * 100
    except OverflowError:
        probability = 100.0 if z > 0 else 0.0
    return probability


def calculate_ssc_risk(age, bpn, sofa, charlson_index, score):
    z = (
        -11.33
        + 0.11 * age
        + 0.999 * bpn
        + 0.037 * sofa
        + 0.089 * charlson_index
        + 0.162 * score
    )
    return _calculate_probability(z)


def calculate_ards_risk(bpn, sofa, charlson_index, copd, urea, pao2_fio2_index):
    z = (
        -2.692
        + 2.009 * bpn
        + 0.116 * sofa
        + 0.218 * charlson_index
        + 0.975 * copd
        + 0.066 * urea
        - 0.031 * pao2_fio2_index
    )
    return _calculate_probability(z)


def calculate_aki_risk(age, sofa, ckd, gfr):
    z = -1.84 + 0.028 * age + 0.041 * sofa + 0.272 * ckd - 0.038 * gfr
    return _calculate_probability(z)


def calculate_iis_risk(age, bpn, iap_mm, urea):
    z = -16.691 + 0.063 * age + 0.677 * bpn + 0.99 * iap_mm + 0.211 * urea
    return _calculate_probability(z)


def calculate_mods_risk(age, sofa, pao2_fio2_index, iap_cm, creatinine):
    z = (
        -8.3
        + 0.106 * age
        + 0.19 * sofa
        - 0.018 * pao2_fio2_index
        + 0.119 * iap_cm
        + 0.03 * creatinine
    )
    return _calculate_probability(z)


def calculate_psc_risk(age, bpn, leukocytes, bilirubin, crp7_crp1_ratio):
    z = (
        1.812
        - 0.016 * age
        + 0.538 * bpn
        + 0.019 * leukocytes
        + 0.003 * bilirubin
        - 1.765 * crp7_crp1_ratio
    )
    return _calculate_probability(z)


def calculate_sepsis_risk(bpn, hospital_day, sofa7, crp7_crp1_ratio):
    z = (
        -4.394
        + 0.986 * bpn
        + 0.556 * hospital_day
        + 0.461 * sofa7
        - 2.05 * crp7_crp1_ratio
    )
    return _calculate_probability(z)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(TITLE)
        self.resize(850, 650)

        self.inputs = {}
        self.outputs = {}

        self.validator = QDoubleValidator()
        self.validator.setLocale(self.locale())
        self.validator.setNotation(QDoubleValidator.Notation.StandardNotation)

        self.default_text_color = "color: white;"  # Будет перезаписан из палитры
        self.risk_text_color = "color: red; font-weight: bold;"

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        columns_layout = QHBoxLayout()

        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_widget = QWidget()
        left_layout = QFormLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_scroll.setWidget(left_widget)

        unit_label_width = 120

        for item in INPUT_CONFIG:
            label = QLabel(item["label"])
            row_hbox = QHBoxLayout()
            unit_label = QLabel(item.get("unit", ""))
            unit_label.setMinimumWidth(unit_label_width)
            unit_label.setAlignment(
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )

            tooltip = item.get("tooltip")
            if tooltip:
                label.setToolTip(tooltip)
                unit_label.setToolTip(tooltip)

            if item["type"] == "number":
                widget = QLineEdit()
                widget.setValidator(self.validator)
                widget.textChanged.connect(self.update_calculations)
                if tooltip:
                    widget.setToolTip(tooltip)
                self.inputs[item["key"]] = widget
                row_hbox.addWidget(widget)
                row_hbox.addWidget(unit_label)

            elif item["type"] == "checkbox":
                widget = QCheckBox()
                widget.stateChanged.connect(self.update_calculations)
                if tooltip:
                    widget.setToolTip(tooltip)
                self.inputs[item["key"]] = widget
                row_hbox.addWidget(widget)
                row_hbox.addStretch()
                row_hbox.addWidget(unit_label)

            elif item["type"] == "ratio":
                widget1, widget2 = QLineEdit(), QLineEdit()
                for widget, key in zip((widget1, widget2), item["keys"]):
                    widget.setValidator(self.validator)
                    widget.textChanged.connect(self.update_calculations)
                    if tooltip:
                        widget.setToolTip(tooltip)
                    self.inputs[key] = widget

                ratio_hbox = QHBoxLayout()
                ratio_hbox.addWidget(widget1)
                ratio_hbox.addWidget(QLabel(" / "))
                ratio_hbox.addWidget(widget2)
                row_hbox.addLayout(ratio_hbox)
                row_hbox.addWidget(unit_label)

            left_layout.addRow(label, row_hbox)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        right_column_widget = QWidget()
        right_column_vbox = QVBoxLayout(right_column_widget)

        right_results_widget = QWidget()
        right_layout = QFormLayout(right_results_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        for name, config in CALCULATION_CONFIG.items():
            self.outputs[name] = self.create_result_label()
            right_layout.addRow(
                QLabel(f"<b>{config["label"]}:</b>"), self.outputs[name]
            )
            right_layout.setVerticalSpacing(20)

        bottom_buttons_layout = QHBoxLayout()
        self.clear_button = QPushButton(BUTTONS["clear"])
        self.clear_button.clicked.connect(self.clear_all_fields)

        self.help_button = QPushButton(BUTTONS["about"])
        self.help_button.setFixedWidth(30)
        self.help_button.clicked.connect(self.show_info)

        bottom_buttons_layout.addStretch()
        bottom_buttons_layout.addWidget(self.clear_button)
        bottom_buttons_layout.addWidget(self.help_button)

        right_column_vbox.addWidget(right_results_widget)
        right_column_vbox.addStretch()
        right_column_vbox.addLayout(bottom_buttons_layout)

        columns_layout.addWidget(left_scroll, 2)
        columns_layout.addWidget(separator)
        columns_layout.addWidget(right_column_widget, 1)

        main_layout.addLayout(columns_layout)

    def create_result_label(self):
        label = QLabel("---")
        font = label.font()
        font.setPointSize(12)
        font.setBold(True)
        label.setFont(font)
        self.default_text_color = (
            f"color: {self.palette().color(QPalette.ColorRole.WindowText).name()};"
        )
        label.setStyleSheet(self.default_text_color)
        return label

    def get_all_input_values(self):
        values = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                text = widget.text().replace(",", ".")
                if text and text not in ("-", "."):
                    try:
                        values[key] = float(text)
                    except ValueError:
                        values[key] = None
                else:
                    values[key] = None
            elif isinstance(widget, QCheckBox):
                values[key] = 1 if widget.isChecked() else 0

        if values.get("iap_mm") is not None:
            values["iap_cm"] = values["iap_mm"] / 10
        else:
            values["iap_cm"] = None

        pao2, fio2 = values.get("pao2"), values.get("fio2")
        values["pao2_fio2_index"] = None
        if pao2 is not None and fio2 is not None and fio2 != 0:
            values["pao2_fio2_index"] = pao2 / fio2

        crp7, crp1 = values.get("crp7"), values.get("crp1")
        values["crp7_crp1_ratio"] = None
        if crp7 is not None and crp1 is not None and crp1 != 0:
            values["crp7_crp1_ratio"] = crp7 / crp1

        return values

    def update_calculations(self):
        values = self.get_all_input_values()

        for name, config in CALCULATION_CONFIG.items():
            self.update_formula(
                name,
                values,
                globals()[f"calculate_{name}_risk"],
                config["cutoff"],
                config["keys"],
            )

    def update_formula(self, name, values, calc_func, cutoff, keys):
        kwargs = {}
        all_present = True

        for key in keys:
            value = values.get(key)
            if value is None:
                all_present = False
                break
            kwargs[key] = value

        output = self.outputs.get(name)
        if not output:
            return

        if all_present:
            try:
                p = calc_func(**kwargs)
                self.set_result(output, p, cutoff)
            except Exception as e:  # pylint: disable=broad-exception-caught
                logging.error("Ошибка расчета %s: %s", name, e, exc_info=True)
                output.setText("Ошибка")
                output.setStyleSheet(self.risk_text_color)
        else:
            output.setText("---")
            output.setStyleSheet(self.default_text_color)

    def set_result(self, output, value, cutoff):
        output.setText(f"{value:.2f}%")
        if value >= cutoff:
            output.setStyleSheet(self.risk_text_color)
        else:
            output.setStyleSheet(self.default_text_color)

    def clear_all_fields(self):
        for widget in self.inputs.values():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)

    def show_info(self):
        try:
            license_path = os_path.join(BASE_DIR, LICENSE)
            with open(license_path, "r", encoding="utf-8") as license_file:
                license_text = license_file.read()
        except FileNotFoundError:
            license_text = f"Файл лицензии {LICENSE} не найден."
            logging.warning(license_text)

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(TITLE_ABOUT)
        msg_box.setText(license_text)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        style_path = os_path.join(BASE_DIR, STYLE_SHEET)
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        logging.warning(
            "Файл стилей %s не найден. Используются стили по умолчанию.", STYLE_SHEET
        )

    window = MainWindow()

    try:
        icon_path = os_path.join(BASE_DIR, ICON)
        window.setWindowIcon(QIcon(icon_path))
    except FileNotFoundError:
        logging.warning("Файл иконки %s не найден.", ICON)

    window.show()
    sys.exit(app.exec())
