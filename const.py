TITLE = (
    "Прогнозирование развития ССО у пациентов с тяжелым течением острого панкреатита"
)
TITLE_ABOUT = "О программе"

ICON = "./resources/icon.ico"
LICENSE = "./LICENSE"
STYLE_SHEET = "./style.qss"

CUTOFF_SSC = 8.0  # Порог для ССО
CUTOFF_ARDS = 4.0  # Порог для ОРДС
CUTOFF_AKI = 15.6  # Порог для ОПП
CUTOFF_IIS = 16.3  # Порог для СКН
CUTOFF_MODS = 6.6  # Порог для СПОН
CUTOFF_PSC = 17.1  # Порог для ГСО
CUTOFF_SEPSIS = 7.4  # Порог для Сепсиса

BUTTONS = {
    "about": "?",
    "clear": "Очистить все поля",
}

CALCULATION_CONFIG = {
    "ssc": {
        "label": "ССО",
        "cutoff": CUTOFF_SSC,
        "keys": ["age", "bpn", "sofa", "charlson_index", "score"],
    },
    "ards": {
        "label": "ОРДС",
        "cutoff": CUTOFF_ARDS,
        "keys": ["bpn", "sofa", "charlson_index", "copd", "urea", "pao2_fio2_index"],
    },
    "aki": {
        "label": "ОПП",
        "cutoff": CUTOFF_AKI,
        "keys": ["age", "sofa", "ckd", "gfr"],
    },
    "iis": {
        "label": "СКН",
        "cutoff": CUTOFF_IIS,
        "keys": ["age", "bpn", "iap_mm", "urea"],
    },
    "mods": {
        "label": "СПОН",
        "cutoff": CUTOFF_MODS,
        "keys": [
            "age",
            "sofa",
            "pao2_fio2_index",
            "iap_cm",
            "creatinine",
        ],
    },
    "psc": {
        "label": "ГСО",
        "cutoff": CUTOFF_PSC,
        "keys": ["age", "bpn", "leukocytes", "bilirubin", "crp7_crp1_ratio"],
    },
    "sepsis": {
        "label": "Сепсис",
        "cutoff": CUTOFF_SEPSIS,
        "keys": ["bpn", "hospital_day", "sofa7", "crp7_crp1_ratio"],
    },
}


INPUT_CONFIG = [
    {
        "label": "Возраст",
        "key": "age",
        "type": "number",
        "unit": "годы",
        "tooltip": "Возраст пациента",
    },
    {
        "label": "БПН",
        "key": "bpn",
        "type": "checkbox",
        "unit": "",
        "tooltip": "Билиарный панкреонекроз",
    },
    {
        "label": "SOFA",
        "key": "sofa",
        "type": "number",
        "unit": "баллы",
        "tooltip": "Тяжесть состояния пациента по шкале SOFA",
    },
    {
        "label": "ИКЧ",
        "key": "charlson_index",
        "type": "number",
        "unit": "баллы",
        "tooltip": "Индекс коморбидности Чарльсона",
    },
    {
        "label": "SCORE",
        "key": "score",
        "type": "number",
        "unit": "%",
        "tooltip": "10-летний риск сердечно-сосудистых осложнений",
    },
    {
        "label": "ХОБЛ",
        "key": "copd",
        "type": "checkbox",
        "unit": "",
        "tooltip": "Хроническая обструктивная болезнь легких",
    },
    {
        "label": "PaO2 / FiO2",
        "key": "pao2_fio2_ratio",
        "type": "ratio",
        "keys": ["pao2", "fio2"],
        "unit": "",
        "tooltip": "Индекс оксигенации",
    },
    {
        "label": "ХБП",
        "key": "ckd",
        "type": "checkbox",
        "unit": "",
        "tooltip": "Хроническая болезнь почек",
    },
    {
        "label": "СКФ",
        "key": "gfr",
        "type": "number",
        "unit": "мл/мин/1,73м2",
        "tooltip": "Скорость клубочковой фильтрации",
    },
    {
        "label": "ВБД",
        "key": "iap_mm",
        "type": "number",
        "unit": "мм рт. ст.",
        "tooltip": "Внутрибрюшное давление",
    },
    {
        "label": "Мочевина",
        "key": "urea",
        "type": "number",
        "unit": "ммоль/л",
        "tooltip": "Уровень мочевины плазмы крови",
    },
    {
        "label": "Креатинин",
        "key": "creatinine",
        "type": "number",
        "unit": "мкмоль/л",
        "tooltip": "Креатинин плазмы крови",
    },
    {
        "label": "Лейкоциты",
        "key": "leukocytes",
        "type": "number",
        "unit": "×10^9",
        "tooltip": "Уровень лейкоцитов крови",
    },
    {
        "label": "Билирубин",
        "key": "bilirubin",
        "type": "number",
        "unit": "мкмоль/л",
        "tooltip": "Уровень общего билирубина",
    },
    {
        "label": "СРБ7 / СРБ1",
        "key": "crp_ratio",
        "type": "ratio",
        "keys": ["crp7", "crp1"],
        "unit": "",
        "tooltip": "Соотношение С-реактивного белка (на 7 сутки / при поступлении)",
    },
    {
        "label": "Сутки госпитализации",
        "key": "hospital_day",
        "type": "number",
        "unit": "",
        "tooltip": "Сутки госпитализации от начала ПН",
    },
    {
        "label": "SOFA на 7 сут.",
        "key": "sofa7",
        "type": "number",
        "unit": "",
        "tooltip": "Тяжесть состояния больного на 7 сутки госпитализации",
    },
]
