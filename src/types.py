import numpy as np
from typing import Tuple, Any

import pyo3_example


class Rows:
    def __init__(self, *records: Tuple[Any]):
        # fixme : change input to cursor
        self._rows = self._array(records)

    def __getitem__(self, item: int):
        return self._rows[item]

    @property
    def size(self):
        return self._rows.size

    @property
    def type(self):
        return self._rows.dtype

    @staticmethod
    def _array(records: Tuple[Tuple[Any]]):
        rows = np.stack(tuple(map(np.rec.array, records)))
        rows.dtype.names = tuple(n.replace('f', 'c') for n in rows.dtype.names)
        return rows

    def __str__(self):
        return str(self._rows)

    def __repr__(self):
        return repr(self._rows)


if __name__ == '__main__':
    import pglast
    # print(p.sum_as_string(10, -1))

    print(pglast.parse_sql("""
ALTER TABLE sales.item_outlet_sales ADD COLUMN "aggregated_outlet" BOOLEAN DEFAULT FALSE;
    """))

    # xs = [(1., 2, '3'), (2, 3, '4')]
    # rows = np.rec.array(xs)
    # rows.type.names = tuple(n.replace('f', 'col') for n in rows.type.names)
    # print(rows[0][2].dtype.name)
