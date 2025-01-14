from __future__ import annotations

import contextlib
import warnings
from typing import TYPE_CHECKING, NoReturn, overload

from polars import functions as F
from polars.datatypes import Float64
from polars.utils._wrap import wrap_expr, wrap_s
from polars.utils.various import find_stacklevel

with contextlib.suppress(ImportError):  # Module not available when building docs
    import polars.polars as plr


if TYPE_CHECKING:
    import sys

    from polars import Expr, Series
    from polars.type_aliases import PolarsDataType, PythonLiteral

    if sys.version_info >= (3, 8):
        from typing import Literal
    else:
        from typing_extensions import Literal


@overload
def repeat(
    value: PythonLiteral | None,
    n: Expr | int,
    *,
    dtype: PolarsDataType | None = ...,
    eager: Literal[False] = ...,
    name: str | None = ...,
) -> Expr:
    ...


@overload
def repeat(
    value: PythonLiteral | None,
    n: int,
    *,
    dtype: PolarsDataType | None = ...,
    eager: Literal[True],
    name: str | None = ...,
) -> Series:
    ...


@overload
def repeat(
    value: PythonLiteral | None,
    n: Expr,
    *,
    dtype: PolarsDataType | None = ...,
    eager: Literal[True],
    name: str | None = ...,
) -> NoReturn:
    ...


@overload
def repeat(
    value: PythonLiteral | None,
    n: Expr | int,
    *,
    dtype: PolarsDataType | None = ...,
    eager: bool,
    name: str | None = ...,
) -> Expr | Series:
    ...


def repeat(
    value: PythonLiteral | None,
    n: Expr | int,
    *,
    dtype: PolarsDataType | None = None,
    eager: bool = False,
    name: str | None = None,
) -> Expr | Series:
    """
    Construct a column of length `n` filled with the given value.

    Parameters
    ----------
    value
        Value to repeat.
    n
        Length of the resulting column.
    dtype
        Data type of the resulting column. If set to ``None`` (default), data type is
        inferred from the given value. Defaults to Int32 for integer values, unless
        Int64 is required to fit the given value. Defaults to Float64 for float values.
    eager
        Evaluate immediately and return a ``Series``. If set to ``False`` (default),
        return an expression instead.
    name
        Name of the resulting column.

        .. deprecated:: 0.17.15
            This argument is deprecated. Use the ``alias`` method instead.

    Notes
    -----
    If you want to construct a column in lazy mode and do not need a pre-determined
    length, use :func:`lit` instead.

    See Also
    --------
    lit

    Examples
    --------
    Construct a column with a repeated value in a lazy context.

    >>> pl.select(pl.repeat("z", n=3)).to_series()
    shape: (3,)
    Series: 'repeat' [str]
    [
            "z"
            "z"
            "z"
    ]

    Generate a Series directly by setting ``eager=True``.

    >>> pl.repeat(3, n=3, dtype=pl.Int8, eager=True)
    shape: (3,)
    Series: 'repeat' [i8]
    [
            3
            3
            3
    ]

    """
    if name is not None:
        warnings.warn(
            "the `name` argument is deprecated. Use the `alias` method instead.",
            DeprecationWarning,
            stacklevel=find_stacklevel(),
        )

    if eager:
        if not isinstance(n, int):
            raise TypeError(
                "`n` must be an integer when using `repeat` in an eager context."
            )
        series = wrap_s(plr.repeat_eager(value, n, dtype))
        if name is not None:
            series = series.alias(name)
        return series
    else:
        if isinstance(n, int):
            n = F.lit(n)
        expr = wrap_expr(plr.repeat_lazy(value, n._pyexpr, dtype))
        if name is not None:
            expr = expr.alias(name)
        return expr


@overload
def ones(
    n: int,
    dtype: PolarsDataType = ...,
    *,
    eager: Literal[False] = ...,
) -> Expr:
    ...


@overload
def ones(
    n: int,
    dtype: PolarsDataType = ...,
    *,
    eager: Literal[True],
) -> Series:
    ...


@overload
def ones(
    n: int,
    dtype: PolarsDataType = ...,
    *,
    eager: bool,
) -> Expr | Series:
    ...


def ones(
    n: int,
    dtype: PolarsDataType = Float64,
    *,
    eager: bool = False,
) -> Expr | Series:
    """
    Construct a column of length `n` filled with ones.

    Syntactic sugar for ``repeat(1.0, ...)``.

    Parameters
    ----------
    n
        Length of the resulting column.
    dtype
        Data type of the resulting column. Defaults to Float64.
    eager
        Evaluate immediately and return a ``Series``. If set to ``False``,
        return an expression instead.

    Notes
    -----
    If you want to construct a column in lazy mode and do not need a pre-determined
    length, use :func:`lit` instead.

    See Also
    --------
    repeat
    lit

    Examples
    --------
    >>> pl.ones(3, pl.Int8, eager=True)
    shape: (3,)
    Series: 'ones' [i8]
    [
        1
        1
        1
    ]

    """
    return repeat(1.0, n=n, dtype=dtype, eager=eager).alias("ones")


@overload
def zeros(
    n: int,
    dtype: PolarsDataType = ...,
    *,
    eager: Literal[False] = ...,
) -> Expr:
    ...


@overload
def zeros(
    n: int,
    dtype: PolarsDataType = ...,
    *,
    eager: Literal[True],
) -> Series:
    ...


@overload
def zeros(
    n: int,
    dtype: PolarsDataType = ...,
    *,
    eager: bool,
) -> Expr | Series:
    ...


def zeros(
    n: int,
    dtype: PolarsDataType = Float64,
    *,
    eager: bool = False,
) -> Expr | Series:
    """
    Construct a column of length `n` filled with zeros.

    Syntactic sugar for ``repeat(0.0, ...)``.

    Parameters
    ----------
    n
        Length of the resulting column.
    dtype
        Data type of the resulting column. Defaults to Float64.
    eager
        Evaluate immediately and return a ``Series``. If set to ``False``,
        return an expression instead.

    Notes
    -----
    If you want to construct a column in lazy mode and do not need a pre-determined
    length, use :func:`lit` instead.

    See Also
    --------
    repeat
    lit

    Examples
    --------
    >>> pl.zeros(3, pl.Int8, eager=True)
    shape: (3,)
    Series: 'zeros' [i8]
    [
        0
        0
        0
    ]

    """
    return repeat(0.0, n=n, dtype=dtype, eager=eager).alias("zeros")
