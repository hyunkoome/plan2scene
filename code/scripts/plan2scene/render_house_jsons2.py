import os
import argparse
import json
import numpy as np
import trimesh
import pyrender
import imageio


def export_gltf(scene_json_path, out_dir, output_format="glb"):
    cfg = json.load(open(scene_json_path))
    scene = trimesh.Scene()
    # add arch geometry
    if 'scene' in cfg and 'arch' in cfg['scene'] and 'elements' in cfg['scene']['arch']:
        for elem in cfg['scene']['arch']['elements']:
            if elem['type'] in ['Floor','Ceiling','Wall']:
                # skip surfaces; geometry comes from objects
                continue
    # add objects
    if 'object' in cfg['scene']:
        for obj in cfg['scene']['object']:
            mesh = trimesh.load(obj['modelId'], force='mesh')
            transform = np.array(obj['transform']['data']).reshape(4,4)
            scene.add_geometry(mesh, node_name=obj['modelId'], transform=transform)
    out_name = os.path.basename(scene_json_path).replace('.scene.json', f'.{output_format}')
    out_path = os.path.join(out_dir, out_name)
    scene.export(out_path)
    print(f"Exported glTF: {out_path}")


def lookat(eye, target, up):
    f = (target - eye)
    f /= np.linalg.norm(f)
    u = up / np.linalg.norm(up)
    s = np.cross(f, u)
    s /= np.linalg.norm(s)
    u = np.cross(s, f)
    M = np.eye(4)
    M[:3,0], M[:3,1], M[:3,2] = s, u, -f
    M[:3,3] = eye
    return M


def render_scene(scene_json_path, out_dir, width=800, height=600):
    cfg = json.load(open(scene_json_path))
    tscene = trimesh.Scene()
    for obj in cfg['scene']['object']:
        mesh = trimesh.load(obj['modelId'], force='mesh')
        transform = np.array(obj['transform']['data']).reshape(4,4)
        tscene.add_geometry(mesh, node_name=obj['modelId'], transform=transform)
    pscene = pyrender.Scene.from_trimesh_scene(tscene)

    cam_cfg = cfg['scene']['sceneCamera'] if 'sceneCamera' in cfg['scene'] else cfg['scene']['camera']
    eye = np.array(cam_cfg['eye']); target = np.array(cam_cfg['center']); up = np.array(cam_cfg['up'])
    camera = pyrender.PerspectiveCamera(yfov=np.deg2rad(cam_cfg['fov_y']), aspectRatio=cam_cfg['aspect'], znear=cam_cfg['near'], zfar=cam_cfg['far'])
    cam_node = pscene.add(camera, pose=lookat(eye, target, up))
    light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
    pscene.add(light, pose=lookat(eye, target, up))

    r = pyrender.OffscreenRenderer(viewport_width=width, viewport_height=height)
    color, _ = r.render(pscene)
    r.delete()

    out_name = os.path.basename(scene_json_path).replace('.scene.json', '.png')
    out_path = os.path.join(out_dir, out_name)
    imageio.imwrite(out_path, color)
    print(f"Rendered image: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Batch export/render house JSON files to glTF and PNG.")
    parser.add_argument('search_path', help='Directory to scan for .scene.json')
    parser.add_argument('--scene-json', action='store_true', help='Process .scene.json files')
    parser.add_argument('--export', action='store_true', help='Export to glTF instead of render')
    parser.add_argument('--width', type=int, default=800, help='Render width')
    parser.add_argument('--height', type=int, default=600, help='Render height')
    args = parser.parse_args()

    ext = '.scene.json' if args.scene_json else '.arch.json'
    for root, _, files in os.walk(args.search_path):
        for fname in files:
            if not fname.endswith(ext):
                continue
            fpath = os.path.join(root, fname)
            out_dir = root
            if args.export:
                export_gltf(fpath, out_dir)
            else:
                render_scene(fpath, out_dir, args.width, args.height)

if __name__ == '__main__':
    main()
