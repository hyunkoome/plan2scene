# Specify seam correction configuration
import os
import os.path as osp
import json
EMBARK_TEX_SYNTH = '/home/hyunkoo/DATA/HDD8TB/Project/texture-synthesis-0.8.2-x86_64-unknown-linux-musl'
texture_synthesis_conf = {
    # "texture_synthesis_path": osp.abspath(osp.join(os.environ["EMBARK_TEX_SYNTH"], "texture-synthesis")),
    # "seam_mask_path": osp.abspath(osp.join(os.environ["EMBARK_TEX_SYNTH"], "1_tile.jpg"))
    "texture_synthesis_path": osp.abspath(osp.join(EMBARK_TEX_SYNTH, "texture-synthesis")),
    "seam_mask_path": osp.abspath(osp.join(EMBARK_TEX_SYNTH, "1_tile.jpg"))
}
with open("./conf/plan2scene/seam_correct.json", "w") as f:
  json.dump(texture_synthesis_conf, f, indent=4)

assert osp.exists(texture_synthesis_conf["texture_synthesis_path"])
assert osp.exists(texture_synthesis_conf["seam_mask_path"])