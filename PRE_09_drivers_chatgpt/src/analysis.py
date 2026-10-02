from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd



BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SUBMISSION_DIR = BASE_DIR / "submission"

DRIVERS_FILE = DATA_DIR / "drivers.csv"
TIMESHEET_FILE = DATA_DIR / "timesheet.csv"
SUMMARY_FILE = SUBMISSION_DIR / "summary.csv"
PLOT_FILE = SUBMISSION_DIR / "top10_drivers.png"


def load_data(drivers_path: Path, timesheet_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carga los datos de conductores y hojas de tiempo desde archivos CSV."""
    try:
        drivers = pd.read_csv(drivers_path)
        timesheet = pd.read_csv(timesheet_path)
        return drivers, timesheet
    except FileNotFoundError as e:
        print(f"Error al cargar los archivos: {e}")
        raise


def compute_summary(drivers: pd.DataFrame, timesheet: pd.DataFrame) -> pd.DataFrame:
    """Calcula el resumen total de horas y millas por conductor."""
    totals = timesheet.groupby("driverId", as_index=False)[
        ["hours-logged", "miles-logged"]
    ].sum()
    
    summary = pd.merge(drivers[["driverId", "name"]], totals, on="driverId")
    return summary.sort_values("driverId").reset_index(drop=True)


def plot_top10(summary: pd.DataFrame, output_path: Path) -> None:
    """Genera y guarda un gráfico de barras horizontales con los 10 mejores conductores."""
    top10 = summary.nlargest(10, "miles-logged").set_index("name")
    
    plt.figure(figsize=(8, 5))
    top10["miles-logged"].sort_values().plot.barh(color="tab:blue")
    
    plt.title("Top 10 conductores por millas registradas")
    plt.xlabel("Millas registradas")
    plt.ylabel("")
    plt.gca().spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    
    plt.savefig(output_path)
    plt.close()


def main() -> None:
    """Función principal que orquesta el flujo de trabajo."""
    # Crear el directorio de salida si no existe usando pathlib
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        drivers, timesheet = load_data(DRIVERS_FILE, TIMESHEET_FILE)
    except FileNotFoundError:
        print("Ejecución cancelada por falta de datos.")
        return

    summary = compute_summary(drivers, timesheet)
    summary.to_csv(SUMMARY_FILE, index=False)
    
    plot_top10(summary, PLOT_FILE)
    print("Resumen y gráfico generados exitosamente.")


if __name__ == "__main__":
    main()