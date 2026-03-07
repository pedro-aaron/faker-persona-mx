"""
Configuración centralizada del proyecto.
"""

import os
import sys
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


def _get_package_data_dir() -> Path:
    """
    Obtiene el directorio de datos del paquete, funciona tanto en desarrollo como instalado.

    Returns:
        Path al directorio data/ dentro del paquete faker_persona_mx
    """
    # Intentar usar importlib.resources primero (Python 3.9+)
    try:
        if sys.version_info >= (3, 9):
            from importlib.resources import files
            # files() retorna un Traversable que podemos convertir a Path
            package_path = files("faker_persona_mx")
            return Path(str(package_path)) / "data"
    except (ImportError, TypeError, AttributeError):
        pass

    # Fallback: usar __file__ relativo al módulo actual
    # Este archivo está en: faker_persona_mx/utils/config.py
    # Necesitamos: faker_persona_mx/data/
    current_file = Path(__file__).resolve()
    package_root = current_file.parent.parent  # faker_persona_mx/
    return package_root / "data"


class Config(BaseSettings):
    """Configuración de la aplicación usando variables de entorno."""

    # Rutas
    DATA_DIR: Path = _get_package_data_dir()
    DATASETS_DIR: Path = DATA_DIR / "datasets"
    CACHE_DIR: Path = DATA_DIR / "cache"

    # Configuración de generación
    DEFAULT_SEED: int = 0
    ENABLE_CACHE: bool = True
    CACHE_SIZE_TOLERANCE: float = 0.01  # 1% de tolerancia

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[Path] = None

    # Dataset files
    NOMBRES_FILE: str = "nombres.csv"
    APELLIDOS_PATERNOS_FILE: str = "apellidos_paternos.csv"
    APELLIDOS_MATERNOS_FILE: str = "apellidos_maternos.csv"
    EMAIL_DOMAINS_FILE: str = "email_domains.csv"
    EMAIL_USERNAMES_FILE: str = "email_usernames.csv"
    LADAS_MEXICO_FILE: str = "ladas_mexico.csv"

    class Config:
        """Configuración de Pydantic."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Crear directorios si no existen
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.DATASETS_DIR.mkdir(parents=True, exist_ok=True)


# Singleton de configuración
config = Config()
