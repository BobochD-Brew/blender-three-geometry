## Blender Mesh => JSON Array

### Install

- Download the <a href="https://raw.githubusercontent.com/BobochD-Brew/blender-three-geometry/refs/heads/main/addon.py" download>addon.py</a> file
- Go to: Edit > Preferences > Add-ons > Top right arrow > Install from disk, and select addon.py

### How to use

- Select a mesh
- Go to: File > Export > Mesh (.json) and select an output location

You can then load it like this 

```js
import { BufferAttribute, BufferGeometry } from "three";
import data from "./path/to/file.json";

function JsonGeometry({ json }) {
    return new BufferGeometry()
        .setAttribute('position', new BufferAttribute(new Float32Array(json[0]), 3))
        .setAttribute('normal', new BufferAttribute(new Float32Array(json[1]), 3))
        .setIndex(new BufferAttribute(new Uint16Array(json[2]), 1));
}

const geometry = JsonGeometry({ json: data });
```

The data is formated like this [flat vertices array, flat normals array, indices array]
