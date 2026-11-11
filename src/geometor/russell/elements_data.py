"""Structured 9-Octave Periodic Element data for Walter Russell's Cosmogony.

Maps Russell's nine octaves of matter (from primordial Hydrogen/Inert-Gas seeds
through Carbon, Silicon, and the heavy radioactive octaves) with their locking
tones (0, 1+, 2+, 3+, 4±, 3-, 2-, 1-), polarity classes, and gyroscopic angles.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RussellElement:
    """An element positioned on Walter Russell's 9-Octave Periodic Wave."""

    symbol: str
    name: str
    octave: int
    tone: str  # "0", "1+", "2+", "3+", "4±", "3-", "2-", "1-"
    polarity: str  # "zero", "positive", "amplitude", "negative"
    azimuth_deg: float  # Angle in Axial Chart (Fig. 177): 180° (0) -> 90° (4±) -> 0° (0)
    atomic_number: int | None = None


@dataclass(frozen=True)
class OctaveSpec:
    """Specification of a single octave wave from Inert Gas (0) to Inert Gas (0)."""

    number: int
    roman: str
    inert_start: tuple[str, str, int | None]
    members: tuple[tuple[str, str, str, int | None], ...]  # (symbol, name, tone, Z)
    inert_end: tuple[str, str, int | None]


OCTAVE_SPECS: tuple[OctaveSpec, ...] = (
    OctaveSpec(
        number=1,
        roman="I",
        inert_start=("Al", "Alphanon (0)", None),
        members=(("Proto-H1", "First Octave Amplitude", "4±", None),),
        inert_end=("Be", "Betanon (0)", None),
    ),
    OctaveSpec(
        number=2,
        roman="II",
        inert_start=("Be", "Betanon (0)", None),
        members=(("Proto-H2", "Second Octave Amplitude", "4±", None),),
        inert_end=("Ga", "Gammanon (0)", None),
    ),
    OctaveSpec(
        number=3,
        roman="III",
        inert_start=("Ga", "Gammanon (0)", None),
        members=(("H", "Hydrogen", "4±", 1),),
        inert_end=("He", "Helium", 2),
    ),
    OctaveSpec(
        number=4,
        roman="IV",
        inert_start=("He", "Helium", 2),
        members=(
            ("Li", "Lithium", "1+", 3),
            ("Be", "Beryllium", "2+", 4),
            ("B", "Boron", "3+", 5),
            ("C", "Carbon", "4±", 6),
            ("N", "Nitrogen", "3-", 7),
            ("O", "Oxygen", "2-", 8),
            ("F", "Fluorine", "1-", 9),
        ),
        inert_end=("Ne", "Neon", 10),
    ),
    OctaveSpec(
        number=5,
        roman="V",
        inert_start=("Ne", "Neon", 10),
        members=(
            ("Na", "Sodium", "1+", 11),
            ("Mg", "Magnesium", "2+", 12),
            ("Al", "Aluminum", "3+", 13),
            ("Si", "Silicon", "4±", 14),
            ("P", "Phosphorus", "3-", 15),
            ("S", "Sulfur", "2-", 16),
            ("Cl", "Chlorine", "1-", 17),
        ),
        inert_end=("Ar", "Argon", 18),
    ),
    OctaveSpec(
        number=6,
        roman="VI",
        inert_start=("Ar", "Argon", 18),
        members=(
            ("K", "Potassium", "1+", 19),
            ("Ca", "Calcium", "2+", 20),
            ("Sc", "Scandium", "3+", 21),
            ("Ti", "Titanium", "4+", 22),
            ("V", "Vanadium", "4+", 23),
            ("Cr", "Chromium", "4+", 24),
            ("Mn", "Manganese", "4+", 25),
            ("Fe", "Iron", "4±", 26),
            ("Co", "Cobalt", "4±", 27),
            ("Ni", "Nickel", "4-", 28),
            ("Cu", "Copper", "4-", 29),
            ("Zn", "Zinc", "4-", 30),
            ("Ga", "Gallium", "3-", 31),
            ("Ge", "Germanium", "3-", 32),
            ("As", "Arsenic", "3-", 33),
            ("Se", "Selenium", "2-", 34),
            ("Br", "Bromine", "1-", 35),
        ),
        inert_end=("Kr", "Krypton", 36),
    ),
    OctaveSpec(
        number=7,
        roman="VII",
        inert_start=("Kr", "Krypton", 36),
        members=(
            ("Rb", "Rubidium", "1+", 37),
            ("Sr", "Strontium", "2+", 38),
            ("Y", "Yttrium", "3+", 39),
            ("Zr", "Zirconium", "4+", 40),
            ("Nb", "Niobium", "4+", 41),
            ("Mo", "Molybdenum", "4+", 42),
            ("Tc", "Technetium", "4+", 43),
            ("Ru", "Ruthenium", "4±", 44),
            ("Rh", "Rhodium", "4±", 45),
            ("Pd", "Palladium", "4-", 46),
            ("Ag", "Silver", "4-", 47),
            ("Cd", "Cadmium", "4-", 48),
            ("In", "Indium", "3-", 49),
            ("Sn", "Tin", "3-", 50),
            ("Sb", "Antimony", "3-", 51),
            ("Te", "Tellurium", "2-", 52),
            ("I", "Iodine", "1-", 53),
        ),
        inert_end=("Xe", "Xenon", 54),
    ),
    OctaveSpec(
        number=8,
        roman="VIII",
        inert_start=("Xe", "Xenon", 54),
        members=(
            ("Cs", "Cesium", "1+", 55),
            ("Ba", "Barium", "2+", 56),
            ("La", "Lanthanum", "3+", 57),
            ("Ce", "Cerium", "3+", 58),
            ("Nd", "Neodymium", "3+", 60),
            ("Gd", "Gadolinium", "4+", 64),
            ("Lu", "Lutetium", "4+", 71),
            ("Hf", "Hafnium", "4+", 72),
            ("Ta", "Tantalum", "4+", 73),
            ("W", "Tungsten", "4±", 74),
            ("Os", "Osmium", "4±", 76),
            ("Ir", "Iridium", "4±", 77),
            ("Pt", "Platinum", "4-", 78),
            ("Au", "Gold", "4-", 79),
            ("Hg", "Mercury", "4-", 80),
            ("Tl", "Thallium", "3-", 81),
            ("Pb", "Lead", "3-", 82),
            ("Bi", "Bismuth", "3-", 83),
            ("Po", "Polonium", "2-", 84),
            ("At", "Astatine", "1-", 85),
        ),
        inert_end=("Rn", "Radon", 86),
    ),
    OctaveSpec(
        number=9,
        roman="IX",
        inert_start=("Rn", "Radon", 86),
        members=(
            ("Fr", "Francium", "1+", 87),
            ("Ra", "Radium", "2+", 88),
            ("Ac", "Actinium", "3+", 89),
            ("Th", "Thorium", "4+", 90),
            ("Pa", "Protactinium", "4+", 91),
            ("U", "Uranium", "4±", 92),
        ),
        inert_end=("Nt", "Omega Inert (0)", None),
    ),
)


def classify_tone_polarity(tone: str) -> str:
    """Classify a Russell tone string into its visual/physical polarity role."""
    if tone == "0":
        return "zero"
    if tone == "4±":
        return "amplitude"
    if "+" in tone:
        return "positive"
    return "negative"


def build_periodic_elements() -> list[RussellElement]:
    """Return the complete ordered list of Russell elements across Octaves I–IX."""
    elements: list[RussellElement] = []
    for spec in OCTAVE_SPECS:
        elements.append(
            RussellElement(
                symbol=spec.inert_start[0],
                name=spec.inert_start[1],
                octave=spec.number,
                tone="0",
                polarity="zero",
                azimuth_deg=180.0,
                atomic_number=spec.inert_start[2],
            )
        )
        count = len(spec.members)
        for idx, (sym, name, tone, z_num) in enumerate(spec.members):
            if count == 1:
                deg = 90.0
            else:
                deg = 162.0 - (144.0 * idx / (count - 1))
            elements.append(
                RussellElement(
                    symbol=sym,
                    name=name,
                    octave=spec.number,
                    tone=tone,
                    polarity=classify_tone_polarity(tone),
                    azimuth_deg=deg,
                    atomic_number=z_num,
                )
            )
        if spec.number == 9:
            elements.append(
                RussellElement(
                    symbol=spec.inert_end[0],
                    name=spec.inert_end[1],
                    octave=spec.number,
                    tone="0",
                    polarity="zero",
                    azimuth_deg=0.0,
                    atomic_number=spec.inert_end[2],
                )
            )
    return elements
