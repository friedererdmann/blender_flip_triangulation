import bpy


def main(context):
    # editmode hack from https://blenderartists.org/t/solved-how-to-get-list-of-selected-faces/495495/2

    selection = [obj for obj in bpy.data.scenes[0].objects if obj.select_get()]
    editmode = False

    for obj in selection:
        if obj.mode == 'EDIT':
            editmode = True
            bpy.ops.object.mode_set(mode = 'OBJECT')
        mesh = obj.to_mesh()
        
        for polygon in obj.data.polygons:
            if not polygon.select:
                continue
            indices = list()
            size = len(polygon.vertices)
            for i in range(size):
                indices.append(polygon.vertices[i])

            for i in range(size):
                polygon.vertices[i] = indices[(i + 1) % size]

        obj.data.update()

    if editmode:
        bpy.ops.object.mode_set(mode = 'EDIT')



class FlipFaceTriangulationOperator(bpy.types.Operator):
    """Flips the triangulation of a selected face"""
    bl_idname = "object.flip_face_triangulation"
    bl_label = "Flip Face Triangulation"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(FlipFaceTriangulationOperator.bl_idname, text=FlipFaceTriangulationOperator.bl_label)

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access)
def register():
    bpy.utils.register_class(FlipFaceTriangulationOperator)
    bpy.types.VIEW3D_MT_edit_mesh_faces.append(menu_func)


def unregister():
    bpy.utils.unregister_class(FlipFaceTriangulationOperator)
    bpy.types.VIEW3D_MT_edit_mesh_faces.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.flip_face_triangulation()
