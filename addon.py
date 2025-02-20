bl_info = {
    "name": "Export Mesh to JSON",
    "description": "Exports a mesh in JSON Array format for three.js",
    "blender": (4, 0, 0),
    "location": "File > Export > Mesh (.json)",
    "category": "Import-Export",
}

import bpy
import bmesh
import json
import os
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty, IntProperty

def export_mesh_to_json(obj, filepath, precision):
    if obj.type != 'MESH':
        print("Selected object is not a mesh.")
        return
    
    mesh = obj.data.copy()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    
    vertices = []
    normals = []
    indices = []
    
    vert_map = {}
    index = 0
    
    for tri in mesh.loop_triangles:
        for loop_index in tri.loops:
            vert = mesh.vertices[mesh.loops[loop_index].vertex_index]
            key = (
                format_number(vert.co.x, precision), format_number(vert.co.y, precision), format_number(vert.co.z, precision),
                format_number(vert.normal.x, precision), format_number(vert.normal.y, precision), format_number(vert.normal.z, precision)
            )
            
            if key not in vert_map:
                vert_map[key] = index
                vertices.extend([format_number(vert.co.x, precision), format_number(vert.co.y, precision), format_number(vert.co.z, precision)])
                normals.extend([format_number(vert.normal.x, precision), format_number(vert.normal.y, precision), format_number(vert.normal.z, precision)])
                index += 1
            
            indices.append(vert_map[key])
    
    with open(filepath, 'w') as f:
        json.dump([vertices,normals,indices], f, separators=(',', ':'))
    
    bpy.data.meshes.remove(mesh)

class ExportMeshToJSON(Operator, ExportHelper):
    bl_idname = "export_mesh.json"
    bl_label = "Export Mesh to JSON"
    filename_ext = ".json"
    
    filepath: StringProperty(subtype='FILE_PATH')
    precision: IntProperty(name="Precision", default=3, min=1, max=10, description="Number of decimal")
    
    def execute(self, context):
        obj = context.active_object
        if obj is None:
            self.report({'ERROR'}, "No active object selected.")
            return {'CANCELLED'}
        
        original_mode = obj.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        export_mesh_to_json(obj, self.filepath, self.precision)
        bpy.ops.object.mode_set(mode=original_mode)

        return {'FINISHED'}

def format_number(num, precision):
    rounded = round(num, precision)
    return int(rounded) if int(rounded) == rounded else rounded

def menu_func_export(self, context):
    self.layout.operator(ExportMeshToJSON.bl_idname, text="Mesh (.json)")

def register():
    bpy.utils.register_class(ExportMeshToJSON)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ExportMeshToJSON)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

def ensure_addon_enabled(dummy):
    if not __name__ in bpy.context.preferences.addons:
        bpy.ops.preferences.addon_enable(module=__name__)

bpy.app.handlers.load_post.append(ensure_addon_enabled)

if __name__ == "__main__":
    register()