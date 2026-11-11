"""GEOMETOR Russell: Cosmogony, 3D wave-field geometry, and the Home Study Course of Walter and Lao Russell."""

from geometor.russell.elements_data import (
    OCTAVE_SPECS,
    OctaveSpec,
    RussellElement,
    build_periodic_elements,
)
from geometor.russell.export import export_json, export_obj, export_svg_projection
from geometor.russell.models3d import (
    GYRO_STAGES,
    MODEL_REGISTRY,
    PALETTE,
    Node3D,
    Polygon3D,
    Polyline3D,
    Scene3D,
    build_all_models,
    build_conical_vortex_field,
    build_cube_sphere_lattice,
    build_gyroscopic_octave_system,
    build_light_sphere_lens,
    build_periodic_helix_9_octave,
)

__version__ = "0.2.0"

__all__ = [
    "GYRO_STAGES",
    "MODEL_REGISTRY",
    "OCTAVE_SPECS",
    "PALETTE",
    "Node3D",
    "OctaveSpec",
    "Polygon3D",
    "Polyline3D",
    "RussellElement",
    "Scene3D",
    "__version__",
    "build_all_models",
    "build_conical_vortex_field",
    "build_cube_sphere_lattice",
    "build_gyroscopic_octave_system",
    "build_light_sphere_lens",
    "build_periodic_elements",
    "build_periodic_helix_9_octave",
    "export_json",
    "export_obj",
    "export_svg_projection",
]
