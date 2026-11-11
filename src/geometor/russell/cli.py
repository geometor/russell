"""CLI entry point for geometor.russell."""

from __future__ import annotations

import argparse
from pathlib import Path

from geometor.russell.export import export_json, export_obj, export_svg_projection
from geometor.russell.models3d import MODEL_REGISTRY, build_all_models


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="geometor-russell",
        description="GEOMETOR Russell: 3D wave-field cosmogony modeling and export toolkit.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List available parametric 3D Russell cosmogony models.")

    exp = sub.add_parser("export", help="Export 3D cosmogony models to .obj, .json, or .svg.")
    exp.add_argument(
        "--model",
        default="all",
        choices=["all", *MODEL_REGISTRY.keys()],
        help="Model key to export (default: all).",
    )
    exp.add_argument(
        "--format",
        default="obj",
        choices=["obj", "json", "svg"],
        help="Output format (default: obj).",
    )
    exp.add_argument(
        "--out",
        type=Path,
        default=Path("exports"),
        help="Target directory for exported files.",
    )
    exp.add_argument("--yaw", type=float, default=34.0, help="Camera yaw in degrees (for svg).")
    exp.add_argument("--pitch", type=float, default=22.0, help="Camera pitch in degrees (for svg).")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the geometor-russell CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list" or args.command is None:
        print("GEOMETOR • russell — Parametric 3D Cosmogony Models")
        print("-" * 58)
        for key, scene in build_all_models().items():
            print(f"  {key:<18} {scene.title} [{scene.figures}]")
        return 0

    if args.command == "export":
        targets = (
            build_all_models()
            if args.model == "all"
            else {args.model: MODEL_REGISTRY[args.model]()}
        )
        args.out.mkdir(parents=True, exist_ok=True)
        for key, scene in targets.items():
            out_file = args.out / f"{key}.{args.format}"
            if args.format == "obj":
                export_obj(scene, out_file)
            elif args.format == "json":
                export_json(scene, out_file)
            else:
                export_svg_projection(scene, out_file, yaw_deg=args.yaw, pitch_deg=args.pitch)
            print(f"Exported {out_file}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
