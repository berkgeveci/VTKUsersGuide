"""Generate Figure 3-2: VTK dataset types."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.family'] = 'Times New Roman'
from matplotlib.collections import LineCollection

def draw_image_data(ax):
    """(a) Uniform rectilinear grid."""
    nx, ny = 7, 6
    for i in range(nx + 1):
        ax.plot([i, i], [0, ny], 'k-', linewidth=1)
    for j in range(ny + 1):
        ax.plot([0, nx], [j, j], 'k-', linewidth=1)
    ax.set_xlim(-0.5, nx + 0.5)
    ax.set_ylim(-1.5, ny + 0.5)
    ax.set_aspect('equal')
    ax.set_title('(a) Image Data\n(vtkImageData)', fontsize=14, fontstyle='italic', pad=8)

def draw_rectilinear_grid(ax):
    """(b) Non-uniform rectilinear grid."""
    xs = [0, 0.5, 1.2, 1.6, 2.5, 3.0, 4.0, 5.0, 5.3, 6.0, 7.0]
    ys = [0, 1.5, 2.0, 2.3, 3.5, 4.0, 6.0]
    for x in xs:
        ax.plot([x, x], [ys[0], ys[-1]], 'k-', linewidth=1)
    for y in ys:
        ax.plot([xs[0], xs[-1]], [y, y], 'k-', linewidth=1)
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-1.5, 6.5)
    ax.set_aspect('equal')
    ax.set_title('(b) Rectilinear Grid\n(vtkRectilinearGrid)', fontsize=14, fontstyle='italic', pad=8)

def draw_structured_grid(ax):
    """(c) Curvilinear structured grid - a warped sector."""
    nr, ntheta = 6, 10
    r_inner, r_outer = 2.0, 5.0
    theta_start, theta_end = np.radians(10), np.radians(80)

    r = np.linspace(r_inner, r_outer, nr + 1)
    theta = np.linspace(theta_start, theta_end, ntheta + 1)
    R, T = np.meshgrid(r, theta)
    X = R * np.cos(T)
    Y = R * np.sin(T)

    # Draw radial lines
    for i in range(nr + 1):
        ax.plot(X[:, i], Y[:, i], 'k-', linewidth=1)
    # Draw arc lines
    for j in range(ntheta + 1):
        ax.plot(X[j, :], Y[j, :], 'k-', linewidth=1)

    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 5.5)
    ax.set_aspect('equal')
    ax.set_title('(c) Structured Grid\n(vtkStructuredGrid)', fontsize=14, fontstyle='italic', pad=8)

def draw_unstructured_points(ax):
    """(d) Random scattered points."""
    rng = np.random.RandomState(42)
    n = 40
    x = rng.uniform(0.5, 6.5, n)
    y = rng.uniform(0.5, 5.5, n)
    ax.plot(x, y, 'ko', markersize=4)
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-0.5, 6.5)
    ax.set_aspect('equal')
    ax.set_title('(d) Unstructured Points\n(use vtkPolyData)', fontsize=14, fontstyle='italic', pad=8)

def draw_polygonal_data(ax):
    """(e) Polygonal data: vertices, polylines, polygons, triangle strips."""
    ms = 5
    lw = 1.2

    # Top-left: scattered vertices
    verts_x = [0.3, 1.0, 0.5, 1.5, 0.8, 1.8, 0.2, 1.3]
    verts_y = [5.0, 5.5, 4.5, 5.2, 4.8, 4.5, 5.3, 4.2]
    ax.plot(verts_x, verts_y, 'ko', markersize=ms)

    # Top-right: polyline
    px = [2.5, 3.0, 3.5, 4.2, 4.8, 5.3, 5.8, 6.2, 6.8]
    py = [4.5, 5.3, 4.8, 5.5, 5.0, 5.4, 4.6, 5.2, 4.8]
    ax.plot(px, py, 'k-o', markersize=ms, linewidth=lw)

    # Bottom-left: polygons
    poly1 = np.array([[0.3, 2.8], [0.8, 3.5], [1.5, 3.2], [1.8, 2.5],
                       [1.2, 2.0], [0.5, 2.2], [0.3, 2.8]])
    ax.plot(poly1[:, 0], poly1[:, 1], 'k-o', markersize=ms, linewidth=lw)

    # Bottom-right: triangle strip
    strip_x = [2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]
    strip_top = [3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
    strip_bot = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]

    # Draw alternating triangles
    for i in range(len(strip_x) - 1):
        if i % 2 == 0:
            tri = np.array([[strip_x[i], strip_bot[i]],
                            [strip_x[i+1], strip_bot[i+1]],
                            [strip_x[i], strip_top[i]],
                            [strip_x[i], strip_bot[i]]])
        else:
            tri = np.array([[strip_x[i-1], strip_top[i-1]],
                            [strip_x[i], strip_bot[i]],
                            [strip_x[i], strip_top[i]],
                            [strip_x[i-1], strip_top[i-1]]])
        ax.plot(tri[:, 0], tri[:, 1], 'k-', linewidth=lw)

    # Draw the strip as connected triangles more cleanly
    for i in range(len(strip_x)):
        ax.plot(strip_x[i], strip_top[i] if i % 2 == 0 else strip_bot[i],
                'ko', markersize=ms)
        ax.plot(strip_x[i], strip_bot[i] if i % 2 == 0 else strip_top[i],
                'ko', markersize=ms)
    # Outer edges
    all_x, all_y = [], []
    for i in range(len(strip_x)):
        all_x.extend([strip_x[i], strip_x[i]])
        all_y.extend([strip_bot[i], strip_top[i]])
    # Top and bottom edges
    ax.plot(strip_x, strip_top, 'k-', linewidth=lw)
    ax.plot(strip_x, strip_bot, 'k-', linewidth=lw)
    # Diagonals
    for i in range(len(strip_x)):
        ax.plot([strip_x[i], strip_x[i]], [strip_bot[i], strip_top[i]],
                'k-', linewidth=lw)
    for i in range(len(strip_x) - 1):
        ax.plot([strip_x[i], strip_x[i+1]],
                [strip_top[i], strip_bot[i+1]], 'k-', linewidth=lw)
    # Dots
    for i in range(len(strip_x)):
        ax.plot(strip_x[i], strip_top[i], 'ko', markersize=ms)
        ax.plot(strip_x[i], strip_bot[i], 'ko', markersize=ms)

    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(1.2, 6.2)
    ax.set_aspect('equal')
    ax.set_title('(e) Polygonal Data\n(vtkPolyData)', fontsize=14, fontstyle='italic', pad=8)

def draw_cell(ax, points, edges, cx=0, cy=0, ms=4, lw=1.0, dashed=None):
    """Draw a cell given points and edge index pairs."""
    if dashed is None:
        dashed = []
    pts = np.array(points) + np.array([cx, cy])
    for i, (a, b) in enumerate(edges):
        style = 'k--' if i in dashed else 'k-'
        ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]],
                style, linewidth=lw)
    ax.plot(pts[:, 0], pts[:, 1], 'ko', markersize=ms)

def draw_unstructured_grid(ax):
    """(f) Unstructured grid: mixed cell types in a 3x3 arrangement."""
    ms = 4
    lw = 1.0

    # Row 1: vertex, polyvertex, line
    # Vertex
    ax.plot(0.5, 5.5, 'ko', markersize=ms)

    # Polyvertex
    pvx = [1.8, 2.2, 2.5, 2.0, 2.7, 2.3, 1.9]
    pvy = [5.8, 5.3, 5.7, 5.1, 5.5, 5.9, 5.5]
    ax.plot(pvx, pvy, 'ko', markersize=ms)

    # Line
    ax.plot([3.5, 5.0], [5.5, 5.5], 'k-o', markersize=ms, linewidth=lw)

    # Polyline
    plx = [5.5, 6.0, 6.5, 7.0, 7.5]
    ply = [5.2, 5.8, 5.3, 5.7, 5.5]
    ax.plot(plx, ply, 'k-o', markersize=ms, linewidth=lw)

    # Row 2: triangle, quad, polygon
    # Triangle
    draw_cell(ax,
              [[0.3, 3.5], [1.5, 4.5], [1.8, 3.3]],
              [(0,1), (1,2), (2,0)], ms=ms, lw=lw)

    # Quad
    draw_cell(ax,
              [[2.8, 3.5], [2.8, 4.5], [4.0, 4.5], [4.0, 3.5]],
              [(0,1), (1,2), (2,3), (3,0)], ms=ms, lw=lw)

    # Polygon (pentagon)
    theta = np.linspace(np.pi/2, np.pi/2 + 2*np.pi, 6)[:-1]
    r = 0.7
    cx, cy = 5.5, 4.0
    pts = [[cx + r*np.cos(t), cy + r*np.sin(t)] for t in theta]
    edges = [(i, (i+1) % 5) for i in range(5)]
    draw_cell(ax, pts, edges, ms=ms, lw=lw)

    # Pixel (small square, axis-aligned, with center dot)
    draw_cell(ax,
              [[7.0, 3.5], [7.0, 4.3], [7.8, 4.3], [7.8, 3.5]],
              [(0,1), (1,2), (2,3), (3,0)], ms=ms, lw=lw)
    ax.plot(7.4, 3.9, 'ko', markersize=ms-1)

    # Row 3: tetrahedron, hexahedron (cube), wedge
    # Tetrahedron
    tet = [[0.5, 1.3], [2.0, 2.3], [2.0, 1.0], [1.2, 1.8]]
    draw_cell(ax, tet,
              [(0,1), (1,2), (2,0), (0,3), (1,3), (2,3)],
              dashed=[3], ms=ms, lw=lw)

    # Voxel / hexahedron (3D cube in 2D projection)
    # Front face
    f = [[3.0, 1.0], [4.2, 1.0], [4.2, 2.2], [3.0, 2.2]]
    # Back face (offset)
    b = [[3.5, 1.5], [4.7, 1.5], [4.7, 2.7], [3.5, 2.7]]
    all_pts = f + b
    hex_edges = [
        (0,1), (1,2), (2,3), (3,0),  # front
        (4,5), (5,6), (6,7), (7,4),  # back
        (0,4), (1,5), (2,6), (3,7),  # connections
    ]
    draw_cell(ax, all_pts, hex_edges, dashed=[4, 7, 8], ms=ms, lw=lw)
    ax.plot(all_pts[4][0], all_pts[4][1], 'ko', markersize=ms)

    # Wedge (pentahedron)
    w = [[5.5, 1.0], [6.8, 1.0], [6.1, 1.8],
         [5.8, 1.5], [7.1, 1.5], [6.4, 2.3]]
    wedge_edges = [
        (0,1), (1,2), (2,0),  # front triangle
        (3,4), (4,5), (5,3),  # back triangle
        (0,3), (1,4), (2,5),  # connections
    ]
    draw_cell(ax, w, wedge_edges, dashed=[5, 6], ms=ms, lw=lw)

    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(0.2, 6.5)
    ax.set_aspect('equal')
    ax.set_title('(f) Unstructured Grid\n(vtkUnstructuredGrid)', fontsize=14, fontstyle='italic', pad=8)


def draw_amr_patch(ax, x0, y0, nx, ny, dx, lw):
    """Draw a uniform grid patch."""
    for i in range(nx + 1):
        ax.plot([x0 + i * dx, x0 + i * dx], [y0, y0 + ny * dx], 'k-', linewidth=lw)
    for j in range(ny + 1):
        ax.plot([x0, x0 + nx * dx], [y0 + j * dx, y0 + j * dx], 'k-', linewidth=lw)

def draw_amr(ax):
    """(g) AMR: coarse grid with separate refined patches."""
    # Level 0: coarse 6x6 grid
    draw_amr_patch(ax, 0, 0, 6, 6, 1.0, lw=1.2)

    # Level 1 patch A: 2x refinement covering coarse cells [0,2] x [3,5] (top-left)
    draw_amr_patch(ax, 0, 3, 6, 6, 0.5, lw=0.8)

    # Level 1 patch B: 2x refinement covering coarse cells [3,5] x [0,2] (bottom-right)
    draw_amr_patch(ax, 3, 0, 6, 4, 0.5, lw=0.8)

    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-1.0, 6.5)
    ax.set_aspect('equal')
    ax.set_title('(g) AMR\n(vtkOverlappingAMR)', fontsize=14, fontstyle='italic', pad=8)


def draw_hypertreegrid(ax):
    """(h) HyperTreeGrid: quadtree-style adaptive refinement."""
    lw = 1.0

    def subdivide(ax, x0, y0, size, level, max_level, rng):
        """Recursively subdivide a cell."""
        if level >= max_level:
            return
        # Draw the subdivision
        mid_x = x0 + size / 2
        mid_y = y0 + size / 2
        ax.plot([mid_x, mid_x], [y0, y0 + size], 'k-', linewidth=lw * 0.8)
        ax.plot([x0, x0 + size], [mid_y, mid_y], 'k-', linewidth=lw * 0.8)

        # Randomly subdivide some children
        children = [(x0, y0), (mid_x, y0), (x0, mid_y), (mid_x, mid_y)]
        for cx, cy in children:
            if rng.random() < 0.5:
                subdivide(ax, cx, cy, size / 2, level + 1, max_level, rng)

    rng = np.random.RandomState(17)
    n = 4  # 4x4 root grid

    # Draw outer boundary and root grid
    for i in range(n + 1):
        ax.plot([i, i], [0, n], 'k-', linewidth=lw)
        ax.plot([0, n], [i, i], 'k-', linewidth=lw)

    # Subdivide some root cells
    for i in range(n):
        for j in range(n):
            if rng.random() < 0.6:
                subdivide(ax, i, j, 1.0, 0, 3, rng)

    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-1.0, 4.5)
    ax.set_aspect('equal')
    ax.set_title('(h) HyperTree Grid\n(vtkHyperTreeGrid)', fontsize=14, fontstyle='italic', pad=8)


fig, axes = plt.subplots(4, 2, figsize=(10, 16))
for ax in axes.flat:
    ax.axis('off')

draw_image_data(axes[0, 0])
draw_rectilinear_grid(axes[0, 1])
draw_structured_grid(axes[1, 0])
draw_unstructured_points(axes[1, 1])
draw_polygonal_data(axes[2, 0])
draw_unstructured_grid(axes[2, 1])
draw_amr(axes[3, 0])
draw_hypertreegrid(axes[3, 1])

plt.tight_layout(pad=1.5)

out = '/Users/berk.geveci/Work/VTK/VTKUsersGuide/chapter03/images/Figure_3-2'
plt.savefig(f'{out}.svg', format='svg', bbox_inches='tight')
plt.savefig(f'{out}.png', dpi=300, bbox_inches='tight')
print(f'Saved {out}.svg and {out}.png')
