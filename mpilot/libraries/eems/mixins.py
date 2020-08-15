from mpilot.libraries.eems.exceptions import MixedArrayShapes


class SameArrayShapeMixin(object):
    def validate_array_shapes(self, arrays, lineno=None):
        if len(arrays) == 1:
            return

        shape = arrays[0].shape

        for arr in arrays:
            if arr.shape != shape:
                raise MixedArrayShapes(shape, arr.shape, lineno)
