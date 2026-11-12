
"""Reconstrucción de mediciones numéricas importadas desde Excel."""

columnas_decimales = [
    "waist(cm)",
    "eyesight(left)",
    "eyesight(right)",
    "hemoglobin",
    "serum creatinine"
]

columnas_enteras = [
    "hearing(left)",
    "hearing(right)",
    "systolic",
    "relaxation",
    "fasting blood sugar",
    "Cholesterol",
    "triglyceride",
    "HDL",
    "LDL",
    "Urine protein",
    "AST",
    "ALT",
    "Gtp"
]


def reconstruir_mediciones(df):
    """Reconstruye mediciones a partir de fracciones de día de Excel."""
    resultado = df.copy()

    for col in columnas_enteras:
        resultado[col] = (
            resultado[col] * 24
        ).round().astype(int)

    for col in columnas_decimales:
        minutos = (
            resultado[col] * 1440
        ).round().astype(int)

        resultado[col] = (
            minutos // 60 + (minutos % 60) / 10
        )

    return resultado
