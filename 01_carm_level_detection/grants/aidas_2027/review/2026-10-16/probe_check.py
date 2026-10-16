"""Show that the panel's check bites: count what it holds labels against, then plant a label over a box, a point
and an image, and one under 7 pt, and list what it reports."""
import sys
sys.path.insert(0, sys.argv[1])
import make_figures as mf

mf.set_style()
fig = mf.figure_panel()
fig.canvas.draw()
found = mf.obstacles(fig, fig.canvas.get_renderer())
kinds = {}
for name, _, _ in found:
    kinds[name] = kinds.get(name, 0) + 1
print("obstacles:", kinds)
print("clean panel problems:", mf.check(fig))
canvas = fig.axes[0]
canvas.text(0.5, 3.1, "planted over a box", fontsize=7)
canvas.text(0.3, 0.6, "planted over an image", fontsize=7)
canvas.text(6.95, 2.45, "planted small", fontsize=5)
results = fig.axes[-1]
results.text(96.4, 1.34, "planted on a point", fontsize=7, ha="center", va="center")
for problem in mf.check(fig):
    print("  ", problem)
