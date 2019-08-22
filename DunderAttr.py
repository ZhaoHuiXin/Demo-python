class Vector:

    def __init__(self, **coords):
        private_coords = {'_' + k: v for k, v in coords.items()}
        self.__dict__.update(private_coords)

    def __repr__(self):
        return "{}({})". format(
            self.__class__.__name__,
            ', '.join("{k} ={v}".format(
                k=k[1:],
                v=self.__dict__[k])
                for k in sorted(self.__dict__.keys())
            )
        )

    def __getattr__(self, k):
        private_k = "_" + k
        try:
            return vars(self)[private_k]
        except KeyError:
            raise KeyError("has no attr {!r}".format(private_k))

    def __setattr__(self, key, value):
        raise AttributeError("can't set attribute{!r}".format(key))

    def __delete__(self, instance):
        raise AttributeError("can't delete attribute {!r}".format(instance))


class ColoredVector(Vector):

    COLOR_INDEXES = ('red', 'green', 'blue')

    def __init__(self, red, green, blue, **coords):
        super().__init__(**coords)
        self.__dict__['color'] = [red, green, blue]

    def __getattr__(self, name):
        try:
            channel = ColoredVector.COLOR_INDEXES.index(name)
        except ValueError:
            super().__getattr__(name)
        else:
            return self.__dict__['color'][channel]

    def __setattr__(self, key, value):
        try:
            channel  = ColoredVector.COLOR_INDEXES.index(key)
        except ValueError:
            super().__setattr__(key, value)
        else:
            self.__dict__['color'][channel] = value

    def __repr__(self):
        keys = set(self.__dict__.keys())
        keys.discard('color')
        coords = ', '.join(
            "{k}={v}".format(k=k[1:], v=self.__dict__[k])
            for k in sorted(keys)
        )

        return "{cls}({red}, {green}, {blue}, {coords})".format(
            cls=self.__class__.__name__,
            red=self.red,
            green=self.green,
            blue=self.blue,
            coords=coords
        )
