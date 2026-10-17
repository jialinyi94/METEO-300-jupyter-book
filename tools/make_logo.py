"""Write the book logo as SVG: assets/logo.svg and assets/logo-dark.svg.

A blue Earth disc. A white Rossby wave (a continuous field, like ERA5) runs from the left and ends
on the first node of an orange triangular mesh (a graph network, like an AI weather model).
"""
import math
import sys
from pathlib import Path

out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "assets"
out.mkdir(parents=True, exist_ok=True)

Y0, AMP, X0, WL = 32.0, 8.5, 8.0, 30.0  # zero crossings at x = 8, 23, 38


def wave_path():
    xs = [X0 + i * 0.5 for i in range(int(WL / 0.5) + 1)]
    pts = [(x, Y0 - AMP * math.sin(2 * math.pi * (x - X0) / WL)) for x in xs]
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts)


NODES = {"a": (38.0, 32.0), "b": (47.0, 20.5), "c": (47.0, 43.5), "d": (56.0, 32.0)}
EDGES = ["ab", "ac", "bd", "cd", "bc"]


def svg(disc, wave, node, edge):
    e = "".join(
        f'<line x1="{NODES[p][0]}" y1="{NODES[p][1]}" x2="{NODES[q][0]}" y2="{NODES[q][1]}"/>' for p, q in EDGES
    )
    n = "".join(f'<circle cx="{x}" cy="{y}" r="{4.2 if k == "a" else 3.4}"/>' for k, (x, y) in NODES.items())
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <title>从 ERA5 到 AI 天气模型</title>
  <circle cx="32" cy="32" r="31" fill="{disc}"/>
  <g stroke="{edge}" stroke-width="2.4" stroke-linecap="round">{e}</g>
  <path d="{wave_path()}" fill="none" stroke="{wave}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <g fill="{node}">{n}</g>
</svg>
"""


(out / "logo.svg").write_text(svg("#1D4ED8", "#FFFFFF", "#FB923C", "#FDBA74"))
(out / "logo-dark.svg").write_text(svg("#3B82F6", "#FFFFFF", "#FDBA74", "#FED7AA"))
print("written", sorted(p.name for p in out.iterdir()))
